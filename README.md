# Base - building the base for your business

## Development Environments

To run de application, in development, needs setting theese environments:

```bash
FLASK_ENV=[development, staging, production]
FLASK_DEBUG=[true, false]

FLASK_APP=base/app.py

SETTINGS_FILE_FOR_DYNACONF=./base/extensions/config/settings.toml
SECRETS_FOR_DYNACONF=./base/extensions/config/.secrets.toml
```
