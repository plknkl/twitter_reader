```mermaid
graph TD
    jupyter[Jupyter Notebook] -->|imports| twitter_reader
    twitter_reader --> |reads writes| db[Database]
    twitter_reader[Twitter Reader] -->|queries| twitter_api[Twitter Api]
```

## Jupyter Notebook
The notebook is used as the interface to the user, it imports the Twitter Reader library and offers some functions to query the Twitter API.

## Twitter Reader
The library which contains the functions to access the Twitter API, and has persistance capabilities thanks to a sqlite interface.

## Database
A simple SQlite database.