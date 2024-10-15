# Swytchit

Context switching made easy for shell geeks

## Usage

```bash
sw your/project/directory
```

- Performs a `cd` operation to the project
- Starts a subshell
- Within the subshell, runs `source` on `.swytchitrc` files in the project directory and any ancestor directories

## Why?

- Easily switch virtual environments for scripting languages (Python, Ruby, etc)
- Easily populate project-specific environment variables and aliases
- Use with the `op` CLI from 1Password to keep project-specific secrets in memory

## Installation (MacOS)

```bash
brew install python3.11
python3.11 -m pip install pipx
pipx install swytchit
```

## Rules

- Only works in TTY shell (no piping)
- Only works for a descendent of user's home directory
- Resolves symlinks first

<a href="https://www.flaticon.com/free-icons/rabbit">Icon by Flaticon</a>
