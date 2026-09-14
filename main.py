import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import json
import os
import re
import uuid

CONFIG_FILE = "utf8_config.json"

root = tk.Tk()
root.title("utf8 문서기 / utf8 Editor")
root.geometry("800x600")

config = {"theme": "light", "font_size": 12, "always_on_top": False, "is_first": True, "lang": "ko"}

# [수정] 정의 오류를 방지하기 위해 메뉴 바와 파일 메뉴 위젯을 최상단에서 먼저 생성합니다.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)

LANG_DICT = {
    "ko": {
        "title": "utf8 문서기", "welcome": "✨ 첫 실행을 환영합니다! ✨\n기본 설정을 완료해주세요.",
        "theme": "테마 설정:", "light": "라이트 모드", "dark": "다크 모드",
        "font_size": "글자 크기:", "preview": "표준 글자 크기 예시: aA가", "always_on_top": "항상 위에 고정",
        "macro_title": "💡 확장 매크로 함수 모음 (총 10종)", "macro_sub": "본문에 아래 함수를 입력하면 실시간으로 자동 변환됩니다:",
        "save_start": "저장 및 시작", "save_apply": "저장 및 적용", "setting": "⚙️ 설정", "file": "파일",
        "open": "열기 (Ctrl+O)", "save": "저장 (Ctrl+S)", "exit": "종료", "success_title": "성공",
        "success_msg": "파일이 성공적으로 저장되었습니다!", "char_count": "공백 포함: {}자  |  공백 제외: {}자",
        "window_pin": "창 고정:", "lang_select": "언어 설정 / Language:"
    },
    "en": {
        "title": "utf8 Editor", "welcome": "✨ Welcome to your first run! ✨\nPlease complete the basic setup.",
        "theme": "Theme Settings:", "light": "Light Mode", "dark": "Dark Mode",
        "font_size": "Font Size:", "preview": "Sample Font Size: aA가", "always_on_top": "Always on Top",
        "macro_title": "💡 Extended Macro Functions (10 Types)", "macro_sub": "Type these macros in the text area for automatic conversion:",
        "save_start": "Save & Start", "save_apply": "Save & Apply", "setting": "⚙️ Settings", "file": "File",
        "open": "Open (Ctrl+O)", "save": "Save (Ctrl+S)", "exit": "Exit", "success_title": "Success",
        "success_msg": "File saved successfully!", "char_count": "Chars (with spaces): {}  |  Chars (no spaces): {}",
        "window_pin": "Window Pinning:", "lang_select": "Language / 언어 설정:"
    }
}

text_area = tk.Text(root, font=("Malgun Gothic", config["font_size"]), undo=True, wrap="word")
status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E, padx=10, pady=3)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["is_first"] = False
                if "lang" not in data:
                    data["lang"] = "ko"
                return data
        except:
            pass
    return {"theme": "light", "font_size": 12, "always_on_top": False, "is_first": True, "lang": "ko"}

def save_config():
    save_data = config.copy()
    save_data.pop("is_first", None)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)

