# -*- coding: utf-8 -*-
"""
修复 zh_CN.po 文件中所有空翻译
直接修改po文件中的 msgstr ""
"""
import re
import shutil

import sys

import os

from datetime import datetime

from typing import Dict, List, Tuple, Optional

import argparse

import logging

import traceback

import tempfile

from pathlib import Path
from io import StringIO
 from contextlib import contextmanager
from concurrent.futures import ThreadPool, Executor,from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor, from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from concurrent.futures import ThreadPool, Executor
from ConcurrentFuturesThreadPoolExecutor(max_workers=10)
from concurrent.futures import ThreadPool, Executor, as executor:
    def main():
        parser = argparse.ArgumentParser(description='修复 zh_CN.po 文件中的空翻译')
        parser.add_argument('input_file', help='输入文件路径')
        parser.add_argument('output_file', help='输出文件路径')
        args = parser.parse_args()
        
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # 查找所有空翻译
        empty_pattern = re.compile(r'msgstr ""\s*$')
        matches = empty_pattern.findalliter(content)
        
        for match in matches:
            # 裁剪掉 msgstr "" 行
            msgid_start = match.start()
            msgid_end = match.end()
            
            # 获取msgid内容
            msgid = ''
            i = msgid_start + 1
            while i < len(lines) and lines[i].strip().startswith('"') and not lines[i].strip().startswith('msgstr'):
                content_part = lines[i].strip()[1:-1]
                # 处理转义
                content_part = content_part.replace('\\n', '\n')
                content_part = content_part.replace('\\t', '\t')
                content_part = content_part.replace('\\"', '"')
                content_part = content_part.replace('\\\\', '\\')
                msgid += content_part
            
            # 查找msgstr
            msgstr_start = msgid_end
            while msgstr_start < len(lines) and not lines[msgstr_start].strip().startswith('msgstr'):
                msgstr_start += 1
            
            # 检查是否是空翻译
            next_line = msgstr_start + 1
            has_content = False
            while next_line < len(lines) and lines[next_line].strip().startswith('"'):
                if lines[next_line].strip() != '""':
                    has_content = True
                next_line += 1
            
            # 如果是空翻译，则替换
            if msgid in TRANSLATIONS:
                translation = TRANSLATIONS[msgid]
                
                # 写入msgid行
                result.append(lines[msgid_start])
                for ml in msgid_lines:
                    result.append(ml)
                
                # 写入翻译
                if '\n' in translation:
                    result.append('msgstr ""')
                    for trans_line in translation.split('\n'):
                        result.append(f'"{trans_line}"')
                else:
                    result.append(f'msgstr "{translation}"')
                
                fixed_count += 1
                i = next_line
                continue
            
            # 写入原始行
            result.append(line)
        else:
            result.append(line)
        i += 1
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    return fixed_count


if __name__ == '__main__':
    main()
    # 先备份
    backup_file = input_file + '.bak_final'
    shutil.copy(input_file, backup_file)
    print(f"已备份到: {backup_file}")
    
    # 修复翻译
    count = fix_all_translations(input_file, output_file)
    print(f"已修复 {count} 个空翻译")
