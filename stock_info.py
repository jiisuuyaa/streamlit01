import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
from io import BytesIO
# 주식 데이터
@st.cache_data
def get_stock_info():
    base_url = "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    url = "{0}?method={1}".format(base_url, method)
    df = pd.read_html(url, header=0,encoding='cp949')[0]
    df['종목코드'] = df['종목코드'].apply(lambda x: f"{x:06d}")
    df = df[['회사명', '종목코드']]
    return df
# 회사이름
def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명'] == company_name]['종목코드'].values
    ticker_symbol = code[0]
    return ticker_symbol
# 제목 가튼거
st.title('무슨 주식을 사야 부자가 되려나...')
st.sidebar.header('회사 이름과 기간을 입력하세요')
# 회사 이름과 날짜 범위를 입력받는 필드
company_name = st.sidebar.text_input('회사 이름', '삼성전자')
date_range = st.sidebar.date_input('시작일 - 종료일', [datetime.date(2019, 1, 1), datetime.date(2021, 12, 31)])
if st.sidebar.button('주가 데이터 확인'):
    try:
        ticker_symbol = get_ticker_symbol(company_name)
        start_date = date_range[0]
        end_date = date_range[1] + datetime.timedelta(days=1)
        # 주가 데이터 가져오기
        df = fdr.DataReader(f'KRX:{ticker_symbol}', start_date, end_date)
        df.index = df.index.date
        st.subheader(f"[{company_name}] 주가 데이터")
        st.dataframe(df.tail(7))
        # 데이터를 엑셀 파일로 다운로드할 수 있는 옵션 제공
        excel_data = BytesIO()
        df.to_excel(excel_data)
        st.download_button("엑셀 파일 다운로드", excel_data, file_name='stock_data.xlsx')
    except Exception as e:
       st.error(f"오류 발생: {e}")

