# from configparser import ConfigParser
# from sqlalchemy.exc import ArgumentError
import pandas as pd
import sqlparse
import typer
from rich.console import Console

# from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Table

# from rich.text import Text

# app = typer.Typer()
console = Console(highlight=True, soft_wrap=False)


def dataframe2table(df, title=None):
    table = Table(title=title)

    for col in df.columns:
        table.add_column(col)

    for row in df.itertuples(False):
        table.add_row(*map(str, row))

    return table


# TODO: future
# def load_dsn_file(fname: str):
#     config = ConfigParser()
#     config.read(fname)
#     return config
#
#
# def dict2url(config):
#     params = urllib.parse.urlencode(config)
#     return params
#


def build_conn(conn_str, use="sa"):
    use = use.lower()
    # try:
    #     return _sa_conn(conn_str)
    # except ArgumentError:
    #     return _pyodbc_conn(conn_str)
    #
    if use == "pyodbc":
        return _pyodbc_conn(conn_str)
    elif use in ["sa", "sqlalchemy"]:
        return _sa_conn(conn_str)


def _pyodbc_conn(url):
    import pyodbc

    con = pyodbc.connect(url)
    return con


def _sa_conn(url):
    import sqlalchemy as sa

    c = sa.create_engine(url)
    con = c.connect()
    return con


def _read(url, q, use="sa", verbose=False, console=None, style="table"):
    q = format_query(q)
    style = style.lower()

    con = build_conn(url, use=use)
    out = pd.read_sql(q, con, parse_dates=True)

    if console is None:
        return out

    # print out
    if verbose:
        console.print(Syntax(url, lexer="html"))
        console.print(Syntax(q, lexer="mysql"))

    if style == "table":
        out = dataframe2table(out)
    else:
        out = eval(f"out.{style}")

    console.print(out)

    return out


def format_query(query):
    out = sqlparse.format(
        query, reindent_aligned=True, reindent=True, keyword_case='upper'
    ).replace("\n\n", "\n")
    return out


def default_kw(kwargs):
    kw = {}
    if kwargs is not None and len(kwargs):
        kw = eval(kwargs)
    return kw


def read(
    url: str,
    query: str,
    style: str = "table",
    v: bool = False,
):
    _read(url, query, console=console, style=style, verbose=v)


def app():
    typer.run(read)


if __name__ == "__main__":
    app()
