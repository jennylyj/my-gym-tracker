import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 設定中文字型 (選用，如果圖表要有中文)
# 在 Colab 或某些環境可能需要額外設定字型，這裡先用預設英文以免報錯
plt.rcParams['font.sans-serif'] = ['Arial'] 
plt.rcParams['axes.unicode_minus'] = False

def plot_gym_data():
    try:
        # 讀取資料
        df = pd.read_csv("data.csv")
        
        # 確保 Count 是數字
        df['Count'] = pd.to_numeric(df['Count'])
        
        # 簡單分析：看某個特定日期的變化 (例如昨天)
        # 這裡我們取最新的那個日期來畫圖
        latest_date = df['Date'].iloc[-1]
        daily_data = df[df['Date'] == latest_date]
        
        plt.figure(figsize=(10, 6))
        
        # 畫長條圖
        bars = plt.bar(daily_data['Time'], daily_data['Count'], color='skyblue')
        
        # 畫一條 50 人的警戒線 (尷尬線)
        plt.axhline(y=50, color='r', linestyle='--', label='Awkward Line (50 ppl)')
        
        plt.title(f"Gym Crowd on {latest_date}")
        plt.xlabel("Time")
        plt.ylabel("People")
        plt.legend()
        plt.xticks(rotation=45)
        plt.ylim(0, 120) 
        
        # 在柱狀圖上標示數字
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig("gym_analysis.png") # 存成圖片
        print(f"圖表已生成: gym_analysis.png")
        # plt.show() # 如果在本地跑可以打開這行
        
    except FileNotFoundError:
        print("還沒有 data.csv，請先執行 main.py 或等待 Action 執行")

if __name__ == "__main__":
    plot_gym_data()
