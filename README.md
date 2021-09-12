## News Crawler And Finder
This project contains two applications.
One( the scrapy crawler) populates a data source by crawling BBC rss feed and creating news items.
The other(search_app) exposes an endpoint to search those news items.

The data source is a docker hosted mongo-db, it comes with a separate mongo-express container.

#### Prerequisites
It is assumed that the running machine has python3, and docker(docker-compose).

After running scrapy_app, the mongo-db should be populated with some data, can be confiremd by using mongo-db-express from browser : ```http://localhost:8081/```

Search app can be queried by curl for example ```curl http://localhost:8888/find?query=news ```
Search is done only on titles at the moment.

### scrapy_app
This project is a scrapy implementation for a BBC rss feed. It follows the recommended scrapy project structure. 

settings.py contains the mongodb location(not the safest way). The mongo-db is where the crawler and the search_app send and read data from.

NOTE: The "tests" folder contains a few to unit tests to show the concept but by no means adequate.
##### Install dependencies
from scrapy-app folder run ```python3 -m venv p3env && source p3env/bin/activate && pip install -r requirements.txt```

##### Unit tests
 from scrapy-app folder run ```python -m unittest discover -s crawler/tests -p "test_*.py"```
##### Run scrapy_app
from scrapy-app folder run ```scrapy crawl bbc```

### search_app
This is a bare minium tornado app, taking advantage of on async MongoDb client (Motor).
The strcutre could be the well known WebRequestHandler-> Service -> repository.
But did not follow the classics due to the simplicity of the project.

To run search_app, switch to search-app folder
##### install dependencies
From search-app folder run
```python3 -m venv p3env && source p3env/bin/activate && pip install -r requirements.txt```

##### Unit tests
From search-app folder run
```python3 -m unittest discover -s tests -p "test_*.py"```

#### Run search App
From search-app folder run
```python3 server.py```


### TODOs
- scrapy: async scrapy insert into mongoDb
- scrapy: add missing unit tests(pipeline)
- scrapy: author
- scrapy: integration tests
- search: integration tests
- search: if mongo server is there, but no db or collection handle exception. 
 