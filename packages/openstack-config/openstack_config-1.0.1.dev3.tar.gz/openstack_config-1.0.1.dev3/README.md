# Openstack-Config

Allows editing the clouds.yaml easily via CLI and adds kubectl-like contexts.

## Usage

```shell
# using uv, you can simply run
uvx --from python-openstackclient --with openstack-config --python=3.10 openstack config get-contexts
```

* *openstack config current-context* - Display the current context
* *openstack config delete-context* - Delete the specified context from the clouds.yaml
* *openstack config get-contexts* - Describe one or many contexts
* *openstack config get-projects* - List all projects that are currently accessible
* *openstack config rename-contexts* - Rename a context from the clouds.yaml file
* *openstack config set* - Set an individual value in a clouds.yaml file
* *openstack config unset* - Unset an individual value in a clouds.yaml file
* *openstack config use-context* - Set the current context for all operations (use none to reset)
* *openstack config use-project* - Override the project in the current context within the clouds.yaml
* *openstack config view* - Display merged clouds.yaml settings or a specified clouds.yaml file

## Installation

### PyPI

```shell
pip install openstack-config
```

### Local build

```shell
git clone $REPO && cd $REPO
pip install -e .

# optional
eval "$(openstack complete)"
```

## Deployment

```shell
export UV_PUBLISH_TOKEN="pypi-..."

# optional
# UV_PUBLISH_URL="https://test.pypi.org/legacy/"

bash publish.sh
```