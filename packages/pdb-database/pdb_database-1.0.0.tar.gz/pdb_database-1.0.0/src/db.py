import sqlite3
from contextlib import contextmanager

class Pdb:
    def __init__(self, db_name: str):
        """Initialize the database connection."""
        self.db_name = db_name

    @contextmanager
    def connect(self):
        """Context manager for database connection."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def create_table(self, table_name: str, columns: dict):
        """Create a table with given columns."""
        columns_with_types = ", ".join([f"{col} {col_type}" for col, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        with self.connect() as cursor:
            cursor.execute(query)

    def insert(self, table_name: str, data: dict):
        """Insert data into a table."""
        if not data:
            raise ValueError("Data dictionary cannot be empty.")
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        with self.connect() as cursor:
            cursor.execute(query, values)



    def select(self, table_name: str, columns: list = None, query: dict = None):
        """Retrieve data from a table and return it as a list of dictionaries."""
        columns_str = ', '.join(columns) if columns else '*'
        query_str = ""
        
        if query:
            # Construct the WHERE clause from the query dictionary
            conditions = []
            for key, value in query.items():
                conditions.append(f"{key} = ?")
            query_str = " WHERE " + " AND ".join(conditions)
        
        # Construct the final SQL query
        sql_query = f"SELECT {columns_str} FROM {table_name}{query_str}"
        
        with self.connect() as cursor:
            cursor.execute(sql_query, tuple(query.values()) if query else [])
            rows = cursor.fetchall()
            
            # Convert rows to a list of dictionaries if columns are specified
            if columns:
                result = [dict(zip(columns, row)) for row in rows]
            else:
                result = [list(row) for row in rows]
        
        return result



    def update(self, table_name: str, updates: dict, conditions: str = ""):
        """Update data in a table."""
        updates_str = ', '.join([f"{col} = ?" for col in updates])
        values = tuple(updates.values())
        query = f"UPDATE {table_name} SET {updates_str} {conditions}"
        with self.connect() as cursor:
            cursor.execute(query, values)

    def delete(self, table_name: str, conditions: str = ""):
        """Delete data from a table."""
        query = f"DELETE FROM {table_name} {conditions}"
        with self.connect() as cursor:
            cursor.execute(query)

    def drop_table(self, table_name: str):
        """Drop a table."""
        query = f"DROP TABLE IF EXISTS {table_name}"
        with self.connect() as cursor:
            cursor.execute(query)
