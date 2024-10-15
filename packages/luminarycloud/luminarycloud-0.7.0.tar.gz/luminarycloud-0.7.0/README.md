# Luminary Cloud Python SDK

- [Quickstart](#quickstart) **(recommended)**
- [Manual Installation](#manual-installation)
- [Building the wheel](#building-the-wheel)
- [Generating Python proto files](#generating-python-proto-files)
- [Generating documentation](#generating-documentation)
- [Configuration](#configuration)

## Quickstart

To start using the SDK (via Python REPL):
```
docker compose run --build sdk
```

![Kapture 2023-03-29 at 14 55 37](https://user-images.githubusercontent.com/6025130/228680101-f6cfea54-07a8-4251-9666-55fb93cedb76.gif)

You only need the `--build` option if you're running for the first time or if
the source has changed.

#### Other useful commands
- `docker compose run sdk sh` to start an interactive shell.
- `docker compose run sdk pytest` to run unit tests.
- `docker compose run sdk python my_script.py` to run an example script.

## Manual Installation

There are two ways to run the SDK.
- If you just want to test it out or run unit tests, you can spin up a docker
  container as detailed in the [Quickstart section](#quickstart) above. This is
  the simplest way to get started with the SDK.
- Otherwise, you can continue with the instructions below. **If you aren't
  careful with your virtualenvs, there's a chance that you will mess up your
  dev environment, so I recommend the previous option.**

### Prerequisites
- [Install virtualenv](https://virtualenv.pypa.io/en/latest/installation.html")
- `luminarycloud-*.whl` file (either download a released SDK or [build the wheel
yourself](#building-the-wheel))

### (optional) Start a local apiserver

In separate/background shell:
```
> bazel run //go/core/cmd/apiserver:apiserver -- --insecure-apis
```

Please see the [apiserver README](/go/core/apiserver/README.md) for more details
on deployment options (e.g. using a local vs test0/main backend).

### Create a new virtualenv

**VS Code users:** it is recommended that you create the virtualenv via the
`Python: Create Environment` command instead of following the method below.

```sh
# create a new venv at a location of your choosing (e.g. ~/lc-sdk-venv),
# preferably OUTSIDE of the core repo so that git and gazelle don't pick
# up on its contents.
> virtualenv ~/lc-sdk-venv

# from here on, do everything in a venv
> source ~/lc-sdk-venv/bin/activate
```

**_NOTE_** - remember to `deactivate` the virtualenv after you're done with
the SDK or before running any of the other python-related scripts in this repository,
including `gazelle.py`, as well as any bazel rules that invoke python (such as the
`//gen:py_proto_library` rule), and even the `format.py` script which is part of the
git pre-commit hook.

If this sounds inconvenient, please take a look at the [Quickstart](#quickstart)
section at the top of the README.

### Install the python wheel

```sh
# --force-reinstall flag is only needed if you're reusing an old venv and want
# to replace any previously installed SDK
(lc-sdk-venv) > pip install --force-reinstall path/to/wheel/luminarycloud-*.whl

# use the REPL to import the SDK and make API calls
(lc-sdk-venv) > python
>>> import luminarycloud as lc
>>> lc.list_projects()

# run an example script that makes requests using the SDK
(lc-sdk-venv) > python my_script.py
```

You will probably also want to install the packages needed for the SDK with
```sh
pip install -r $CORE/python/sdk/requirements-dev.txt
```
The SDK tests also have some additional required packages that can be installed with
```sh
pip install -r $CORE/python/sdk_test/requirements.txt
```

## Building the wheel

### Prerequisites
- Install build: `pip install --upgrade build`

```sh
python -m build $CORE/python/sdk
```

You will find the resulting wheel file in `$CORE/python/sdk/dist`.

## Generating Python proto files

This is only relevant for SDK developers. Run the following command to generate
the *.py and *.pyi files from the proto files in `$CORE/proto`. Remember to `deactivate`
any active virtualenvs before running this command (or you may end up with incorrect
behavior).

```sh
$CORE/./bazel/gazelle.py
```

## Generating documentation

**[https://docs.eng.luminarycloud.com/python-sdk](https://docs.eng.luminarycloud.com/python-sdk)**

The docs are [automatically generated](../../../.github/workflows/generate-docs-site.yml)
and are hosted in our [internal documentation index](https://docs.eng.luminarycloud.com).

To generate the docs yourself:

```
docker compose run --build docs
```

To run the SDK quickstart notebook (which we make available on the doc website)

```
docker compose up --build quickstart
```

## Configuration

You may configure default values for the Luminary Python SDK using any of the
following environment variables.

| Name                | Default                                                    | Description                                                |
| ------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| LC_DOMAIN           | apis.luminarycloud.com                                     | The target API service domain.                             |
| LC_AUTH_DOMAIN      | luminarycloud-prod.us.auth0.com                            | The Auth0 tenant domain.                                   |
| LC_AUTH_CLIENT_ID   | JTsXa4fbArSCl6i9xylUpwrwpovtkss1                           | The Auth0 client ID for the SDK.                           |
| LC_AUTH_SERVICE_ID  | https://apis.luminarycloud.com                             | The Auth0 service identifier for the Luminary API service. |
| LC_REFRESH_ROTATION | TRUE                                                       | If TRUE, refresh token rotation is enabled.                |
| LC_CREDENTIALS_DIR  | ~/.config/luminarycloud or $APP_DATA/Roaming/luminarycloud | The directory to store credentials.                        |

To see the values for other Auth0 tenants, see:
`devops/terraform/ci-template/modules/auth0-metadata/main.tf`

### Using `.env`

You may set the above values inside a `.env` file placed at your project root or working directory.
The values set in a `.env` do not override existing environment variables.
