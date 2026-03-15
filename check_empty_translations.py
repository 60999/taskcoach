# -*- coding: utf-8 -*-
"""
检查 zh_CN.po 文件中的所有空翻译
"""
import re

def check_empty_translations():
    """检查并输出所有空翻译"""
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    empty_translations = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检查是否是 msgid 行
        if line.startswith('msgid "'):
            msgid_lines = []
            if line == 'msgid ""':
                # 多行 msgid
                i += 1
                while i < len(lines) and lines[i].strip().startswith('"') and not lines[i].strip().startswith('msgstr'):
                    msgid_lines.append(lines[i].strip().strip('"'))
                    i += 1
                msgid = ''.join(msgid_lines)
            else:
                # 单行 msgid
                msgid = line[7:].rstrip('"')
                i += 1
            
            # 找 msgstr
            while i < len(lines) and not lines[i].strip().startswith('msgstr'):
                i += 1
            
            if i < len(lines):
                msgstr_line = lines[i].strip()
                if msgstr_line == 'msgstr ""':
                    # 检查是否有多行翻译
                    i += 1
                    has_translation = False
                    while i < len(lines) and lines[i].strip().startswith('"'):
                        if lines[i].strip() != '""':
                            has_translation = True
                        i += 1
                    
                    if not has_translation and msgid:
                        empty_translations.append(msgid)
                else:
                    # msgstr 有内容
                    i += 1
        else:
            i += 1
    
    print(f"找到 {len(empty_translations)} 个空翻译:\n")
    for idx, msgid in enumerate(empty_translations, 1):
        display = msgid[:80] + '...' if len(msgid) > 80 else msgid
        print(f"{idx}. {display}")
    
    return empty_translations

if __name__ == '__main__':
    check_empty_translations()
