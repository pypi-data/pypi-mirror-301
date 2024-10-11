# NC-MIS
The ncubed MIS application is used to configure (network) IT systems.

## Possible interpretations
- Make it so...
- Managed infrastructure services
- My inferiour scripts
- My Imaginary Solutions
- My Internet Struggles
- Make it simple
- maybe it's not

## Installation and updating
pip install nc(-/_)mis

## Usage
A `.env` file is automatically created when the above scripts are run. This file is excluded from git. Use this file to store secrets and import the Python `dotenv` package in your modules to load the values automatically when executing.

```python
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
```

`dotenv` can also be used on the CLI to load environment variables when executing a command:
```bash
$ dotenv ansible-playbook playbook.yml -i inventory
```
