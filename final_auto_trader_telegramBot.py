
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

bot = telegram.Bot(token='토큰값') # 본인 토큰 값으로 변경
chat_id = 챗ID # 본인값으로 변경
##############################################################################
access = "액세스키"          # 본인 값으로 변경
secret = "시크릿키"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
##############################################################################

o = 900000   #투자금 900000 은 본인에게 맞는 금액으로 변경하세요. 
k = 0
##############################################################################
def post_message(text):
    bot.sendMessage(chat_id=chat_id, text=text) # 텔레그램 알림으로 변경함.
    print(text)
##############################################################################    

##############################################################################
# 매수수량 x 매수시 평균 단가 
def getVolumeAvgBuyPrice():
    result=0.0
    balances = upbit.get_balances()
    for i in range(0,len(balances)):
        ticker='KRW-' + balances[i]['currency']
        ticker_id = balances[i]['currency']
        if ticker_id == 'BTC' or ticker_id == 'XRP' or ticker_id == 'DOGE' or ticker_id == 'ETH':
            w0 = float(balances[i]['avg_buy_price']) # 매수시 단가
            #w1 = float(pyupbit.get_current_price(ticker)) # 현재 단가
            v = float(balances[i]['balance'])
            #print(ticker, balances[i]['avg_buy_price'], pyupbit.get_current_price(ticker),  (w1*v)/(w0*v)  - 1.0) # 매수시 단가 조회,  현재단가조회
            result += w0 * v
            
    return result
##############################################################################


def job(): # 아래 것을 주기적으로 실행
    global o, k
    try:
        
        a0 = upbit.get_balance("KRW")
        a1 = getVolumeAvgBuyPrice()
        
        if a1>900000: #투자금 900000 은 본인에게 맞는 금액으로 변경하세요. 
            a0=0
        else :
            a2 = 900000 - a1 #투자금 900000 은 본인에게 맞는 금액으로 변경하세요. 
            if a2<=a0:
                a0 = a2
        a = a0
        
        b = upbit.get_balance("KRW-BTC") * pyupbit.get_current_price("KRW-BTC")
        c = upbit.get_balance("KRW-ETH") * pyupbit.get_current_price("KRW-ETH")
        d = upbit.get_balance("KRW-XRP") * pyupbit.get_current_price("KRW-XRP")
        e = upbit.get_balance("KRW-DOGE") * pyupbit.get_current_price("KRW-DOGE")
        f = a + b + c + d + e - k
    
        if f/o >= 1.10 :
            k = (f-o)/2
            o = o + k
    
        if f/o <= 0.90 :
            k = (f-o)/2
            o = o + k
            
        f = a + b + c + d + e - k
        if b/f <= 0.695 and a>5000: 
            # 참이려면 비트코인 가격이 하락하였을 때지
            ticker ="KRW-BTC"
            tmpNum = 0.7*f-b
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum)     
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if b/f >= 0.705 :
            ticker ="KRW-BTC"
            tmpNum = (b-0.7*f)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)    
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
    
        if c/f <= 0.145 and a>5000:
            ticker ="KRW-ETH"
            tmpNum = 0.15*f-c
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum)    
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if c/f >= 0.155 :
            ticker ="KRW-ETH"
            tmpNum = (c-0.15*f)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)   
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
    
        if d/f <= 0.145  and a>5000 :
            ticker ="KRW-XRP"
            tmpNum = 0.15*f-d
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum) 
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if d/f >= 0.155 :
            ticker ="KRW-XRP"
            tmpNum = (d-0.15*f)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)       # DOGE로
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if e/f <= 0.145  and a>5000 :
            ticker ="KRW-DOGE"
            tmpNum = 0.15*f-e
            if tmpNum> 5000 :
                upbit.buy_market_order(ticker, tmpNum) 
                strMsg = "매수 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)
            
        if e/f >= 0.155 :
            ticker ="KRW-DOGE"
            tmpNum = (e-0.15*f)/pyupbit.get_current_price(ticker)
            if tmpNum *pyupbit.get_current_price(ticker) > 5000 :
                upbit.sell_market_order(ticker, tmpNum)       # DOGE로
                strMsg = "매도 : " + ticker + " = " + str(tmpNum)
                post_message(strMsg)

    #except Exception as ex:
    except :
        #tb.print_exc()
        strMsg = tb.format_exc()
        post_message(strMsg)
        
strMsg ="==fial_auto 자동매래 시작 (구글 클라우드)=="    
post_message(strMsg)
schedule.every().minute.at(":00").do(job)
schedule.every().minute.at(":30").do(job)
while True:
    schedule.run_pending()
    time.sleep(2)