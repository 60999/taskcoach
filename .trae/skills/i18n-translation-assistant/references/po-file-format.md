# PO文件格式规范

## 概述

PO（Portable Object）文件是GNU gettext工具链使用的翻译文件格式，是可读的文本文件。MO（Machine Object）文件是编译后的二进制格式，用于程序运行时加载。

## 文件结构

### 基本格式

```po
# 翻译者注释
#. 提取注释（由xgettext自动生成）
#: 源代码位置：filename.py:123
#, 标志（fuzzy, c-format等）
msgid "源字符串"
msgstr "翻译字符串"
```

### 文件头部

```po
# translation of zh_CN.po to Chinese (Simplified)
# Copyright (C) YEAR Free Software Foundation, Inc.
# This file is distributed under the same license as the PACKAGE package.
# First Author <email@example.com>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-01-01 12:00+0000\n"
"PO-Revision-Date: 2024-01-01 12:00+0000\n"
"Last-Translator: Full Name <email@example.com>\n"
"Language-Team: Chinese (Simplified) <zh_CN@li.org>\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=1; plural=0;\n"
```

## 条目类型

### 1. 简单翻译

```po
msgid "Hello World"
msgstr "你好世界"
```

### 2. 多行翻译

**格式一：使用空msgid开始**
```po
msgid ""
"This is a very long string "
"that spans multiple lines."
msgstr ""
"这是一个很长的字符串，"
"跨越多行。"
```

**格式二：直接连接**
```po
msgid "Line one\n"
"Line two\n"
"Line three"
msgstr "第一行\n"
"第二行\n"
"第三行"
```

### 3. 带上下文的翻译

```po
msgctxt "menu"
msgid "Open"
msgstr "打开"

msgctxt "file"
msgid "Open"
msgstr "打开文件"
```

### 4. 复数形式

```po
msgid "item"
msgid_plural "items"
msgstr[0] "项目"
msgstr[1] "项目"
```

**不同语言的复数规则**：
```po
# 中文（无复数变化）
"Plural-Forms: nplurals=1; plural=0;\n"

# 英语（单数/复数）
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

# 法语（单数/复数）
"Plural-Forms: nplurals=2; plural=(n > 1);\n"

# 俄语（三种形式）
"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"
```

### 5. 带注释的翻译

```po
#. 菜单项：文件菜单
#: taskcoachlib/gui/menu.py:45
msgid "&File"
msgstr "文件(&F)"

# 警告消息
#: taskcoachlib/gui/dialog.py:123
#, c-format
msgid "Cannot open file: %s"
msgstr "无法打开文件：%s"
```

## 特殊字符处理

### 转义字符

| 字符 | 含义 | 示例 |
|------|------|------|
| `\"` | 双引号 | `msgid "Say \"Hello\""` |
| `\\` | 反斜杠 | `msgid "Path: C:\\Users"` |
| `\n` | 换行符 | `msgid "Line 1\nLine 2"` |
| `\t` | 制表符 | `msgid "File\tCtrl+S"` |
| `\r` | 回车符 | `msgid "Text\r\n"` |

### Unicode字符

```po
# 直接使用Unicode字符
msgid "Hello 世界"
msgstr "你好 World"

# 或使用转义序列（不推荐）
msgid "Hello \u4e16\u754c"
msgstr "你好 World"
```

## 标志（Flags）

### 常用标志

```po
#, fuzzy          # 翻译不确定，需要人工审核
#, c-format       # 包含C风格的格式化字符串（%s, %d等）
#, python-format  # 包含Python风格的格式化字符串
#, no-c-format    # 不包含格式化字符串
#, php-format     # 包含PHP风格的格式化字符串
```

### 示例

```po
#, fuzzy, c-format
msgid "Found %d errors"
msgstr "发现 %d 个错误"
```

## Python字符串自动连接问题

### 问题说明

Python源代码中的多行字符串会自动连接：

```python
# 源代码
_("This is line one "
  "and this is line two")

# Python自动连接后（无换行符）
"This is line one and this is line two"
```

### 解决方案

需要在翻译文件中提供两种版本：

```po
# 版本1：带换行符（PO文件标准格式）
msgid ""
"This is line one\n"
"and this is line two"
msgstr ""
"这是第一行\n"
"这是第二行"

# 版本2：无换行符（Python自动连接格式）
msgid "This is line one and this is line two"
msgstr "这是第一行这是第二行"
```

## 快捷键格式

### Windows风格

```po
# 菜单项
msgid "&File"
msgstr "文件(&F)"

# 带快捷键
msgid "&Save\tCtrl+S"
msgstr "保存(&S)\tCtrl+S"

# 带省略号
msgid "Open..."
msgstr "打开..."
```

### macOS风格

```po
msgid "Preferences..."
msgstr "偏好设置..."
```

## 占位符格式

### C风格（printf格式）

```po
# 位置参数
msgid "Hello, %s!"
msgstr "你好，%s！"

# 带数字的位置参数
msgid "File %1$s has %2$d errors"
msgstr "文件 %1$s 有 %2$d 个错误"
```

### Python风格

```po
# 命名参数
msgid "User %(name)s has %(count)d items"
msgstr "%(name)s 用户有 %(count)d 个项目"

# 混合格式
msgid "Processing %(count)d files, %d%% complete"
msgstr "正在处理 %(count)d 个文件，已完成 %d%%"
```

### JavaScript风格

```po
# 大括号占位符
msgid "Hello, {name}!"
msgstr "你好，{name}！"
```

## 文件编码

### 推荐编码

- **UTF-8**：推荐使用，支持所有语言
- **字符集声明**：在文件头部声明

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

### BOM问题

- 避免使用UTF-8 with BOM
- BOM可能导致解析错误

## 验证工具

### msgfmt验证

```bash
# 检查PO文件语法
msgfmt --check-format zh_CN.po

# 检查翻译完整性
msgfmt --statistics zh_CN.po
```

### 常见错误

1. **引号不匹配**
```po
# 错误
msgid "Hello
msgstr "你好"

# 正确
msgid "Hello"
msgstr "你好"
```

2. **占位符数量不匹配**
```po
# 错误
msgid "Found %d items in %s"
msgstr "在 %s 中找到项目"

# 正确
msgid "Found %d items in %s"
msgstr "在 %2$s 中找到 %1$d 个项目"
```

3. **格式字符串错误**
```po
# 错误
msgid "%d items"
msgstr "%s 个项目"

# 正确
msgid "%d items"
msgstr "%d 个项目"
```

## 最佳实践

### 1. 翻译条目组织

```po
# 按模块分组
# ===== 文件菜单 =====
msgid "&File"
msgstr "文件(&F)"

msgid "&Open..."
msgstr "打开(&O)..."

# ===== 编辑菜单 =====
msgid "&Edit"
msgstr "编辑(&E)"
```

### 2. 术语一致性

```po
# 保持术语一致
msgid "Task"
msgstr "任务"  # 不是"工作"

msgid "Task list"
msgstr "任务列表"

msgid "Task properties"
msgstr "任务属性"
```

### 3. 注释使用

```po
# 翻译者注释（帮助翻译者理解上下文）
# This is the title of the main window
msgid "Task Coach"
msgstr "Task Coach"

# 上下文注释
# Context: Error message when file cannot be opened
msgid "Cannot open file"
msgstr "无法打开文件"
```

## 参考链接

- [GNU gettext手册](https://www.gnu.org/software/gettext/manual/)
- [PO文件格式规范](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html)
- [Transifex PO格式指南](https://docs.transifex.com/formats/gettext)
