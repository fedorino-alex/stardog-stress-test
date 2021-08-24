from typing import Dict, Union
import stardog
import re

def convert_date(s: str) -> str:
    # Just remove date field
    return re.sub("\^\^xsd:dateTime", "", s)


def insert_to_stardog(ttl_file_path: str, conn_details: Dict, db_name: str) -> Union:
    with stardog.Connection(db_name, **conn_details) as conn:
        conn.begin()
        with open(ttl_file_path, 'rb') as f:
            ttl_data = convert_date(f.read().decode("UTF-8")).encode("UTF-8")
        conn.add(stardog.content.Raw(ttl_data, 'text/turtle'))
        conn.commit()

def __get_conn_details(endpoint: str) -> Dict:
    conn_details = {'endpoint': endpoint}
    return conn_details

def check_database(db_name: str, conn_details: Dict) -> Union:
    with stardog.Admin(**conn_details) as admin:
        databases = {db.name for db in admin.databases()}
        if db_name in databases:
            use_existing_database = input(f"Files will be upload to existing {db_name}! Are you sure[Y/n]:")
            if use_existing_database.lower() == "n":
                print("Exit. You don't want to use existing database")
                exit(0)
        else:
            create_new_database = input(f"There is no database {db_name}. Create it? [Y/n]:")
            if create_new_database.lower() == "y":
                db = admin.new_database(db_name)
            else:
                print("Exit. You don't want to create new database")
                exit(0)
