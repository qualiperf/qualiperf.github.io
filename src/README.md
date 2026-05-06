# README
## Qualiperf news & achievements
Python scripts for data processing and data preparation for the webpage.
Helper functions for creating reports and processing the reported news and achievements.

## Installation
You can install the dependencies with uv:

```bash
uv sync
```

## Update information
The master file for the information is in [`./assets/news/qualiferf_news.xlsx`](./assets/news/qualiferf_news.xlsx)

The the news and achievement form is at
https://docs.google.com/forms/d/1FO7ZWOKAkyTJUvzysJaWg9M9dRp6lS8JID6Euj9s3hw/edit?usp=drive_web&ouid=107726306318006226544
The unprocessed results are available here
https://docs.google.com/spreadsheets/d/14V3cw2eMRYb2L9utxKAl4vtFpwSonklIhW2ixByKIis/edit?gid=1338950615#gid=1338950615

Before the scripts are executed the new entries have to be manually cleaned up and transferred to the `qualiperf_news.xlsx`.

Based on these files the webpage can be updated via
```bash
src/data_processing/update_data.py
```

## TODO
- [ ] create category figure (barplot with categories)
- [ ] interactive figures for report (https://altair-viz.github.io/gallery/index.html#example-gallery)

- [ ] deploy newspage
- [ ] webpage with figures and tables
- [ ] deploy webpage

