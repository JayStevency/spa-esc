# SPA-ESC(Elastic Search Crawler)

## Overview

This project is to collect SPA brands products for search engine

## Requirements

* Python 3.5+
* Works on Ubuntu, Mac OSX
* Additional virtual environment Docker 17.09+ ce
* Need to MySQL 5.5+ for RDS
* Need to ElasticSearch 6.0+ for Search Engine


## Set Environment variables

### For Mac OS

`~/.bash_profile` to set the following env variables on this file.

    export DB_USERNAME="<DB_USERNAME>"
    export DB_PORT="<DB_PORT>"
    export DB_PASSWORD="<DB_PASSWORD>"
    export DB_DATABASE="<DB_DATABASE>"
    export DB_HOST="<DB_HOST>"
    export DB_DIALECT="mysql"
    export SPLASH_URL="<SPLASH_URL>"
    export ES_URL="<ES_URL>"
    
### For Ubuntu

`/etc/environment` to set the following env variables on this file. 

    DB_USERNAME="<DB_USERNAME>"
    DB_PORT="<DB_PORT>"
    DB_PASSWORD="<DB_PASSWORD>"
    DB_DATABASE="<DB_DATABASE>"
    DB_HOST="<DB_HOST>"
    DB_DIALECT="mysql"
    SPLASH_URL="<SPLASH_URL>"
    ES_URL="<ES_URL>"

## Install

The quick way:

    git clone https://github.com/Jaystevency/spa-esc.git
    cd spa-esc
    pip install -r requirements.txt

## How to run?

### Docker exec for splash 

    docker pull scrapinghub/splash
    docker run -dit -p 8050:8050 scrapinghub/splash
    
### When do you want exec single crawler?
    
    cd <project root>
    scrapy crawl <brand_name>

### When do you want exec crawler system?

    cd <dir executed>
    nohub scarpyd &
    
### Reference 

Document scrapy cli at: https://doc.scrapy.org/en/latest/topics/commands.html

Document scrapyd cli at: https://scrapyd.readthedocs.io/en/latest/overview.html#scheduling-a-spider-run

Document scrapyd api at: https://scrapyd.readthedocs.io/en/latest/api.html

## Releases

Note v(0.0.2) : Connected to ES System

Note v(0.0.1) : Prototype scrapy system

## How to Contribute?

1. create dev branch
2. commit to one's dev branch
3. push to origin one's branch  
4. pull request to develop branch
5. after test, integrate develop on release
6. up to version and integrate release on master

##Code of Conduct

PEP8
