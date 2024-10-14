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
  * Python 3.10+
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
poetry run just bump patch
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

This project was generated using [a fork](https://github.com/luca-penasa/wolt-python-package-cookiecutter) of the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
