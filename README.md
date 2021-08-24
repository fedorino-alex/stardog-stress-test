# stardog-stress-test

Small project for demonstrating how to ingest data into StarDog graph database.

## Building image 

```{bash}
docker build -t stress-test .
```

## Run container

```{bash}
docker run -it -v <folder-with-tpls>:/data stress-test
```

## Parameters

By default, using next parameters:
- --db_name: name of database; 
- --path='/data'
- --count=100
- --workers=10
- --endpoint: path to stardog server