config = load_config()
def update_status(event=None):
    content = text_area.get("1.0", tk.END)[:-1]
    lang = config.get("lang", "ko")
    
    macro_map = {
        "(time(f))": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "(date(f))": lambda: datetime.now().strftime("%Y-%m-%d"),
        "(uuid(f))": lambda: str(uuid.uuid4())
    }
    
    for macro, func in macro_map.items():
        if macro in content:
            pos = text_area.search(macro, "1.0", stopindex=tk.END)
            if pos:
                text_area.delete(pos, f"{pos} + {len(macro)}c")
                text_area.insert(pos, func())
                content = text_area.get("1.0", tk.END)[:-1]

    if "(cal(f))" in content:
        pos = text_area.search("(cal(f))", "1.0", stopindex=tk.END)
        if pos:
            line_start = f"{pos} linestart"
            pre_text = text_area.get(line_start, pos)
            match = re.search(r'([\d+\-*/\s().]+)$', pre_text)
            if match:
                expr = match.group(1).strip()
                try:
                    res = str(eval(expr))
                    expr_start = text_area.search(expr, line_start, stopindex=pos)
                    if expr_start:
                        text_area.delete(expr_start, f"{pos} + 8c")
                        text_area.insert(expr_start, res)
                except:
                    text_area.delete(pos, f"{pos} + 8c")
            else:
                text_area.delete(pos, f"{pos} + 8c")
            content = text_area.get("1.0", tk.END)[:-1]

    if "(upper(f))" in content:
        pos = text_area.search("(upper(f))", "1.0", stopindex=tk.END)
        if pos:
            text_area.delete(pos, f"{pos} + 10c")
            full_text = text_area.get("1.0", tk.END)[:-1].upper()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", full_text)
            content = text_area.get("1.0", tk.END)[:-1]

    if "(lower(f))" in content:
        pos = text_area.search("(lower(f))", "1.0", stopindex=tk.END)
        if pos:
            text_area.delete(pos, f"{pos} + 10c")
            full_text = text_area.get("1.0", tk.END)[:-1].lower()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", full_text)
            content = text_area.get("1.0", tk.END)[:-1]

    if "(strip(f))" in content:
        pos = text_area.search("(strip(f))", "1.0", stopindex=tk.END)
        if pos:
            text_area.delete(pos, f"{pos} + 9c")
            full_text = text_area.get("1.0", tk.END)[:-1]
            cleaned_text = "\n".join([line for line in full_text.splitlines() if line.strip()])
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", cleaned_text)
            content = text_area.get("1.0", tk.END)[:-1]

    if "(len(f))" in content:
        pos = text_area.search("(len(f))", "1.0", stopindex=tk.END)
        if pos:
            text_area.delete(pos, f"{pos} + 8c")
            current_len = len(text_area.get("1.0", tk.END)[:-1])
            insert_text = f"[현재 글자수: {current_len}자]" if lang == "ko" else f"[Current Length: {current_len} chars]"
            text_area.insert(pos, insert_text)
            content = text_area.get("1.0", tk.END)[:-1]

    if "(rev(f))" in content:
        pos = text_area.search("(rev(f))", "1.0", stopindex=tk.END)
        if pos:
            line_start = f"{pos} linestart"
            pre_text = text_area.get(line_start, pos).strip()
            text_area.delete(line_start, f"{pos} + 8c")
            text_area.insert(line_start, pre_text[::-1])
            content = text_area.get("1.0", tk.END)[:-1]

    if "(clear(f))" in content:
        text_area.delete("1.0", tk.END)
        content = ""

    total_chars = len(content)
    no_space_chars = len(content.replace(" ", "").replace("\n", "").replace("\r", ""))
    status_label.config(text=LANG_DICT[lang]["char_count"].format(total_chars, no_space_chars))
def apply_settings():
    lang = config["lang"]
    root.title(LANG_DICT[lang]["title"])
    
    if config["theme"] == "dark":
        text_area.config(bg="#2d2d2d", fg="#ffffff", insertbackground="white")
        status_label.config(bg="#1e1e1e", fg="#ffffff")
    else:
        text_area.config(bg="#ffffff", fg="#000000", insertbackground="black")
        status_label.config(bg="#f0f0f0", fg="#000000")
    
    text_area.config(font=("Malgun Gothic", config["font_size"]))
    root.attributes("-topmost", config["always_on_top"])
    update_status()

def zoom(event):
    if event.delta > 0:
        config["font_size"] = min(config["font_size"] + 1, 40)
    else:
        config["font_size"] = max(config["font_size"] - 1, 8)
    text_area.config(font=("Malgun Gothic", config["font_size"]))
    save_config()

def open_file(event=None):
    lang = config["lang"]
    file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", file.read())
        root.title(f"{LANG_DICT[lang]['title']} - {file_path}")
        update_status()
    return "break"

def save_file(event=None):
    lang = config["lang"]
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", tk.END))
        root.title(f"{LANG_DICT[lang]['title']} - {file_path}")
        messagebox.showinfo(LANG_DICT[lang]["success_title"], LANG_DICT[lang]["success_msg"])
    return "break"

def update_menu_text():
    lang = config["lang"]
    menu_bar.entryconfig(1, label=LANG_DICT[lang]["file"])
    menu_bar.entryconfig(2, label=LANG_DICT[lang]["setting"])
    file_menu.entryconfig(0, label=LANG_DICT[lang]["open"])
    file_menu.entryconfig(1, label=LANG_DICT[lang]["save"])
    file_menu.entryconfig(3, label=LANG_DICT[lang]["exit"])
