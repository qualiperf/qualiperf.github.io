# README
Python scripts for data processing and data preparation for the webpage.
Helper functions for creating reports.

## Installation
You can then create a new environment with name from the anaconda prompt via:

```bash
conda create -n qualiperf-site python=3.11
```

The dependencies can be installed in a virtual environment via:
```bash
cd src
conda activate qualiperf-site
(qualiperf-site) pip install -r requirements.txt --upgrade
```

## Update information
The master file for the information is in [`./assets/news/qualiferf_news.xlsx`](./assets/news/qualiferf_news.xlsx)

Based on these files the webpage can be updated via
```bash
src/data_processing/update_data.py
``





## TODO
- [ ] process all assets in standardized format for webpage & reports
- [ ] deploy webpage

- [ ] interactive tables for report (interactive tables (https://datatables.net/))
- [ ] interactive figures for report (https://altair-viz.github.io/gallery/index.html#example-gallery)
- [ ] webpage with figures and tables