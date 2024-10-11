from __future__ import annotations

import os
import typing

from mince.dashboards.dashboard import Dashboard

if typing.TYPE_CHECKING:
    from typing import Type, TypeVar
    from typing_extensions import TypeGuard
    from mince.types import Registry, RegistryReference, RegistryEntry

    T = TypeVar('T', bound=Dashboard)


def create_blank_registry() -> Registry:
    import mince

    return {
        'mince_version': mince.__version__,
        'dashboards': {},
    }


#
# # data loading
#


def get_dashboard_config(
    name: str, registry: RegistryReference = None
) -> RegistryEntry:
    registry = resolve_registry(registry)
    return registry['dashboards'][name]


def get_dashboard_class(
    name: str, *, registry: RegistryReference = None
) -> Type[Dashboard]:
    if '.' in name:
        return resolve_dashboard_class(name)
    else:
        entry = get_dashboard_config(name=name, registry=registry)
        return resolve_dashboard_class(entry['dashboard'])


#
# # reference resolution
#


def resolve_registry(registry: RegistryReference = None) -> Registry:
    if isinstance(registry, str):
        registry = {'path': registry}
    if registry is None:
        return load_registry_file()
    elif isinstance(registry, dict) and 'path' in registry:
        return load_registry_file(
            path=registry.get('path'),  # type: ignore
            validate=registry.get('validate', True),  # type: ignore
            create_if_dne=registry.get('create_if_dne', True),  # type: ignore
        )
    elif isinstance(registry, dict) and 'dashboards' in registry:
        return registry  # type: ignore
    else:
        raise Exception('invalid registry reference')


def resolve_dashboard_class(reference: str) -> Type[Dashboard]:
    """syntax:

    module.submodule.DashboardClassName
    OR
    module (will try module.mince)
    """
    import importlib

    *module_name_pieces, class_name = reference.split('.')
    module_name = '.'.join(module_name_pieces)
    module = importlib.import_module(module_name)
    DashboardClass: type[Dashboard] = getattr(module, class_name)
    if not issubclass(DashboardClass, Dashboard):
        raise Exception('not a subclass of Dashboard')
    return DashboardClass


def find_dashboard_class(package: str) -> Type[Dashboard]:
    import importlib

    module_name = package + '.mince'
    module = importlib.import_module(module_name)
    candidates = []
    for name, value in vars(module).items():
        if type(value) is type and issubclass(value, Dashboard):
            candidates.append(value)
    if len(candidates) == 0:
        raise Exception('no Dashboard classes in ' + module_name)
    elif len(candidates) > 1:
        raise Exception('multiple Dashboard classes in ' + module_name)
    else:
        return candidates[0]


#
# # registration
#


def register_dashboard(
    dashboard: str | Type[Dashboard],
    *,
    registry: RegistryReference | None = None,
    name: str | None = None,
    description: str | None = None,
    data_dir: str | None = None,
    use_disk_cache: bool = True,
) -> None:
    # resolve Dashboard class
    if isinstance(dashboard, str):
        if '.' in dashboard:
            DashboardClass = resolve_dashboard_class(dashboard)
            dashboard_reference = dashboard
        else:
            DashboardClass = find_dashboard_class(dashboard)
            dashboard_reference = (
                DashboardClass.__module__ + '.' + DashboardClass.__name__
            )
    elif issubclass(dashboard, Dashboard):
        DashboardClass = dashboard
        dashboard_reference = (
            DashboardClass.__module__ + ':' + DashboardClass.__name__
        )
    else:
        raise Exception('dashboard class is not a subclass of Dashboard')

    # get metadata
    if name is None or description is None:
        spec = DashboardClass.load_spec()
        if name is None:
            name = spec['name']
        if description is None:
            description = spec['description']

    # add entry to registry
    resolved = resolve_registry(registry)
    resolved['dashboards'][name] = {
        'dashboard': dashboard_reference,
        'name': name,
        'description': description,
        'data_dir': data_dir,
        'use_disk_cache': use_disk_cache,
    }

    # save registry to disk
    if registry is None:
        save_registry_file(resolved, path=None)
    elif 'path' in registry:
        save_registry_file(
            resolved,
            path=registry['path'],  # type: ignore
        )

    print('registered', name)


def unregister_dashboard(
    name: str | typing.Type[Dashboard],
    *,
    idempotent: bool = False,
    path: str | None = None,
    validate: bool = True,
) -> None:
    registry = load_registry_file(path=path, validate=validate)
    if isinstance(name, str):
        if name not in registry['dashboards'] and not idempotent:
            raise Exception('dashboard is not registered')
        del registry['dashboards'][name]
    elif type(name) is type and issubclass(name, Dashboard):
        dashboard_path = name.__module__ + '.' + name.__name__
        for candidate_name, candidate in registry['dashboards'].items():
            if candidate['dashboard'] == dashboard_path:
                del registry['dashboards'][candidate_name]
    else:
        raise Exception('invalid type: ' + str(name))
    save_registry_file(registry=registry, path=path)


#
# # file io
#


def get_registry_path() -> str:
    path = os.environ.get('MINCE_REGISTRY_PATH')
    if path is not None:
        return path
    else:
        return os.path.expanduser('~/.config/mince/mince_registry.json')


def load_registry_file(
    *,
    path: str | None = None,
    validate: bool = True,
    create_if_dne: bool = True,
) -> Registry:
    import json

    if path is None:
        path = get_registry_path()
    if not os.path.exists(path):
        if create_if_dne:
            registry = create_blank_registry()
            save_registry_file(registry, path=path)
        else:
            raise Exception('registry file does not exist')
    else:
        with open(path, 'r') as f:
            registry = json.load(f)
    if validate_registry(registry):
        return registry
    else:
        raise Exception('invalid registry')


def save_registry_file(registry: Registry, *, path: str | None) -> None:
    import json

    if path is None:
        path = get_registry_path()

    validate_registry(registry)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(registry, f)


#
# # validation
#


def validate_registry(registry: typing.Any) -> TypeGuard[Registry]:
    if not isinstance(registry, dict):
        raise Exception('invalid type for registry: ' + str(type(registry)))
    assert set(registry.keys()) == {'mince_version', 'dashboards'}
    assert isinstance(registry['mince_version'], str)
    assert isinstance(registry['dashboards'], dict)
    for key, value in registry['dashboards'].items():
        assert isinstance(key, str)
        validate_registry_entry(value)
    return True


def validate_registry_entry(entry: typing.Any) -> TypeGuard[RegistryEntry]:
    assert isinstance(entry, dict)
    assert set(entry.keys()) == {
        'dashboard',
        'name',
        'description',
        'data_dir',
        'use_disk_cache',
    }
    assert isinstance(entry['dashboard'], str)
    assert isinstance(entry['name'], str)
    assert entry['description'] is None or isinstance(entry['description'], str)
    assert entry['data_dir'] is None or isinstance(entry['data_dir'], str)
    assert isinstance(entry['use_disk_cache'], bool)
    return True
