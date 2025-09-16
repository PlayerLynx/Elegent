import os
import tkinter as tk
from tkinter import filedialog, messagebox

def batch_rename(directory, prefix, replace_from=None, replace_to=None, file_ext=None):
    if not os.path.exists(directory):
        messagebox.showerror("错误", f"目录 '{directory}' 不存在！")
        return

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if file_ext:
        files = [f for f in files if f.lower().endswith(file_ext.lower())]

    if len(files) == 0:
        messagebox.showinfo("提示", "没有找到符合条件的文件！")
        return

    for idx, filename in enumerate(files, start=1):
        original_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]

        new_name = f"{prefix}{idx:03d}"
        if replace_from and replace_to:
            new_name = new_name.replace(replace_from, replace_to)

        new_filename = f"{new_name}{ext}"
        original_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)

        if os.path.exists(new_path):
            messagebox.showwarning("警告", f"'{new_filename}' 已存在，跳过重命名。")
            continue

        os.rename(original_path, new_path)

    messagebox.showinfo("完成", f"成功重命名 {len(files)} 个文件！")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def run_tool():
    directory = entry_directory.get()
    prefix = entry_prefix.get()
    replace_from = entry_replace_from.get()
    replace_to = entry_replace_to.get()
    file_ext = entry_ext.get()

    if not directory:
        messagebox.showerror("错误", "请选择目录！")
        return

    batch_rename(directory, prefix, replace_from, replace_to, file_ext)

# 创建 GUI 窗口
root = tk.Tk()
root.title("批量重命名工具")

# 目录选择
tk.Label(root, text="目标目录：").grid(row=0, column=0, padx=5, pady=5)
entry_directory = tk.Entry(root, width=40)
entry_directory.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="选择目录", command=select_directory).grid(row=0, column=2, padx=5, pady=5)

# 文件名前缀
tk.Label(root, text="文件名前缀：").grid(row=1, column=0, padx=5, pady=5)
entry_prefix = tk.Entry(root, width=40)
entry_prefix.grid(row=1, column=1, padx=5, pady=5)

# 替换字符
tk.Label(root, text="替换字符（从）：").grid(row=2, column=0, padx=5, pady=5)
entry_replace_from = tk.Entry(root, width=40)
entry_replace_from.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="替换字符（到）：").grid(row=3, column=0, padx=5, pady=5)
entry_replace_to = tk.Entry(root, width=40)
entry_replace_to.grid(row=3, column=1, padx=5, pady=5)

# 文件扩展名
tk.Label(root, text="文件扩展名：").grid(row=4, column=0, padx=5, pady=5)
entry_ext = tk.Entry(root, width=40)
entry_ext.grid(row=4, column=1, padx=5, pady=5)

# 运行按钮
tk.Button(root, text="开始重命名", command=run_tool).grid(row=5, column=1, padx=5, pady=10)

# 运行窗口
root.mainloop()
