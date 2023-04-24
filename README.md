# qualiperf.github.io

# Update information
- update the news form
- the information has to be included in the `qualiperf_news.xlsx`

# Installation & setup
This section describes how to setup the environment for local development.

## Jekyll local development server
Install dependencies for bundle
```bash
sudo apt -y install make build-essential ruby ruby-dev ruby-bundler
```

Install bundle
```bash
bundle config set --local path 'vendor/bundle'
bundle install
```

Serve local site
```
bundle exec jekyll serve --livereload
```
This starts a development server at http://127.0.0.1:4000/


## Python
For validation and processing of the information some python scripts exists.
These should be executed in a virtual environment.

### Setup virtual environment
```bash
cd src
mkvirtualenv qualiperf-site
(qualiperf-site) pip install -r requirements.txt
```

### Run scripts
- `data_processing/persons.py`: script for validating and checking person information
- `data_processing/news.py`: script for validating and checking person information


