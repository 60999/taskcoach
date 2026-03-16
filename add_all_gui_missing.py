# -*- coding: utf-8 -*-
"""添加所有缺失的GUI翻译"""

import os

# 翻译列表
translations = '''
# Missing GUI translations
msgid "&Activate next viewer\\tCtrl+PgDn"
msgstr "激活下一个查看器(&A)\\tCtrl+PgDn"

msgid "&Add attachment...\\tShift-Ctrl-A"
msgstr "添加附件(&A)...\\tShift-Ctrl-A"

msgid "&Clear all filters\\tShift-Ctrl-R"
msgstr "清除所有过滤器(&C)\\tShift-Ctrl-R"

msgid "&Close\\tCtrl+W"
msgstr "关闭(&C)\\tCtrl+W"

msgid "&Copy\\tCtrl+C"
msgstr "复制(&C)\\tCtrl+C"

msgid "&Decrease priority\\tCtrl+D"
msgstr "降低优先级(&D)\\tCtrl+D"

msgid "&Delete\\tCtrl+DEL"
msgstr "删除(&D)\\tCtrl+DEL"

msgid "&Deselect All\\tCtrl+Shift+A"
msgstr "取消全选(&D)\\tCtrl+Shift+A"

msgid "&Edit...\\tRETURN"
msgstr "编辑(&E)...\\t回车"

msgid "&Expand all\\tShift+Ctrl+E"
msgstr "全部展开(&E)\\tShift+Ctrl+E"

msgid "&Help contents\\tCtrl+?"
msgstr "帮助内容(&H)\\tCtrl+?"

msgid "&Help contents\\tCtrl+H"
msgstr "帮助内容(&H)\\tCtrl+H"

msgid "&Increase priority\\tCtrl+I"
msgstr "提高优先级(&I)\\tCtrl+I"

msgid "&Mail...\\tCtrl-M"
msgstr "邮件(&M)...\\tCtrl-M"

msgid "&Mail...\\tShift-Ctrl-M"
msgstr "邮件(&M)...\\tShift-Ctrl-M"

msgid "&Maximize priority\\tShift+Ctrl+I"
msgstr "最大化优先级(&M)\\tShift+Ctrl+I"

msgid "&Minimize priority\\tShift+Ctrl+D"
msgstr "最小化优先级(&M)\\tShift+Ctrl+D"

msgid "&New effort...\\tCtrl+E"
msgstr "新建花费(&N)...\\tCtrl+E"

msgid "&Open all attachments...\\tShift+Ctrl+O"
msgstr "打开所有附件(&O)...\\tShift+Ctrl+O"

msgid "&Open...\\tCtrl+O"
msgstr "打开(&O)...\\tCtrl+O"

msgid "&Page setup...\\tShift+Ctrl+P"
msgstr "页面设置(&P)...\\tShift+Ctrl+P"

msgid "&Paste\\tCtrl+V"
msgstr "粘贴(&P)\\tCtrl+V"

msgid "&Preferences...\\tAlt+P"
msgstr "首选项(&P)...\\tAlt+P"

msgid "&Print...\\tCtrl+P"
msgstr "打印(&P)...\\tCtrl+P"

msgid "&Quit\\tCtrl+Q"
msgstr "退出(&Q)\\tCtrl+Q"

msgid "&Reset all categories\\tCtrl-R"
msgstr "重置所有类别(&R)\\tCtrl-R"

msgid "&Resume tracking %s\\tShift+Ctrl+T"
msgstr "继续跟踪 %s(&R)\\tShift+Ctrl+T"

msgid "&Save\\tCtrl+S"
msgstr "保存(&S)\\tCtrl+S"

msgid "&Start tracking effort\\tCtrl-T"
msgstr "开始跟踪花费(&S)\\tCtrl-T"

msgid "Activate &previous viewer\\tCtrl+PgUp"
msgstr "激活上一个查看器(&P)\\tCtrl+PgUp"

msgid "Add &note...\\tCtrl+B"
msgstr "添加备注(&N)...\\tCtrl+B"

msgid "Co&llapse all\\tShift+Ctrl+C"
msgstr "全部折叠(&L)\\tShift+Ctrl+C"

msgid "Cu&t\\tCtrl+X"
msgstr "剪切(&T)\\tCtrl+X"

msgid "Edit &tracked task...\\tShift-Alt-T"
msgstr "编辑跟踪任务(&T)...\\tShift-Alt-T"

msgid "Mark task &active\\tAlt+RETURN"
msgstr "标记任务为活动(&A)\\tAlt+回车"

msgid "Mark task &completed\\tCtrl+RETURN"
msgstr "标记任务为已完成(&C)\\tCtrl+回车"

msgid "Mark task &inactive\\tCtrl+Alt+RETURN"
msgstr "标记任务为非活动(&I)\\tCtrl+Alt+回车"

msgid "Merge &disk changes\\tShift-Ctrl-M"
msgstr "合并磁盘更改(&D)\\tShift-Ctrl-M"

msgid "New category...\\tCtrl-G"
msgstr "新建类别...\\tCtrl-G"

msgid "New note...\\tCtrl-J"
msgstr "新建备注...\\tCtrl-J"

msgid "Open all notes...\\tShift+Ctrl+B"
msgstr "打开所有备注...\\tShift+Ctrl+B"

msgid "S&ave as...\\tShift+Ctrl+S"
msgstr "另存为(&A)...\\tShift+Ctrl+S"

msgid "Select &All\\tCtrl+A"
msgstr "全选(&A)\\tCtrl+A"

msgid "St&op tracking %s\\tShift+Ctrl+T"
msgstr "停止跟踪 %s(&O)\\tShift+Ctrl+T"

msgid "Cannot import template %s\\n%s"
msgstr "无法导入模板 %s\\n%s"

msgid "Cannot open %(filename)s\\nbecause it is locked."
msgstr "无法打开 %(filename)s\\n因为文件已锁定。"

msgid "Cannot open %s\\n%s"
msgstr "无法打开 %s\\n%s"

msgid "Cannot open URL:\\n%s"
msgstr "无法打开URL:\\n%s"

msgid "Cannot save %s\\n%s"
msgstr "无法保存 %s\\n%s"

msgid "Cannot send email:\\n%s"
msgstr "无法发送邮件:\\n%s"

msgid "Error while reading %s:\\n"
msgstr "读取 %s 时出错:\\n"

msgid "Error while saving %s.ini:\\n%s\\n"
msgstr "保存 %s.ini 时出错:\\n%s\\n"

msgid "Purging deleted items cannot be undone.\\n\\nDo you still want to purge?"
msgstr "清除已删除项目无法撤销。\\n\\n您确定要清除吗？"
'''

# 读取现有文件
filename = r'D:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 \\t 为 \t 和 \\n 为 \n
translations = translations.replace('\\\\t', '\t').replace('\\\\n', '\n')

# 添加翻译到文件末尾
if content.endswith('\n'):
    content = content + '\n' + translations
else:
    content = content + '\n\n' + translations

# 写回文件
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("翻译已添加到zh_CN.po文件")
