## v0.4.2 (2024-10-10)

### Refactor

- **diffsync**: moved models to diffsyncmodels

## v0.4.1 (2024-10-07)

### Fix

- **diffsync**: updated datetime fields from str to datetime and added timezone

## v0.4.0 (2024-10-07)

### Feat

- **tripitadapter**: added adapter and status model
- **tools**: added progress bar to api calls

## v0.3.0 (2024-10-05)

### Feat

- **client**: made returned json consistent and promoted first class citizen fields

### Refactor

- **client.py**: split into several mixins

## v0.2.0 (2024-10-05)

### Feat

- **all**: added flights support

## v0.1.2 (2024-10-05)

### Fix

- **__version__.py**: removed local part from version, added automatic stripping of local path when calculating tuple

## v0.1.1 (2024-10-05)

### Fix

- **docker**: removed VERSION build arg
- **__version__.py**: created and removed from .gitignore

## v0.1.0 (2024-10-05)

### Feat

- **all**: initial release
