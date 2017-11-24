#Crawler_Fair

##Overview

Fair에 필요한 상품 데이터를 브랜드 별로 크롤링 하는 시스템

##Requirements

* Python 3.5+
* Works on Ubuntu, Mac OSX
* Additional virtual environment Docker 17.09+ ce
* Need to MySQL 5.5+ for RDS


##Install

The quick way::

    git clone git@bitbucket.org:jaemkor/crawler_fair.git
    cd crawler_fair
    pip install -r requirements.txt

##How to run?

###Docker 실행 

    docker pull scrapinghub/splash
    docker run -dit -p 8050:8050 scrapinghub/splash
    
###단일 크롤러 실행 시
    
    cd <project root>
    scrapy crawl <brand명>

###크롤러 시스템 실행 시

    cd <dir executed>
    nohub scarpyd &
    
크롤러 시스템 실행 시 크롤러 동작은 api 요청으로 실행 가능 합니다. 

자세한 사항은 아래 scrapyd api 문서를 참고하세요

Document scrapy cli at: https://doc.scrapy.org/en/latest/topics/commands.html

Document scrapyd cli at: https://scrapyd.readthedocs.io/en/latest/overview.html#scheduling-a-spider-run

Document scrapyd api at: https://scrapyd.readthedocs.io/en/latest/api.html

##Releases

Note v(0.0.1) : Prototype scrapy system

##Contributing

1. 각 계정별 dev branch 생성
- ex> dev-jayu
2. 코드 수정은 본인 dev branch 에 commit
3. origin branch 에 커밋 사항 반영 
4. develop branch 에 pull request
5. develop 단계 테스트 거친 후 realise 로 통합
6. version 업 한 후 master 로 통합

##Code of Conduct

PEP8를 준수 합니다.

##Commercial Support

이 시스템에 대한 문의 사항은 jayu에게 문의해 주세요
> jay.yu@jaem.me