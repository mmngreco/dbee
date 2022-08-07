# dbee-cli

WIP

## Installation

```bash
pipx install git+https://github.com/mmngreco/dbee
```

### Developers

```bash
git clone https://github.com/mmngreco/dbee
pip install -e ./dbee
```


## Usage

```
dbee --help
dbee read "mssql+pyodbc://user:pass@host:1433/dbname?driver=FreeTDS" "select top 5 from tab.users"
```
