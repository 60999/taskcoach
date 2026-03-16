# JSON翻译文件格式规范

## 概述

JSON格式的翻译文件广泛用于JavaScript/TypeScript项目，特别是使用i18next、vue-i18n、react-intl等框架的项目。

## 支持的框架

| 框架 | 文件格式 | 特点 |
|------|----------|------|
| i18next | .json | 支持嵌套、插值、复数 |
| vue-i18n | .json | Vue.js官方国际化方案 |
| react-intl | .json | React生态国际化 |
| angular-i18n | .json | Angular官方国际化 |

## 基本格式

### 简单键值对

```json
{
  "hello": "你好",
  "world": "世界",
  "welcome": "欢迎"
}
```

### 嵌套结构

```json
{
  "menu": {
    "file": {
      "open": "打开",
      "save": "保存",
      "close": "关闭"
    },
    "edit": {
      "copy": "复制",
      "paste": "粘贴"
    }
  },
  "messages": {
    "success": "操作成功",
    "error": "操作失败"
  }
}
```

### 带描述的格式（vue-i18n）

```json
{
  "hello": {
    "message": "你好，{name}！",
    "description": "用户问候语"
  }
}
```

## 插值（变量替换）

### i18next格式

```json
{
  "greeting": "你好，{{name}}！",
  "items": "你有 {{count}} 个项目",
  "user": {
    "profile": "{{name}}的个人资料",
    "settings": "{{name}}的设置"
  }
}
```

```javascript
// 使用方式
t('greeting', { name: '张三' });  // "你好，张三！"
t('items', { count: 5 });         // "你有 5 个项目"
```

### vue-i18n格式

```json
{
  "greeting": "你好，{name}！",
  "items": "你有 {count} 个项目"
}
```

```javascript
// 使用方式
$t('greeting', { name: '张三' });  // "你好，张三！"
```

### react-intl格式

```json
{
  "greeting": "你好，{name}！",
  "items": "你有 {count, number} 个项目"
}
```

```jsx
// 使用方式
<FormattedMessage id="greeting" values={{ name: '张三' }} />
```

## 复数形式

### i18next复数

```json
{
  "item_one": "1个项目",
  "item_other": "{{count}}个项目",
  "person_one": "1个人",
  "person_other": "{{count}}个人"
}
```

```javascript
// 使用方式
t('item', { count: 1 });   // "1个项目"
t('item', { count: 5 });   // "5个项目"
```

### 完整复数形式（俄语等）

```json
{
  "item_one": "{{count}} элемент",
  "item_few": "{{count}} элемента",
  "item_many": "{{count}} элементов",
  "item_other": "{{count}} элемента"
}
```

### vue-i18n复数

```json
{
  "apple": "没有苹果 | 一个苹果 | {count}个苹果"
}
```

```javascript
// 使用方式
$tc('apple', 0);   // "没有苹果"
$tc('apple', 1);   // "一个苹果"
$tc('apple', 5);   // "5个苹果"
```

## 文件组织结构

### 按语言分目录

```
locales/
├── en/
│   ├── common.json
│   ├── menu.json
│   └── messages.json
├── zh-CN/
│   ├── common.json
│   ├── menu.json
│   └── messages.json
└── zh-TW/
    ├── common.json
    ├── menu.json
    └── messages.json
```

### 按模块分文件

```json
// common.json
{
  "buttons": {
    "save": "保存",
    "cancel": "取消",
    "delete": "删除"
  },
  "labels": {
    "name": "名称",
    "email": "邮箱",
    "phone": "电话"
  }
}

// messages.json
{
  "success": {
    "saved": "保存成功",
    "deleted": "删除成功"
  },
  "error": {
    "network": "网络错误",
    "server": "服务器错误"
  }
}
```

## 特殊处理

### HTML内容

```json
{
  "rich_text": "点击<a href='/link'>这里</a>了解更多",
  "bold_text": "这是<strong>重要</strong>信息"
}
```

### 组件插值（vue-i18n）

```json
{
  "terms": "我同意{0}和{1}",
  "privacy": "隐私政策",
  "terms_of_service": "服务条款"
}
```

```vue
<template>
  <i18n path="terms" tag="p">
    <a href="/privacy">{{ $t('privacy') }}</a>
    <a href="/terms">{{ $t('terms_of_service') }}</a>
  </i18n>
</template>
```

### 日期和时间格式

```json
{
  "date": {
    "short": {
      "year": "numeric",
      "month": "short",
      "day": "numeric"
    },
    "long": {
      "year": "numeric",
      "month": "long",
      "day": "numeric",
      "weekday": "long"
    }
  },
  "time": {
    "short": "HH:mm",
    "long": "HH:mm:ss"
  }
}
```

### 数字格式

```json
{
  "number": {
    "currency": {
      "style": "currency",
      "currency": "CNY"
    },
    "percent": {
      "style": "percent"
    },
    "decimal": {
      "style": "decimal",
      "minimumFractionDigits": 2
    }
  }
}
```

## 命名约定

### 键命名规范

```json
{
  // 推荐：使用点分隔的层级结构
  "user.profile.name": "用户名",
  "user.profile.email": "邮箱",
  
  // 或使用嵌套对象
  "user": {
    "profile": {
      "name": "用户名",
      "email": "邮箱"
    }
  }
}
```

### 命名风格

```json
{
  // 驼峰命名（推荐）
  "userProfile": "用户资料",
  "saveChanges": "保存更改",
  
  // 下划线命名
  "user_profile": "用户资料",
  "save_changes": "保存更改",
  
  // 短横线命名
  "user-profile": "用户资料",
  "save-changes": "保存更改"
}
```

## 验证工具

### JSON Schema验证

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "key": {
      "type": "string"
    }
  },
  "additionalProperties": {
    "type": "string"
  }
}
```

### i18next验证

```bash
# 安装验证工具
npm install -g i18next-parser

# 提取翻译字符串
i18next 'src/**/*.js' -o 'locales/{{lng}}/{{ns}}.json'
```

## 常见问题

### 1. 键冲突

```json
// 问题：嵌套键与字符串键冲突
{
  "user": "用户",           // 字符串键
  "user.name": "用户名"     // 与上面的user冲突
}

// 解决：使用不同的命名空间
{
  "userLabel": "用户",
  "user.name": "用户名"
}
```

### 2. 编码问题

```json
// 确保使用UTF-8编码
{
  "chinese": "中文",
  "emoji": "😀",
  "special": "特殊字符：© ® ™"
}
```

### 3. 转义字符

```json
{
  "quote": "他说：\"你好\"",
  "backslash": "路径：C:\\Users",
  "newline": "第一行\n第二行"
}
```

## 与PO文件对比

| 特性 | JSON | PO |
|------|------|-----|
| 可读性 | 高 | 高 |
| 嵌套支持 | 原生 | 无 |
| 复数支持 | 框架相关 | 原生 |
| 上下文支持 | 无 | msgctxt |
| 注释支持 | 无 | 支持 |
| 编译需要 | 否 | 是（mo文件） |
| 工具支持 | 丰富 | 丰富 |

## 最佳实践

1. **保持键名简短且有意义**
2. **使用一致的命名约定**
3. **按模块组织翻译文件**
4. **添加描述性注释（如果框架支持）**
5. **使用版本控制跟踪翻译变更**
6. **定期同步各语言的翻译键**
