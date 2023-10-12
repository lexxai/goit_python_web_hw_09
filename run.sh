#!/bin/bash

export PYTHONPATH=/app/src/hw09:/app/src
cd /app/src/hw09
echo Run Parser BeautifulSoup: src/hw09/parse.py
python parse.py
echo Run Parser Scrapy: src/hw09/main.py
python main.py