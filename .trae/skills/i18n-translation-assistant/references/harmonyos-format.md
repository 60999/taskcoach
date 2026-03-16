# HarmonyOS翻译文件格式规范

## 概述

HarmonyOS（鸿蒙）使用JSON格式的翻译文件，具体是`string.json`文件。这是华为为HarmonyOS平台定义的国际化资源格式。

## 标准来源

| 项目 | 说明 |
|------|------|
| **标准组织** | 华为 |
| **官方文档** | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/i18n-0000001774125985 |
| **基础格式** | JSON (ECMA-404) |
| **开发工具** | DevEco Studio |
| **开发语言** | ArkTS |

## 文件结构

### 目录组织

```
resources/
├── base/                  # 默认资源（必需）
│   └── element/
│       └── string.json
├── en_US/                 # 美式英语
│   └── element/
│       └── string.json
├── zh_CN/                 # 简体中文
│   └── element/
│       └── string.json
├── zh_TW/                 # 繁体中文（台湾）
│   └── element/
│       └── string.json
└── ja_JP/                 # 日语
    └── element/
        └── string.json
```

### 语言目录命名

| 目录名 | 语言 |
|--------|------|
| base | 默认资源 |
| zh_CN | 简体中文 |
| zh_TW | 繁体中文（台湾） |
| zh_HK | 繁体中文（香港） |
| en_US | 美式英语 |
| en_GB | 英式英语 |
| ja_JP | 日语 |
| ko_KR | 韩语 |
| de_DE | 德语 |
| fr_FR | 法语 |

## string.json格式

### 基本格式

```json
{
  "string": [
    {
      "name": "app_name",
      "value": "任务管理器"
    },
    {
      "name": "welcome",
      "value": "欢迎"
    },
    {
      "name": "greeting",
      "value": "你好，%s！"
    }
  ]
}
```

### 带参数的字符串

```json
{
  "string": [
    {
      "name": "user_greeting",
      "value": "你好，%1$s！你有%2$d条新消息。"
    },
    {
      "name": "items_count",
      "value": "%d个项目"
    }
  ]
}
```

### 复数形式

HarmonyOS使用ICU MessageFormat处理复数：

```json
{
  "string": [
    {
      "name": "items_count",
      "value": "{count, plural, one{#个项目} other{#个项目}}"
    }
  ]
}
```

## 使用方式

### ArkTS代码中使用

```typescript
// 引用字符串资源
import { $r } from '@ohos/hvigor';

// 在组件中使用
@Entry
@Component
struct MainPage {
  build() {
    Column() {
      Text($r('app.string.welcome'))
        .fontSize(20)
      
      Text($r('app.string.greeting', '张三'))
        .fontSize(16)
    }
  }
}
```

### 国际化API

```typescript
import { I18n } from '@ohos/i18n';

// 获取系统语言
let systemLanguage = I18n.System.getSystemLanguage();

// 设置应用语言
I18n.System.setSystemLanguage('zh_CN');
```

## 应用商店多语言描述

### 描述文件结构

```
resources/
└── rawfile/
    └── descriptions/
        ├── en-US/
        │   ├── short.txt      # 短描述 (10-80字符)
        │   └── full.txt        # 长描述 (100-4000字符)
        └── zh-CN/
            ├── short.txt
            └── full.txt
```

### 描述要求

| 类型 | 长度限制 |
|------|----------|
| 短描述 | 10-80字符 |
| 长描述 | 100-4000字符 |
| 截图 | 1280x720和1920x1080两种尺寸 |

## 资源限定符

### 设备类型

```
resources/
├── base/              # 默认
├── phone/             # 手机
├── tablet/            # 平板
└── tv/                # 电视
```

### 屏幕方向

```
resources/
├── base/
├── vertical/          # 竖屏
└── horizontal/        # 横屏
```

### 组合限定符

```
resources/
├── base/
├── en_US-vertical-phone/    # 英语+竖屏+手机
└── zh_CN-horizontal-tablet/ # 中文+横屏+平板
```

## 验证工具

### DevEco Studio验证

DevEco Studio会自动检查：
- 缺失的翻译键
- 格式错误
- 参数数量不匹配

### 命令行验证

```bash
# 使用hvigor构建工具
hvigorw clean
hvigorw assembleHap
```

## 与其他平台对比

| 特性 | HarmonyOS | Android | iOS |
|------|-----------|---------|-----|
| 文件格式 | JSON | XML | Strings |
| 标准来源 | 华为 | Google | Apple |
| 开发工具 | DevEco Studio | Android Studio | Xcode |
| 复数支持 | ICU MessageFormat | XML plurals | stringsdict |
| 参数格式 | %1$s, %2$d | %1$s, %2$d | %@, %ld |

## 最佳实践

1. **始终提供base资源**：作为默认回退
2. **使用有意义的键名**：如`user_profile_title`
3. **保持参数顺序一致**：跨语言翻译时注意参数位置
4. **测试多语言切换**：在DevEco Studio中预览不同语言
5. **检查描述长度**：应用商店描述有严格长度限制

## 参考链接

- [HarmonyOS国际化开发指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/i18n-0000001774125985)
- [HarmonyOS资源管理](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/resource-overview-0000001774125697)
- [DevEco Studio用户指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/ide-overview-0000001573248045)
