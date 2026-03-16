# -*- coding: utf-8 -*-
"""
CSV 导出器模块
将 TaskCoach 任务数据导出为 CSV 格式，便于后续导入到新版程序。

文件功能:
- 将任务数据导出为标准 CSV 格式
- 支持任务层次结构（通过缩进表示）
- 支持分类、优先级、日期等所有字段
- 生成兼容新版导入格式的 CSV 文件
"""

import csv
import os
from datetime import datetime
from typing import List, Optional, TextIO
from .tsk_reader import TaskData, CategoryData, flatten_tasks, flatten_categories


class CSVExporter:
    """
    CSV 导出器类。
    
    将 TaskCoach 任务数据导出为 CSV 格式，支持：
    - 任务基本信息（主题、描述、优先级等）
    - 日期时间字段（计划开始、截止、完成日期等）
    - 分类关联
    - 工时记录
    - 任务层次结构（通过缩进表示）
    
    使用示例:
        exporter = CSVExporter(tasks, categories)
        exporter.export("output.csv")
    """
    
    TASK_HEADERS = [
        "ID",
        "Subject",
        "Description",
        "Planned Start Date",
        "Planned Start Time",
        "Due Date",
        "Due Time",
        "Actual Start Date",
        "Actual Start Time",
        "Completion Date",
        "Completion Time",
        "Priority",
        "Percentage Complete",
        "Budget (hours)",
        "Hourly Fee",
        "Fixed Fee",
        "Reminder Date",
        "Reminder Time",
        "Categories",
        "Prerequisites",
        "Parent ID",
        "Indent Level",
        "Creation Date",
        "Modification Date",
        "Status",
        "Foreground Color",
        "Background Color",
        "Icon",
    ]
    
    CATEGORY_HEADERS = [
        "ID",
        "Subject",
        "Description",
        "Parent ID",
        "Color",
        "Icon",
        "Categorizables Count",
    ]
    
    EFFORT_HEADERS = [
        "Task ID",
        "Start Date",
        "Start Time",
        "Stop Date",
        "Stop Time",
        "Duration (minutes)",
        "Description",
    ]
    
    def __init__(
        self, 
        tasks: List[TaskData], 
        categories: List[CategoryData]
    ):
        """
        初始化导出器。
        
        参数:
            tasks: 任务数据列表
            categories: 分类数据列表
        """
        self.tasks = tasks
        self.categories = categories
        self._categories_by_id = {
            cat.id: cat for cat in flatten_categories(categories)
        }
    
    def export_tasks(self, filepath: str, encoding: str = "utf-8-sig") -> int:
        """
        导出任务数据到 CSV 文件。
        
        参数:
            filepath: 输出文件路径
            encoding: 文件编码，默认 utf-8-sig（带 BOM，Excel 兼容）
            
        返回:
            导出的任务数量
        """
        with open(filepath, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f)
            writer.writerow(self.TASK_HEADERS)
            
            count = 0
            for task in self.tasks:
                count += self._write_task(writer, task, parent_id="", indent=0)
            
            return count
    
    def export_categories(self, filepath: str, encoding: str = "utf-8-sig") -> int:
        """
        导出分类数据到 CSV 文件。
        
        参数:
            filepath: 输出文件路径
            encoding: 文件编码
            
        返回:
            导出的分类数量
        """
        with open(filepath, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f)
            writer.writerow(self.CATEGORY_HEADERS)
            
            count = 0
            for category in self.categories:
                count += self._write_category(writer, category, parent_id="")
            
            return count
    
    def export_efforts(self, filepath: str, encoding: str = "utf-8-sig") -> int:
        """
        导出工时记录到 CSV 文件。
        
        参数:
            filepath: 输出文件路径
            encoding: 文件编码
            
        返回:
            导出的工时记录数量
        """
        with open(filepath, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f)
            writer.writerow(self.EFFORT_HEADERS)
            
            count = 0
            flat_tasks = flatten_tasks(self.tasks)
            for task in flat_tasks:
                for effort in task.efforts:
                    writer.writerow(self._effort_to_row(task.id, effort))
                    count += 1
            
            return count
    
    def export_all(self, output_dir: str, encoding: str = "utf-8-sig") -> dict:
        """
        导出所有数据到指定目录。
        
        参数:
            output_dir: 输出目录
            encoding: 文件编码
            
        返回:
            包含各类型导出数量的字典
        """
        os.makedirs(output_dir, exist_ok=True)
        
        return {
            "tasks": self.export_tasks(
                os.path.join(output_dir, "tasks.csv"), encoding
            ),
            "categories": self.export_categories(
                os.path.join(output_dir, "categories.csv"), encoding
            ),
            "efforts": self.export_efforts(
                os.path.join(output_dir, "efforts.csv"), encoding
            ),
        }
    
    def _write_task(
        self, 
        writer: csv.writer, 
        task: TaskData, 
        parent_id: str, 
        indent: int
    ) -> int:
        """
        递归写入任务行。
        
        参数:
            writer: CSV 写入器
            task: 任务数据
            parent_id: 父任务 ID
            indent: 缩进级别
            
        返回:
            写入的任务数量
        """
        row = self._task_to_row(task, parent_id, indent)
        writer.writerow(row)
        
        count = 1
        for child in task.children:
            count += self._write_task(writer, child, task.id, indent + 1)
        
        return count
    
    def _task_to_row(
        self, 
        task: TaskData, 
        parent_id: str, 
        indent: int
    ) -> List[str]:
        """
        将任务数据转换为 CSV 行。
        
        参数:
            task: 任务数据
            parent_id: 父任务 ID
            indent: 缩进级别
            
        返回:
            CSV 行数据
        """
        indent_str = "  " * indent
        
        category_names = []
        for cat_id in task.categories:
            if cat_id in self._categories_by_id:
                category_names.append(self._categories_by_id[cat_id].subject)
        
        prereq_ids = ", ".join(task.prerequisites) if task.prerequisites else ""
        
        planned_date, planned_time = self._split_datetime(task.planned_start_date)
        due_date, due_time = self._split_datetime(task.due_date)
        actual_date, actual_time = self._split_datetime(task.actual_start_date)
        completion_date, completion_time = self._split_datetime(task.completion_date)
        reminder_date, reminder_time = self._split_datetime(task.reminder)
        creation_date, creation_time = self._split_datetime(task.creation_datetime)
        modification_date, modification_time = self._split_datetime(task.modification_datetime)
        
        budget_hours = task.budget / 3600.0 if task.budget else 0
        
        fg_color = self._color_to_string(task.fg_color)
        bg_color = self._color_to_string(task.bg_color)
        
        return [
            task.id,
            indent_str + task.subject,
            task.description,
            planned_date,
            planned_time,
            due_date,
            due_time,
            actual_date,
            actual_time,
            completion_date,
            completion_time,
            str(task.priority),
            str(task.percentage_complete),
            f"{budget_hours:.2f}",
            f"{task.hourly_fee:.2f}",
            f"{task.fixed_fee:.2f}",
            reminder_date,
            reminder_time,
            ", ".join(category_names),
            prereq_ids,
            parent_id,
            str(indent),
            creation_date,
            modification_date,
            str(task.status),
            fg_color,
            bg_color,
            task.icon,
        ]
    
    def _write_category(
        self, 
        writer: csv.writer, 
        category: CategoryData, 
        parent_id: str
    ) -> int:
        """
        递归写入分类行。
        
        参数:
            writer: CSV 写入器
            category: 分类数据
            parent_id: 父分类 ID
            
        返回:
            写入的分类数量
        """
        row = self._category_to_row(category, parent_id)
        writer.writerow(row)
        
        count = 1
        for child in category.children:
            count += self._write_category(writer, child, category.id)
        
        return count
    
    def _category_to_row(
        self, 
        category: CategoryData, 
        parent_id: str
    ) -> List[str]:
        """
        将分类数据转换为 CSV 行。
        
        参数:
            category: 分类数据
            parent_id: 父分类 ID
            
        返回:
            CSV 行数据
        """
        color = self._color_to_string(category.color)
        
        return [
            category.id,
            category.subject,
            category.description,
            parent_id,
            color,
            category.icon,
            str(len(category.categorizables)),
        ]
    
    def _effort_to_row(self, task_id: str, effort) -> List[str]:
        """
        将工时记录转换为 CSV 行。
        
        参数:
            task_id: 所属任务 ID
            effort: 工时记录数据
            
        返回:
            CSV 行数据
        """
        start_date, start_time = self._split_datetime(effort.start)
        stop_date, stop_time = self._split_datetime(effort.stop)
        
        duration_minutes = 0
        if effort.start and effort.stop:
            delta = effort.stop - effort.start
            duration_minutes = int(delta.total_seconds() / 60)
        
        return [
            task_id,
            start_date,
            start_time,
            stop_date,
            stop_time,
            str(duration_minutes),
            effort.description,
        ]
    
    def _split_datetime(
        self, 
        dt: Optional[datetime]
    ) -> tuple:
        """
        将日期时间分割为日期和时间字符串。
        
        参数:
            dt: 日期时间对象
            
        返回:
            (日期字符串, 时间字符串) 元组
        """
        if dt is None:
            return ("", "")
        return (dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S"))
    
    def _color_to_string(self, color: Optional[tuple]) -> str:
        """
        将颜色元组转换为字符串。
        
        参数:
            color: RGBA 颜色元组
            
        返回:
            颜色字符串
        """
        if color is None:
            return ""
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def export_to_csv(
    tasks: List[TaskData],
    categories: List[CategoryData],
    output_dir: str,
    encoding: str = "utf-8-sig"
) -> dict:
    """
    便捷函数：导出任务和分类数据到 CSV 文件。
    
    参数:
        tasks: 任务数据列表
        categories: 分类数据列表
        output_dir: 输出目录
        encoding: 文件编码
        
    返回:
        包含各类型导出数量的字典
    """
    exporter = CSVExporter(tasks, categories)
    return exporter.export_all(output_dir, encoding)
