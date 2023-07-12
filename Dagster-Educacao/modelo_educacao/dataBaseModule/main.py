import sys
from database import DataBase
from xlsximport import XlsxImport

db = DataBase()

db.connect()

# if len(sys.argv) < 4:
#     print("Argumentos insuficientes. Utilize: main.py <schema_name> <table_name> <file_path>")
#     sys.exit(1)

# schema_name = sys.argv[1]
# table_name = sys.argv[2]
# file_path = sys.argv[3]

# column_names = XlsxImport.get_column_names(file_path)

# if not db.schema_exists(schema_name):
#     db.create_schema(schema_name)

# if not db.table_exists(schema_name, table_name):
#     column_types = XlsxImport.get_column_types(column_names)
#     db.create_table(schema_name, table_name, column_names, column_types)

# data_rows = XlsxImport.get_data_rows(file_path)

# data_rows = [[value.replace("'", "") if isinstance(value, str) else value for value in row] for row in data_rows]

# for row in data_rows:
#     data = dict(zip(column_names, row))
#     db.add_data_to_table(schema_name, table_name, data)

db.disconnect()