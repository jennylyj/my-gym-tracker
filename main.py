import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import pytz

# 1. 設定目標 URL
URL = "https://wsjjsc.com.tw/"  

def get_gym_count():
    try:
        # 偽裝成瀏覽器（有些網站會擋爬蟲）
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status() 
        
        # 2. 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 結構: <div class="pcount">健身房<div class="notice">71</div>人/120人</div>
        pcounts = soup.find_all("div", class_="pcount")
        
        gym_people = None
        
        for item in pcounts:
            if "健身房" in item.text:
                notice_div = item.find("div", class_="notice")
                if notice_div:
                    gym_people = notice_div.text.strip()
                    break
        
        if gym_people is None:
            print("找不到健身房人數數據，網站結構可能改變了")
            return None
            
        return gym_people

    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

def save_to_csv(count):
    if count is None:
        return

    file_exists = os.path.isfile("data.csv")
    
    # 設定時區為台北
    tw_timezone = pytz.timezone('Asia/Taipei')
    now = datetime.now(tw_timezone)
    
    # 格式：日期, 時間, 星期, 人數
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    weekday_str = now.strftime("%A") # Monday, Tuesday...
    
    # 寫入檔案
    with open("data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # 如果檔案不存在，先寫標題
        if not file_exists:
            writer.writerow(["Date", "Time", "Weekday", "Count"])
        
        writer.writerow([date_str, time_str, weekday_str, count])
    
    print(f"已記錄: {date_str} {time_str} - {count}人")

if __name__ == "__main__":
    count = get_gym_count()
    save_to_csv(count)
