# -*- coding: utf-8 -*-
"""
全面检查 zh_CN.po 文件中的翻译问题
1. 空翻译 (msgstr "")
2. 部分翻译 (翻译不完整)
"""
import re

def check_translation_issues():
    """检查并输出所有翻译问题"""
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    empty_translations = []
    partial_translations = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检查是否是 msgid 行
        if line.startswith('msgid'):
            msgid_lines = []
            msgstr_lines = []
            
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
                
                # 收集msgstr内容
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
                if msgid_text:
                    if not msgstr_text:
                        # 空翻译
                        empty_translations.append({
                            'msgid': msgid_text,
                            'msgid_lines': msgid_lines,
                            'line_num': i - len(msgstr_lines) - 1
                        })
                    elif msgstr_text and not any('\u4e00' <= c <= '\u9fff' for c in msgstr_text):
                        # 没有中文字符的翻译（可能是未翻译的）
                        if msgid_text != msgstr_text:  # 排除故意保持相同的
                            partial_translations.append({
                                'msgid': msgid_text,
                                'msgstr': msgstr_text,
                                'line_num': i - len(msgstr_lines) - 1
                            })
        else:
            i += 1
    
    print(f"=== 空翻译 ({len(empty_translations)} 个) ===\n")
    for idx, item in enumerate(empty_translations[:30], 1):
        display = item['msgid'][:80] + '...' if len(item['msgid']) > 80 else item['msgid']
        print(f"{idx}. 行{item['line_num']}: {display}")
    
    if len(empty_translations) > 30:
        print(f"... 还有 {len(empty_translations) - 30} 个空翻译")
    
    print(f"\n=== 无中文翻译 ({len(partial_translations)} 个) ===\n")
    for idx, item in enumerate(partial_translations[:30], 1):
        msgid_display = item['msgid'][:40] + '...' if len(item['msgid']) > 40 else item['msgid']
        msgstr_display = item['msgstr'][:40] + '...' if len(item['msgstr']) > 40 else item['msgstr']
        print(f"{idx}. 行{item['line_num']}: '{msgid_display}' -> '{msgstr_display}'")
    
    if len(partial_translations) > 30:
        print(f"... 还有 {len(partial_translations) - 30} 个无中文翻译")
    
    return empty_translations, partial_translations


if __name__ == '__main__':
    check_translation_issues()
