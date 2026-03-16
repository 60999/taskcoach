# 翻译检测工具

## Python 翻译字符串提取

```python
import re

def extract_gettext_strings(file_path):
    """
    从 Python 文件中提取 gettext 翻译字符串。
    
    Args:
        file_path: Python 源文件路径
        
    Returns:
        list: 翻译字符串列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 _("...") 格式
    pattern = re.compile(r'_\("([^"]+)"\)')
    return pattern.findall(content)

def extract_multiline_strings(file_path):
    """
    处理 Python 多行字符串自动连接问题。
    
    Args:
        file_path: Python 源文件路径
        
    Returns:
        list: 合并后的翻译字符串列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    strings = []
    current_string = ""
    in_string = False
    
    for line in lines:
        if '_("' in line:
            in_string = True
            # 提取第一部分
            match = re.search(r'_\("([^"]*)"', line)
            if match:
                current_string = match.group(1)
        elif in_string:
            if '"' in line:
                # 提取中间部分
                match = re.search(r'"([^"]*)"', line)
                if match:
                    current_string += match.group(1)
                if line.strip().endswith(')'):
                    # 字符串结束
                    strings.append(current_string)
                    current_string = ""
                    in_string = False
    
    return strings
```

## PO 文件解析器

```python
def parse_po_file(po_path):
    """
    解析 PO 文件返回翻译字典。
    
    Args:
        po_path: PO 文件路径
        
    Returns:
        dict: {msgid: msgstr} 翻译字典
    """
    translations = {}
    
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    msgid = ""
    msgstr = ""
    in_msgid = False
    in_msgstr = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('msgid "'):
            # 保存前一个条目
            if msgid and msgid != "":
                translations[msgid] = msgstr
            msgid = line[7:-1]  # 去掉 msgid " 和结尾的 "
            msgstr = ""
            in_msgid = True
            in_msgstr = False
        elif line.startswith('msgstr "'):
            msgstr = line[8:-1]  # 去掉 msgstr " 和结尾的 "
            in_msgid = False
            in_msgstr = True
        elif line.startswith('"') and line.endswith('"'):
            # 多行字符串续行
            content = line[1:-1]
            if in_msgid:
                msgid += content
            elif in_msgstr:
                msgstr += content
    
    # 保存最后一个条目
    if msgid and msgid != "":
        translations[msgid] = msgstr
    
    return translations
```

## 翻译缺失检测

```python
def check_missing_translations(source_files, po_path):
    """
    检查翻译缺失情况。
    
    Args:
        source_files: 源代码文件列表
        po_path: PO 文件路径
        
    Returns:
        dict: 缺失翻译信息
    """
    # 提取源代码中的翻译字符串
    source_strings = set()
    for file_path in source_files:
        strings = extract_gettext_strings(file_path)
        source_strings.update(strings)
    
    # 解析翻译文件
    translations = parse_po_file(po_path)
    
    # 找出缺失翻译
    missing = []
    untranslated = []
    
    for s in source_strings:
        if s not in translations:
            missing.append(s)
        elif translations[s] == "" or translations[s] == s:
            untranslated.append(s)
    
    return {
        "total": len(source_strings),
        "translated": len(source_strings) - len(missing) - len(untranslated),
        "missing": missing,
        "untranslated": untranslated
    }
```

## 添加翻译条目

```python
def add_translation_entry(po_path, msgid, msgstr, comment=None):
    """
    添加新翻译到 PO 文件。
    
    Args:
        po_path: PO 文件路径
        msgid: 源字符串
        msgstr: 翻译字符串
        comment: 可选注释
    """
    with open(po_path, 'a', encoding='utf-8') as f:
        f.write('\n')
        if comment:
            f.write(f'# {comment}\n')
        f.write(f'msgid "{msgid}"\n')
        f.write(f'msgstr "{msgstr}"\n')
```

## 快捷键处理

```python
def translate_menu_item(english_text):
    """
    翻译菜单项，保留快捷键格式。
    
    Args:
        english_text: 英文菜单项文本
        
    Returns:
        str: 中文翻译
    """
    # 翻译映射表
    translations = {
        "File": "文件",
        "Edit": "编辑",
        "View": "视图",
        "Help": "帮助",
        # ... 更多翻译
    }
    
    # 提取快捷键
    parts = english_text.split('\t')
    main_text = parts[0]
    shortcut = parts[1] if len(parts) > 1 else None
    
    # 提取加速键标记 (&)
    accel_match = re.search(r'&(\w)', main_text)
    accel_char = accel_match.group(1) if accel_match else None
    
    # 翻译主文本
    text_without_accel = main_text.replace('&', '')
    translated = translations.get(text_without_accel, text_without_accel)
    
    # 添加中文加速键
    if accel_char:
        translated = f"{translated}({accel_char})"
    
    # 添加快捷键
    if shortcut:
        translated = f"{translated}\t{shortcut}"
    
    return translated
```
