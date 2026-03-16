---
name: i18n-translation-assistant
description: 本技能应在用户要求"检查翻译"、"检测翻译"、"添加翻译"、"国际化"、"i18n"、"本地化"、"多语言支持"、"翻译缺失"时使用。自动检测源代码中需要翻译的内容，生成和维护多语言翻译文件，支持Python、JavaScript、Java、HarmonyOS等多种编程语言和翻译框架。

license: Apache-2.0

metadata:
  author: taskcoach-team
  version: "1.2.0"
  tags:
    - i18n
    - translation
    - localization
    - gettext
    - internationalization
    - harmonyos
---

# i18n 翻译助手

## 功能概述

自动检测源代码中的翻译字符串，解析现有翻译文件，对比找出缺失项，生成翻译建议并更新翻译文件。

## 支持的翻译文件格式

| 格式 | 扩展名 | 适用框架 | 标准来源 | 详细规范 |
|------|--------|----------|----------|----------|
| PO/MO | .po, .mo | Python gettext, C gettext | GNU Project | [PO文件格式规范](references/po-file-format.md) |
| JSON | .json | i18next, vue-i18n, react-intl | ECMA-404 | [JSON文件格式规范](references/json-file-format.md) |
| Properties | .properties | Java ResourceBundle, Spring | Oracle/OpenJDK | [Properties文件格式规范](references/properties-file-format.md) |
| Android XML | .xml | Android | Google/AOSP | [其他格式规范](references/other-formats.md) |
| iOS Strings | .strings | iOS, macOS | Apple | [其他格式规范](references/other-formats.md) |
| HarmonyOS JSON | string.json | HarmonyOS NEXT | 华为 | [HarmonyOS格式规范](references/harmonyos-format.md) |
| YAML | .yaml, .yml | Rails, Symfony | YAML 1.2 | [其他格式规范](references/other-formats.md) |

## 支持的编程语言

| 语言 | 框架 | 翻译函数 |
|------|------|----------|
| Python | gettext, babel | `_()`, `gettext()`, `ngettext()` |
| JavaScript | i18next, vue-i18n | `t()`, `i18n.t()` |
| React | react-intl | `<FormattedMessage>`, `formatMessage()` |
| Java | ResourceBundle, Spring | `ResourceBundle.getBundle()` |
| C/C++ | gettext | `gettext()`, `_()` |
| ArkTS | HarmonyOS | `$r('app.string.key')` |

## 工作流程

### 1. 检测翻译字符串

根据编程语言识别翻译标记：

```python
# Python gettext 模式
_("Translate this string")
gettext("Translate this string")
```

```javascript
// JavaScript i18next 模式
t("translation.key")
i18n.t("translation.key")
```

```typescript
// HarmonyOS ArkTS 模式
$r('app.string.welcome')
```

### 2. 解析翻译文件

支持多种翻译文件格式，详见各格式规范文档。

### 3. 对比缺失项

对比源代码中的翻译字符串与翻译文件，找出缺失或未翻译的条目。

### 4. 生成翻译建议

根据上下文生成中文翻译建议，处理特殊格式：
- 快捷键格式保留：`&File\tCtrl+S` -> `文件(&F)\tCtrl+S`
- 占位符保留：`Hello, %s!` -> `你好，%s！`
- 多行字符串处理

### 5. 更新翻译文件

将新翻译追加到翻译文件，保持文件格式一致性。

## 特殊处理

### Python 字符串自动连接

```python
# 源代码中的多行字符串
_("This is a very long string "
  "that spans multiple lines")

# 检测时合并为单行
msgid "This is a very long string that spans multiple lines"
```

详见 [PO文件格式规范 - Python字符串自动连接问题](references/po-file-format.md#python字符串自动连接问题)

### 快捷键格式

```po
msgid "&File\tCtrl+S"
msgstr "文件(&F)\tCtrl+S"
```

详见 [PO文件格式规范 - 快捷键格式](references/po-file-format.md#快捷键格式)

### 占位符格式

```po
msgid "User %(name)s has %(count)d items"
msgstr "%(name)s 用户有 %(count)d 个项目"
```

详见 [PO文件格式规范 - 占位符格式](references/po-file-format.md#占位符格式)

## 使用方法

1. **检查翻译缺失**：扫描项目，生成缺失翻译报告
2. **添加新翻译**：为缺失的字符串生成翻译建议
3. **更新翻译文件**：将翻译写入对应的翻译文件
4. **验证翻译**：检查翻译完整性和格式正确性

## 输出示例

```markdown
## 翻译检测报告

### 统计信息
- 总翻译字符串: 100
- 已翻译: 95
- 缺失翻译: 5

### 缺失翻译列表
| 文件 | 行号 | 字符串 |
|------|------|--------|
| main.py | 123 | "Save settings" |

### 建议翻译
msgid "Save settings"
msgstr "保存设置"
```

## 参考文档

### 格式规范
- [PO文件格式规范](references/po-file-format.md) - GNU gettext翻译文件格式
- [JSON文件格式规范](references/json-file-format.md) - JavaScript/TypeScript翻译文件格式
- [Properties文件格式规范](references/properties-file-format.md) - Java翻译文件格式
- [HarmonyOS格式规范](references/harmonyos-format.md) - 鸿蒙NEXT翻译文件格式
- [其他格式规范](references/other-formats.md) - Android、iOS、YAML等格式

### 标准来源
- [翻译文件格式标准来源](references/standards-sources.md) - 各格式的官方标准文档链接

## 注意事项

1. 始终使用 UTF-8 编码
2. 保持占位符格式不变
3. 快捷键字母避免冲突
4. 使用命名占位符处理语序差异
5. HarmonyOS需要提供base默认资源
