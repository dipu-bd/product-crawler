# Dungulie Product Crawler

Clone this repository:

`git clone ssh://git@phabricator.codemaster.io:2222/diffusion/28/dung-prod.git`


## daraz-crawler
To run this crawler:

- Setup MongoDB
- Go inside `daraz-crawler/daraz`
- Update mongodb uri and database name in scrappy `settings.py`
- Run crawler from `daraz-crawler` with `scrapy crawl products`
- The crawled items are stored in your specified database.

