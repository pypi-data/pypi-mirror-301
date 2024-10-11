
# mince 🔪🧄🧅

toolkit for slicing up data into bite-sized dashboards

Steps for using mince:
1. ingest raw data into standardized format
2. define dashboard specification
3. serve dashboard
4. continually update the data


## Building a dashboard

In mince dashboards have 2 components:
1. Data: a dict of polars dataframes
2. UI Specification: metadata describing the dashboard's UI


## Dashboard maintenance

There are many tasks associated with building and maintaining a data dashboard including:
- data collection
- data management
- deployment
- monitoring

`mince` aims to automate as many of these tasks as possible

## Command Line Interface

The `mince` cli aims to automate as many of these tasks as possible

- run dashboard
    `mince run ... --pdb`
- run dashboard with interactive debugger
    `mince run ... --pdb`
- list info about all running dashboards
    - `mince ls`
- disk caching of loaded datasets for quick dashboard restarts
- standardized hooks for data collection
    `mince collect <DASHBOARD>`
- cli generator to create a management cli for each dashboard
    `<DASHBOARD> <SUBCOMMAND> ...`
- easily load a dashboard's data into an interactive python session
    `mince data <DASHBOARD> -i`
