# 🎯 StockSniper 股市狙擊手

這是一個基於 Python 的台股自動化分析系統，結合了「技術面篩選」與「新聞 AI 語意分析」，並提供 Streamlit 視覺化戰情室儀表板。

## ✨ 主要功能

* **全市場掃描**：自動抓取台股上市股票，計算技術指標。
* **雙刀流分析**：
    * ⚡ **技術面**：偵測底部翻揚、突破新高、歷史低檔等型態。
    * 📰 **消息面**：自動爬取 Google 新聞，分析利多/利空關鍵字。
* **視覺化戰情室**：提供 Web 介面 (Streamlit)，支援多維度篩選 (價格、漲幅、訊號)。
* **一鍵操作**：內附 `.bat` 腳本，點兩下即可更新數據或看盤。

## 🛠️ 安裝方式

本專案使用 `Miniconda` 管理環境，請確保已安裝 Anaconda 或 Miniconda。

===================================================================
   StockSniper 股市狙擊手 - 系統安裝指南 (Windows)
===================================================================

[重要觀念說明]
本專案使用 "Miniconda" 來管理 Python 環境。
Miniconda 安裝包已內含 Python 核心，因此您「不需要」另外去 Python 官網下載安裝，
以免電腦裡有多個 Python 版本互相衝突。

[第一階段] 下載與安裝基礎工具 (Miniconda)
-------------------------------------------------------------------
1. 下載 Miniconda (這就是您的 Python 安裝程式):
   請前往官方下載頁面：
   https://docs.conda.io/en/latest/miniconda.html#windows-installers
   
   * 請選擇列表中的: "Miniconda3 Windows 64-bit" 進行下載。

2. 安裝步驟:
   A. 點擊執行下載的安裝檔 (.exe)。
   B. 一路點擊 "Next" 或 "I Agree"。
   C. 安裝路徑建議維持預設。
   D. 【安裝選項】(Advanced Options)：
      - 建議勾選 "Register Miniconda3 as my default Python 3.10"。
      - (選用) "Add Miniconda3 to my PATH..." 建議「不要」勾選 (紅色字體)，
        我們之後使用專屬的 Anaconda Prompt 來操作會比較穩定。
   E. 點擊 "Install" 直到完成。

[第二階段] 建立專案環境 (這裡會安裝 Python 3.10)
-------------------------------------------------------------------
請全部在「Anaconda Prompt」視窗中進行。

1. 開啟終端機:
   點擊 Windows 「開始」按鈕 -> 搜尋 "Anaconda Prompt (Miniconda3)" 並開啟。
   (以後我們都用這個黑色視窗來下指令)

2. 切換到 D 槽並建立資料夾:
   d:
   mkdir AI\StockSniper
   cd AI\StockSniper

3. 建立虛擬環境:
   (這行指令會自動下載並安裝 Python 3.10 到此環境中)
   
   conda create -n stock_ai python=3.10 -y

4. 啟動環境:
   (看到最前面出現 (stock_ai) 代表成功進入環境)
   
   conda activate stock_ai

[第三階段] 安裝必要的程式庫
-------------------------------------------------------------------
1. 安裝 TA-Lib (金融技術指標庫):
   * 這是最難裝的套件，使用 conda 可以一鍵完成。
   
   conda install -c conda-forge ta-lib -y

2. 安裝其他 Python 套件:
   
   pip install twstock pandas requests schedule line-bot-sdk beautifulsoup4 lxml streamlit

[第四階段] 初始化資料庫
-------------------------------------------------------------------
1. 執行建檔程式 (需時約 30-40 分鐘):
   
   python data_builder.py

2. 當看到「✅ 建檔完成」且資料夾中出現 stock_db.csv，安裝即完成。

## ⚠️ 免責聲明 (Disclaimer)

**本專案僅供程式開發研究與學術交流使用，並非投資建議。**
**This project is for educational and research purposes only and does not constitute financial advice.**

1.  **不保證獲利 (No Guarantee of Profit)**：
    本程式使用的策略與參數（如 MACD、布林通道等）僅基於歷史數據回測，**過去的績效不代表未來的表現**。金融市場具有高度不確定性，使用者應自行評估風險。
2.  **風險自負 (Use at Your Own Risk)**：
    使用本程式產生的任何交易損益、資金損失或系統錯誤（如網路斷線、API 延遲、報價錯誤等），開發者 **不承擔任何法律責任**。請務必在實盤操作前做好充分的風險控管。
3.  **無須證券投資顧問執照 (Not Investment Advice)**：
    本程式碼僅提供技術分析工具的自動化實作範例，不涉及個股推薦或買賣價位指導。
4.  **資料來源 (Data Source)**：
    本專案使用 `yfinance` 獲取數據，數據來源為 Yahoo Finance。請遵守其服務條款，數據僅供個人參考，可能存在延遲或誤差。

---

## 🔒 安全提醒 (Security Warning)

* 請勿將您的 **LINE Channel Access Token** 或 **User ID** 上傳至公開的 GitHub 儲存庫。
* 建議使用環境變數 (`.env` 檔案) 來管理您的敏感資訊。

===================================================================

執行程式 請參考
使用說明檔 (README).txt
