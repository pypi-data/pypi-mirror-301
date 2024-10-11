from __future__ import annotations

from typing import Any, TYPE_CHECKING

from mince.figures import ui_figures
from mince import transforms
import mince.spec
from . import apps
from . import shortcuts

if TYPE_CHECKING:
    from typing_extensions import Unpack
    from dash import Dash, html  # type: ignore
    import plotly.graph_objects as go  # type: ignore
    import polars as pl
    from mince import types
    from mince.types import LoadKwargs, SpecKwargs, CollectKwargs, UiSpec


class Dashboard:
    """main object to instantiate or modify when building a dashboard

    the methods exposed in this class are those that may be useful to override
    """

    # class properties

    use_disk_cache: bool = True

    @classmethod
    def load_data(cls, **kwargs: Unpack[LoadKwargs]) -> dict[str, pl.DataFrame]:
        raise NotImplementedError('load_data() not implemented')

    @classmethod
    def load_spec(cls, **kwargs: Unpack[SpecKwargs]) -> UiSpec:
        raise NotImplementedError('load_spec() not implemented')

    @classmethod
    def collect_data(cls, **kwargs: Unpack[CollectKwargs]) -> None:
        raise NotImplementedError('collect_data() not implemented')

    @classmethod
    def data_last_collected(cls, **kwargs: Unpack[CollectKwargs]) -> int | None:
        raise NotImplementedError('data_last_collected() not implemented')

    @classmethod
    def validate(cls, spec: types.UiSpec, dfs: dict[str, pl.DataFrame]) -> None:
        mince.spec.validate_ui_spec(spec)
        mince.schema.validate_data_matches_spec(dfs, spec)

    # instance properties

    spec: types.UiSpec
    dfs: dict[str, pl.DataFrame]
    date_ranges: dict[str, tuple[int, int]]
    debug: bool
    app: Dash
    t_run_start: float | None
    n_keydowns: int

    def __init__(
        self,
        *,
        dfs: dict[str, pl.DataFrame],
        spec: types.UiSpec,
        debug: bool = False,
        pdb: bool = False,
        assets_folder: str | None = None,
    ):
        self.validate(dfs=dfs, spec=spec)
        self.spec = spec
        self.dfs = dfs
        self.debug = debug
        self.mince_version = mince.spec.get_package_version('mince')
        self.date_ranges = {
            name: transforms.get_date_range(df) for name, df in dfs.items()
        }
        self.app = apps._create_app(
            dashboard=self, assets_folder=assets_folder, pdb=pdb
        )
        self.n_keydowns = 0
        self.t_run_start = None

    def run(
        self,
        port: str | int | None = None,
        jupyter_mode: str = 'external',
        **kwargs: Any,
    ) -> None:
        import time
        import mince.ops

        if port is None:
            port = str(mince.ops.find_available_port(8052))
        else:
            port = str(port)
        self.t_run_start = time.time()

        try:
            import mince.ops

            mince.ops.create_pid_file(dashboard=self, port=port)
            self.app.run(jupyter_mode=jupyter_mode, port=port, **kwargs)
        except Exception:
            pass
        finally:
            mince.ops.clear_pid_file(dashboard=self, port=port)

    def get_metadata(self) -> dict[str, Any]:
        import tooltime

        if self.t_run_start is not None:
            t_run_start = tooltime.timestamp_to_iso_pretty(self.t_run_start)
        else:
            t_run_start = None
        return {
            'mince_version': self.mince_version,
            'dashboard_version': self.spec['version'],
            'name': self.spec['name'],
            'description': self.spec['description'],
            'time_started': t_run_start,
        }

    def get_layout(self, inputs: dict[str, html.Div]) -> list[html.Div]:
        from dash import dcc, html

        return [
            shortcuts._create_shortcuts_listeners(self.spec['shortcuts']),
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='initial-load', data=True),
            dcc.Store(id='radio-group-visibility', data=True),
            html.Div(list(inputs.values()), id='radio-group-row'),
            dcc.Graph(
                id='main-chart',
                config={'responsive': True, 'displayModeBar': False},
            ),
            shortcuts._create_help_modal(self.spec['shortcuts']),
            html.Div(id='prevent-focus-trigger'),
        ]

    def get_dataset(self, state: dict[str, Any]) -> str:
        if len(self.dfs) == 1:
            return next(iter(self.dfs.keys()))
        else:
            raise NotImplementedError('get_dataset()')

    def process_shortcuts(
        self,
        display_state: dict[str, Any],
        ui_state: dict[str, Any],
        raw_shortcut: dict[str, Any],
    ) -> None:
        shortcuts._process_keyboard_shortcuts(
            display_state=display_state,
            ui_state=ui_state,
            raw_shortcut=raw_shortcut,
            data_date_range=self.date_ranges[self.get_dataset(display_state)],
            ui_spec=self.spec,
        )

    def create_chart(self, state: dict[str, Any]) -> go.Figure:
        data_name = self.get_dataset(state)
        df = self.dfs[data_name]
        date_range = self.date_ranges[data_name]

        title = self.create_title(
            df=df, state=state, data_date_range=date_range, ui_spec=self.spec
        )

        if state['format'] in ['line', 'line %', 'area', 'area %']:
            return ui_figures.create_time_series_fig(
                df, state, self.debug, ui_spec=self.spec, title=title
            )
        elif state['format'] == 'tree':
            return ui_figures.create_treemap_fig(
                df,
                state,
                ui_spec=self.spec,
                data_date_range=date_range,
                title=title,
            )
        else:
            raise Exception('invalid format: ' + str(state['format']))

    def create_title(
        self,
        df: pl.DataFrame,
        state: dict[str, Any],
        data_date_range: tuple[int, int],
        ui_spec: types.UiSpec,
    ) -> str | None:
        return None
