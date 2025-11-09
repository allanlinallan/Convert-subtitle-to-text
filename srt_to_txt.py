import pysrt
import re
import argparse
import os

def clean_and_format_text(text):
    """
    清理字幕文本中的 HTML 標籤、格式標記和內部換行符。
    """
    # 1. 移除 HTML 標籤 (例如 <i>, <b>)
    cleaned_text = re.sub(r'<[^>]+>', '', text)
    
    # 2. 移除 ASS/SSA 風格的標籤 (例如 {/i}, {\an8})
    cleaned_text = re.sub(r'{[^}]+}', '', cleaned_text)
    
    # 3. 將字幕中內部的換行符 (例如 \n) 替換成單個空格
    cleaned_text = cleaned_text.replace('\n', ' ')
    
    return cleaned_text.strip()

def srt_to_text(srt_filepath, output_filepath=None, segment_by_line=False):
    """
    使用 pysrt 函式庫將 .srt 轉換為純文字檔。
    
    :param srt_filepath: 輸入的 .srt 檔案路徑。
    :param output_filepath: 輸出的 .txt 檔案路徑。如果為 None，則根據輸入檔案命名。
    :param segment_by_line: 如果為 True，每個字幕塊的文本會佔用一行。
                            如果為 False (預設)，所有文本會連貫地輸出。
    """
    if not os.path.exists(srt_filepath):
        print(f"❌ 錯誤：找不到檔案 {srt_filepath}")
        return

    # 確定輸出檔案路徑
    if output_filepath is None:
        base_name = os.path.splitext(srt_filepath)[0]
        output_filepath = base_name + ".txt"

    try:
        # 讀取 SRT 檔案
        # pysrt 會自動處理編碼問題，通常使用 utf-8 或 chardet 檢測
        subs = pysrt.open(srt_filepath)
        
        processed_texts = []
        
        for sub in subs:
            cleaned_line = clean_and_format_text(sub.text)
            if cleaned_line:
                processed_texts.append(cleaned_line)
        
        # 決定文本輸出格式
        if segment_by_line:
            # 每個字幕塊佔一行
            final_text = '\n'.join(processed_texts)
        else:
            # 所有文本連貫輸出，用空格連接每個字幕塊
            # 注意：如果字幕內容很長，建議使用 segment_by_line=True 保持可讀性
            final_text = ' '.join(processed_texts)

        # 寫入文字檔
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(final_text)
            
        print(f"✅ 轉換成功！純文字檔已儲存至：{output_filepath}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        print("請檢查檔案是否為有效的 SRT 格式。")

if __name__ == '__main__':
    # 設置參數解析器，讓程式可以從命令列接收檔案路徑
    parser = argparse.ArgumentParser(
        description="將 SRT 字幕檔轉換為純文字檔。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help="要轉換的 SRT 檔案路徑 (例如: movie.srt)"
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help="輸出的文字檔路徑 (例如: transcript.txt)。\n若不指定，則與輸入檔同名但副檔名為 .txt。"
    )

    parser.add_argument(
        '-l', '--line',
        action='store_true',
        help="將每個字幕塊的文本獨立成一行輸出，而不是連貫地接在一起。"
    )

    args = parser.parse_args()
    
    srt_to_text(args.input_file, args.output, args.line)