import time
import RPi.GPIO as gpio
from datetime import datetime
import pandas as pd
from glob import glob

hi_sw_pin = 20
lo_sw_pin = 21
control_out = 18


gpio.cleanup()

gpio.setmode(gpio.BCM)
gpio.setup(hi_sw_pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(lo_sw_pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(control_out,gpio.OUT)
pwmoutput = gpio.PWM(control_out,50) #GPIO１８をpwmoutputオブジェクトとして作成。50Hzで設定

count = 0

while True:
    print("Hi ",gpio.input(hi_sw_pin ))
    print("Lo ",gpio.input(lo_sw_pin ))
    if (gpio.input(hi_sw_pin )) == (gpio.input(lo_sw_pin )) ==1:
        print("ポンプON！")
        count += 1
        print("count:",count)
        pwmoutput.start(100) #PWMを初期化。また、初期の値を50(duty比)とする。
        time.sleep(5)

    if (gpio.input(hi_sw_pin )) == (gpio.input(lo_sw_pin )) ==0:
        print("ポンプOFF！")
        pwmoutput.stop()
    time.sleep(2)

#---------- 案件名 ----------#
project_title = "sansui_project"

#---------- csvファイルを保存するフォルダのパス ----------#
dir_path = "/home/pi/python/sansui/"

#---------- ヘッダー名作成 ----------#
header = pd.MultiIndex.from_tuples([
        ("日時"),
        ("状態"),
        ("count")
        ])

#---------- job内容 ----------#
def job():
        #---------- 日時設定 ----------#
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        l = [now]
        l.append(count)
        print(l)

        #---------- 上記のリストとヘッダーをデータフレーム化 ----------#
        df = pd.DataFrame([l])
        #　（重要！）lでなく[l]とするのはlistをDataFrame化する際に一次元リストだと行方向（縦方向）にデータが書き込まれる。
        # 二重リストとすることで列方向に書き込まれる！
        try:
                #---------- CSVへの書き出し（追記） ----------#
                df.to_csv(file_path, mode="a",encoding='cp932',index=False,header=False)
        except:
                print("csvへの書き込みエラー")



#---------- 新規ファイル作成 ----------#
def create_new_file():
    today_str = datetime.today().strftime("%y%m%d") #日付を文字列へ変換
    file_name = "{}_{}".format(project_title,today_str)
    #csv保存フォルダ内のcsvファイル名をリストで取得
    csv_list = glob("{}*.csv".format(dir_path))
    #csvファイルのパス
    file_path = "{}{}.csv".format(dir_path,file_name)
    #csvファイル名リスト内にf_nameのファイルが存在しない場合は、新規でfile_name名のファイルを作成する。
    if file_path not in csv_list:
        print("新規ファイル名:{}".format(file_name))
        df_h = pd.DataFrame(columns = header)
        df_h.to_csv(file_path, mode="w",encoding='cp932',index=False)
    else:
        print("ファイルに加筆:{}".format(file_name))
    #ファイル名を返す
    return file_path

if __name__ == "__main__":
    file_path = create_new_file()
    job()
