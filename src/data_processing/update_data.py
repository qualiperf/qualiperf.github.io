"""Update webpage information.
To create the webpage data run
```
data_processing/persons.py
data_processing/news.py
```


## Create statistics
To create the statistics run
```
data_processing/news_statistics.py
```
"""
from data_processing.news import create_news_yaml
from data_processing.news_statistics import run_all as run_all_statistics
from data_processing.persons import create_persons_yaml

if __name__ == "__main__":
    # update data
    create_persons_yaml()
    create_news_yaml()

    # create statistics
    run_all_statistics()
