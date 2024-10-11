# juice-core-uplink-api-client

[![PyPI](https://img.shields.io/pypi/v/juice-core-uplink-api-client?style=flat-square)](https://pypi.python.org/pypi/juice-core-uplink-api-client/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/juice-core-uplink-api-client?style=flat-square)](https://pypi.python.org/pypi/juice-core-uplink-api-client/)
[![PyPI - License](https://img.shields.io/pypi/l/juice-core-uplink-api-client?style=flat-square)](https://pypi.python.org/pypi/juice-core-uplink-api-client/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://JANUS-JUICE.github.io/juice-core-uplink-api-client](https://JANUS-JUICE.github.io/juice-core-uplink-api-client)

**Source Code**: [https://github.com/JANUS-JUICE/juice-core-uplink-api-client](https://github.com/JANUS-JUICE/juice-core-uplink-api-client)

**PyPI**: [https://pypi.org/project/juice-core-uplink-api-client/](https://pypi.org/project/juice-core-uplink-api-client/)

---

A client library for accessing Juice Core Uplink API

## Installation

```sh
pip install juice-core-uplink-api-client
```

## Usage example

First, create a client:

```python
from juice_core import SHTRestInterface
i = SHTRestInterface()
```

and access the list of available plans on the server:

```python
i.plans()
```

will output a pandas dataframe with the list of plans (just some here):

|    | trajectory   | name                       | mnemonic                   | is_public   | created                    |   id | author   | description                                                                                                                                                           | refine_log   | ptr_file                                                                |
|---:|:-------------|:---------------------------|:---------------------------|:------------|:---------------------------|-----:|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|:------------------------------------------------------------------------|
|  0 | CREMA_3_0    | CASE4                      | CASE4                      | True        | 2021-03-04 13:29:58.835199 |   17 | rlorente | Demonstration Case 4                                                                                                                                                  |              |                                                                         |
|  1 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v0 | CREMA_5_0_OPPORTUNITIES_v0 | True        | 2021-08-26 09:12:06.767139 |   31 | cvallat  | 1st run opf opportunities generation (UC22), based on existing definitions of oppportunities (inherited from crema 3_0)                                               |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |
|  2 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v1 | CREMA_5_0_OPPORTUNITIES_v1 | True        | 2021-10-04 13:49:49.262682 |   36 | cvallat  | Added two opportunities for JMAG_CALROL for the last 2 perijoves before JOI (PJ69 not considered since too clsoe to GoI for observations to take place --> MPAD rule) |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |
|  3 | CREMA_5_0    | CREMA_5_0_OPPORTUNITIES_v2 | CREMA_5_0_OPPORTUNITIES_v2 | True        | 2021-10-05 07:24:07.742653 |   37 | cvallat  | Modified GANYMEDE_GM opportunity around 3G3 for WG3 prime allocation (1 hour centered at CA)                                                                          |              | https://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/ |


You can also directly interact with the underalying `juice-core-uplink-api-client` module:


## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.8+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](https://github.com/JANUS-JUICE/juice-core-uplink-api-client/tree/master/docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github Pages page](https://pages.github.com/) automatically as part each release.

### Releasing


#### Manual release

Releases are done with the command, e.g. incrementing patch:

```bash
kacl-cli release -t -c $(poetry version --dry-run  -s patch) -m
# also push, of course:
git push origin main --tags
```

this will update the changelog, commit it, and make a corresponding tag.

as the CI is not yet configured for publish on pypi it can be done by hand:

```bash
poetry publish --build



```
#### Automatic release - to be fixed

Trigger the [Draft release workflow](https://github.com/JANUS-JUICE/juice-core-uplink-api-client/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/JANUS-JUICE/juice-core-uplink-api-client/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/JANUS-JUICE/juice-core-uplink-api-client/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.


## OpenAPI definition issues:

- Version 3 of openapi definition should probably be used for the API. 

- `/rest_api/plan/` (for example) is actually an array not a list, even if it is described to return a model called `PlanList` it actually returns an array of `PlanList` items (here the correction I made to make it work properly with current API):
  
  ```json
  "/rest_api/plan/": {
        "get": {
          "tags": [
            "rest_api"
          ],
          "summary": "Retrieve the list of available PUBLIC plans",
          "description": "List the PUBLIC plans available in the system",
          "operationId": "rest_api_plan_list",
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "array",
                    "items": {
                      "$ref": "#/components/schemas/PlanList"
                    }
                  }
                }
              }
            }
          }
        },
  ```

  I found this same issue to be common within the API: several endpoints are described to return a `SomethingList`, but in practice it returns an array of `SomethingList`. Ideally one would probably rename `SomethingList` into a `Something` and then set the type to `array` as above.

- Some endpoints have 'hidden' parameters. For example `/rest_api/series` expects a `body` parameter that is not listed in the definition! Same for `/rest_api/events`
  

- There are duplicated operationId for different services in the definition. For example `rest_api_plan_read` is used to identify several endpoints (here the descriptions):
  
  - "Retrieve, update or delete a segmentation instance."
  - "Retrieve a PTR correspondig to a plan."
  - "Retrieves statistics for a plan."
  - "Retrieve, update or delete a segmentation instance."
  
  `operationId`, if present, should be [unique within the same API](https://swagger.io/docs/specification/v3_0/paths-and-operations/#operationid).

  A full list of duplications can be found here:

```
operationId rest_api_checks_read used for get within path /rest_api/checks/{working_group_mnemonic}{format} already in use.
  -> replacing id rest_api_checks_read with rest_api_checks_read_1
operationId rest_api_read used for get within path /rest_api/config{format} already in use.
  -> replacing id rest_api_read with rest_api_read_1
operationId rest_api_detailed_scenario_read used for get within path /rest_api/detailed_scenario/{id}{format} already in use.
  -> replacing id rest_api_detailed_scenario_read with rest_api_detailed_scenario_read_1
operationId rest_api_read used for get within path /rest_api/detailed_scenario{format} already in use.
  -> replacing id rest_api_read with rest_api_read_2
operationId rest_api_create used for post within path /rest_api/eps_package{format} already in use.
  -> replacing id rest_api_create with rest_api_create_1
operationId rest_api_read used for get within path /rest_api/events{format} already in use.
  -> replacing id rest_api_read with rest_api_read_3
operationId rest_api_read used for get within path /rest_api/fdyn_event_definition{format} already in use.
  -> replacing id rest_api_read with rest_api_read_4
operationId rest_api_read used for get within path /rest_api/fdyn_event_file{format} already in use.
  -> replacing id rest_api_read with rest_api_read_5
operationId rest_api_read used for get within path /rest_api/fdyn_event{format} already in use.
  -> replacing id rest_api_read with rest_api_read_6
operationId rest_api_file_read used for get within path /rest_api/file/{filename}{format} already in use.
  -> replacing id rest_api_file_read with rest_api_file_read_1
operationId rest_api_git_read used for get within path /rest_api/git/{branch}/ already in use.
  -> replacing id rest_api_git_read with rest_api_git_read_1
operationId rest_api_git_read used for get within path /rest_api/git/{branch}/{hexsha}/ already in use.
  -> replacing id rest_api_git_read with rest_api_git_read_2
operationId rest_api_git_read used for get within path /rest_api/git/{branch}/{hexsha}{format} already in use.
  -> replacing id rest_api_git_read with rest_api_git_read_3
operationId rest_api_git_read used for get within path /rest_api/git/{branch}{format} already in use.
  -> replacing id rest_api_git_read with rest_api_git_read_4
operationId rest_api_read used for get within path /rest_api/git{format} already in use.
  -> replacing id rest_api_read with rest_api_read_7
operationId rest_api_read used for get within path /rest_api/mode{format} already in use.
  -> replacing id rest_api_read with rest_api_read_8
operationId rest_api_observation_definition_read used for get within path /rest_api/observation_definition/{mnemonic}{format} already in use.
  -> replacing id rest_api_observation_definition_read with rest_api_observation_definition_read_1
operationId rest_api_read used for get within path /rest_api/observation_definition{format} already in use.
  -> replacing id rest_api_read with rest_api_read_9
operationId rest_api_pcw_read used for get within path /rest_api/pcw/{mnemonic}/ already in use.
  -> replacing id rest_api_pcw_read with rest_api_pcw_read_1
operationId rest_api_pcw_read used for get within path /rest_api/pcw/{mnemonic}{format} already in use.
  -> replacing id rest_api_pcw_read with rest_api_pcw_read_2
operationId rest_api_read used for get within path /rest_api/pcw{format} already in use.
  -> replacing id rest_api_read with rest_api_read_10
operationId rest_api_plan_read used for get within path /rest_api/plan/{id}/ptr{format} already in use.
  -> replacing id rest_api_plan_read with rest_api_plan_read_1
operationId rest_api_plan_read used for get within path /rest_api/plan/{id}/stats{format} already in use.
  -> replacing id rest_api_plan_read with rest_api_plan_read_2
operationId rest_api_plan_read used for get within path /rest_api/plan/{id}{format} already in use.
  -> replacing id rest_api_plan_read with rest_api_plan_read_3
operationId rest_api_plan_update used for put within path /rest_api/plan/{id}{format} already in use.
  -> replacing id rest_api_plan_update with rest_api_plan_update_1
operationId rest_api_plan_delete used for delete within path /rest_api/plan/{id}{format} already in use.
  -> replacing id rest_api_plan_delete with rest_api_plan_delete_1
operationId rest_api_create used for post within path /rest_api/plan_ptr_skeleton{format} already in use.
  -> replacing id rest_api_create with rest_api_create_2
operationId rest_api_create used for post within path /rest_api/plan_ptr_xml{format} already in use.
  -> replacing id rest_api_create with rest_api_create_3
operationId rest_api_create used for post within path /rest_api/plan_ptr{format} already in use.
  -> replacing id rest_api_create with rest_api_create_4
operationId rest_api_plan_simphony_groups_read used for get within path /rest_api/plan_simphony/groups/{id}{format} already in use.
  -> replacing id rest_api_plan_simphony_groups_read with rest_api_plan_simphony_groups_read_1
operationId rest_api_plan_simphony_opps_read used for get within path /rest_api/plan_simphony/opps/{id}{format} already in use.
  -> replacing id rest_api_plan_simphony_opps_read with rest_api_plan_simphony_opps_read_1
operationId rest_api_plan_simphony_timeline_read used for get within path /rest_api/plan_simphony/timeline/{id}{format} already in use.
  -> replacing id rest_api_plan_simphony_timeline_read with rest_api_plan_simphony_timeline_read_1
operationId rest_api_plan_simphony_read used for get within path /rest_api/plan_simphony/{id}{format} already in use.
  -> replacing id rest_api_plan_simphony_read with rest_api_plan_simphony_read_1
operationId rest_api_read used for get within path /rest_api/plan{format} already in use.
  -> replacing id rest_api_read with rest_api_read_11
operationId rest_api_create used for post within path /rest_api/plan{format} already in use.
  -> replacing id rest_api_create with rest_api_create_5
operationId rest_api_read used for get within path /rest_api/plnview_file{format} already in use.
  -> replacing id rest_api_read with rest_api_read_12
operationId rest_api_read used for get within path /rest_api/plnview_sessions{format} already in use.
  -> replacing id rest_api_read with rest_api_read_13
operationId rest_api_segment_definition_read used for get within path /rest_api/segment_definition/{mnemonic}{format} already in use.
  -> replacing id rest_api_segment_definition_read with rest_api_segment_definition_read_1
operationId rest_api_read used for get within path /rest_api/series{format} already in use.
  -> replacing id rest_api_read with rest_api_read_14
operationId rest_api_read used for get within path /rest_api/session_flush{format} already in use.
  -> replacing id rest_api_read with rest_api_read_15
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/detailed_scenario{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_1
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/engineering_segment_types{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_2
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/engineering_segments{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_3
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/event{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_4
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/plan{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_5
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/ptr{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_6
operationId trajectory_segment_definitions used for get within path /rest_api/trajectory/{mnemonic}/segment_definition{format} already in use.
  -> replacing id trajectory_segment_definitions with trajectory_segment_definitions_1
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}/series{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_7
operationId rest_api_trajectory_read used for get within path /rest_api/trajectory/{mnemonic}{format} already in use.
  -> replacing id rest_api_trajectory_read with rest_api_trajectory_read_8
operationId rest_api_read used for get within path /rest_api/trajectory{format} already in use.
  -> replacing id rest_api_read with rest_api_read_16
operationId rest_api_user_read used for get within path /rest_api/user/{username}{format} already in use.
  -> replacing id rest_api_user_read with rest_api_user_read_1
operationId rest_api_uvt_event_read used for get within path /rest_api/uvt_event/{source}{format} already in use.
  -> replacing id rest_api_uvt_event_read with rest_api_uvt_event_read_1
operationId rest_api_read used for get within path /rest_api/uvt_event_file{format} already in use.
  -> replacing id rest_api_read with rest_api_read_17
operationId rest_api_read used for get within path /rest_api/version{format} already in use.
  -> replacing id rest_api_read with rest_api_read_18
```