# dbee-cli

> very WIP

![](./demo.gif)

## Why?

Other tools like `tsql` or `sqlcmd` requires complex configuration and setup
that I've never found necessary using python directly, so I've decided to go
for a CLI around `SQLAlchemy` and `pandas` to offer the most simple
functionality without opening any IDE or configuring anything.


## Installation

```bash
pipx install git+https://github.com/mmngreco/dbee
```

## Usage

```
dbee --help
dbee read "mssql+pyodbc://user:pass@host:1433/table?driver=FreeTDS" "select top 5 from table.users"
```


## Pro-tips


You can create alias in your `.bashrc`, as follows:

```bash
alias dbms='dbee read "mssql+pyodbc://user:pass@host:1433/dbname?driver=FreeTDS"'
alias dblite='dbee read "sqlite:///database.db'
```

And use them:

```bash
dbms "select top 5 from Table"
dblite "select * from Hero"
```

### Developers

```bash
git clone https://github.com/mmngreco/dbee
pip install -e ./dbee
```

