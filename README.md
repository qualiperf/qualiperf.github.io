# qualiperf.github.io

# Webpage information
Information is either manually updated in this repository in the `_data` folder (everything besides `news.yml` and `persons.yml`) or by running the `update_data.py` script. 

- update the news form
- the information has to be included in the `qualiperf_news.xlsx`


# Installation & setup
This section describes how to setup the environment for local development of the webpage. 

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

For setup of the python environment see
[`./src/README.md`](./src/README.md).



