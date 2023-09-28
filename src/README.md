# README
## Installation

You can then create a new environment with name from the anaconda prompt via:

conda create -n qualiperf-site python=3.9

The dependencies can be installed in a virtual environment via:
```
cd src
conda activate qualiperf-site
(qualiperf-site) pip install -r requirements.txt --upgrade
```

## Create statistics
To create the statistics run
```
data_processing/news_statistics.py
```
