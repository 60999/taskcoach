# 翻译助手 (i18n Translation Assistant)

## 技能描述

本技能用于在软件开发和重构过程中，自动检测需要翻译的内容，并生成多语言翻译文件。支持多种编程语言、翻译框架和国际化模式。

## 触发条件

当用户要求以下操作时，应激活此技能：

- "检查翻译"、"检测翻译"、"翻译检查"
- "添加翻译"、"生成翻译"、"创建翻译"
- "国际化"、"i18n"、"本地化"、"l10n"
- "多语言支持"、"语言包"
- "翻译缺失"、"未翻译"
- "生成po文件"、"生成mo文件"
- "翻译文件更新"

## 支持的编程语言和框架

### Python
- **gettext**: 标准的Python国际化框架
  - 使用 `_()` 函数标记翻译字符串
  - `.po` 文件格式（可读文本）
  - `.mo` 文件格式（编译后二进制）
- **babel**: 现代Python国际化工具
- **po2dict**: 自定义po文件解析器

### JavaScript/TypeScript
- **i18next**: 流行的JavaScript国际化框架
- **react-intl**: React应用的国际化
- **vue-i18n**: Vue.js的国际化插件
- **angular-i18n**: Angular的国际化支持

### Java
- **ResourceBundle**: Java标准国际化
- **Spring MessageSource**: Spring框架国际化

### C/C++
- **gettext**: GNU gettext工具链

### 其他
- **.NET**: resx资源文件
- **Ruby**: i18n gem
- **Go**: go-i18n

## 工作流程

### 1. 检测翻译字符串

根据编程语言检测源代码中需要翻译的字符串：

#### Python (gettext模式)
```python
# 检测模式
_("Translate this string")
gettext("Translate this string")
ngettext("singular", "plural", count)
```

#### JavaScript (i18next模式)
```javascript
// 检测模式
t("translation.key")
i18n.t("translation.key")
<Trans>Hello World</Trans>
```

#### React (react-intl模式)
```jsx
// 检测模式
<FormattedMessage id="greeting" defaultMessage="Hello" />
useIntl().formatMessage({ id: "greeting" })
```

### 2. 分析翻译文件格式

#### .po 文件格式 (gettext)
```
msgid "Source string"
msgstr "翻译字符串"

# 多行字符串
msgid ""
"Multiple line string "
"continues here"
msgstr ""
"多行字符串 "
"继续在这里"

# 带上下文
msgctxt "context"
msgid "Source"
msgstr "翻译"
```

#### JSON 格式 (i18next/vue-i18n)
```json
{
  "translation": {
    "key": "翻译内容",
    "nested": {
      "key": "嵌套翻译"
    }
  }
}
```

### 3. 检测缺失翻译

```python
# 检测逻辑伪代码
def check_missing_translations(source_files, translation_file):
    source_strings = extract_translation_strings(source_files)
    translated_strings = parse_translation_file(translation_file)
    
    missing = []
    for s in source_strings:
        if s not in translated_strings:
            missing.append(s)
    
    return missing
```

### 4. 处理特殊格式

#### Python字符串自动连接
```python
# 源代码中
_("This is a very long string "
  "that spans multiple lines "
  "for readability")

# 实际字符串（无换行符）
"This is a very long string that spans multiple lines for readability"
```

#### 快捷键格式
```python
# 带快捷键的菜单项
"&File\tCtrl+S"  # 翻译时保留\t
msgstr "文件(&F)\tCtrl+S"
```

#### 占位符格式
```python
# Python格式化
"Hello, %s!"  # 使用 %s
"User %(name)s has %(count)d items"  # 使用命名占位符

# JavaScript格式化
"Hello, {name}!"  # 使用 {}
```

## 翻译生成规则

### 中文翻译规范

1. **菜单项翻译**
   - 保留快捷键标记 `&` 放在中文括号内
   - 保留制表符 `\t` 和快捷键组合
   ```
   msgid "&File\tCtrl+S"
   msgstr "文件(&F)\tCtrl+S"
   ```

2. **按钮翻译**
   ```
   msgid "OK"
   msgstr "确定"
   
   msgid "Cancel"
   msgstr "取消"
   ```

3. **错误消息翻译**
   - 保持占位符不变
   - 保持专业术语一致性
   ```
   msgid "Cannot open file: %s"
   msgstr "无法打开文件：%s"
   ```

