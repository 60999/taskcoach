# 翻译文件格式标准来源

本文档列出了各翻译文件格式的官方标准和规范来源。

## 官方标准格式

### PO/MO格式 - GNU gettext

**标准组织**: GNU Project / Free Software Foundation

**官方文档**:
- GNU gettext手册: https://www.gnu.org/software/gettext/manual/
- PO文件格式: https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html
- MO文件格式: https://www.gnu.org/software/gettext/manual/html_node/MO-Files.html

**标准历史**:
- 1995年首次发布
- POSIX国际化标准的一部分
- 被大多数Unix/Linux系统采用

**适用语言**: C, C++, Python, PHP, Ruby, Perl, 等

---

### Properties格式 - Java Platform

**标准组织**: Oracle / OpenJDK

**官方文档**:
- java.util.Properties: https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html
- ResourceBundle: https://docs.oracle.com/javase/8/docs/api/java/util/ResourceBundle.html
- MessageFormat: https://docs.oracle.com/javase/8/docs/api/java/text/MessageFormat.html

**标准历史**:
- JDK 1.0开始内置
- Java SE标准的一部分
- Spring框架官方支持

**适用语言**: Java, Kotlin, Scala

---

### Android XML格式

**标准组织**: Google / Android Open Source Project

**官方文档**:
- String Resources: https://developer.android.com/guide/topics/resources/string-resource
- Localization: https://developer.android.com/guide/topics/resources/localization
- Plurals: https://developer.android.com/guide/topics/resources/string-resource#Plurals

**标准历史**:
- Android 1.0开始内置
- Android SDK标准的一部分

**适用平台**: Android

---

### iOS Strings格式

**标准组织**: Apple Inc.

**官方文档**:
- Localization: https://developer.apple.com/documentation/xcode/localization
- String Resources: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/LocalizingYourApp/LocalizingYourApp.html
- Stringsdict: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/LocalizingYourApp/LocalizingYourApp.html#//apple_ref/doc/uid/10000171i-CH5-SW12

**标准历史**:
- iOS 2.0开始内置
- macOS 10.0开始内置

**适用平台**: iOS, macOS, watchOS, tvOS

---

## 行业事实标准格式

### JSON格式

**基础标准**: JSON (ECMA-404)
- 规范: https://www.ecma-international.org/publications-and-standards/standards/ecma-404/

**框架标准**:

| 框架 | 官方文档 |
|------|----------|
| i18next | https://www.i18next.com/overview/configuration-options |
| vue-i18n | https://vue-i18n.intlify.dev/guide/essentials/syntax.html |
| react-intl | https://formatjs.io/docs/react-intl/components/ |
| angular-i18n | https://angular.io/guide/i18n-overview |

**适用语言**: JavaScript, TypeScript

---

### YAML格式

**基础标准**: YAML (YAML 1.2)
- 规范: https://yaml.org/spec/1.2/spec.html

**框架标准**:

| 框架 | 官方文档 |
|------|----------|
| Ruby on Rails | https://guides.rubyonrails.org/i18n.html |
| Symfony (PHP) | https://symfony.com/doc/current/translation.html#yaml-translations |
| Laravel (PHP) | https://laravel.com/docs/localization |

**适用语言**: Ruby, PHP, Python

---

## 其他格式

### TOML格式

**标准组织**: TOML Specification
- 规范: https://toml.io/en/
- GitHub: https://github.com/toml-lang/toml

**适用语言**: Rust, Python, Go

---

### CSV格式

**标准组织**: RFC 4180
- 规范: https://tools.ietf.org/html/rfc4180

**适用场景**: 翻译管理平台导入导出

---

## 标准合规性检查

### 如何验证格式合规

#### PO文件
```bash
# 使用GNU gettext工具验证
msgfmt --check-format file.po
msgfmt --statistics file.po
```

#### Properties文件
```bash
# 使用Java native2ascii验证
native2ascii -encoding UTF-8 input.txt output.properties
```

#### Android XML
```bash
# 使用Android Lint检查
./gradlew lint
# 或
lint --check MissingTranslation project/
```

#### iOS Strings
```bash
# 使用Xcode验证
plutil -lint Localizable.strings
```

#### JSON
```bash
# 使用JSON Schema验证
ajv validate -s schema.json -d messages.json
```

---

## 国际化标准组织

### 主要组织

| 组织 | 网站 | 主要标准 |
|------|------|----------|
| GNU Project | https://www.gnu.org/ | gettext |
| Unicode Consortium | https://unicode.org/ | CLDR, ICU |
| W3C | https://www.w3.org/ | Web国际化 |
| ISO | https://www.iso.org/ | 语言代码(ISO 639) |
| IETF | https://www.ietf.org/ | 语言标签(RFC 5646) |

### 相关标准

- **ISO 639**: 语言代码标准
- **ISO 3166**: 国家代码标准
- **RFC 5646**: 语言标签（如zh-CN）
- **CLDR**: Unicode通用区域数据仓库
- **ICU**: Unicode国际化组件

---

## 参考链接

- [GNU gettext官方手册](https://www.gnu.org/software/gettext/manual/)
- [Java Internationalization](https://docs.oracle.com/javase/tutorial/i18n/)
- [Android Localization](https://developer.android.com/guide/topics/resources/localization)
- [Apple Localization](https://developer.apple.com/documentation/xcode/localization)
- [Unicode CLDR](https://cldr.unicode.org/)
- [W3C Internationalization](https://www.w3.org/International/)
