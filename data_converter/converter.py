# -*- coding: utf-8 -*-
"""
数据转换控制器模块
整合 TSK 读取、CSV 导出和导入功能，提供完整的数据转换流程。

文件功能:
- 协调数据转换的各个步骤
- 提供命令行接口
- 支持批量转换
- 生成转换报告
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .tsk_reader import TSKReader, TaskData, CategoryData, flatten_tasks, flatten_categories
from .csv_exporter import CSVExporter, export_to_csv
from .csv_importer import CSVImporter, import_from_csv


class ConversionReport:
    """
    转换报告类。
    
    记录转换过程中的统计信息和问题。
    
    属性:
        source_file: 源文件路径
        output_dir: 输出目录
        start_time: 开始时间
        end_time: 结束时间
        tasks_exported: 导出的任务数量
        categories_exported: 导出的分类数量
        efforts_exported: 导出的工时记录数量
        tasks_imported: 导入的任务数量
        warnings: 警告信息列表
        errors: 错误信息列表
    """
    
    def __init__(self, source_file: str, output_dir: str):
        """
        初始化转换报告。
        
        参数:
            source_file: 源文件路径
            output_dir: 输出目录
        """
        self.source_file = source_file
        self.output_dir = output_dir
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.tasks_exported = 0
        self.categories_exported = 0
        self.efforts_exported = 0
        self.tasks_imported = 0
        self.categories_imported = 0
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    def finish(self) -> None:
        """标记转换结束。"""
        self.end_time = datetime.now()
    
    def add_warning(self, message: str) -> None:
        """
        添加警告信息。
        
        参数:
            message: 警告信息
        """
        self.warnings.append(message)
    
    def add_error(self, message: str) -> None:
        """
        添加错误信息。
        
        参数:
            message: 错误信息
        """
        self.errors.append(message)
    
    @property
    def duration(self) -> float:
        """
        计算转换耗时（秒）。
        
        返回:
            转换耗时
        """
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_string(self) -> str:
        """
        生成报告字符串。
        
        返回:
            格式化的报告字符串
        """
        lines = [
            "=" * 60,
            "TaskCoach 数据转换报告",
            "=" * 60,
            "",
            f"源文件: {self.source_file}",
            f"输出目录: {self.output_dir}",
            f"转换时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"耗时: {self.duration:.2f} 秒",
            "",
            "-" * 40,
            "导出统计:",
            f"  任务: {self.tasks_exported}",
            f"  分类: {self.categories_exported}",
            f"  工时记录: {self.efforts_exported}",
            "",
            "-" * 40,
            "导入统计:",
            f"  任务: {self.tasks_imported}",
            f"  分类: {self.categories_imported}",
        ]
        
        if self.warnings:
            lines.extend([
                "",
                "-" * 40,
                f"警告 ({len(self.warnings)}):",
            ])
            for warning in self.warnings[:10]:
                lines.append(f"  - {warning}")
            if len(self.warnings) > 10:
                lines.append(f"  ... 还有 {len(self.warnings) - 10} 条警告")
        
        if self.errors:
            lines.extend([
                "",
                "-" * 40,
                f"错误 ({len(self.errors)}):",
            ])
            for error in self.errors:
                lines.append(f"  ! {error}")
        
        lines.extend([
            "",
            "=" * 60,
        ])
        
        return "\n".join(lines)


class DataConverter:
    """
    数据转换控制器类。
    
    协调 TSK 读取、CSV 导出和导入的完整流程。
    
    使用示例:
        converter = DataConverter()
        report = converter.convert("old_data.tsk", "output_dir")
        print(report.to_string())
    """
    
    def __init__(self):
        """初始化转换器。"""
        self.reader = TSKReader()
        self.report: Optional[ConversionReport] = None
    
    def convert(
        self,
        source_tsk: str,
        output_dir: str,
        encoding: str = "utf-8-sig",
        create_new_tsk: bool = True
    ) -> ConversionReport:
        """
        执行完整的数据转换流程。
        
        参数:
            source_tsk: 源 TSK 文件路径
            output_dir: 输出目录
            encoding: 文件编码
            create_new_tsk: 是否创建新版 TSK 文件
            
        返回:
            ConversionReport 对象
        """
        self.report = ConversionReport(source_tsk, output_dir)
        
        if not os.path.exists(source_tsk):
            self.report.add_error(f"源文件不存在: {source_tsk}")
            self.report.finish()
            return self.report
        
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            tasks, categories, notes = self.reader.read(source_tsk)
            
            flat_tasks = flatten_tasks(tasks)
            flat_categories = flatten_categories(categories)
            
            self.report.tasks_exported = len(flat_tasks)
            self.report.categories_exported = len(flat_categories)
            
            total_efforts = sum(
                len(task.efforts) for task in flat_tasks
            )
            self.report.efforts_exported = total_efforts
            
            exporter = CSVExporter(tasks, categories)
            csv_files = exporter.export_all(output_dir, encoding)
            
            tasks_csv_path = os.path.join(output_dir, "tasks.csv")
            categories_csv_path = os.path.join(output_dir, "categories.csv")
            
            if create_new_tsk:
                new_tsk_path = os.path.join(output_dir, "converted_data.tsk")
                importer = CSVImporter()
                self.report.tasks_imported = importer.import_tasks(
                    tasks_csv_path, new_tsk_path, encoding
                )
                if os.path.exists(categories_csv_path):
                    self.report.categories_imported = len(flat_categories)
            
            self._check_data_integrity(flat_tasks, flat_categories)
            
        except Exception as e:
            self.report.add_error(f"转换过程中发生错误: {str(e)}")
        
        self.report.finish()
        return self.report
    
    def _check_data_integrity(
        self,
        tasks: List[TaskData],
        categories: List[CategoryData]
    ) -> None:
        """
        检查数据完整性。
        
        参数:
            tasks: 任务列表
            categories: 分类列表
        """
        task_ids = {task.id for task in tasks}
        category_ids = {cat.id for cat in categories}
        
        for task in tasks:
            for prereq_id in task.prerequisites:
                if prereq_id not in task_ids:
                    self.report.add_warning(
                        f"任务 '{task.subject}' 的前置任务 '{prereq_id}' 不存在"
                    )
            
            for cat_id in task.categories:
                if cat_id not in category_ids:
                    self.report.add_warning(
                        f"任务 '{task.subject}' 的分类 '{cat_id}' 不存在"
                    )
    
    def export_only(
        self,
        source_tsk: str,
        output_dir: str,
        encoding: str = "utf-8-sig"
    ) -> Tuple[str, str, str]:
        """
        仅导出数据到 CSV，不创建新版 TSK 文件。
        
        参数:
            source_tsk: 源 TSK 文件路径
            output_dir: 输出目录
            encoding: 文件编码
            
        返回:
            (任务CSV路径, 分类CSV路径, 工时CSV路径) 元组
        """
        tasks, categories, notes = self.reader.read(source_tsk)
        
        exporter = CSVExporter(tasks, categories)
        csv_files = exporter.export_all(output_dir, encoding)
        
        return (
            csv_files["tasks"],
            csv_files.get("categories", ""),
            csv_files.get("efforts", "")
        )


def main():
    """
    命令行入口函数。
    
    支持的命令:
    - convert: 完整转换（导出 + 导入）
    - export: 仅导出为 CSV
    - import: 从 CSV 导入
    """
    parser = argparse.ArgumentParser(
        description="TaskCoach 数据转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整转换
  python -m data_converter convert old_data.tsk output_dir/
  
  # 仅导出为 CSV
  python -m data_converter export old_data.tsk csv_output/
  
  # 从 CSV 导入
  python -m data_converter import tasks.csv categories.csv output.tsk
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    convert_parser = subparsers.add_parser(
        "convert", help="完整转换：从旧版 TSK 导出为 CSV 并导入到新版"
    )
    convert_parser.add_argument("source", help="源 TSK 文件路径")
    convert_parser.add_argument("output", help="输出目录")
    convert_parser.add_argument(
        "--encoding", default="utf-8-sig", help="文件编码（默认: utf-8-sig）"
    )
    convert_parser.add_argument(
        "--no-tsk", action="store_true", help="不创建新版 TSK 文件"
    )
    
    export_parser = subparsers.add_parser(
        "export", help="导出：将 TSK 数据导出为 CSV"
    )
    export_parser.add_argument("source", help="源 TSK 文件路径")
    export_parser.add_argument("output", help="输出目录")
    export_parser.add_argument(
        "--encoding", default="utf-8-sig", help="文件编码（默认: utf-8-sig）"
    )
    
    import_parser = subparsers.add_parser(
        "import", help="导入：从 CSV 文件创建新版 TSK"
    )
    import_parser.add_argument("tasks", help="任务 CSV 文件路径")
    import_parser.add_argument("categories", nargs="?", help="分类 CSV 文件路径（可选）")
    import_parser.add_argument("output", help="输出 TSK 文件路径")
    import_parser.add_argument(
        "--encoding", default="utf-8-sig", help="文件编码（默认: utf-8-sig）"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "convert":
        converter = DataConverter()
        report = converter.convert(
            args.source,
            args.output,
            args.encoding,
            create_new_tsk=not args.no_tsk
        )
        print(report.to_string())
        
    elif args.command == "export":
        converter = DataConverter()
        try:
            tasks_csv, cats_csv, efforts_csv = converter.export_only(
                args.source, args.output, args.encoding
            )
            print(f"导出完成:")
            print(f"  任务: {tasks_csv}")
            if cats_csv:
                print(f"  分类: {cats_csv}")
            if efforts_csv:
                print(f"  工时: {efforts_csv}")
        except Exception as e:
            print(f"导出失败: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "import":
        result = import_from_csv(
            args.tasks,
            args.categories,
            args.output,
            args.encoding
        )
        print(f"导入完成:")
        print(f"  任务: {result['tasks']}")
        print(f"  分类: {result['categories']}")


if __name__ == "__main__":
    main()