4. **多行字符串翻译**
   - 保持原格式（换行符位置）
   - 或合并为单行（如果源代码使用自动连接）

### 翻译文件维护

1. **添加新翻译**
   - 追加到文件末尾
   - 添加注释说明来源

2. **更新翻译**
   - 保持msgid不变
   - 更新msgstr内容

3. **删除翻译**
   - 保留翻译但标记为废弃
   - 或在清理时删除

## 常见问题处理

### 1. Python字符串自动连接问题

**问题**：源代码中的多行字符串会自动连接，但翻译文件中的msgid包含换行符，导致匹配失败。

**解决方案**：
```python
# 检测源代码格式
pattern = re.compile(r'_\(\s*"([^"]+)"\s*\n\s*"([^"]+)"\s*\)')

# 生成无换行符的翻译版本
msgid "This is line oneThis is line two"
msgstr "这是第一行这是第二行"
```

### 2. 快捷键冲突

**问题**：不同菜单项使用相同的快捷键字母。

**解决方案**：
- 检查并避免快捷键冲突
- 使用不同的字母或数字

### 3. 占位符顺序

**问题**：不同语言的语序不同，占位符顺序需要调整。

**解决方案**：
```python
# 使用命名占位符
msgid "User %(name)s has %(count)d items"
msgstr "%(name)s 用户有 %(count)d 个项目"
```

### 4. 复数形式

**问题**：不同语言的复数规则不同。

**解决方案**：
```po
msgid "item"
msgid_plural "items"
msgstr[0] "项目"
msgstr[1] "项目"
```

## 工具函数

### 提取翻译字符串
```python
import re

def extract_translation_strings(file_path, pattern):
    """从源文件中提取翻译字符串"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 _("...") 格式
    pattern = re.compile(r'_\("([^"]+)"\)')
    return pattern.findall(content)
```

### 解析PO文件
```python
def parse_po_file(po_path):
    """解析PO文件返回翻译字典"""
    translations = {}
    
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    msgid = msgstr = ""
    for line in lines:
        if line.startswith('msgid'):
            msgid = extract_string(line)
        elif line.startswith('msgstr'):
            msgstr = extract_string(line)
            if msgid:
                translations[msgid] = msgstr
    
    return translations
```

### 添加翻译
```python
def add_translation(po_path, msgid, msgstr):
    """添加新翻译到PO文件"""
    with open(po_path, 'a', encoding='utf-8') as f:
        f.write(f'\nmsgid "{msgid}"\n')
        f.write(f'msgstr "{msgstr}"\n')
```

## 最佳实践

### 1. 翻译文件组织
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

### 2. 翻译工作流
1. 提取源代码中的翻译字符串
2. 与现有翻译文件对比
3. 生成缺失翻译列表
4. 翻译新字符串
5. 更新翻译文件
6. 编译翻译文件（如需要）

### 3. 自动化建议
- 使用CI/CD检查翻译完整性
- 使用翻译管理平台（如Crowdin、Transifex）
- 定期同步翻译文件

## 输出格式

### 检测报告
```markdown
## 翻译检测报告

### 统计信息
- 总翻译字符串: XXX
- 已翻译: XXX
- 缺失翻译: XXX
- 未翻译(原文=译文): XXX

### 缺失翻译列表
| 文件 | 行号 | 字符串 |
|------|------|--------|
| file.py | 123 | "Hello World" |

### 建议翻译
msgid "Hello World"
msgstr "你好世界"
```

### 翻译文件更新
```diff
+ msgid "New string"
+ msgstr "新字符串"
```

## 注意事项

1. **编码问题**
   - 始终使用UTF-8编码
   - 注意BOM标记

2. **特殊字符**
   - 转义引号 `\"`
   - 转义反斜杠 `\\`
   - 换行符 `\n`

3. **上下文**
   - 相同字符串可能有不同翻译
   - 使用msgctxt区分上下文

4. **术语一致性**
   - 建立术语表
   - 保持翻译一致性

## 示例对话

**用户**: 检查项目中的翻译缺失

**助手**: 
我来检查项目中的翻译缺失情况...

1. 扫描源代码中的翻译字符串
2. 解析现有翻译文件
3. 对比找出缺失项

检查完成：
- 找到 100 个翻译字符串
- 已翻译 95 个
- 缺失 5 个

缺失的翻译：
1. `msgid "Save settings"` - file.py:123
2. `msgid "Language missing"` - file.py:456
...

是否需要我添加这些翻译？
