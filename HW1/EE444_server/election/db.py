import sqlite3

import click
from flask import current_app
from flask import g

import csv

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_region_info():
    db = get_db()
    with current_app.open_resource('regions.csv','rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for region in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(region)
                db.execute(
                    "INSERT INTO region (region_name, seats) VALUES (?, ?)",
                    (region[0],region[1])
                )
                db.commit()

        # db.execute(
        #             "INSERT INTO parties (party_name) VALUES ('party_A')"
        #         )
        # db.execute(
        #             "INSERT INTO parties (party_name) VALUES ('party_B')"
        #         )
        # db.execute(
        #             "INSERT INTO parties (party_name) VALUES ('party_C')"
        #         )
        # db.commit()          

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    get_region_info()    


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
