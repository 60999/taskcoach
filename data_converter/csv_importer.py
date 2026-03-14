# -*- coding: utf-8 -*-
"""
CSV 导入器模块
将 CSV 格式的任务数据导入到新版 TaskCoach 格式。

文件功能:
- 读取 CSV 格式的任务数据
- 创建新版 TaskCoach 兼容的 XML (.tsk) 文件
- 支持任务层次结构和分类关联
- 处理日期时间格式转换
"""

import csv
import os
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from xml.dom import minidom


class CSVImporter:
    """
    CSV 导入器类。
    
    将 CSV 格式的任务数据导入到新版 TaskCoach 的 XML 格式。
    支持导入：
    - 任务基本信息
    - 日期时间字段
    - 分类关联
    - 工时记录
    - 任务层次结构
    
    使用示例:
        importer = CSVImporter()
        importer.import_tasks("tasks.csv", "output.tsk")
    """
    
    TSK_VERSION = 37
    RELEASE_VERSION = "2.0.0"
    
    def __init__(self):
        """初始化导入器。"""
        self.tasks_by_id: Dict[str, dict] = {}
        self.categories_by_id: Dict[str, dict] = {}
        self.category_names: Dict[str, str] = {}
        self.efforts: List[dict] = []
        
    def import_tasks(
        self, 
        csv_filepath: str, 
        output_filepath: str,
        encoding: str = "utf-8-sig"
    ) -> int:
        """
        从 CSV 文件导入任务并生成 TSK 文件。
        
        参数:
            csv_filepath: CSV 文件路径
            output_filepath: 输出 TSK 文件路径
            encoding: 文件编码
            
        返回:
            导入的任务数量
        """
        tasks = self._read_tasks_csv(csv_filepath, encoding)
        
        self._write_tsk_file(tasks, output_filepath)
        
        return len(tasks)
    
    def import_categories(
        self, 
        csv_filepath: str, 
        output_filepath: str,
        encoding: str = "utf-8-sig"
    ) -> int:
        """
        从 CSV 文件导入分类并生成 TSK 文件。
        
        参数:
            csv_filepath: CSV 文件路径
            output_filepath: 输出 TSK 文件路径
            encoding: 文件编码
            
        返回:
            导入的分类数量
        """
        categories = self._read_categories_csv(csv_filepath, encoding)
        
        return len(categories)
    
    def import_efforts(
        self, 
        csv_filepath: str, 
        encoding: str = "utf-8-sig"
    ) -> int:
        """
        从 CSV 文件导入工时记录。
        
        参数:
            csv_filepath: CSV 文件路径
            encoding: 文件编码
            
        返回:
            导入的工时记录数量
        """
        count = 0
        with open(csv_filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                effort = self._parse_effort_row(row)
                if effort and effort["task_id"] in self.tasks_by_id:
                    self.efforts.append(effort)
                    count += 1
        return count
    
    def _read_tasks_csv(self, filepath: str, encoding: str) -> List[dict]:
        """
        读取任务 CSV 文件。
        
        参数:
            filepath: CSV 文件路径
            encoding: 文件编码
            
        返回:
            任务字典列表
        """
        tasks = []
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                task = self._parse_task_row(row)
                tasks.append(task)
                self.tasks_by_id[task["id"]] = task
        
        self._build_task_hierarchy(tasks)
        
        return tasks
    
    def _read_categories_csv(self, filepath: str, encoding: str) -> List[dict]:
        """
        读取分类 CSV 文件。
        
        参数:
            filepath: CSV 文件路径
            encoding: 文件编码
            
        返回:
            分类字典列表
        """
        categories = []
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = self._parse_category_row(row)
                categories.append(category)
                self.categories_by_id[category["id"]] = category
                self.category_names[category["id"]] = category["subject"]
        
        self._build_category_hierarchy(categories)
        
        return categories
    
    def _parse_task_row(self, row: dict) -> dict:
        """
        解析任务 CSV 行。
        
        参数:
            row: CSV 行字典
            
        返回:
            任务字典
        """
        task_id = row.get("ID", "").strip()
        if not task_id:
            task_id = str(uuid.uuid4())
        
        planned_start = self._combine_datetime(
            row.get("Planned Start Date", "").strip(),
            row.get("Planned Start Time", "").strip()
        )
        due_date = self._combine_datetime(
            row.get("Due Date", "").strip(),
            row.get("Due Time", "23:59:59").strip()
        )
        actual_start = self._combine_datetime(
            row.get("Actual Start Date", "").strip(),
            row.get("Actual Start Time", "").strip()
        )
        completion_date = self._combine_datetime(
            row.get("Completion Date", "").strip(),
            row.get("Completion Time", "23:59:59").strip()
        )
        reminder = self._combine_datetime(
            row.get("Reminder Date", "").strip(),
            row.get("Reminder Time", "").strip()
        )
        
        categories_str = row.get("Categories", "").strip()
        categories = [
            c.strip() for c in categories_str.split(",") if c.strip()
        ]
        
        prereq_str = row.get("Prerequisites", "").strip()
        prerequisites = [
            p.strip() for p in prereq_str.split(",") if p.strip()
        ]
        
        try:
            budget_hours = float(row.get("Budget (hours)", "0").strip())
        except ValueError:
            budget_hours = 0.0
        
        try:
            priority = int(row.get("Priority", "0").strip())
        except ValueError:
            priority = 0
        
        try:
            percentage = int(row.get("Percentage Complete", "0").strip())
        except ValueError:
            percentage = 0
        
        try:
            hourly_fee = float(row.get("Hourly Fee", "0").strip())
        except ValueError:
            hourly_fee = 0.0
        
        try:
            fixed_fee = float(row.get("Fixed Fee", "0").strip())
        except ValueError:
            fixed_fee = 0.0
        
        try:
            status = int(row.get("Status", "1").strip())
        except ValueError:
            status = 1
        
        try:
            indent = int(row.get("Indent Level", "0").strip())
        except ValueError:
            indent = 0
        
        return {
            "id": task_id,
            "subject": row.get("Subject", "").strip(),
            "description": row.get("Description", "").strip(),
            "planned_start_date": planned_start,
            "due_date": due_date,
            "actual_start_date": actual_start,
            "completion_date": completion_date,
            "priority": priority,
            "percentage_complete": percentage,
            "budget_hours": budget_hours,
            "hourly_fee": hourly_fee,
            "fixed_fee": fixed_fee,
            "reminder": reminder,
            "categories": categories,
            "prerequisites": prerequisites,
            "parent_id": row.get("Parent ID", "").strip(),
            "indent": indent,
            "creation_datetime": self._parse_datetime(row.get("Creation Date", "").strip()),
            "modification_datetime": self._parse_datetime(row.get("Modification Date", "").strip()),
            "status": status,
            "fg_color": row.get("Foreground Color", "").strip(),
            "bg_color": row.get("Background Color", "").strip(),
            "icon": row.get("Icon", "").strip(),
            "children": [],
            "efforts": [],
            "notes": [],
        }
    
    def _parse_category_row(self, row: dict) -> dict:
        """
        解析分类 CSV 行。
        
        参数:
            row: CSV 行字典
            
        返回:
            分类字典
        """
        cat_id = row.get("ID", "").strip()
        if not cat_id:
            cat_id = str(uuid.uuid4())
        
        return {
            "id": cat_id,
            "subject": row.get("Subject", "").strip(),
            "description": row.get("Description", "").strip(),
            "parent_id": row.get("Parent ID", "").strip(),
            "color": row.get("Color", "").strip(),
            "icon": row.get("Icon", "").strip(),
            "children": [],
            "notes": [],
        }
    
    def _parse_effort_row(self, row: dict) -> Optional[dict]:
        """
        解析工时记录 CSV 行。
        
        参数:
            row: CSV 行字典
            
        返回:
            工时记录字典或 None
        """
        task_id = row.get("Task ID", "").strip()
        if not task_id:
            return None
        
        start = self._combine_datetime(
            row.get("Start Date", "").strip(),
            row.get("Start Time", "").strip()
        )
        stop = self._combine_datetime(
            row.get("Stop Date", "").strip(),
            row.get("Stop Time", "").strip()
        )
        
        return {
            "id": str(uuid.uuid4()),
            "task_id": task_id,
            "start": start,
            "stop": stop,
            "description": row.get("Description", "").strip(),
        }
    
    def _combine_datetime(
        self, 
        date_str: str, 
        time_str: str
    ) -> Optional[datetime]:
        """
        合并日期和时间字符串为 datetime 对象。
        
        参数:
            date_str: 日期字符串
            time_str: 时间字符串
            
        返回:
            datetime 对象或 None
        """
        if not date_str:
            return None
        
        if not time_str:
            time_str = "00:00:00"
        
        datetime_str = f"{date_str} {time_str}"
        
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _parse_datetime(self, datetime_str: str) -> Optional[datetime]:
        """
        解析日期时间字符串。
        
        参数:
            datetime_str: 日期时间字符串
            
        返回:
            datetime 对象或 None
        """
        if not datetime_str:
            return None
        
        formats = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _build_task_hierarchy(self, tasks: List[dict]) -> None:
        """
        构建任务层次结构。
        
        参数:
            tasks: 任务列表
        """
        for task in tasks:
            parent_id = task.get("parent_id", "")
            if parent_id and parent_id in self.tasks_by_id:
                parent = self.tasks_by_id[parent_id]
                parent["children"].append(task)
    
    def _build_category_hierarchy(self, categories: List[dict]) -> None:
        """
        构建分类层次结构。
        
        参数:
            categories: 分类列表
        """
        for category in categories:
            parent_id = category.get("parent_id", "")
            if parent_id and parent_id in self.categories_by_id:
                parent = self.categories_by_id[parent_id]
                parent["children"].append(category)
    
    def _write_tsk_file(self, tasks: List[dict], filepath: str) -> None:
        """
        写入 TSK XML 文件。
        
        参数:
            tasks: 任务列表
            filepath: 输出文件路径
        """
        root = ET.Element("tasks")
        
        for task in tasks:
            if not task.get("parent_id"):
                task_element = self._create_task_element(task)
                root.append(task_element)
        
        for category_id, category in self.categories_by_id.items():
            if not category.get("parent_id"):
                cat_element = self._create_category_element(category)
                root.append(cat_element)
        
        guid_element = ET.SubElement(root, "guid")
        guid_element.text = str(uuid.uuid4())
        
        xml_str = ET.tostring(root, encoding="unicode")
        
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="")
        
        header = f'<?xml version="1.0" encoding="utf-8"?>\n'
        header += f'<?taskcoach release="{self.RELEASE_VERSION}" tskversion="{self.TSK_VERSION}"?>\n\n'
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(pretty_xml.split("\n", 1)[1])
    
    def _create_task_element(self, task: dict) -> ET.Element:
        """
        创建任务 XML 元素。
        
        参数:
            task: 任务字典
            
        返回:
            XML 元素
        """
        elem = ET.Element("task")
        elem.set("id", task["id"])
        elem.set("status", str(task.get("status", 1)))
        
        if task.get("subject"):
            elem.set("subject", task["subject"])
        
        if task.get("creation_datetime"):
            elem.set("creationDateTime", task["creation_datetime"].strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        if task.get("modification_datetime"):
            elem.set("modificationDateTime", task["modification_datetime"].strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        if task.get("planned_start_date"):
            elem.set("plannedstartdate", task["planned_start_date"].strftime("%Y-%m-%d %H:%M:%S"))
        
        if task.get("due_date"):
            elem.set("duedate", task["due_date"].strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        if task.get("actual_start_date"):
            elem.set("actualstartdate", task["actual_start_date"].strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        if task.get("completion_date"):
            elem.set("completiondate", task["completion_date"].strftime("%Y-%m-%d %H:%M:%S.%f"))
            elem.set("percentageComplete", "100")
        elif task.get("percentage_complete", 0) > 0:
            elem.set("percentageComplete", str(task["percentage_complete"]))
        
        if task.get("priority", 0) != 0:
            elem.set("priority", str(task["priority"]))
        
        if task.get("hourly_fee", 0) > 0:
            elem.set("hourlyFee", str(task["hourly_fee"]))
        
        if task.get("fixed_fee", 0) > 0:
            elem.set("fixedFee", str(task["fixed_fee"]))
        
        if task.get("reminder"):
            elem.set("reminder", task["reminder"].strftime("%Y-%m-%d %H:%M:%S"))
        
        if task.get("prerequisites"):
            elem.set("prerequisites", " ".join(task["prerequisites"]))
        
        if task.get("bg_color"):
            elem.set("bgColor", self._color_to_tuple_string(task["bg_color"]))
        
        if task.get("fg_color"):
            elem.set("fgColor", self._color_to_tuple_string(task["fg_color"]))
        
        if task.get("icon"):
            elem.set("icon", task["icon"])
        
        if task.get("description"):
            desc_elem = ET.SubElement(elem, "description")
            desc_elem.text = task["description"]
        
        for child in task.get("children", []):
            child_elem = self._create_task_element(child)
            elem.append(child_elem)
        
        for effort in task.get("efforts", []):
            effort_elem = self._create_effort_element(effort)
            elem.append(effort_elem)
        
        return elem
    
    def _create_category_element(self, category: dict) -> ET.Element:
        """
        创建分类 XML 元素。
        
        参数:
            category: 分类字典
            
        返回:
            XML 元素
        """
        elem = ET.Element("category")
        elem.set("id", category["id"])
        elem.set("status", "1")
        
        if category.get("subject"):
            elem.set("subject", category["subject"])
        
        if category.get("color"):
            elem.set("bgColor", self._color_to_tuple_string(category["color"]))
        
        if category.get("icon"):
            elem.set("icon", category["icon"])
        
        categorizables = [
            task_id for task_id, task in self.tasks_by_id.items()
            if category["id"] in task.get("categories", [])
        ]
        if categorizables:
            elem.set("categorizables", " ".join(categorizables))
        
        if category.get("description"):
            desc_elem = ET.SubElement(elem, "description")
            desc_elem.text = category["description"]
        
        for child in category.get("children", []):
            child_elem = self._create_category_element(child)
            elem.append(child_elem)
        
        return elem
    
    def _create_effort_element(self, effort: dict) -> ET.Element:
        """
        创建工时记录 XML 元素。
        
        参数:
            effort: 工时记录字典
            
        返回:
            XML 元素
        """
        elem = ET.Element("effort")
        elem.set("id", effort["id"])
        elem.set("status", "1")
        
        if effort.get("start"):
            elem.set("start", effort["start"].strftime("%Y-%m-%d %H:%M:%S"))
        
        if effort.get("stop"):
            elem.set("stop", effort["stop"].strftime("%Y-%m-%d %H:%M:%S"))
        
        return elem
    
    def _color_to_tuple_string(self, color_str: str) -> str:
        """
        将颜色字符串转换为元组格式。
        
        参数:
            color_str: 颜色字符串（如 #RRGGBB）
            
        返回:
            元组格式字符串（如 (255, 255, 255, 255)）
        """
        if not color_str:
            return ""
        
        if color_str.startswith("#"):
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return f"({r}, {g}, {b}, 255)"
        
        if color_str.startswith("("):
            return color_str
        
        return ""


def import_from_csv(
    tasks_csv: str,
    categories_csv: Optional[str],
    output_tsk: str,
    encoding: str = "utf-8-sig"
) -> dict:
    """
    便捷函数：从 CSV 文件导入数据并生成 TSK 文件。
    
    参数:
        tasks_csv: 任务 CSV 文件路径
        categories_csv: 分类 CSV 文件路径（可选）
        output_tsk: 输出 TSK 文件路径
        encoding: 文件编码
        
    返回:
        包含导入统计的字典
    """
    importer = CSVImporter()
    
    task_count = importer.import_tasks(tasks_csv, output_tsk, encoding)
    
    category_count = 0
    if categories_csv and os.path.exists(categories_csv):
        category_count = importer.import_categories(categories_csv, output_tsk, encoding)
    
    return {
        "tasks": task_count,
        "categories": category_count,
    }
