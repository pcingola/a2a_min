# Publishing a2a-min to PyPI

This document provides instructions on how to publish the a2a-min package to PyPI so it can be installed with `pip install a2a-min`.

## Prerequisites

- A PyPI account (register at https://pypi.org/account/register/ if you don't have one)
- Python 3.12 or later
- Build tools: `build` and `twine`

## Step 1: Prepare your package files

Ensure your package has the following files properly configured:

- **pyproject.toml**: Contains metadata about your package
- **README.md**: Documentation for your package
- **LICENSE**: License information
- **MANIFEST.in**: Specifies additional files to include in the package

Make sure your MANIFEST.in includes all necessary files:

```
include LICENSE
include README.md
include pyproject.toml
recursive-include a2a_min/examples *.py
```

## Step 2: Install build tools

```bash
# Using uv
uv pip install build twine
```

## Step 3: Build the package

```bash
python -m build
```

This will create two distribution files in the `dist/` directory:
- `a2a_min-x.y.z-py3-none-any.whl` (wheel distribution)
- `a2a_min-x.y.z.tar.gz` (source distribution)

where `x.y.z` is the version number specified in your pyproject.toml.

## Step 4: Create a PyPI API token

1. Log in to your PyPI account
2. Go to Account Settings → API tokens
3. Create a new API token with the scope set to "Entire account" or just the specific project
4. Save this token securely - you'll only see it once!

## Step 5: Configure your PyPI credentials

Create or update your `~/.pypirc` file:

```
[pypi]
username = __token__
password = pypi-your-token-here
```

Replace `pypi-your-token-here` with your actual PyPI API token.

## Step 6: Upload your package to PyPI

```bash
python -m twine upload dist/*
```

If you haven't configured your credentials in `~/.pypirc`, you'll be prompted to enter your username and password.

## Step 7: Verify the installation

After uploading, verify that your package can be installed from PyPI:

```bash
# Using pip
pip install a2a-min

# Using uv
uv pip install a2a-min
```

## Updating your package

When you want to release a new version:

1. Update the version number in `pyproject.toml`
2. Make your code changes
3. Rebuild the package: `python -m build`
4. Upload to PyPI again: `python -m twine upload dist/*`

## Security best practices

- Always use API tokens instead of your PyPI password
- Never commit your PyPI credentials to version control
- Consider using keyring for more secure credential storage

## Troubleshooting

- If you get a "File already exists" error, it means you're trying to upload a version that already exists on PyPI. You need to update the version number in your pyproject.toml.
- If you get a "403 Forbidden" error, check your API token permissions.

Your package is now available at: https://pypi.org/project/a2a-min/