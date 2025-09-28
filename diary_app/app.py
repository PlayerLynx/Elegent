from flask import Flask, render_template, request, redirect, url_for,flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

os.chdir(r'C:\Users\15879\Desktop\Laptop\diary_app')

ENTRIES_DIR = "entries"
if not os.path.exists(ENTRIES_DIR):
    os.makedirs(ENTRIES_DIR)

@app.route('/')
def index():
    """显示主页和日记输入表单"""
    return render_template('index.html')

@app.route('/save_entry', methods=['POST'])
def save_entry():
    """保存日记条目"""
    title = request.form.get('title', '无标题')
    content = request.form.get('content', '')
    
    if content.strip():  # 确保内容不为空
        # 使用时间戳作为文件名，确保唯一性
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{title.replace(' ', '_')}.txt"
        filepath = os.path.join(ENTRIES_DIR, filename)
        
        # 保存日记内容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"标题: {title}\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"内容:\n{content}")
    
    return redirect(url_for('view_entries'))

@app.route('/del_entry/<filename>')
def del_entry(filename):
    """删除日记条目"""
    filepath = os.path.join(ENTRIES_DIR,filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        flash('日记已删除','success')
    
    return redirect(url_for('view_entries'))


@app.route('/entries')
def view_entries():
    """显示所有日记条目"""
    entries = []
    
    # 读取所有日记文件
    if os.path.exists(ENTRIES_DIR):
        for filename in sorted(os.listdir(ENTRIES_DIR), reverse=True):
            if filename.endswith('.txt'):
                filepath = os.path.join(ENTRIES_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取标题和日期
                lines = content.split('\n')
                title = lines[0].replace('标题: ', '')
                date = lines[1].replace('时间: ', '')
                
                # 只显示内容的前100个字符作为预览
                preview = content[content.find('内容:')+3:].strip()
                if len(preview) > 100:
                    preview = preview[:100] + '...'
                
                entries.append({
                    'filename': filename,
                    'title': title,
                    'date': date,
                    'preview': preview,
                    'full_content': content
                })
    
    return render_template('entries.html', entries=entries)

@app.route('/entry/<filename>')
def view_entry(filename):
    """查看单个日记的完整内容"""
    filepath = os.path.join(ENTRIES_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析内容
        lines = content.split('\n')
        title = lines[0].replace('标题: ', '')
        date = lines[1].replace('时间: ', '')
        diary_content = '\n'.join(lines[3:]) if len(lines) > 3 else ''
        
        return render_template('entry_detail.html', 
                              title=title, 
                              date=date, 
                              content=diary_content,
                              filename=filename)
    else:
        return "日记未找到", 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)