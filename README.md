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

Run a spider
------------

### Comic relief

To output funds found to a `funds.jl` [JSON lines](http://jsonlines.org/) file
run: `scrapy crawl comicrelief -o funds.jl`
