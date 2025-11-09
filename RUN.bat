REM　@echo off
title SRT 字幕轉文字工具 (Conda)

REM -----------------------------------------------------------
REM 方法一：使用 CALL 啟動環境，並嘗試在同一行執行 Python (最推薦)
REM 我們將 conda activate 和 python 運行用 '&&' 串聯起來，確保前一個成功才執行後一個。
REM 使用 CALL 來處理環境激活指令。

CALL conda activate subtitle_env && (
    echo.
    echo ? 環境啟動成功，正在運行 UI...
    python srt_gui.py
    goto :eof
)

REM 如果激活失敗，則執行到這裡
echo.
echo ? 錯誤：無法啟動 Conda 環境：subtitle_env
pause
:eof