# square_database_structure (WIP)

## about

square_database_structure is a Python module that provides a structured and modular way to define database schemas and
tables using SQLAlchemy. It is designed to work with **PostgreSQL** databases, which natively support a
database-schema-table hierarchy. This structure allows for clear separation between schemas within a single database,
making it easier to manage large and complex database systems.

This module abstracts the database structure from the rest of the application logic, making schema definitions reusable
and easy to maintain across multiple projects.

### goals

- Centralize Database Schema Definitions: Serve as a single source of truth for defining database structures across
  multiple projects.
- Modular Design: Allow databases and schemas to be independently defined and easily extended.
- PostgreSQL Compatibility: Utilize PostgreSQL's native support for database-schema-table hierarchy, allowing for
  separation of concerns and scalability.
- Replaceability: The module should be easy to substitute with another implementation if necessary, while still
  following the same mechanisms for schema and data definition.
- Explicit Structure: Ensure a clear, standardized structure that is easy to follow, making the design more explicit for
  users.

## installation

```shell
pip install square_database_structure
```

## usage

This module organizes database schemas in a standardized folder structure where each top-level folder represents a
database, and subfolders within it represent schemas. All mandatory components, such as ```__init__.py``` and tables.py,
need to follow this structure.

### Folder Structure

Here’s how you should organize your project when using this module:

```
square_database_structure/
├───main.py                    # Global definition file (mandatory)
├───create_database.py         # Global database creation file (mandatory)
└───database1/                 # Each folder corresponds to a separate database
    ├───__init__.py            # Mandatory: Contains the global name for the database
    └───schema1/               # Each subfolder corresponds to a schema within the database
        ├───__init__.py        # Mandatory: Contains the global name for the schema
        └───tables.py          # Mandatory: Defines tables and optional data for insertion
```

- Top-level folders: Represent individual databases (e.g., database1).
- Subfolders: Represent schemas within each database (e.g., public, schema1).
- Mandatory files:
    - ```__init__.py``` (both at the database and schema level).
    - tables.py within each schema.

### Defining Database and Schema Names in ```__init__.py```

Each database and schema folder must contain an ```__init__.py``` file where the database and schema names are defined
as
global variables.

#### Example for Database:

```python
# database1/__init__.py

global_string_database_name = "database1"  # Mandatory: Database name
```

#### Example for Schema:

```python
# database1/schema1/__init__.py

global_string_schema_name = "schema1"  # Mandatory: Schema name
```

### Defining Tables in tables.py

Each schema folder must contain a tables.py file where:

- You must declare a Base object tied to the schema.
- You can define table classes, extending the Base object.
- You must declare a data_to_insert list to store optional data that may be inserted into the schema's tables.

#### Example tables.py:

```python
# database1/schema1/tables.py

from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from database1.schema1 import global_string_schema_name

# 1. Mandatory: Declare Base with MetaData pointing to the schema

Base = declarative_base(metadata=MetaData(schema=global_string_schema_name))

# 2. Mandatory: Initialize a list for optional data insertion

data_to_insert = []


# 3. Optional: Define table classes by extending Base

class App(Base):
    __tablename__ = 'app'


id = Column(Integer, primary_key=True)
app_name = Column(String, nullable=False)

# Optional: Append data to be inserted into the table

data_to_insert.append(App(app_name="example_app"))
```

### Centralized Definitions in main.py

The main.py file is mandatory and contains a global list that maps databases to schemas and their corresponding table
definitions. This list is manually created by the user (for now).

#### Example main.py:

```python
# main.py

from database1.schema1 import global_string_schema_name as schema1_name
from database1.schema1.tables import Base as Schema1Base, data_to_insert as schema1_data

from database1 import global_string_database_name as database1_name

# Global list that maps databases and schemas

global_list_create = [
    {
        "database": database1_name,  # Mandatory: Database name
        "schemas": [
            {
                "schema": schema1_name,  # Mandatory: Schema name
                "base": Schema1Base,  # Mandatory: Base for this schema
                "data_to_insert": schema1_data,  # Mandatory: Data to insert (even if empty)
            },
        ],
    }
]
```

This file centralizes the definition of each database and schema, including the associated Base and data_to_insert for
table definitions.

### Creating Tables

Once you have defined your databases, schemas, and tables, you can create them in your PostgreSQL database by using the
`create_database_and_tables` function.

```python
from square_database_structure import create_database_and_tables

# Define the database connection details
db_username = "your_username"
db_password = "your_password"
db_ip = "localhost"
db_port = 5432

# Call the function to create the database and tables
create_database_and_tables(db_username, db_password, db_ip, db_port)
```

## env

- python>=3.12.0

## changelog

### v1.1.0

- add database, schema and table creation logic (from square database) (removed logs).

### v1.0.3

- change structure of square->authentication->UserApp and square->authentication->UserSession (due to complications with
  Composite Key).
- change default data in square->public->app.

### v1.0.2

- replace file_purpose with app_id in file_storage.

### v1.0.1

- add main.py file to have explicit mapping and ordering for schemas to be created.
- move database and schema names to ```__init__.py```.
- add app table in public, change user, remove profile and add user app and remove enums.

### v1.0.0

- initial commit.

## Feedback is appreciated. Thank you!
