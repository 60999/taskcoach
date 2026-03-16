# 其他翻译文件格式规范

本文档涵盖不常用但重要的翻译文件格式。

## Android XML格式

### 文件位置

```
res/
├── values/           # 默认语言
│   └── strings.xml
├── values-zh-rCN/   # 简体中文
│   └── strings.xml
├── values-zh-rTW/   # 繁体中文
│   └── strings.xml
└── values-ja/       # 日语
    └── strings.xml
```

### 基本格式

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- 简单字符串 -->
    <string name="app_name">任务管理器</string>
    <string name="welcome">欢迎</string>
    
    <!-- 带占位符 -->
    <string name="greeting">你好，%1$s！</string>
    <string name="items">你%2$d个任务中有%1$d个已完成</string>
    
    <!-- 复数形式 -->
    <plurals name="items_count">
        <item quantity="one">%d个项目</item>
        <item quantity="other">%d个项目</item>
    </plurals>
    
    <!-- 数组 -->
    <string-array name="colors">
        <item>红色</item>
        <item>绿色</item>
        <item>蓝色</item>
    </string-array>
</resources>
```

### 占位符说明

| 占位符 | 说明 |
|--------|------|
| %1$s | 第一个参数，字符串 |
| %2$d | 第二个参数，整数 |
| %1$d | 第一个参数，整数 |

### 复数规则

```xml
<plurals name="items">
    <item quantity="zero">无项目</item>
    <item quantity="one">一个项目</item>
    <item quantity="two">两个项目</item>
    <item quantity="few">几个项目</item>
    <item quantity="many">很多项目</item>
    <item quantity="other">%d个项目</item>
</plurals>
```

## iOS Strings格式

### 文件位置

```
Resources/
├── Localizable.strings       # 默认语言
├── zh-Hans.lproj/
│   └── Localizable.strings   # 简体中文
├── zh-Hant.lproj/
│   └── Localizable.strings   # 繁体中文
└── ja.lproj/
    └── Localizable.strings   # 日语
```

### 基本格式

```strings
/* 注释 */
"app_name" = "任务管理器";

/* 带占位符 */
"greeting" = "你好，%@！";

/* 格式化字符串 */
"items_count" = "你已完成了 %ld 个任务";

/* 复数形式（需要.stringsdict文件）*/
"items" = "%#@items@";
```

### .stringsdict复数文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@items@</string>
        <key>items</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>无项目</string>
            <key>one</key>
            <string>%d个项目</string>
            <key>other</key>
            <string>%d个项目</string>
        </dict>
    </dict>
</dict>
</plist>
```

## YAML格式

### 基本格式

```yaml
# 简单键值对
app_name: 任务管理器
welcome: 欢迎

# 嵌套结构
menu:
  file:
    open: 打开
    save: 保存
    close: 关闭
  edit:
    copy: 复制
    paste: 粘贴

# 带参数的翻译
greeting: 你好，%{name}！
items: 你有 %{count} 个任务
```

### Ruby on Rails

```yaml
# config/locales/zh-CN.yml
zh-CN:
  helpers:
    submit:
      create: "创建%{model}"
      update: "更新%{model}"
  
  activerecord:
    models:
      task: 任务
    attributes:
      task:
        title: 标题
        description: 描述

# 使用方式
t('helpers.submit.create', model: t('activerecord.models.task'))
# 输出: 创建任务
```

### Symfony

```yaml
# translations/messages.zh_CN.yaml
messages:
  greeting: 你好，%name%！
  items: 任务列表
  number_of_tasks: "你有 %count% 个任务"
```

## TOML格式

### 基本格式

```toml
[app]
name = "Task Coach"
version = "1.0.0"

[menu]
file = "文件"
edit = "编辑"
view = "查看"

[menu.file]
open = "打开"
save = "保存"
close = "关闭"
```

## INI格式

### 基本格式

```ini
[General]
AppName=Task Coach
Version=1.0.0

[Menu]
File=文件
Edit=编辑

[Menu.File]
Open=打开
Save=保存
```

## Gettext Rust格式

### 使用rust-i18n或fluent

```rust
// 使用 fluent-rs
let fluent = FluentBundle::new(vec!["zh-CN".into()]);

let msg = fluent.add_message("greeting", "你好，{$name}！");
let value = fluent.format("greeting", Some(&[("name", "张三".into())][..]));
```

## CSV格式（通用）

### 基本格式

```csv
key,zh_CN,en,ja
app_name,任务管理器,Task Coach,タスク管理
welcome,欢迎,Welcome,ようこそ
greeting,你好,Hello,こんにちは
```

### 带上下文的格式

```csv
context,key,zh_CN,en
menu,open,打开,Open
file,open,打开文件,Open File
```

## RESS格式

### React Native

```json
{
  "zh-CN": {
    "common": {
      "save": "保存",
      "cancel": "取消"
    },
    "menu": {
      "file": "文件",
      "edit": "编辑"
    }
  }
}
```

## 格式对比表

| 格式 | 扩展名 | 嵌套支持 | 复数支持 | 备注 |
|------|--------|----------|----------|------|
| PO | .po | 无 | 原生 | GNU标准 |
| JSON | .json | 原生 | 框架相关 | JavaScript |
| Properties | .properties | 无 | ChoiceFormat | Java标准 |
| XML | .xml | 原生 | 有 | Android |
| Strings | .strings | 无 | stringsdict | iOS |
| YAML | .yaml | 原生 | 框架相关 | Ruby |
| TOML | .toml | 原生 | 无 | 配置文件 |
| CSV | .csv | 无 | 无 | 表格数据 |

## 工具推荐

### 格式转换

- **po2json**: PO转JSON
- **i18next-conv**: i18next格式转换
- **native2ascii**: Java编码转换

### 翻译管理平台

- **Crowdin**: 支持多种格式
- **Transifex**: 支持PO、JSON等
- **Lokalise**: 现代翻译管理

### 本地化工具

- **Android Lint**: 检查缺失翻译
- **Xcode**: iOS Strings验证
- **poedit**: PO文件编辑器
