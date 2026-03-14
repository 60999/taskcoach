# TaskCoach 数据转换工具

将旧版 TaskCoach 1.4.6 的数据导出为 CSV 格式，并导入到新版程序中。

## 功能特性

- **TSK 文件读取** - 解析 XML 格式的 .tsk 文件
- **CSV 导出** - 将任务、分类、工时记录导出为 CSV
- **CSV 导入** - 将 CSV 数据导入到新版 TSK 格式
- **中文 CSV 支持** - 支持中文列名和缩进层次结构
- **独立运行** - 无需依赖 TaskCoach 源码，仅使用 Python 标准库

## 文件结构

```
data_converter/
├── __init__.py              # 模块初始化
├── tsk_reader.py            # TSK 文件读取器
├── csv_exporter.py          # CSV 导出器
├── csv_importer.py          # 标准 CSV 导入器
├── chinese_csv_importer.py  # 中文 CSV 导入器
├── converter.py             # 转换控制器
├── test_converter.py        # 单元测试
└── run_converter.py         # 独立启动脚本
```

## 快速开始

### 命令行使用

```powershell
# 显示帮助
python run_converter.py

# 完整转换（从旧版 TSK 导出 CSV 并生成新版 TSK）
python run_converter.py convert input.tsk output_dir/

# 仅导出为 CSV
python run_converter.py export input.tsk output_dir/

# 从标准 CSV 导入
python run_converter.py import tasks.csv output.tsk

# 从中文 CSV 导入
python run_converter.py import-chinese categories.csv tasks.csv output.tsk
```

### Python API 使用

```python
from data_converter.chinese_csv_importer import import_chinese_csv

# 从中文 CSV 导入
result = import_chinese_csv(
    categories_csv="分类.csv",
    tasks_csv="任务.csv",
    output_tsk="output.tsk"
)

print(f"分类: {result['categories']}, 任务: {result['tasks']}")
```

```python
from data_converter.converter import DataConverter

# 完整转换
converter = DataConverter()
report = converter.convert("input.tsk", "output_dir/")
print(report.to_string())

# 仅导出 CSV
tasks_csv, cats_csv, efforts_csv = converter.export_only("input.tsk", "output_dir/")
```

## 命令详解

### convert - 完整转换

从旧版 TSK 文件读取数据，导出为 CSV，并生成新版 TSK 文件。

```powershell
python run_converter.py convert <input.tsk> <output_dir>
```

**参数：**
- `input.tsk` - 源 TSK 文件路径
- `output_dir` - 输出目录

**输出文件：**
- `tasks.csv` - 任务数据
- `categories.csv` - 分类数据
- `efforts.csv` - 工时记录
- `converted_data.tsk` - 新版 TSK 文件

### export - 仅导出 CSV

从 TSK 文件导出数据到 CSV 格式。

```powershell
python run_converter.py export <input.tsk> <output_dir>
```

### import - 从标准 CSV 导入

从标准格式 CSV 文件导入数据并生成 TSK 文件。

```powershell
python run_converter.py import <tasks.csv> <output.tsk>
```

### import-chinese - 从中文 CSV 导入

从中文格式 CSV 文件导入数据并生成 TSK 文件。

```powershell
python run_converter.py import-chinese <categories.csv> <tasks.csv> <output.tsk>
```

**参数：**
- `categories.csv` - 分类 CSV 文件（可为空，用 `''` 表示）
- `tasks.csv` - 任务 CSV 文件
- `output.tsk` - 输出 TSK 文件路径

## 支持的 CSV 格式

### 中文 CSV 格式

**分类 CSV 列名：**
| 列名 | 说明 |
|------|------|
| 主题 | 分类名称 |
| 描述 | 分类描述 |
| 创建日期 | 创建时间 |
| 修改日期 | 修改时间 |

**任务 CSV 列名：**
| 列名 | 说明 |
|------|------|
| 主题 | 任务标题（支持缩进表示层次） |
| 描述 | 任务描述 |
| 分类 | 所属分类（支持 `父分类 -> 子分类` 格式） |
| 计划开始日期 | 计划开始日期 |
| 到期日期 | 截止日期 |
| 完成日期 | 完成日期 |
| % complete | 完成百分比 |
| 优先级 | 任务优先级 |
| 预算 | 预算时间 |
| 时间花费 | 已花费时间 |
| 创建日期 | 创建时间 |
| 修改日期 | 修改时间 |

### 缩进层次结构

任务通过主题列的前导空格表示层次关系：

```csv
主题,描述
父任务,这是父任务
 子任务1,这是子任务（1个空格缩进）
 子任务2,另一个子任务
  孙任务,孙任务（2个空格缩进）
```

### 标准 CSV 格式

**任务 CSV 列名：**
- ID, Subject, Description, Planned Start Date, Planned Start Time
- Due Date, Due Time, Actual Start Date, Actual Start Time
- Completion Date, Completion Time, Priority, Percentage Complete
- Budget (hours), Hourly Fee, Fixed Fee, Reminder Date, Reminder Time
- Categories, Prerequisites, Parent ID, Indent Level
- Creation Date, Modification Date, Status, Foreground Color, Background Color, Icon

## 版本兼容性

| 源版本 | 目标版本 |
|--------|----------|
| TaskCoach 1.4.6 (tskversion 30) | TaskCoach 2.0+ (tskversion 37) |

### 主要差异

| 特性 | 旧版 1.4.6 | 新版 |
|------|-----------|------|
| TSK 版本 | tskversion 30 | tskversion 37+ |
| 计划开始日期属性 | `startdate` | `plannedstartdate` |
| 背景颜色属性 | `color` | `bgColor` |
| 分类关联属性 | `tasks` | `categorizables` |

## 依赖

仅使用 Python 标准库，无需安装额外依赖：

- Python 3.6+
- csv
- xml.etree.ElementTree
- xml.dom.minidom
- datetime
- uuid
- argparse

## 错误处理

工具会在转换报告中记录：
- 警告信息（如缺失的前置任务引用）
- 错误信息（如文件不存在、解析错误）

## 示例

### 从中文 CSV 导入

```powershell
# 有分类文件
python run_converter.py import-chinese test1.csv test2.csv output.tsk

# 无分类文件
python run_converter.py import-chinese "" test2.csv output.tsk
```

### 从旧版 TSK 转换

```powershell
python run_converter.py convert old_data.tsk converted/
```

输出：
```
============================================================
TaskCoach 数据转换报告
============================================================

源文件: old_data.tsk
输出目录: converted/
转换时间: 2024-01-15 10:30:00
耗时: 0.05 秒

----------------------------------------
导出统计:
  任务: 50
  分类: 10
  工时记录: 25

----------------------------------------
导入统计:
  任务: 50
  分类: 10

============================================================
```

## 许可证

本工具为 TaskCoach 项目的数据转换工具，遵循项目许可证。
