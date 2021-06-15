import requests
from bs4 import BeautifulSoup
import openpyxl
import math

#対象となるURLを指定する
url = "https://fund.smtb.jp/smtb/qsearch.exe?F=openlist3&KEY22=&KEY23=1"

#htmlを取得する
base_html = requests.get(url).text

#bsオブジェクトに変換する
my_soup = BeautifulSoup(base_html, "html5lib")

#tbodyタグの中身を取得する
body = my_soup.find("tbody")

#ファンドごとのhtmlを配列化する
all_fund_data = body.find_all("tr")

#修正したデータを格納するための空配列を定義する
modified_data = []

#繰返し処理により、必要なデータだけを取り出し、配列に入れ直す
for fund_data in all_fund_data:

	#基準価額・手数料率・分配金を取り出すための配列を作成する
	data_array = fund_data.find_all("td",class_="data")

	#分配金単価が0の場合、処理をスキップする
	if data_array[4].text == "0" or data_array[4].text == "--" :
			continue

	#分配金単価を取り出す
	f_dividend = int(data_array[4].text)
	
	#基準価額を取り出す
	f_price = int(data_array[0].find("em").text)

	#購入時手数料率を取り出す。百分率表示から小数点表示に変換
	f_fee = data_array[1].find("noscript").text
	f_fee = float(f_fee[:-2])/100
	
	#ファンド名を取り出す
	f_name = fund_data.find("a").text

	#分配金手取額を計算する
	f_income = math.floor(1000000/(1+f_fee)/f_price*f_dividend*(1-0.20315))
	
	f_fiscal = data_array[6].text

	#抽出したデータを配列に追加する
	modified_data.append([f_name, f_price, f_fee, f_dividend, f_income, f_fiscal])

#エクセルファイルを開き、先頭のシートを指定する
my_book = openpyxl.load_workbook("price_list.xlsx")
my_sheet = my_book.worksheets[0]

#行数を指定するためのカウンタ変数を定義する
j = 2

#ループ処理でデータをエクセルに書き込む
for data in modified_data:
	for k in range(1,7):
		my_sheet.cell(j,k).value = data[k-1]
	j += 1

#エクセルファイルを上書き保存する
my_book.save("price_list.xlsx")








