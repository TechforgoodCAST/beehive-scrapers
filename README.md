Funder scrapers
===============

A collection of scrapers for gathering data from grant funders, intended
to be used in the Beehive funding platform.

Written using python3 and [scrapy](https://scrapy.org/)

Install
-------

1. Clone into new directory `git clone https://github.com/TechforgoodCAST/beehive-scrapers.git`
2. Setup virtual environment `python3 venv env`
3. Enter virtual environment `source env\bin\activate` (linux) or `env\Scripts\activate` (windows)
4. Install requirements `pip install -r requirements.txt`
5. (Windows only) install pypiwin32: `pip install pypiwin32`

Write a new spider
------------------

Run the command:

```bash
scrapy genspider -t fund_spider fundname "fundurl.com/path-to-fund-list"
```

Where:

- `fundname` is the name of the funder (all lowercase, no spaces or special characters)
- `"fundurl.com/path-to-fund-list"` should be the URL of the fund list page.

This will generate a skeleton scraper with the capability to:

- go through a fund list page
- generate titles and links for each fund
- go to a particular fund page and get more details
- go to the next page if the fund list is on more than one page

You'll need to adjust the css selectors depending on the exact structure
of the list page.

Run a spider
------------

### Comic relief

To output funds found to a `funds.jl` [JSON lines](http://jsonlines.org/) file
run: `scrapy crawl comicrelief -o funds.jl`

Run all spiders
---------------

To run all spiders use the following command:

```bash
python funderscrapers/crawl_all.py
```

You can also use `crawl_all.bat` in Windows or `./crawl_all.sh` in Bash.
