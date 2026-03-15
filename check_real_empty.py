# -*- coding: utf-8 -*-
"""
检查 zh_CN.po 文件中的真正空翻译
只检查 msgstr "" 后面没有翻译内容的情况
"""
import re

def check_real_empty_translations():
    """检查真正的空翻译"""
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    empty_translations = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检查是否是 msgid 行
        if line.startswith('msgid'):
            msgid_lines = []
            msgid_start = i
            
            # 收集msgid
            if line == 'msgid ""':
                # 多行 msgid
                i += 1
                while i < len(lines) and lines[i].strip().startswith('"') and not lines[i].strip().startswith('msgstr'):
                    msgid_lines.append(lines[i].strip())
                    i += 1
            else:
                # 单行 msgid
                match = re.match(r'msgid "(.*)"', line)
                if match:
                    msgid_lines.append(f'"{match.group(1)}"')
                i += 1
            
            # 提取msgid文本
            msgid_text = ''
            for ml in msgid_lines:
                content_part = ml.strip()
                if content_part.startswith('"') and content_part.endswith('"'):
                    content_part = content_part[1:-1]
                    content_part = content_part.replace('\\n', '\n')
                    content_part = content_part.replace('\\t', '\t')
                    content_part = content_part.replace('\\"', '"')
                    content_part = content_part.replace('\\\\', '\\')
                    msgid_text += content_part
            
            # 找 msgstr
            while i < len(lines) and not lines[i].strip().startswith('msgstr'):
                i += 1
            
            if i < len(lines):
                msgstr_line = lines[i].strip()
                
                # 检查是否是空翻译
                if msgstr_line == 'msgstr ""':
                    # 检查下一行是否有翻译内容
                    i += 1
                    next_line_idx = i
                    has_translation = False
                    while next_line_idx < len(lines) and lines[next_line_idx].strip().startswith('"'):
                        if lines[next_line_idx].strip() != '""':
                            has_translation = True
                        next_line_idx += 1
                    
                    if not has_translation and msgid_text:
                        empty_translations.append({
                            'msgid': msgid_text,
                            'line': msgid_start + 1
                        })
                else:
                    i += 1
        else:
            i += 1
    
    print(f"找到 {len(empty_translations)} 个真正的空翻译:\n")
    for idx, item in enumerate(empty_translations, 1):
        display = item['msgid'][:80] + '...' if len(item['msgid']) > 80 else item['msgid']
        print(f"{idx}. 行{item['line']}: {display}")
    
    return empty_translations


if __name__ == '__main__':
    check_real_empty_translations()
