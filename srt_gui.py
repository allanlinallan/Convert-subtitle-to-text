import pysrt
import re
import os
from tkinter import Tk, Button, Label, filedialog, messagebox, Checkbutton, StringVar, BooleanVar, Entry, W, E

# --- 簡繁轉換依賴設定 (使用純 Python 的 zhconv) ---
try:
    from zhconv import convert
    CONVERTER_AVAILABLE = True
except ImportError:
    CONVERTER_AVAILABLE = False
    
# --- 核心工具函式 ---

def clean_and_format_text(text):
    """
    清理字幕文本中的 HTML 標籤、格式標記和內部換行符。
    """
    cleaned_text = re.sub(r'<[^>]+>', '', text)
    cleaned_text = re.sub(r'{[^}]+}', '', cleaned_text)
    cleaned_text = cleaned_text.replace('\n', ' ')
    
    return cleaned_text.strip()

def process_and_convert(srt_filepath, convert_to_trad, segment_by_line=False):
    """
    核心處理函式：讀取、清理、簡繁轉換文本。
    返回：處理後的文本字串 (換行分隔)，或在失敗時返回 None。
    """
    if not os.path.exists(srt_filepath):
        messagebox.showerror("錯誤", f"找不到檔案: {srt_filepath}")
        return None

    if convert_to_trad and not CONVERTER_AVAILABLE:
        messagebox.showwarning("警告", "簡繁轉換函式庫未安裝！請安裝 zhconv 以啟用此功能。")
        return None

    try:
        subs = pysrt.open(srt_filepath)
        processed_texts = []
        
        for sub in subs:
            cleaned_line = clean_and_format_text(sub.text)
            
            # 執行簡繁轉換
            if convert_to_trad and cleaned_line:
                cleaned_line = convert(cleaned_line, 'zh-tw')
            
            if cleaned_line:
                processed_texts.append(cleaned_line)
        
        # 決定文本輸出格式
        if segment_by_line:
            return '\n'.join(processed_texts)
        else:
            return '\n'.join(processed_texts)

    except Exception as e:
        messagebox.showerror("轉換失敗 (核心錯誤)", f"請檢查 SRT 檔案是否損壞或編碼錯誤。\n\n詳細錯誤: {e}")
        return None

def srt_to_text(srt_filepath, segment_by_line, convert_to_trad, output_name):
    """
    生成 TXT 檔案的核心函式。
    """
    final_text = process_and_convert(srt_filepath, convert_to_trad, segment_by_line)
    
    if final_text is None:
        return # 處理失敗，提示已在 process_and_convert 中顯示

    try:
        # 確定輸出檔案路徑
        output_dir = os.path.dirname(srt_filepath)
        
        if output_name:
            output_filepath = os.path.join(output_dir, os.path.splitext(output_name)[0] + ".txt")
        else:
            base_name = os.path.splitext(os.path.basename(srt_filepath))[0]
            output_filepath = os.path.join(output_dir, base_name + ".txt")

        # 寫入文字檔
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(final_text)
            
        messagebox.showinfo("成功", f"轉換完成！\n文字檔已儲存至：{output_filepath}")

    except Exception as e:
        messagebox.showerror("檔案寫入失敗", f"無法寫入文件：{output_filepath}\n詳細錯誤: {e}")

