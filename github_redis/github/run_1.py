import logging
import os

def main():
    logging.warning("爬虫开启....")
    os.system("scrapy crawl github")


if __name__ == '__main__':
    main()

