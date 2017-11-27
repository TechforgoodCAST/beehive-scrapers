#!/bin/sh
scrapy list | while read x; do scrapy crawl $x; done