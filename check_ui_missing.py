# -*- coding: utf-8 -*-
"""检查缺失的UI翻译（排除图标名称）"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from taskcoachlib.i18n import po2dict

# 解析中文翻译
zh_cn_file = r'D:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
zh_translations, _ = po2dict.parse(zh_cn_file)

# 检查所有Python文件
source_dirs = [
    r'D:\Development\taskcoach\taskcoachlib',
    r'D:\Development\taskcoach\taskcoach.py',
]

# 匹配 _("...") 中的字符串
pattern = re.compile(r'_\("([^"]*)"\)')

all_strings = set()
for source_dir in source_dirs:
    if os.path.isfile(source_dir):
        with open(source_dir, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = pattern.findall(content)
            all_strings.update(matches)
    elif os.path.isdir(source_dir):
        for root, dirs, files in os.walk(source_dir):
            # 排除图标目录
            if 'icons' in root.lower():
                continue
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            matches = pattern.findall(content)
                            all_strings.update(matches)
                    except Exception:
                        pass

# 过滤掉图标名称（通常是驼峰命名或特殊格式）
def is_icon_name(s):
    # 图标名称特征：驼峰命名、包含特定关键词
    icon_keywords = ['Medal', 'Trophy', 'Button', 'Sign', 'Face', 'Emoji', 'Icon', 'Kde', 'Gnome']
    if any(kw in s for kw in icon_keywords):
        return True
    # 驼峰命名（多个大写字母开头）
    if re.match(r'^[A-Z][a-z]+[A-Z]', s):
        return True
    # 纯数字
    if s.isdigit():
        return True
    return False

# 检查哪些字符串没有翻译
missing = []
same = []
for s in sorted(all_strings):
    if s and len(s) > 1 and not is_icon_name(s):
        if s not in zh_translations:
            missing.append(s)
        elif zh_translations[s] == s:
            same.append(s)

print(f"总共找到 {len(all_strings)} 个翻译字符串")
print(f"缺失翻译: {len(missing)} 个")
print(f"未翻译(原文=译文): {len(same)} 个")

print("\n=== 缺失的翻译 ===")
for s in missing[:150]:
    print(f"  - {s[:80]}..." if len(s) > 80 else f"  - {s}")
if len(missing) > 150:
    print(f"  ... 还有 {len(missing) - 150} 个")

print("\n=== 未翻译(原文=译文) ===")
for s in same[:50]:
    print(f"  - {s[:80]}..." if len(s) > 80 else f"  - {s}")
if len(same) > 50:
    print(f"  ... 还有 {len(same) - 50} 个")
