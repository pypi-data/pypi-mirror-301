# lenv-py

Manage symlinks from a root file to multiple destinations.

Useful for monorepos that use a single `.env` file as a source of truth for many child projects.

## Usage

In the root of your project:

1. Create a `.env` (or other named) file you want to symlink
2. Create a `.lenv` file with the destination locations to symlink to, such as:

```
project/a/.env
project/b/.env
```

3. Execute `uv add --dev lenv-py` to install lenv (or with another package manager)
4. Execute `uv run lenv link` to create symlinks

Use the `-help` flag to see all usage instructions.
