from typing import Dict
import os
import json
import tqdm
from multiprocessing import Pool
from functools import partial
import click
from insert_to_graph import insert_to_stardog, __get_conn_details, check_database

@click.command()
@click.option('--db_name', prompt='Database name into StarDog', default="stress-test", help='Database name into StarDog')
@click.option('--path', default="/data", prompt='Path to directory with ttl decomposed files', help='Path to directory with ttl decomposed files')
@click.option('--count', default=500, prompt='Count of documents to insert into StarDog', help='Count of documents to insert into StarDog. To load all documents, use count=0')
@click.option('--workers', default=10, prompt='Number of cpus to process', help='Number of cpus to process')
@click.option('--endpoint', prompt='StarDog server', help='Endpoint to StarDog')
def main(db_name: str, path: str, workers: int, endpoint: str, count: int):  # , username: str, password: str):
    workers = int(workers)
    count = int(count)
    ttl_file_names = os.listdir(path)
    if count == 0:
        count = len(ttl_file_names)
    conn_details = __get_conn_details(endpoint)
    check_database(db_name, conn_details)

    print("/")
    result_of_insert_to_graphdb = []
    with Pool(processes=workers) as p:
        # https://stackoverflow.com/a/41921948
        with tqdm.tqdm(total=count) as pbar:
            for i, r in enumerate(
                    p.imap_unordered(partial(__task, path=path, conn_details=conn_details, db_name=db_name),
                                     ttl_file_names[:count])):
                pbar.update()
                result_of_insert_to_graphdb.append(r)
    print("/")
    print(f"{len(result_of_insert_to_graphdb)} files was processed")

    exceptions = [json.dumps(e) for e in result_of_insert_to_graphdb if e['exception']]

    if exceptions:
        print(f"There are {len(exceptions)} files that didn't load to StarDog")
        print(f"Please look at errors.log file for more information")
        with open("errors.log", "w") as f:
            f.writelines(exceptions)


def __task(ttl_file_name: str, path: str, db_name: str, conn_details: Dict):
    ttl_file_path = f"{path}/{ttl_file_name}"
    try:
        insert_to_stardog(ttl_file_path, conn_details=conn_details, db_name=db_name)
    except Exception as e:
        return {"exception": str(e), "file_name": ttl_file_path}
    return {"exception": None, "file_name": ttl_file_path}


if __name__ == '__main__':
    main()
