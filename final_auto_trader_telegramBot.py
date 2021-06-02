
import traceback as tb # https://hashcode.co.kr/questions/7570/python%EC%97%90%EC%84%9C-%EB%A6%AC%EC%8A%A4%ED%8A%B8%EA%B0%80-nonetype%EC%9C%BC%EB%A1%9C-%EB%B3%80%ED%95%A9%EB%8B%88%EB%8B%A4
import telegram
import pyupbit
import schedule
import time

# !!!주의사항!!!!
# 아래 본인값으로 변경 을 채우지 않으면 
# 이 소스는 정상적으로 작동되지 않습니다.
# 업비트 현금에 금액이 많이 들어가 있을때는 테스트 하지 마세요.
# 소액으로 테스트 해보고 사용하기 괜찮다 싶으면 고쳐서 사용하세요.
# 무엇보다 수익율이 검증 안된 소스이므로 사용전에 정말 신중하게 판단하세요.

bot = telegram.Bot(token='토큰값') # 본인값으로 변경
chat_id = 챗ID # 본인값으로 변경
##############################################################################
access = "액세스키"          # 본인 값으로 변경
secret = "시크릿키"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
##############################################################################

o = 900000   #투자금 은 본인에게 맞는 금액으로 변경하세요. 
k = 0
##############################################################################
def post_message(text):
    bot.sendMessage(chat_id=chat_id, text=text) # 텔레그램 알림으로 변경함.
    print(text)
##############################################################################    

def job(): # 아래 것을 주기적으로 실행
    global o, k
    try:
        
        a = upbit.get_balance("KRW")
        b = upbit.get_balance("KRW-BTC") * pyupbit.get_current_price("KRW-BTC")
        c = upbit.get_balance("KRW-XRP") * pyupbit.get_current_price("KRW-XRP")
        d = upbit.get_balance("KRW-DOGE") * pyupbit.get_current_price("KRW-DOGE")
        e = a + b + c + d - k
    
        if e/o >= 1.10 :
            k = (e-o)/2
            o = o + k
    
        if e/o <= 0.90 :
            k = (e-o)/2
            o = o + k
            
        e = a + b + c + d - k
        if b/e <= 0.695 and a>5000: 
            # 참이려면 비트코인 가격이 하락하였을 때지
            ticker ="KRW-BTC"
            tmpNum = 0.7*e-b
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum)     
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if b/e >= 0.705 :
            ticker ="KRW-BTC"
            tmpNum = (b-0.7*e)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)    
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
    
        if c/e <= 0.145 and a>5000:
            ticker ="KRW-XRP"
            tmpNum = 0.15*e-c
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum)    
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if c/e >= 0.155 :
            ticker ="KRW-XRP"
            tmpNum = (c-0.15*e)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)   
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
    
        if d/e <= 0.145  and a>5000 :
            ticker ="KRW-DOGE"
            tmpNum = 0.15*e-d
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum) 
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if d/e >= 0.155 :
            ticker ="KRW-DOGE"
            tmpNum = (d-0.15*e)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)       # DOGE로
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
    #except Exception as ex:
    except :
        #tb.print_exc()
        strMsg = tb.format_exc()
        post_message(strMsg)
        
strMsg ="==fial_auto 자동매매 시작 (구글 클라우드)=="    
post_message(strMsg)
schedule.every().minute.at(":00").do(job)
schedule.every().minute.at(":30").do(job)
while True:
    schedule.run_pending()
    time.sleep(2)