# --- 新增功能：SRT 格式轉換 ---
def srt_to_traditional_srt(srt_filepath, convert_to_trad):
    """
    僅對 SRT 檔案的字幕文本進行簡繁轉換，並儲存為新的 SRT 檔案。
    """
    if not os.path.exists(srt_filepath):
        messagebox.showerror("錯誤", f"找不到檔案: {srt_filepath}")
        return

    if not convert_to_trad:
        messagebox.showwarning("警告", "請先勾選「自動轉為繁體中文」選項才能執行此操作！")
        return

    if not CONVERTER_AVAILABLE:
        messagebox.showwarning("警告", "簡繁轉換函式庫未安裝，無法執行此操作。")
        return

    try:
        # 讀取 SRT 檔案
        subs = pysrt.open(srt_filepath)
        
        # 遍歷並修改每個字幕塊的文本
        for sub in subs:
            original_text = sub.text
            
            # 執行簡繁轉換（使用 zhconv）
            converted_text = convert(original_text, 'zh-tw')
            
            # 更新字幕塊的文本
            sub.text = converted_text
        
        # 確定輸出檔案路徑
        base, ext = os.path.splitext(srt_filepath)
        output_filepath = base + "_T" + ext  # 新增 _T 來區分繁體版
        
        # 寫入新的 SRT 檔案
        subs.save(output_filepath, encoding='utf-8')
        
        messagebox.showinfo("成功", f"簡轉繁成功！\n已儲存為新的 SRT 檔案：\n{output_filepath}")

    except Exception as e:
        messagebox.showerror("SRT 轉換失敗", f"在處理或寫入 SRT 檔案時發生錯誤：{e}")


# --- UI 界面邏輯 (Tkinter) ---

class SrtConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("SRT 字幕轉文字工具")
        
        # UI 伸縮性設定
        master.grid_columnconfigure(1, weight=1) 
        master.minsize(width=500, height=450) # 稍微增加高度以容納新按鈕

        # 變數儲存 (預設簡繁轉換為 True)
        self.srt_file_path = StringVar(master, value="請點擊「選擇檔案」按鈕")
        self.segment_by_line = BooleanVar(master, value=True)
        self.convert_to_trad = BooleanVar(master, value=True) # <-- 預設打勾
        self.output_file_name = StringVar(master, value="") 

        # 1. 檔案路徑顯示
        Label(master, text="SRT 檔案路徑:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(master, textvariable=self.srt_file_path, width=20, state='readonly').grid(
            row=0, column=1, padx=10, pady=5, sticky=W+E) 

        # 2. 選擇檔案按鈕
        Button(master, text="選擇 SRT 檔案", command=self.browse_file).grid(
            row=1, column=0, columnspan=2, pady=5, padx=10, sticky=W+E) 

        # --- 分隔線與標題 ---
        Label(master, text="-"*50).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=W+E)
        Label(master, text="輸出/格式選項:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=W, padx=10, pady=5)


        # --- 第二區塊：格式選項 ---
        
        # 3. 輸出格式 (每行獨立)
        Checkbutton(master, text="✅ 每個字幕塊獨立成一行 (推薦)", 
                    variable=self.segment_by_line).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=W) 
        
        # 4. 簡繁轉換 (新增選項)
        trad_state = 'normal' if CONVERTER_AVAILABLE else 'disabled'
        Checkbutton(master, text="🇹🇼 自動轉為繁體中文 (簡轉繁)", 
                    variable=self.convert_to_trad, state=trad_state).grid(
                        row=5, column=0, columnspan=2, padx=10, pady=5, sticky=W)
                                                                                        
        # 5. 自定義輸出檔名 (可選)
        Label(master, text="自定義輸出檔名 (可選):").grid(row=6, column=0, sticky=W, padx=10, pady=5)
        
        Entry(master, textvariable=self.output_file_name, width=20).grid(
            row=6, column=1, padx=10, pady=5, sticky=W+E) 
        Label(master, text="(例如：transcript.txt)").grid(row=7, column=1, sticky=W, padx=10, pady=0)


        # --- 執行按鈕 (功能區) ---
        
        # 8. 僅顯示轉換結果按鈕
        Button(master, text="📝 僅顯示轉換結果 (供複製)", command=self.show_conversion_result,
               bg='lightyellow', fg='black', font=('Arial', 10), padx=10, pady=5).grid(
            row=8, column=0, columnspan=2, pady=5, padx=10, sticky=W+E) 

        # 9. 簡轉繁 SRT 檔案按鈕 (新增功能)
        Button(master, text="🔄 簡轉繁 (SRT 檔案格式不變，輸出 _T.srt)", command=self.run_srt_conversion,
               bg='#FFD700', fg='black', font=('Arial', 10, 'bold'), padx=10, pady=5).grid(
            row=9, column=0, columnspan=2, pady=5, padx=10, sticky=W+E) 
            
        # 10. 執行轉換按鈕 (生成 TXT)
        self.convert_btn = Button(master, text="🚀 執行轉換 (生成純文字檔)", 
                                  command=self.run_conversion, 
                                  bg='lightblue', fg='black', font=('Arial', 12, 'bold'), padx=10, pady=10)
        
        self.convert_btn.grid(row=10, column=0, columnspan=2, pady=20, padx=10, sticky=W+E) 


    def browse_file(self):
        """開啟檔案對話框，讓使用者選擇 SRT 檔案。"""
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(), 
            title="選擇 SRT 字幕檔案",
            filetypes=(("SRT files", "*.srt"), ("all files", "*.*"))
        )
        if filename:
            self.srt_file_path.set(filename)
            base_name = os.path.basename(filename)
            output_suggestion = os.path.splitext(base_name)[0] + ".txt"
            self.output_file_name.set(output_suggestion)


    def show_conversion_result(self):
        """點擊「僅顯示轉換結果」按鈕後執行的動作。"""
        input_path = self.srt_file_path.get()
        if not input_path or input_path == "請點擊「選擇檔案」按鈕":
            messagebox.showwarning("警告", "請先選擇一個 SRT 檔案！")
            return

        convert_trad = self.convert_to_trad.get()

        converted_text = process_and_convert(input_path, convert_trad, segment_by_line=True)

        if converted_text:
            temp_file = filedialog.asksaveasfilename(
                title=f"簡轉繁結果 (請複製文本)",
                initialfile="Converted_Text.txt",
                defaultextension=".txt",
                filetypes=(("Text files", "*.txt"),)
            )
            
            if temp_file:
                try:
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        f.write(converted_text)
                    
                    messagebox.showinfo("操作完成", f"簡轉繁文本已暫存至：\n{temp_file}\n\n您可以從該檔案中複製文本。")
                except Exception as e:
                    messagebox.showerror("寫入錯誤", f"無法創建臨時文件: {e}")


    def run_conversion(self):
        """點擊轉換按鈕後執行的動作 (生成 TXT 檔案)。"""
        
        input_path = self.srt_file_path.get()
        
        if not input_path or input_path == "請點擊「選擇檔案」按鈕":
            messagebox.showwarning("警告", "請先選擇一個 SRT 檔案！")
            return

        segment = self.segment_by_line.get()
        convert_trad = self.convert_to_trad.get()
        output_name = self.output_file_name.get()

        srt_to_text(input_path, segment, convert_trad, output_name)
        
        
    def run_srt_conversion(self):
        """點擊「簡轉繁 SRT 檔案」按鈕後執行的動作。"""
        input_path = self.srt_file_path.get()
        if not input_path or input_path == "請點擊「選擇檔案」按鈕":
            messagebox.showwarning("警告", "請先選擇一個 SRT 檔案！")
            return

        convert_trad = self.convert_to_trad.get()
        if not convert_trad:
            messagebox.showwarning("警告", "請先勾選「自動轉為繁體中文」選項才能執行此操作！")
            return
            
        srt_to_traditional_srt(input_path, convert_trad)


if __name__ == '__main__':
    try:
        root = Tk()
        app = SrtConverterApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_info = traceback.format_exc()
        messagebox.showerror("啟動失敗", f"UI 啟動時發生致命錯誤:\n{e}\n\n詳細追蹤已輸出到控制台。")
        print("\n--- 致命錯誤 ---")
        print(error_info)
        print("----------------\n")