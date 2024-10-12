# Releasing

The Python port is published to [PyPI](https://pypi.org/).

Run these commands in the `py` directory:

1. `git checkout main` to get on the main branch
2. `git pull` to get the latest from the remote
3. `git status` to check if there are any dirty files
4. `uv sync` to make sure the environment is up to date
5. `uv build` to build the wheel and tar binaries
6. Generate or use an existing a PyPI token in the PyPI web application
7. `uv publish --token [your-token]`
