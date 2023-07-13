import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any, Tuple

load_dotenv(dotenv_path=r".env")

class DataBase:
    dotenv_path = r".env"
    def __init__(self):
        """
        Class initialization method.
        """
        self.sql_alchemy = os.environ.get("SQLALCHEMY")
        self.connection = ""
        self.engine = ""

    def connect(self):
        """
        Method to connect to the database.
        """
        try:
            self.engine = create_engine(self.sql_alchemy)
            self.connection = self.engine.connect()
            print("Connection to the database established successfully!")
        except Exception as e:
            print(f'Error: {e}')
            print("Failed to create a connection to the database.")

    def disconnect(self):
        """
        Method to disconnect from the database.
        """
        if self.connection != '':
            try:
                self.connection.close()
                self.connection = ''
                print('Connection to the database closed successfully!')
            except Exception as e:
                print('Failed to close the connection to the database.')
        else:
            print('No connection established, no need to disconnect.')

    def create_schema(self, name: str):
        """
        Creates a schema in the database.

        Args:
            name: Name of the schema.
        """
        if self.connection != "":
            try:
                self.connection.execute(f"CREATE SCHEMA IF NOT EXISTS {name}")
                print("Schema created successfully!")
            except Exception as e:
                print("Failed to create the schema.")
        else:
            print("No connection established, connect to the database.")

    def drop_schema(self, name: str):
        """
        Removes a schema from the database.

        Args:
            name: Name of the schema.
        """
        if self.connection != "":
            try:
                self.connection.execute(f"DROP SCHEMA IF EXISTS {name} CASCADE")
                print("Schema removed successfully!")
            except Exception as e:
                print("Failed to remove the schema.")
        else:
            print("No connection established, connect to the database.")

    def create_table(self, schema_name: str, table_name: str, column_names: List[str], column_types: List[str]):
        """
        Creates a new table in the specified schema.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table.
            column_names: List of column names for the table.
            column_types: List of column types for the table.
        """
        if self.connection != "":
            try:
                columns = []
                for name, type in zip(column_names, column_types):
                    column = f"{name} {type}"
                    columns.append(column)
                column_str = ", ".join(columns)
                query = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({column_str})"
                self.connection.execute(query)
                print(f"Table {schema_name}.{table_name} created successfully!")
            except Exception as e:
                print(f"Failed to create table {schema_name}.{table_name}. Error: {str(e)}")
        else:
            print("No connection established, connect to the database.")

    def drop_table(self, schema_name: str, table_name: str):
        """
        Removes a table from the specified schema.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table.
        """
        if self.connection != "":
            try:
                query = f"DROP TABLE IF EXISTS {schema_name}.{table_name}"
                self.connection.execute(query)
                print(f"Table {schema_name}.{table_name} removed successfully!")
            except Exception as e:
                print(f"Failed to remove table {schema_name}.{table_name}.")
        else:
            print("No connection established, connect to the database.")

    def truncate_table(self, schema_name: str, table_name: str):
        """
        Deletes all rows from a table.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table.
        """
        if self.connection != '':
            try:
                query = f"TRUNCATE TABLE {schema_name}.{table_name}"
                self.connection.execute(query)
                print(f'Table {schema_name}.{table_name} truncated successfully!')
            except Exception as e:
                print(f'Failed to truncate table {schema_name}.{table_name}.')
        else:
            print('No connection established, connect to the database.')

    def create_view(self, view_name: str, query: str):
        """
        Creates a view.

        Args:
            view_name: Name of the view.
            query: SQL query for the view.
        """
        if self.connection != '':
            try:
                self.connection.execute(f"CREATE VIEW {view_name} AS {query}")
                print(f'View {view_name} created successfully!')
            except Exception as e:
                print(f'Failed to create view {view_name}.')
        else:
            print('No connection established, connect to the database.')

    def drop_view(self, view_name: str):
        """
        Removes a view.

        Args:
            view_name: Name of the view.
        """
        if self.connection != '':
            try:
                self.connection.execute(f"DROP VIEW IF EXISTS {view_name}")
                print(f'View {view_name} removed successfully!')
            except Exception as e:
                print(f'Failed to remove view {view_name}.')
        else:
            print('No connection established, connect to the database.')

    def create_materialized_view(self, view_name: str, query: str):
        """
        Creates a materialized view.

        Args:
            view_name: Name of the materialized view.
            query: SQL query for the materialized view.
        """
        if self.connection != '':
            try:
                self.connection.execute(f"CREATE MATERIALIZED VIEW {view_name} AS {query}")
                print(f'Materialized view {view_name} created successfully!')
            except Exception as e:
                print(f'Failed to create materialized view {view_name}.')
        else:
            print('No connection established, connect to the database.')

    def refresh_materialized_view(self, schema_name: str, table_name: str):
        """
        Refreshes a materialized view.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table (materialized view).
        """
        if self.connection != '':
            try:
                query = f"REFRESH MATERIALIZED VIEW {schema_name}.{table_name}"
                self.connection.execute(query)
                print(f'Table {schema_name}.{table_name} refreshed successfully!')
            except Exception as e:
                print(f'Failed to refresh table {schema_name}.{table_name}.')
        else:
            print('No connection established, connect to the database.')

    def drop_materialized_view(self, schema_name: str, table_name: str):
        """
        Removes a materialized view.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table (materialized view).
        """
        if self.connection != '':
            try:
                self.connection.execute(f"DROP MATERIALIZED VIEW IF EXISTS {schema_name}.{table_name}")
                print(f'Materialized view {schema_name}.{table_name} removed successfully!')
            except Exception as e:
                print(f'Failed to remove materialized view {schema_name}.{table_name}.')
        else:
            print('No connection established, connect to the database.')

    def add_data_to_table(self, schema_name: str, table_name: str, data: dict):
        """
        Adds data to a table.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table.
            data: Dictionary containing the data to be inserted into the table.
        """
        if self.connection != '':
            try:
                columns = ', '.join(data.keys())
                values = ', '.join([f"'{value}'" for value in data.values()])
                query = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({values})"
                self.connection.execute(query)
                print(f'Data added to table {schema_name}.{table_name} successfully!')
            except Exception as e:
                print(f'Failed to add data to table {schema_name}.{table_name}.')
        else:
            print('No connection established, connect to the database.')

    def remove_data_from_table(self, schema_name: str, table_name: str, condition: str):
        """
        Removes data from a table.

        Args:
            schema_name: Name of the schema.
            table_name: Name of the table.
            condition: Condition to filter the data to be removed.
        """
        if self.connection != '':
            try:
                query = f"DELETE FROM {schema_name}.{table_name} WHERE {condition}"
                self.connection.execute(query)
                print(f'Data removed from table {schema_name}.{table_name} successfully!')
            except Exception as e:
                print(f'Failed to remove data from table {schema_name}.{table_name}.')
        else:
            print('No connection established, connect to the database.')

    def update_data_in_table(self, table_name: str, filters: dict, new_data: dict):
        """
        Updates a data in the table.

        Args:
            table_name: Name of the table.
            filters: Dictionary containing the filters for the WHERE clause.
            new_data: Dictionary containing the new data to be updated.
        """
        if self.connection != '':
            try:
                # Construct the WHERE clause based on the filters
                where_clause = ' AND '.join([f"{key} = '{value}'" for key, value in filters.items()])
                # Construct the SET clause based on the new data
                set_clause = ', '.join([f"{key} = '{value}'" for key, value in new_data.items()])
                query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                self.connection.execute(query)
                print(f'Data updated in table {table_name} successfully!')
            except Exception as e:
                print(f'Failed to update data in table {table_name}.')
        else:
            print('No connection established, connect to the database.')

    def select_from_table(self, table_name: str, columns: Optional[List[str]] = None, filters: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None) -> List[Tuple]:
        """
        Selects data from a table.

        Args:
            table_name: Name of the table.
            columns: List of columns to be selected. If not specified, all columns will be selected.
            filters: Dictionary containing the filters for the WHERE clause. Each key represents the column name and the value represents the filter value.
            order_by: String containing the field and classification for ordering. Example: 'id ASC'
        Returns:
            A list of tuples containing the selected data.
        """
        if self.connection != '':
            try:
                select_columns = '*' if columns is None else ', '.join(columns)
                where_clause = '' if filters is None else 'WHERE ' + ' AND '.join([f"{key} = '{value}'" for key, value in filters.items()])
                query = f"SELECT {select_columns} FROM {table_name} {where_clause} ORDER BY {order_by}"
                result = self.connection.execute(query)
                return result.fetchall()
            except Exception as e:
                print(f'Failed to fetch data from table {table_name}.')
        else:
            print('No connection established, connect to the database.')

    
    def execute_query(self, query: str) -> List[Tuple]:
        """
        Executes an SQL query.

        Args:
            query: SQL query to be executed.
        """
        if self.connection != '':
            try:
                result = self.connection.execute(query)
                print('Query executed successfully!')
                return result.fetchall()
            except Exception as e:
                print('Failed to execute the query.')
        else:
            print('No connection established, connect to the database.')

    
    def schema_exists(self, schema_name: str):
        """
        Checks if a schema exists in the database.

        Args:
            schema_name: Name of the schema to be checked.
        Returns:
            True if the schema exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return schema_name in inspector.get_schema_names()

    def table_exists(self, schema_name: str, table_name: str):
        """
        Checks if a table exists in the database.

        Args:
            schema_name: Name of the schema that contains the table.
        Returns:
            True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return inspector.has_table(table_name, schema=schema_name)
