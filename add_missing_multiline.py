# -*- coding: utf-8 -*-
"""添加缺失的多行翻译"""

import os

# 翻译列表
translations = '''
# Missing multiline translations
msgid "Cannot acquire a lock because locking is not supported\\non the location of %s.\\nOpen %s unlocked?"
msgstr "无法获取锁定，因为 %s 的位置不支持锁定。\\n是否以未锁定方式打开 %s？"

msgid "Cannot open %(filename)s\\nbecause it was created by a newer version of %(name)s.\\nPlease upgrade %(name)s."
msgstr "无法打开 %(filename)s，\\n因为它是由更新版本的 %(name)s 创建的。\\n请升级 %(name)s。"

msgid "Could not open an IMAP connection to %(server)s:%(port)s\\nto retrieve Thunderbird email message:\\n%(error)s"
msgstr "无法打开到 %(server)s:%(port)s 的IMAP连接\\n来获取Thunderbird邮件：\\n%(error)s"

msgid "WARNING: The selected language's locale is not installed on your system. Some date and time formats may appear in your system's format instead."
msgstr "警告：所选语言的区域设置未安装在您的系统上。某些日期和时间格式可能会以您系统的格式显示。"
'''

# 读取现有文件
filename = r'D:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 \\n 为 \n
translations = translations.replace('\\\\n', '\\n')

# 添加翻译到文件末尾
if content.endswith('\n'):
    content = content + '\n' + translations
else:
    content = content + '\n\n' + translations

# 写回文件
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("翻译已添加到zh_CN.po文件")
