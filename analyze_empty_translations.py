# -*- coding: utf-8 -*-
"""
直接修复 zh_CN.po 文件中的空翻译
使用简单的字符串替换方式
"""
import shutil
import re

def get_all_empty_msgids():
    """获取所有空翻译的msgid"""
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    empty_msgids = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('msgid'):
            # 收集msgid内容
            msgid_start = i
            msgid_lines = []
            
            if line == 'msgid ""':
                # 多行msgid
                i += 1
                while i < len(lines) and lines[i].strip().startswith('"') and not lines[i].strip().startswith('msgstr'):
                    msgid_lines.append(lines[i].strip())
                    i += 1
            else:
                # 单行msgid
                match = re.match(r'msgid "(.*)"', line)
                if match:
                    msgid_lines.append(f'"{match.group(1)}"')
                i += 1
            
            # 找msgstr
            while i < len(lines) and not lines[i].strip().startswith('msgstr'):
                i += 1
            
            if i < len(lines) and lines[i].strip() == 'msgstr ""':
                # 检查是否是空翻译
                i += 1
                has_translation = False
                while i < len(lines) and lines[i].strip().startswith('"'):
                    if lines[i].strip() != '""':
                        has_translation = True
                    i += 1
                
                if not has_translation:
                    # 提取msgid文本
                    msgid_text = ''
                    for ml in msgid_lines:
                        # 去掉引号
                        content = ml.strip()[1:-1] if ml.strip().startswith('"') else ml.strip()
                        msgid_text += content
                    
                    # 处理转义
                    msgid_text = msgid_text.replace('\\n', '\n')
                    msgid_text = msgid_text.replace('\\t', '\t')
                    msgid_text = msgid_text.replace('\\"', '"')
                    msgid_text = msgid_text.replace('\\\\', '\\')
                    
                    empty_msgids.append({
                        'text': msgid_text,
                        'lines': msgid_lines,
                        'start': msgid_start
                    })
        else:
            i += 1
    
    return empty_msgids


def main():
    po_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    # 获取所有空翻译
    empty_msgids = get_all_empty_msgids()
    print(f"找到 {len(empty_msgids)} 个空翻译")
    
    # 输出前10个
    for idx, item in enumerate(empty_msgids[:10], 1):
        text = item['text'][:60] + '...' if len(item['text']) > 60 else item['text']
        print(f"{idx}. {text}")


if __name__ == '__main__':
    main()
