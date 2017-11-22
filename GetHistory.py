import oandapy
import csv
import datetime as dt

environment = "practice"
access_token = "access_token"
oanda = oandapy.API(environment=environment,
                    access_token=access_token
                    )
buffer = []
history = []
granularity = "S5"# every 5 second
count = 0

def set_end(instrument):
    # 先頭のデータのtimeを取得して、RFC3339フォーマットをpythonのdatetimeフォーマットに変換
    dtime = dt.datetime.strptime(instrument[0]['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    # もう一度RFC3339フォーマットに変換
    rfc_endtime = dtime.isoformat('T')
    return rfc_endtime


try:
    response = oanda.get_history(instrument="USD_JPY", granularity=granularity, count=5000)
    USD_JPY_D = response.get("candles")  # get candles
    for R in USD_JPY_D:
        time = R['time'].rstrip('.000000Z').rstrip(':')
        year = time[0:4]  # get year
        month = time[5:7]  # get month
        day = time[8:10]  # get day
        t_time = time[11:19]  # get time
        if len(t_time) == 5:
            t_time += ':00'
        elif len(t_time) == 7:
            t_time += '0'
        openBid = str(R['openBid'])
        openAsk = str(R['openAsk'])
        highBid = str(R['highBid'])
        highAsk = str(R['highAsk'])
        lowBid = str(R['lowBid'])
        lowAsk = str(R['lowAsk'])
        closeBid = str(R['closeBid'])
        closeAsk = str(R['closeAsk'])
        volume = str(R['volume'])
        complete = R['complete']
        Body = [year, month, day, t_time, openBid, openAsk, highBid, highAsk, lowBid, lowAsk, closeBid, closeAsk,
                volume]
        buffer.append(Body)
        count+=1
        print(str(count)+"周目")
except Exception as e:
    print(e)

buffer.reverse()
for b in buffer:
    history.append(b)

for i in range(10):
    buffer = []
    try:
        end_time = set_end(USD_JPY_D)
        response2 = oanda.get_history(instrument="USD_JPY", granularity=granularity, end=end_time, count=5000)
        USD_JPY_D = response2.get("candles")  # responseのcandles部分を回収
        for R in USD_JPY_D:
            time = R['time'].rstrip('.000000Z').rstrip(':')
            year = time[0:4]  # 年取り出し
            month = time[5:7]  # 月取り出し
            day = time[8:12]  # 日取り出し
            t_time = time[11:19]  # 時刻取り出し
            if len(t_time) == 5:
                t_time += ':00'
            elif len(t_time) == 7:
                t_time += '0'
            openBid = str(R['openBid'])
            openAsk = str(R['openAsk'])
            highBid = str(R['highBid'])
            highAsk = str(R['highAsk'])
            lowBid = str(R['lowBid'])
            lowAsk = str(R['lowAsk'])
            closeBid = str(R['closeBid'])
            closeAsk = str(R['closeAsk'])
            volume = str(R['volume'])
            complete = R['complete']
            Body = [year, month, day, t_time, openBid, openAsk, highBid, highAsk, lowBid, lowAsk, closeBid, closeAsk,
                    volume]
            buffer.append(Body)
            count += 1
            print(str(count) + "周目")
    except  Exception as e:
        print(e)

    buffer.reverse()
    for b in buffer:
        history.append(b)

header = ['年','月','日','時刻', '開始買値', '開始売値', '最高買値', '最高売値', '最低買値', '最低売値', '終了買値', '終了売値', '出来高']
with open(str(response['instrument']) + '.csv', 'w') as f:
    writer = csv.writer(f)  # writerオブジェクトを作成
    writer.writerow(header)  # ヘッダーを書き込む
    writer.writerows(history)  # 内容を書き込む
    print("complete")
    print("get" + str(len(history)) + "line")
