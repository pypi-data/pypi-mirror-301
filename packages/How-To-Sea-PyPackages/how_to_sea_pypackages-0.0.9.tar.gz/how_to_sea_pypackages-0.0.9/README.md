# Introduction
This repository provides the Python bindings for gRPC services used in the How To Sea project. gRPC facilitates inter-service communication, serving as an internal API.

To avoid code duplication in gRPC client stub implementations across various services, we have packaged these implementations and made them available on PyPi.

**Note:** This package is hosted on the public PyPi server. For sensitive information, a private PyPi server should be used to ensure privacy.

## Structure
Each folder represents a distinct package.

### how_to_sea_auth_grpc
This package includes the Python bindings for a gRPC server, allowing any service to communicate with the authentication service for verifications.

## Adding a New Package
To create and release a new package, follow these steps:

1. Create a new top-level module with a unique name.
2. Add the source code.
3. Include the module name in the package list in the top-level `pyproject.toml` file.
4. Deploy a new version.

## Deploying a New Version
1. Clear the `dist` folder.
2. Run `python3 -m build` from the top module.
3. Run `python3 -m twine upload --repository pypi dist/*` to upload the new release to PyPi.

**Note:** Ensure you have the correct API keys set in your `~/.pypirc` file to upload to PyPi.