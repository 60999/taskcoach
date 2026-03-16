# 翻译缺失检测报告示例

## 检测命令

```bash
# 扫描项目并生成报告
python tools/check_translations.py --source taskcoach --po locales/zh_CN/LC_MESSAGES/messages.po
```

## 检测报告输出

```markdown
## 翻译检测报告

### 项目信息
- 项目名称: TaskCoach
- 检测时间: 2024-01-15 10:30:00
- 源代码目录: taskcoach/
- 翻译文件: locales/zh_CN/LC_MESSAGES/messages.po

### 统计信息
- 总翻译字符串: 256
- 已翻译: 245 (95.7%)
- 缺失翻译: 6 (2.3%)
- 未翻译(原文=译文): 5 (2.0%)

### 缺失翻译列表

| 文件 | 行号 | 字符串 | 上下文 |
|------|------|--------|--------|
| gui/mainframe.py | 123 | "Save settings" | 菜单项 |
| gui/mainframe.py | 456 | "Language missing" | 对话框 |
| domain/task.py | 78 | "Task priority" | 属性标签 |
| domain/task.py | 89 | "Due date" | 属性标签 |
| widgets/statusbar.py | 34 | "Task count" | 状态栏 |
| widgets/toolbar.py | 56 | "Quick filter" | 工具栏 |

### 未翻译条目

| msgid | msgstr | 位置 |
|-------|--------|------|
| "OK" | "OK" | dialogs.py:12 |
| "Cancel" | "Cancel" | dialogs.py:13 |
| "Apply" | "Apply" | dialogs.py:14 |
| "Close" | "Close" | dialogs.py:15 |
| "Help" | "Help" | menu.py:8 |

### 建议翻译

```po
# 缺失翻译建议

msgid "Save settings"
msgstr "保存设置"

msgid "Language missing"
msgstr "语言缺失"

msgid "Task priority"
msgstr "任务优先级"

msgid "Due date"
msgstr "截止日期"

msgid "Task count"
msgstr "任务数量"

msgid "Quick filter"
msgstr "快速筛选"

# 未翻译条目建议

msgid "OK"
msgstr "确定"

msgid "Cancel"
msgstr "取消"

msgid "Apply"
msgstr "应用"

msgid "Close"
msgstr "关闭"

msgid "Help"
msgstr "帮助"
```

### 快捷键冲突检查

| 菜单 | 快捷键 | 冲突项 |
|------|--------|--------|
| 文件(&F) | Alt+F | 无冲突 |
| 编辑(&E) | Alt+E | 无冲突 |
| 视图(&V) | Alt+V | 无冲突 |
| 帮助(&H) | Alt+H | 无冲突 |

### 占位符检查

| msgid | 占位符 | 状态 |
|-------|--------|------|
| "Cannot open file: %s" | %s | 正确 |
| "User %(name)s has %(count)d items" | %(name)s, %(count)d | 正确 |
| "Task %d of %d" | %d, %d | 正确 |

### 建议

1. **优先处理缺失翻译**：6个缺失翻译需要立即添加
2. **更新未翻译条目**：5个条目需要翻译
3. **术语一致性检查**：建议建立术语表
4. **定期同步**：建议在每次发布前检查翻译完整性
```

## 自动修复脚本

```python
# tools/fix_translations.py
"""
自动修复翻译缺失问题
"""

def fix_missing_translations(po_path, suggestions):
    """
    自动添加缺失的翻译。
    
    Args:
        po_path: PO 文件路径
        suggestions: 翻译建议字典
    """
    with open(po_path, 'a', encoding='utf-8') as f:
        f.write('\n# 自动添加的翻译\n')
        for msgid, msgstr in suggestions.items():
            f.write(f'\nmsgid "{msgid}"\n')
            f.write(f'msgstr "{msgstr}"\n')

if __name__ == '__main__':
    suggestions = {
        "Save settings": "保存设置",
        "Language missing": "语言缺失",
        "Task priority": "任务优先级",
        "Due date": "截止日期",
        "Task count": "任务数量",
        "Quick filter": "快速筛选",
    }
    
    fix_missing_translations(
        'locales/zh_CN/LC_MESSAGES/messages.po',
        suggestions
    )
    print("翻译已更新")
```

## CI/CD 集成

```yaml
# .github/workflows/check-translations.yml
name: Check Translations

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install polib
      
      - name: Check translations
        run: |
          python tools/check_translations.py \
            --source taskcoach \
            --po locales/zh_CN/LC_MESSAGES/messages.po \
            --fail-on-missing
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: translation-report
          path: translation-report.md
```
