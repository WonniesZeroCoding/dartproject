#!/usr/bin/env python
# coding: utf-8


### 설치할 프로그램 및 라이브러리 , API
# pip install pykrx
# pip install opendartreader
# python -m pip install -U matplotlib
# python install beautifulsoup4
# pip install pandas

# krx 정보데이터 시스템에서 제공하는 라이브러리
from pykrx import stock

from bs4 import BeautifulSoup

import pandas as pd

# Dart에서 제공하는 라이브러리
import OpenDartReader

import re
import datetime

# 현재 날짜 구하기
currentDate = datetime.date.today()

# date 사용하기 - format 형태 %Y%m%d
today = currentDate.strftime("%Y%m%d")

# dart를 사용하기 위한 Api_key
api_key = "af27b93d3dd0c6f0aed900dda6f3a09daccb7360"
dart = OpenDartReader(api_key)

# tickers = stock.get_market_ticker_list("20190225", market="KOSDAQ") market=에 KOSPI, KOSDAQ, KONEX 등 조회할 시장 지정 가능
tickers = stock.get_market_ticker_list(market="ALL")

# print(tickers) 기업 코드 잘 가지고 오는지 확인
# print(len(tickers)) len을 써서 list안의 갯수가 몇개인지 확인 -> 2635개

# 회사 리스트 초기화
companyList = []

for i in tickers:

    # 기업 코드 내에 영어가 포함된 값 찾기 - 파이썬 정규 표현 모듈 re
    exp = re.findall("[a-zA-Z]", i)

    # 기업 코드 내에 K등의 영어가 포함된 코드는 우선주 이기 때문에 보고자 하는 데이터에서 제외시켜야함

    # 필터에 걸리지 않은 데이터만 리스트에 Input
    if not exp:
        companyList.append(i)

# 필터링된 기업 갯수 조회
# print(len(companyList)) 2612개 (2635 -> 2612)


# 재무제표 가져오기
income = dart.finstate_all(
    # reprt_code = "11013"=1분기보고서,  "11012"=반기보고서,  "11014"=3분기보고서, "11011"=사업보고서
    "005930",
    2021,
    reprt_code="11011",
)  # 단일 기업 재무제표 가져오기 ex- 삼성전자

# 재무제표 항목에서 어떤 항목이 있는지 확인 --> 영업이익 부분 확인
# for i in income["account_nm"]:
#     print(i)

# 영업이익 금액 확인
salesAmount = int(income["thstrm_amount"][57])
print(salesAmount)  # 결과 값 9382868000000 (단위는 원)

## 결과값에서 000000 제거 -> 백만원으로 표기


# 시가 총액 구하기
data = stock.get_market_cap(today, today, "005930")
totalAmount = data["시가총액"][0]
print(totalAmount)  # 결과 값 369529539845000 원

# 멀티플(10) 개념을 이용하여 영업 이익에 PER 밸류를 구하고 시총과 비교하여 저평가 기업 산출
# 순이익이 아니라 영업이익을 이용해서 산출하는 이유 : 당기 순이익은 금융 손익과 영업외 손익도 계산된 수치이므로 이익의 질 훼손의 우려가 있음
# (영업이익 * 10) > 시가총액 == 저평가 기업
print(salesAmount * 10 > totalAmount)  # True False 로 리턴. 결과 값이 True 라면 저평가 기업
print(f"salesAmoun*10: {salesAmount*10} totalAmount: {totalAmount}")
