# from configparser import ConfigParser
# from sqlalchemy.exc import ArgumentError
from typing import Optional
import pandas as pd
import sqlparse
import typer
from rich.console import Console

# from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Table
from rich.errors import NotRenderableError

# from rich.text import Text

# app = typer.Typer()
console = Console(highlight=True, soft_wrap=False)


def dataframe2table(df, title=None):
    table = Table(title=title)

    for col in df.columns:
        table.add_column(str(col))

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


def read(
    url: str,
    query: str,
    use: str = "sa",
    verbose: bool = False,
    style: str = "table",
    evaluate: Optional[str] = None,
    stdout: bool = True,
    pdb: bool = False,
):
    if pdb:
        __import__("pdb").set_trace()

    query = format_query(query)
    con = build_conn(url, use=use)
    df = pd.read_sql(query, con, parse_dates=True)
    style = style.strip()

    if evaluate:
        df = eval(evaluate, {}, {"df": df, "x": df})
        if not isinstance(df, pd.DataFrame):
            style = ""

    if console is None:
        return df

    if verbose and stdout:
        console.print(Syntax(url, lexer="html"))
        console.print(Syntax(query, lexer="mysql"))

    if style == "":
        out = df
    elif style == "table":
        out = dataframe2table(df)
    elif style == "csv":
        out = df.to_csv()
    elif style == "md":
        out = df.to_markdown()
    elif style == "str":
        out = df.to_string()
    else:
        if style.startswith("."):
            style = style[1:]
        out = eval(f"df.{style}")

    if stdout:
        try:
            console.print(out)
        except NotRenderableError:
            console.print(df)

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


def app():
    typer.run(read)


if __name__ == "__main__":
    app()