def open_settings():
    lang = config["lang"]
    settings_win = tk.Toplevel(root)
    settings_win.title(LANG_DICT[lang]["setting"])
    settings_win.geometry("320x350")
    settings_win.resizable(False, False)
    settings_win.attributes("-topmost", True)
    
    tk.Label(settings_win, text=LANG_DICT[lang]["lang_select"]).pack(pady=5)
    lang_var = tk.StringVar(value=config["lang"])
    tk.Radiobutton(settings_win, text="한국어", variable=lang_var, value="ko").pack()
    tk.Radiobutton(settings_win, text="English", variable=lang_var, value="en").pack()
    
    tk.Label(settings_win, text=LANG_DICT[lang]["theme"]).pack(pady=5)
    theme_var = tk.StringVar(value=config["theme"])
    tk.Radiobutton(settings_win, text=LANG_DICT[lang]["light"], variable=theme_var, value="light").pack()
    tk.Radiobutton(settings_win, text=LANG_DICT[lang]["dark"], variable=theme_var, value="dark").pack()
    
    tk.Label(settings_win, text=LANG_DICT[lang]["font_size"]).pack(pady=5)
    size_var = tk.IntVar(value=config["font_size"])
    preview_label = tk.Label(settings_win, text=LANG_DICT[lang]["preview"], font=("Malgun Gothic", config["font_size"]))
    
    def update_win_preview():
        try:
            current_size = int(size_spin.get())
            preview_label.config(font=("Malgun Gothic", current_size))
        except ValueError:
            pass

    size_spin = tk.Spinbox(settings_win, from_=8, to=40, textvariable=size_var, width=5, command=update_win_preview)
    size_spin.pack()
    size_spin.bind("<KeyRelease>", lambda e: update_win_preview())
    preview_label.pack(pady=10)
    
    tk.Label(settings_win, text=LANG_DICT[lang]["window_pin"]).pack(pady=5)
    top_var = tk.BooleanVar(value=config["always_on_top"])
    tk.Checkbutton(settings_win, text=LANG_DICT[lang]["always_on_top"], variable=top_var).pack()
    
    def save_and_close():
        config["lang"] = lang_var.get()
        config["theme"] = theme_var.get()
        config["font_size"] = size_var.get()
        config["always_on_top"] = top_var.get()
        save_config()
        apply_settings()
        update_menu_text()
        settings_win.destroy()
        
    tk.Button(settings_win, text=LANG_DICT[lang]["save_apply"], command=save_and_close, width=15).pack(pady=10)

