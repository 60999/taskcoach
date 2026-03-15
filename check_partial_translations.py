# -*- coding: utf-8 -*-
"""
检查 zh_CN.po 文件中的部分翻译问题
检查多行翻译是否完整
"""
import re

def check_partial_translations():
    """检查部分翻译"""
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    partial_translations = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('msgid'):
            msgid_lines = []
            msgstr_lines = []
            msgid_start = i
            
            # 收集msgid
            if line == 'msgid ""':
                i += 1
                while i < len(lines) and lines[i].strip().startswith('"') and not lines[i].strip().startswith('msgstr'):
                    msgid_lines.append(lines[i].strip())
                    i += 1
            else:
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
                
                # 收集msgstr
                if msgstr_line == 'msgstr ""':
                    i += 1
                    while i < len(lines) and lines[i].strip().startswith('"'):
                        msgstr_lines.append(lines[i].strip())
                        i += 1
                elif msgstr_line.startswith('msgstr "'):
                    match = re.match(r'msgstr "(.*)"', msgstr_line)
                    if match:
                        msgstr_lines.append(f'"{match.group(1)}"')
                    i += 1
                else:
                    i += 1
                
                # 提取msgstr文本
                msgstr_text = ''
                for ml in msgstr_lines:
                    content_part = ml.strip()
                    if content_part.startswith('"') and content_part.endswith('"'):
                        content_part = content_part[1:-1]
                        content_part = content_part.replace('\\n', '\n')
                        content_part = content_part.replace('\\t', '\t')
                        content_part = content_part.replace('\\"', '"')
                        content_part = content_part.replace('\\\\', '\\')
                        msgstr_text += content_part
                
                # 检查翻译问题
                if msgid_text and msgstr_text:
                    # 检查是否翻译不完整（没有中文字符）
                    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in msgstr_text)
                    
                    # 检查msgid行数和msgstr行数是否匹配
                    msgid_newlines = msgid_text.count('\n')
                    msgstr_newlines = msgstr_text.count('\n')
                    
                    if not has_chinese and len(msgid_text) > 3:
                        # 没有中文的翻译
                        partial_translations.append({
                            'msgid': msgid_text,
                            'msgstr': msgstr_text,
                            'line': msgid_start + 1,
                            'type': 'no_chinese'
                        })
                    elif msgid_newlines > 0 and msgstr_newlines > 0 and abs(msgid_newlines - msgstr_newlines) > 2:
                        # 行数差异过大
                        partial_translations.append({
                            'msgid': msgid_text,
                            'msgstr': msgstr_text,
                            'line': msgid_start + 1,
                            'type': 'line_mismatch'
                        })
    
    print(f"找到 {len(partial_translations)} 个可能的部分翻译问题:\n")
    
    no_chinese = [p for p in partial_translations if p['type'] == 'no_chinese']
    line_mismatch = [p for p in partial_translations if p['type'] == 'line_mismatch']
    
    if no_chinese:
        print(f"=== 无中文翻译 ({len(no_chinese)} 个) ===\n")
        for idx, item in enumerate(no_chinese[:50], 1):
            msgid_display = item['msgid'][:50] + '...' if len(item['msgid']) > 50 else item['msgid']
            msgstr_display = item['msgstr'][:50] + '...' if len(item['msgstr']) > 50 else item['msgstr']
            print(f"{idx}. 行{item['line']}: '{msgid_display}' -> '{msgstr_display}'")
    
    if line_mismatch:
        print(f"\n=== 行数不匹配 ({len(line_mismatch)} 个) ===\n")
        for idx, item in enumerate(line_mismatch[:20], 1):
            msgid_display = item['msgid'][:50] + '...' if len(item['msgid']) > 50 else item['msgid']
            msgstr_display = item['msgstr'][:50] + '...' if len(item['msgstr']) > 50 else item['msgstr']
            print(f"{idx}. 行{item['line']}: '{msgid_display}' -> '{msgstr_display}'")
    
    return partial_translations


if __name__ == '__main__':
    check_partial_translations()
