# READ HERE
# https://azure.microsoft.com/en-us/documentation/articles/sql-database-develop-python-simple/
# check here if not working -> http://stackoverflow.com/questions/37771434/mac-pip-install-pymssql-error

import pymssql
import ConfigParser


def create_table(conn):
    sql_query = """
        CREATE TABLE some_table
        (
          id int,
          field1 varchar(255)
        );
    """
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()

    return


def query_table(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM some_table;")
    row = cursor.fetchone()
    while row:
        print row[0]
        row = cursor.fetchone()

    return


def main():
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")

    # get constant variables from config file
    SERVER_NAME = Config.get('azure-sql', 'SERVER_NAME')
    USER_NAME = Config.get('azure-sql', 'USER_NAME')
    PASSWORD = Config.get('azure-sql', 'PASSWORD')
    DB_NAME = Config.get('azure-sql', 'DB_NAME')

    # initialize connection object
    conn = pymssql.connect(server=SERVER_NAME, user='{0}@{1}'.format(USER_NAME, SERVER_NAME),
                           password=PASSWORD, database=DB_NAME)

    # create a fake table to test the library
    # create_table(conn)

    # try a query
    query_table(conn)

    # close connection
    conn.close()

    return


if __name__ == "__main__":
    main()