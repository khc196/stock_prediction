#-*-coding utf-16-*-
import pandas as pd
import urllib.request, time, os, re, csv, sys, ast
from bs4 import BeautifulSoup
import unicodedata

f = open("code_list.txt", "r")
string_content = f.read()
dict_code = ast.literal_eval(string_content)
f.close()

def preformat_cjk (string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
        }[align](string)


def get_url(code, page=None):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    if page != None:
        url +='&page='+ str(page)

    #url = 'http://finance.daum.net/item/main.daum?code={code}'.format(code=code)
    #print("URL = {}".format(url))
    return url
                        
def fetch(url, ticker):
    req = urllib.request.urlopen(url)
    charset=req.info().get_content_charset() 
    if not charset == None:
        txt=req.read().decode(charset)
    else:
        txt=req.read().decode()
    source = BeautifulSoup(txt, "html.parser")
    table = source.find("table")
    tr_list = table.find_all("tr")
    data_list = []
    for tr in tr_list:
        if tr.span != None:
            date = tr.find_all("td",align="center")[0].text
            price_list = tr.find_all("td",class_="num")
            is_up = True

            for price in price_list:
                temp = price.find_all("img")
                if len(temp) > 0:
                    for item in temp:
                        if "상승" in item['alt']:
                            is_up = True
                            break
                        elif "하락" in item['alt']:
                            is_up = False
                            break
                        else:
                            is_up = None
                            break
            temp = [ date, ]
            for i in price_list:
                temp.append(re.sub('[^A-Za-z0-9.]+', '', i.text))
            temp.append(is_up)
            data_list.append(tuple(temp))
    return data_list
    
def get_maxpage(ticker):
    url = get_url(dict_code[ticker])
    req = urllib.request.urlopen(url)
    charset=req.info().get_content_charset() 
    if not charset == None:
        txt=req.read().decode(charset)
    else:
        txt=req.read().decode()
    source = BeautifulSoup(txt, "html.parser")

    maxPage= source.find_all("table",align="center") 
    mp = maxPage[0].find_all("td",class_="pgRR") 
    mpNum = int(mp[0].a.get('href')[-3:])
    return mpNum

def combine(ticker, page=None):
    url = get_url(ticker, page)
    data_list = fetch(url, ticker)
    t=time.localtime()    
    
    #output=[t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec,ticker,price,rate]
    output=data_list
    return output

if __name__ == "__main__":
    #tickers = ["신라젠", "SK네트웍스"]
    tickers = dict_code.keys()
    # Set local time zone to Seoul
    os.environ['TZ']='Asia/Seoul'
    time.tzset()
    t=time.localtime() # string
    print(time.ctime())

    # define the name of an output file
    fname="portfolio.csv"

    # remove a file, if exist
    os.path.exists(fname) and os.remove(fname)

    # set frequency
    freq=1


    with open(fname,'a') as f:

        writer=csv.writer(f,dialect="excel") #,delimiter=" ")
        print("{} | {} | {} | {} | {} | {} | {} | {}".format(preformat_cjk("날짜", 10), preformat_cjk("이름", 20), preformat_cjk("종가", 8), preformat_cjk("전일비", 8), preformat_cjk("시가", 8), preformat_cjk("고가", 8), preformat_cjk("저가", 8), preformat_cjk("거래량", 10)))
        print("-------------------------------------------------------------------------------------------------")
        while(True):
            if(t.tm_hour==15):
                while(t.tm_min<30):
                    for ticker in tickers:
                        data=combine(dict_code[ticker])
                        print(data)
                        writer.writerow(data)
                    time.sleep(freq)

                else:
                    break
            else:
                if sys.argv[1] == "all": 
                    for ticker in tickers:
                        data_list = combine(dict_code[ticker])
                        for data in data_list:
                            up_or_down = ""
                            if int(data[2]) == 0:
                                up_or_down = "-" 
                            elif data[7] is True:
                                up_or_down = "↑"
                            elif data[7] is False:
                                up_or_down = "↓"
                            else:
                                up_or_down = "-"
                            rate = data[2] + ' ' + up_or_down
                            output = "{data[0]:^10} | {ticker} | {data[1]:<8} | {rate:<8} | {data[3]:<8} | {data[4]:<8} | {data[5]:<8} | {data[6]:<10}"                
                            name = preformat_cjk(ticker, 20)
                            print(output.format(data=data, ticker=name, rate=rate))
                            writer.writerow(data)
                        time.sleep(freq)
                else:
                    ticker = sys.argv[1]
                    maxpage = get_maxpage(ticker)
                    for page in range(1, maxpage):
                        data_list = combine(dict_code[ticker], page)
                        for data in data_list:
                            up_or_down = ""
                            if int(data[2]) == 0:
                                up_or_down = "-" 
                            elif data[7] is True:
                                up_or_down = "↑"
                            elif data[7] is False:
                                up_or_down = "↓"
                            else:
                                up_or_down = "-"
                            rate = data[2] + ' ' + up_or_down
                            output = "{data[0]:^10} | {ticker} | {data[1]:<8} | {rate:<8} | {data[3]:<8} | {data[4]:<8} | {data[5]:<8} | {data[6]:<10}"                
                            name = preformat_cjk(ticker, 20)
                            print(output.format(data=data, ticker=name, rate=rate))
                            writer.writerow(data)
                        time.sleep(freq)






