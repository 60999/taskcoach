# Python gettext 翻译示例

## 基本用法

```python
# main.py
import gettext
import os

# 设置翻译
localedir = os.path.join(os.path.dirname(__file__), 'locales')
translate = gettext.translation('messages', localedir, languages=['zh_CN'], fallback=True)
translate.install()
_ = translate.gettext

# 使用翻译
print(_("Hello World"))
print(_("Welcome to TaskCoach"))
```

## 菜单项翻译

```python
# menu.py
def create_menu():
    """创建菜单栏"""
    menu_bar = MenuBar()
    
    # 文件菜单
    file_menu = Menu(_("&File"))
    file_menu.Append(ID_NEW, _("&New\tCtrl+N"), _("Create a new task"))
    file_menu.Append(ID_OPEN, _("&Open\tCtrl+O"), _("Open a task file"))
    file_menu.Append(ID_SAVE, _("&Save\tCtrl+S"), _("Save current task"))
    file_menu.AppendSeparator()
    file_menu.Append(ID_EXIT, _("E&xit\tAlt+F4"), _("Exit the application"))
    
    # 编辑菜单
    edit_menu = Menu(_("&Edit"))
    edit_menu.Append(ID_CUT, _("Cu&t\tCtrl+X"), _("Cut selection"))
    edit_menu.Append(ID_COPY, _("&Copy\tCtrl+C"), _("Copy selection"))
    edit_menu.Append(ID_PASTE, _("&Paste\tCtrl+V"), _("Paste from clipboard"))
    
    menu_bar.Append(file_menu, _("&File"))
    menu_bar.Append(edit_menu, _("&Edit"))
    
    return menu_bar
```

## 错误消息翻译

```python
# errors.py
def show_error(message, *args):
    """显示错误消息"""
    translated_msg = message % args if args else message
    dialog = ErrorDialog(translated_msg)
    dialog.ShowModal()

# 使用示例
show_error(_("Cannot open file: %s"), filename)
show_error(_("User %(name)s has %(count)d items"), name="John", count=5)
```

## 多行字符串

```python
# dialogs.py
def show_about():
    """显示关于对话框"""
    about_text = _(
        "TaskCoach is a free open source todo manager.\n"
        "It allows you to manage tasks and to-do lists.\n"
        "\n"
        "Version: %s\n"
        "License: GPL v3"
    ) % VERSION
    
    dialog = AboutDialog(about_text)
    dialog.ShowModal()
```

## 复数形式

```python
# task_count.py
def format_task_count(count):
    """格式化任务数量"""
    return ngettext(
        "You have %d task",
        "You have %d tasks",
        count
    ) % count

# 使用示例
print(format_task_count(1))   # "You have 1 task"
print(format_task_count(5))   # "You have 5 tasks"
```

## 上下文翻译

```python
# contexts.py
import gettext

# 创建上下文翻译函数
pgettext = gettext.pgettext

# 相同字符串在不同上下文的不同翻译
open_menu = pgettext("menu", "Open")      # 菜单中的"打开"
open_file = pgettext("file", "Open")      # 文件操作的"开启"
open_status = pgettext("status", "Open")  # 状态的"开放"
```

## 翻译文件生成

```bash
# 提取翻译字符串
xgettext --language=Python --keyword=_ --keyword=ngettext:1,2 \
         --output=locales/messages.pot *.py

# 创建中文翻译文件
msginit --input=locales/messages.pot \
        --locale=zh_CN \
        --output=locales/zh_CN/LC_MESSAGES/messages.po

# 编译翻译文件
msgfmt locales/zh_CN/LC_MESSAGES/messages.po \
       --output-file=locales/zh_CN/LC_MESSAGES/messages.mo
```

## 翻译文件示例 (messages.po)

```po
# Chinese (Simplified) translation for TaskCoach
msgid ""
msgstr ""
"Project-Id-Version: TaskCoach 1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-01-01 00:00+0000\n"
"PO-Revision-Date: 2024-01-01 00:00+0000\n"
"Last-Translator: TaskCoach Team\n"
"Language-Team: Chinese (Simplified)\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

msgid "Hello World"
msgstr "你好世界"

msgid "&File"
msgstr "文件(&F)"

msgid "&New\\tCtrl+N"
msgstr "新建(&N)\\tCtrl+N"

msgid "Cannot open file: %s"
msgstr "无法打开文件：%s"

msgid "User %(name)s has %(count)d items"
msgstr "%(name)s 用户有 %(count)d 个项目"

msgid "You have %d task"
msgid_plural "You have %d tasks"
msgstr[0] "您有 %d 个任务"
msgstr[1] "您有 %d 个任务"
```
