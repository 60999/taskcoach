#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TaskCoach 数据转换工具 - 独立启动脚本

此脚本可以独立运行，无需依赖 TaskCoach 源码。

使用方法:
    # 完整转换（从旧版TSK导出CSV并生成新版TSK）
    python run_converter.py convert input.tsk output_dir/
    
    # 仅导出为CSV
    python run_converter.py export input.tsk output_dir/
    
    # 从中文CSV导入
    python run_converter.py import-chinese categories.csv tasks.csv output.tsk
    
    # 从标准CSV导入
    python run_converter.py import tasks.csv output.tsk
"""

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_script_dir)

if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from data_converter.converter import DataConverter
from data_converter.chinese_csv_importer import import_chinese_csv


def print_usage():
    """打印使用说明。"""
    print(__doc__)
    print("\n可用命令:")
    print("  convert <input.tsk> <output_dir>  - 完整转换")
    print("  export <input.tsk> <output_dir>   - 仅导出CSV")
    print("  import <tasks.csv> <output.tsk>   - 从标准CSV导入")
    print("  import-chinese <categories.csv> <tasks.csv> <output.tsk>  - 从中文CSV导入")


def cmd_convert(args):
    """执行完整转换命令。"""
    if len(args) < 2:
        print("用法: python run_converter.py convert <input.tsk> <output_dir>")
        return 1
    
    input_tsk = args[0]
    output_dir = args[1]
    
    converter = DataConverter()
    report = converter.convert(input_tsk, output_dir)
    print(report.to_string())
    return 0


def cmd_export(args):
    """执行仅导出命令。"""
    if len(args) < 2:
        print("用法: python run_converter.py export <input.tsk> <output_dir>")
        return 1
    
    input_tsk = args[0]
    output_dir = args[1]
    
    converter = DataConverter()
    try:
        tasks_csv, cats_csv, efforts_csv = converter.export_only(input_tsk, output_dir)
        print("导出完成:")
        print(f"  任务: {tasks_csv}")
        if cats_csv:
            print(f"  分类: {cats_csv}")
        if efforts_csv:
            print(f"  工时: {efforts_csv}")
        return 0
    except Exception as e:
        print(f"导出失败: {e}")
        return 1


def cmd_import(args):
    """执行标准CSV导入命令。"""
    if len(args) < 2:
        print("用法: python run_converter.py import <tasks.csv> <output.tsk>")
        return 1
    
    tasks_csv = args[0]
    output_tsk = args[1]
    
    from data_converter.csv_importer import CSVImporter
    importer = CSVImporter()
    count = importer.import_tasks(tasks_csv, output_tsk)
    print(f"导入完成: {count} 个任务")
    print(f"输出文件: {output_tsk}")
    return 0


def cmd_import_chinese(args):
    """执行中文CSV导入命令。"""
    if len(args) < 3:
        print("用法: python run_converter.py import-chinese <categories.csv> <tasks.csv> <output.tsk>")
        print("      categories.csv 可以为空，用 '' 表示")
        return 1
    
    categories_csv = args[0] if args[0] else None
    tasks_csv = args[1]
    output_tsk = args[2]
    
    result = import_chinese_csv(categories_csv, tasks_csv, output_tsk)
    
    print("导入完成:")
    print(f"  分类: {result['categories']}")
    print(f"  任务: {result['tasks']}")
    print(f"  输出: {output_tsk}")
    return 0


def main():
    """主入口函数。"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "convert": cmd_convert,
        "export": cmd_export,
        "import": cmd_import,
        "import-chinese": cmd_import_chinese,
    }
    
    if command in commands:
        exit_code = commands[command](args)
        sys.exit(exit_code)
    else:
        print(f"未知命令: {command}")
        print("可用命令: convert, export, import, import-chinese")
        sys.exit(1)


if __name__ == "__main__":
    main()
