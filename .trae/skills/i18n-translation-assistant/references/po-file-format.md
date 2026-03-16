# PO 文件格式规范

## 基本结构

```po
# 翻译文件头
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-01-01 00:00+0000\n"
"PO-Revision-Date: 2024-01-01 00:00+0000\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: Chinese (Simplified)\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

# 翻译条目
msgid "Source string"
msgstr "翻译字符串"
```

## 多行字符串

```po
msgid ""
"This is a very long string "
"that spans multiple lines "
"for readability"
msgstr ""
"这是一个很长的字符串 "
"跨越多行 "
"便于阅读"
```

## 带上下文的翻译

```po
msgctxt "menu"
msgid "Open"
msgstr "打开"

msgctxt "file"
msgid "Open"
msgstr "开启"
```

## 复数形式

```po
msgid "item"
msgid_plural "items"
msgstr[0] "项目"
msgstr[1] "项目"
```

## 注释格式

```po
# 普通注释
#. 提取注释（来自源代码）
#: 源代码位置注释
#, 标志（如 fuzzy, c-format）
```

## 特殊字符转义

| 字符 | 转义序列 |
|------|----------|
| 换行 | `\n` |
| 制表符 | `\t` |
| 引号 | `\"` |
| 反斜杠 | `\\` |

## 中文翻译规范

### 菜单项翻译

```po
msgid "&File\tCtrl+S"
msgstr "文件(&F)\tCtrl+S"

msgid "&Edit"
msgstr "编辑(&E)"

msgid "&Help\tF1"
msgstr "帮助(&H)\tF1"
```

### 按钮翻译

```po
msgid "OK"
msgstr "确定"

msgid "Cancel"
msgstr "取消"

msgid "Apply"
msgstr "应用"

msgid "Close"
msgstr "关闭"
```

### 错误消息翻译

```po
msgid "Cannot open file: %s"
msgstr "无法打开文件：%s"

msgid "User %(name)s has %(count)d items"
msgstr "%(name)s 用户有 %(count)d 个项目"
```

## 文件组织结构

```
project/
├── locales/
│   ├── en/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po
│   │       └── messages.mo
│   ├── zh_CN/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po
│   │       └── messages.mo
│   └── zh_TW/
│       └── LC_MESSAGES/
│           ├── messages.po
│           └── messages.mo
```