def show_first_setup():
    text_area.pack_forget()
    status_label.pack_forget()
    
    setup_frame = tk.Frame(root, bg="#f0f0f0")
    setup_frame.pack(expand=True, fill="both")
    
    welcome_label = tk.Label(setup_frame, text=LANG_DICT["ko"]["welcome"], font=("Malgun Gothic", 16, "bold"), fg="blue", bg="#f0f0f0")
    welcome_label.pack(pady=10)
    
    tk.Label(setup_frame, text="언어 설정 / Language:", font=("Malgun Gothic", 11, "bold"), bg="#f0f0f0").pack(pady=2)
    lang_var = tk.StringVar(value="ko")
    
    theme_lbl = tk.Label(setup_frame, text=LANG_DICT["ko"]["theme"], font=("Malgun Gothic", 11, "bold"), bg="#f0f0f0")
    rb_light = tk.Radiobutton(setup_frame, text=LANG_DICT["ko"]["light"], variable=tk.StringVar(value="light"), value="light", bg="#f0f0f0")
    rb_dark = tk.Radiobutton(setup_frame, text=LANG_DICT["ko"]["dark"], variable=tk.StringVar(value="light"), value="dark", bg="#f0f0f0")
    size_lbl = tk.Label(setup_frame, text=LANG_DICT["ko"]["font_size"], font=("Malgun Gothic", 11, "bold"), bg="#f0f0f0")
    pin_lbl = tk.Label(setup_frame, text=LANG_DICT["ko"]["window_pin"], font=("Malgun Gothic", 11, "bold"), bg="#f0f0f0")
    rb_pin = tk.Checkbutton(setup_frame, text=LANG_DICT["ko"]["always_on_top"], bg="#f0f0f0")
    macro_box = tk.LabelFrame(setup_frame, text=LANG_DICT["ko"]["macro_title"], font=("Malgun Gothic", 10, "bold"), bg="#ffffff", fg="#333333", padx=15, pady=8)
    macro_lbl = tk.Label(macro_box, text=LANG_DICT["ko"]["macro_sub"], font=("Malgun Gothic", 9, "bold"), bg="#ffffff", fg="#555555")
    btn_start = tk.Button(setup_frame, text=LANG_DICT["ko"]["save_start"], width=20, font=("Malgun Gothic", 11, "bold"))
    
    def on_lang_change():
        l = lang_var.get()
        welcome_label.config(text=LANG_DICT[l]["welcome"])
        theme_lbl.config(text=LANG_DICT[l]["theme"])
        rb_light.config(text=LANG_DICT[l]["light"])
        rb_dark.config(text=LANG_DICT[l]["dark"])
        size_lbl.config(text=LANG_DICT[l]["font_size"])
        preview_label.config(text=LANG_DICT[l]["preview"])
        pin_lbl.config(text=LANG_DICT[l]["window_pin"])
        rb_pin.config(text=LANG_DICT[l]["always_on_top"])
        macro_box.config(text=LANG_DICT[l]["macro_title"])
        macro_lbl.config(text=LANG_DICT[l]["macro_sub"])
        btn_start.config(text=LANG_DICT[l]["save_start"])

    tk.Radiobutton(setup_frame, text="한국어", variable=lang_var, value="ko", bg="#f0f0f0", command=on_lang_change).pack()
    tk.Radiobutton(setup_frame, text="English", variable=lang_var, value="en", bg="#f0f0f0", command=on_lang_change).pack()
    
    theme_lbl.pack(pady=2)
    theme_var = tk.StringVar(value="light")
    rb_light.config(variable=theme_var)
    rb_dark.config(variable=theme_var)
    rb_light.pack()
    rb_dark.pack()
    
    size_lbl.pack(pady=2)
    size_var = tk.IntVar(value=12)
    preview_label = tk.Label(setup_frame, text=LANG_DICT["ko"]["preview"], font=("Malgun Gothic", 12), bg="#f0f0f0")
    
    def update_preview():
        try:
            preview_label.config(font=("Malgun Gothic", int(size_spin.get())))
        except:
            pass

    size_spin = tk.Spinbox(setup_frame, from_=8, to=40, textvariable=size_var, width=5, command=update_preview)
    size_spin.pack()
    size_spin.bind("<KeyRelease>", lambda e: update_preview())
    preview_label.pack(pady=2)
    
    pin_lbl.pack(pady=2)
    top_var = tk.BooleanVar(value=False)
    rb_pin.config(variable=top_var)
    rb_pin.pack()
    
    macro_box.pack(pady=5, padx=50, fill="x")
    macro_lbl.pack(anchor="w")
    
    canvas = tk.Canvas(macro_box, bg="#ffffff", bd=0, highlightthickness=0, height=80)
    scrollbar = ttk.Scrollbar(macro_box, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    funcs = [
        "• (time(f)) : Insert current date & time", "• (date(f)) : Insert current date only",
        "• (cal(f)) : Calculate expression automatically", "• (upper(f)) : Convert all text to UPPERCASE",
        "• (lower(f)) : Convert all text to lowercase", "• (strip(f)) : Remove all empty lines",
        "• (len(f)) : Insert total character count", "• (rev(f)) : Reverse text on the current line",
        "• (uuid(f)) : Insert random unique UUID", "• (clear(f)) : Clear all content"
    ]
    for text in funcs:
        tk.Label(scrollable_frame, text=text, font=("Malgun Gothic", 9), bg="#ffffff", anchor="w").pack(fill="x", pady=1)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def save_and_start():
        config["lang"] = lang_var.get()
        config["theme"] = theme_var.get()
        config["font_size"] = size_var.get()
        config["always_on_top"] = top_var.get()
        config["is_first"] = False
        save_config()
        
        setup_frame.pack_forget()
        text_area.pack(expand=True, fill="both")
        status_label.pack(fill="x")
        root.config(menu=menu_bar)
        update_menu_text()
        apply_settings()
        
    btn_start.config(command=save_and_start)
    btn_start.pack(pady=10)

file_menu.add_command(label="", command=open_file)
file_menu.add_command(label="", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="", command=root.quit)
menu_bar.add_cascade(label="", menu=file_menu)
menu_bar.add_command(label="", command=open_settings)

text_area.bind("<KeyRelease>", update_status)
text_area.bind("<Control-MouseWheel>", zoom)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-O>", open_file)
root.bind("<Control-S>", save_file)

if config["is_first"]:
    show_first_setup()
else:
    root.config(menu=menu_bar)
    text_area.pack(expand=True, fill="both")
    status_label.pack(fill="x")
    update_menu_text()
    apply_settings()

root.mainloop()
