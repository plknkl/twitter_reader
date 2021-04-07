```mermaid
graph TD
    jupyter[Jupyter Notebook] -->|imports| data_storage[Data Storage]
    jupyter -->|imports| twitter_manager[Twitter Manager]
    data_storage -->|rw| database[Database]
    twitter_manager[Twitter Reader] -->|queries| twitter_api[Twitter Api]
```

## Jupyter Notebook
The notebook is used as the interface to the user, it imports the Twitter Manager library for some functionality to query the Twitter API. Imports the data storage module to have some persistance.

## Twitter Manager
Can query the Twitter API with a term.

## Data Storage
Can save and read saved tweets.