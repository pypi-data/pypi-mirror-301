from square_database_structure.square import (
    global_string_database_name as local_string_square_database_name,
)
from square_database_structure.square.authentication import (
    global_string_schema_name as local_string_square_authentication_schema_name,
)
from square_database_structure.square.authentication.tables import (
    Base as SquareAuthenticationBase,
    data_to_insert as local_list_square_authentication_data_to_insert,
)
from square_database_structure.square.file_storage import (
    global_string_schema_name as local_string_square_file_storage_schema_name,
)
from square_database_structure.square.file_storage.tables import (
    Base as SquareFileStorageBase,
    data_to_insert as local_list_square_file_storage_data_to_insert,
)
from square_database_structure.square.public import (
    global_string_schema_name as local_string_square_public_schema_name,
)
from square_database_structure.square.public.tables import (
    Base as SquarePublicBase,
    data_to_insert as local_list_square_public_data_to_insert,
)

global_list_create = [
    {
        "database": local_string_square_database_name,
        "schemas": [
            {
                "schema": local_string_square_public_schema_name,
                "base": SquarePublicBase,
                "data_to_insert": local_list_square_public_data_to_insert,
            },
            {
                "schema": local_string_square_file_storage_schema_name,
                "base": SquareFileStorageBase,
                "data_to_insert": local_list_square_file_storage_data_to_insert,
            },
            {
                "schema": local_string_square_authentication_schema_name,
                "base": SquareAuthenticationBase,
                "data_to_insert": local_list_square_authentication_data_to_insert,
            },
        ],
    }
]
