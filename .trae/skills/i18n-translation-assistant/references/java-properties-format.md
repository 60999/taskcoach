# Java Properties翻译文件格式规范

## 概述

Java Properties文件是Java平台标准的国际化资源文件格式，用于存储键值对形式的翻译字符串。

## 文件结构

### 基本格式

```properties
# 注释以#或!开头
key1=value1
key2=value2
```

### 文件命名约定

```
# 默认资源文件
messages.properties

# 特定语言资源文件
messages_zh_CN.properties    # 简体中文
messages_zh_TW.properties    # 繁体中文
messages_en.properties       # 英语
messages_ja.properties       # 日语
```

## 基本语法

### 键值对

```properties
# 简单键值对
greeting=你好
farewell=再见
welcome=欢迎

# 带空格的值
message=这是一个很长的消息
```

### 转义字符

```properties
# 换行符
multiline=第一行\n第二行\n第三行

# 制表符
tabbed=列1\t列2\t列3

# 引号
quote=他说：\"你好\"

# 反斜杠
path=C\\Users\\Documents

# Unicode字符
chinese=\\u4e2d\\u6587
```

### 续行

```properties
# 使用反斜杠续行
long.message=这是一个很长的消息，\
它跨越了多行，\
但仍然是一个完整的字符串。
```

## 占位符

### ResourceBundle格式

```properties
# 位置参数
greeting=你好，{0}！
message=用户{0}有{1}条消息
```

```java
// Java使用方式
ResourceBundle bundle = ResourceBundle.getBundle("messages", Locale.CHINA);
String msg = MessageFormat.format(bundle.getString("greeting"), "张三");
```

### MessageFormat格式

```properties
# 数字格式
items=找到{0,number}个项目
price=价格：{0,number,currency}

# 日期格式
date=日期：{0,date,short}
datetime=时间：{0,date,medium} {0,time,short}

# 选择格式
choice={0,choice,0#没有项目|1#一个项目|1<{0,number}个项目}
```

## 文件编码

### ISO-8859-1编码

传统Properties文件使用ISO-8859-1编码，非ASCII字符需要转义：

```properties
# Unicode转义
chinese=\u4e2d\u6587
japanese=\u65e5\u672c\u8a9e
```

### UTF-8编码（Java 9+）

```properties
# 文件开头声明
# encoding: UTF-8

# 直接使用Unicode字符
chinese=中文
japanese=日本語
```

## Spring框架

### messages.properties

```properties
# Spring Boot默认位置
# src/main/resources/messages.properties

# 简单消息
app.title=任务管理器
app.description=一个简单的任务管理应用

# 验证消息
field.required={0}是必填项
field.min={0}必须至少有{1}个字符
field.max={0}不能超过{1}个字符
field.email={0}必须是有效的邮箱地址
field.pattern={0}格式不正确
```

### 使用方式

```java
@Service
public class MessageService {
    @Autowired
    private MessageSource messageSource;
    
    public String getMessage(String code, Object... args) {
        return messageSource.getMessage(code, args, LocaleContextHolder.getLocale());
    }
}
```

### Thymeleaf模板

```html
<!-- 使用#{}表达式 -->
<h1 th:text="#{app.title}">Task Manager</h1>
<p th:text="#{app.description}">Description</p>

<!-- 带参数的消息 -->
<p th:text="#{greeting(${user.name})}">Hello</p>
```

## 文件组织

### 按模块组织

```
src/main/resources/
├── messages.properties           # 默认
├── messages_zh_CN.properties     # 简体中文
├── messages_en.properties        # 英语
├── validation.properties         # 验证消息
├── validation_zh_CN.properties
├── errors.properties             # 错误消息
└── errors_zh_CN.properties
```

### 按功能组织

```properties
# === 用户相关 ===
user.login=登录
user.logout=登出
user.register=注册
user.profile=个人资料

# === 任务相关 ===
task.create=创建任务
task.edit=编辑任务
task.delete=删除任务
task.complete=完成任务

# === 消息相关 ===
message.success=操作成功
message.error=操作失败
message.confirm=确认删除？
```

## 复数处理

### 使用ChoiceFormat

```properties
# 定义复数规则
items={0,choice,0#没有项目|1#一个项目|1<{0,number}个项目}
files={0,choice,0#无文件|1#一个文件|1<{0,number}个文件}
```

```java
// 使用方式
MessageFormat.format(bundle.getString("items"), 0);   // "没有项目"
MessageFormat.format(bundle.getString("items"), 1);   // "一个项目"
MessageFormat.format(bundle.getString("items"), 5);   // "5个项目"
```

## 验证和工具

### native2ascii工具

```bash
# 将UTF-8转换为ISO-8859-1（带Unicode转义）
native2ascii -encoding UTF-8 messages_zh_CN.txt messages_zh_CN.properties

# 反向转换
native2ascii -reverse -encoding UTF-8 messages_zh_CN.properties messages_zh_CN.txt
```

### Spring Boot配置

```yaml
# application.yml
spring:
  messages:
    basename: messages,validation,errors
    encoding: UTF-8
    fallback-to-system-locale: true
```

## 常见问题

### 1. 编码问题

```properties
# 问题：直接写入中文可能导致乱码
# 解决：使用Unicode转义或UTF-8编码

# 方式1：Unicode转义
chinese=\u4e2d\u6587

# 方式2：UTF-8编码（Java 9+）
# 文件保存为UTF-8编码
chinese=中文
```

### 2. 空格处理

```properties
# 值前后的空格会被保留
key1= 前面有空格
key2=后面有空格 
key3= 两边都有空格 

# 如果不需要空格，去掉它们
key1=前面没有空格
```

### 3. 特殊字符

```properties
# 等号和冒号需要转义
key1=value=with=equals
key2=value:with:colons

# 或使用不同的分隔符
key1 value with spaces
key2:value with colons
```

## 与PO文件对比

| 特性 | Properties | PO |
|------|------------|-----|
| 可读性 | 中等 | 高 |
| 嵌套支持 | 无 | 无 |
| 复数支持 | ChoiceFormat | 原生 |
| 上下文支持 | 无 | msgctxt |
| 注释支持 | #开头 | 支持 |
| 编码 | ISO-8859-1/UTF-8 | UTF-8 |

## 最佳实践

1. **使用UTF-8编码**（Java 9+）
2. **按模块组织翻译文件**
3. **使用有意义的键名**
4. **添加注释说明上下文**
5. **保持键名一致性**
6. **使用版本控制跟踪变更**
