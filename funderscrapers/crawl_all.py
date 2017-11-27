from subprocess import check_output, call
scrapers = check_output("scrapy list").splitlines()
for s in scrapers:
    call("scrapy crawl {}".format(s.decode("utf8")))
