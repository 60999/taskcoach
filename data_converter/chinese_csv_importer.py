# -*- coding: utf-8 -*-
"""
中文CSV导入器模块
专门处理旧版TaskCoach导出的中文格式CSV文件。

文件功能:
- 支持中文列名的CSV文件
- 支持缩进表示的任务层次结构
- 支持分类路径解析（如 "软件开发 -> 会遇到的问题"）
- 自动创建不存在的分类
"""

import csv
import os
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from xml.dom import minidom


class ChineseCSVImporter:
    """
    中文CSV导入器类。
    
    专门处理旧版TaskCoach导出的中文格式CSV文件。
    支持通过缩进表示任务层次结构，支持分类路径解析。
    
    使用示例:
        importer = ChineseCSVImporter()
        result = importer.import_from_files(
            categories_csv="test1.csv",
            tasks_csv="test2.csv",
            output_tsk="output.tsk"
        )
    """
    
    TSK_VERSION = 37
    RELEASE_VERSION = "2.0.0"
    
    def __init__(self):
        """初始化导入器。"""
        self.categories_by_id: Dict[str, dict] = {}
        self.categories_by_name: Dict[str, dict] = {}
        self.tasks_by_id: Dict[str, dict] = {}
    
    def import_from_files(
        self,
        categories_csv: Optional[str],
        tasks_csv: str,
        output_tsk: str,
        encoding: str = "utf-8-sig"
    ) -> dict:
        """
        从CSV文件导入数据并生成TSK文件。
        
        参数:
            categories_csv: 分类CSV文件路径（可选）
            tasks_csv: 任务CSV文件路径
            output_tsk: 输出TSK文件路径
            encoding: 文件编码
            
        返回:
            包含导入统计的字典
        """
        category_count = 0
        if categories_csv and os.path.exists(categories_csv):
            category_count = self._read_categories_csv(categories_csv, encoding)
        
        task_count = self._read_tasks_csv(tasks_csv, encoding)
        
        self._resolve_category_references()
        
        self._write_tsk_file(output_tsk)
        
        return {
            "categories": len(self.categories_by_id),
            "tasks": task_count,
        }
    
    def _read_categories_csv(self, filepath: str, encoding: str) -> int:
        """
        读取分类CSV文件。
        
        参数:
            filepath: CSV文件路径
            encoding: 文件编码
            
        返回:
            分类数量
        """
        categories = []
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = self._parse_category_row(row)
                categories.append(category)
                self.categories_by_id[category["id"]] = category
                self.categories_by_name[category["subject"]] = category
        
        return len(categories)
    
    def _read_tasks_csv(self, filepath: str, encoding: str) -> int:
        """
        读取任务CSV文件。
        
        参数:
            filepath: CSV文件路径
            encoding: 文件编码
            
        返回:
            任务数量
        """
        tasks = []
        with open(filepath, "r", newline="", encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                task = self._parse_task_row(row)
                tasks.append(task)
                self.tasks_by_id[task["id"]] = task
        
        self._build_task_hierarchy(tasks)
        
        return len(tasks)
    
    def _parse_category_row(self, row: dict) -> dict:
        """
        解析分类CSV行。
        
        参数:
            row: CSV行字典
            
        返回:
            分类字典
        """
        subject = row.get("主题", "").strip()
        
        return {
            "id": str(uuid.uuid4()),
            "subject": subject,
            "description": row.get("描述", "").strip(),
            "creation_datetime": self._parse_datetime(row.get("创建日期", "").strip()),
            "modification_datetime": self._parse_datetime(row.get("修改日期", "").strip()),
            "parent_id": "",
            "children": [],
            "tasks": [],
        }
    
    def _parse_task_row(self, row: dict) -> dict:
        """
        解析任务CSV行。
        
        参数:
            row: CSV行字典
            
        返回:
            任务字典
        """
        subject = row.get("主题", "")
        indent = self._calculate_indent(subject)
        clean_subject = subject.strip()
        
        planned_start = self._combine_datetime(
            row.get("计划开始日期", "").strip(),
            row.get("Planned start time", "").strip()
        )
        due_date = self._combine_datetime(
            row.get("到期日期", "").strip(),
            row.get("Due time", "23:59:59").strip()
        )
        actual_start = self._combine_datetime(
            row.get("实际开始日期", "").strip(),
            row.get("Actual start time", "").strip()
        )
        completion_date = self._combine_datetime(
            row.get("完成日期", "").strip(),
            row.get("Completion time", "23:59:59").strip()
        )
        reminder = self._combine_datetime(
            row.get("提示日期", "").strip(),
            row.get("Reminder time", "").strip()
        )
        creation_datetime = self._combine_datetime(
            row.get("创建日期", "").strip(),
            row.get("Creation time", "").strip()
        )
        modification_datetime = self._parse_datetime(
            row.get("修改日期", "").strip()
        )
        
        categories_str = row.get("分类", "").strip()
        categories = self._parse_categories_field(categories_str)
        
        try:
            percentage_str = row.get("% complete", "0").strip().replace("%", "")
            percentage = int(percentage_str) if percentage_str else 0
        except ValueError:
            percentage = 0
        
        try:
            priority = int(row.get("优先级", "0").strip() or "0")
        except ValueError:
            priority = 0
        
        try:
            hourly_fee = float(row.get("每小时报酬", "0").strip() or "0")
        except ValueError:
            hourly_fee = 0.0
        
        try:
            fixed_fee = float(row.get("固定报酬", "0").strip() or "0")
        except ValueError:
            fixed_fee = 0.0
        
        budget_str = row.get("预算", "").strip()
        budget_seconds = self._parse_duration(budget_str)
        
        time_spent_str = row.get("时间花费", "").strip()
        time_spent_seconds = self._parse_duration(time_spent_str)
        
        prerequisites_str = row.get("先决条件", "").strip()
        prerequisites = self._parse_prerequisites_field(prerequisites_str)
        
        return {
            "id": str(uuid.uuid4()),
            "subject": clean_subject,
            "description": row.get("描述", "").strip(),
            "indent": indent,
            "planned_start_date": planned_start,
            "due_date": due_date,
            "actual_start_date": actual_start,
            "completion_date": completion_date,
            "percentage_complete": percentage,
            "priority": priority,
            "hourly_fee": hourly_fee,
            "fixed_fee": fixed_fee,
            "budget": budget_seconds,
            "time_spent": time_spent_seconds,
            "reminder": reminder,
            "categories": categories,
            "prerequisites": prerequisites,
            "parent_id": "",
            "children": [],
            "creation_datetime": creation_datetime,
            "modification_datetime": modification_datetime,
            "attachment": row.get("附件", "").strip(),
            "notes": row.get("便笺", "").strip(),
            "recurrence": row.get("重复", "").strip(),
            "status": 1,
        }
    
    def _calculate_indent(self, subject: str) -> int:
        """
        计算主题的缩进级别。
        
        参数:
            subject: 任务主题（可能包含前导空格）
            
        返回:
            缩进级别
        """
        stripped = subject.lstrip()
        spaces = len(subject) - len(stripped)
        return spaces
    
    def _parse_categories_field(self, categories_str: str) -> List[str]:
        """
        解析分类字段。
        
        参数:
            categories_str: 分类字符串（如 "软件开发 -> 会遇到的问题"）
            
        返回:
            分类名称列表
        """
        if not categories_str:
            return []
        
        categories = []
        parts = categories_str.split(",")
        for part in parts:
            part = part.strip()
            if " -> " in part:
                path_parts = part.split(" -> ")
                for path_part in path_parts:
                    path_part = path_part.strip()
                    if path_part:
                        categories.append(path_part)
            elif part:
                categories.append(part)
        
        return list(set(categories))
    
    def _parse_prerequisites_field(self, prereq_str: str) -> List[str]:
        """
        解析先决条件字段，返回任务主题列表。
        
        参数:
            prereq_str: 先决条件字符串（如 "任务1 -> 任务2"）
            
        返回:
            任务主题列表
        """
        if not prereq_str:
            return []
        
        result = []
        parts = prereq_str.split(",")
        for part in parts:
            part = part.strip()
            if " -> " in part:
                path_parts = part.split(" -> ")
                last_part = path_parts[-1].strip()
                if last_part:
                    result.append(last_part)
            elif part:
                result.append(part)
        
        return result
    
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
            "%Y/%m/%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _combine_datetime(
        self, 
        date_str: str, 
        time_str: str
    ) -> Optional[datetime]:
        """
        合并日期和时间字符串。
        
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
        return self._parse_datetime(datetime_str)
    
    def _parse_duration(self, duration_str: str) -> int:
        """
        解析持续时间字符串，返回秒数。
        
        参数:
            duration_str: 持续时间字符串（如 "40:02:25"）
            
        返回:
            秒数
        """
        if not duration_str:
            return 0
        
        parts = duration_str.split(":")
        if len(parts) == 3:
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return hours * 3600 + minutes * 60 + seconds
            except ValueError:
                return 0
        
        return 0
    
    def _build_task_hierarchy(self, tasks: List[dict]) -> None:
        """
        根据缩进构建任务层次结构。
        
        参数:
            tasks: 任务列表
        """
        stack: List[dict] = []
        
        for task in tasks:
            indent = task["indent"]
            
            while len(stack) > indent:
                stack.pop()
            
            if stack:
                parent = stack[-1]
                task["parent_id"] = parent["id"]
                parent["children"].append(task)
            
            stack.append(task)
    
    def _resolve_category_references(self) -> None:
        """
        解析任务中的分类引用，自动创建不存在的分类。
        """
        for task_id, task in self.tasks_by_id.items():
            resolved_categories = []
            for cat_name in task.get("categories", []):
                if cat_name in self.categories_by_name:
                    cat = self.categories_by_name[cat_name]
                    resolved_categories.append(cat["id"])
                    if task_id not in cat["tasks"]:
                        cat["tasks"].append(task_id)
                else:
                    new_cat = {
                        "id": str(uuid.uuid4()),
                        "subject": cat_name,
                        "description": "",
                        "parent_id": "",
                        "children": [],
                        "tasks": [task_id],
                    }
                    self.categories_by_id[new_cat["id"]] = new_cat
                    self.categories_by_name[cat_name] = new_cat
                    resolved_categories.append(new_cat["id"])
            
            task["categories"] = resolved_categories
    
    def _resolve_prerequisites(self, prereq_names: List[str]) -> List[str]:
        """
        将先决条件任务名称转换为任务ID。
        
        参数:
            prereq_names: 先决条件任务名称列表
            
        返回:
            任务ID列表
        """
        prereq_ids = []
        for name in prereq_names:
            for task_id, task in self.tasks_by_id.items():
                if task.get("subject") == name:
                    prereq_ids.append(task_id)
                    break
        return prereq_ids
    
    def _resolve_all_prerequisites(self) -> None:
        """
        解析所有任务的先决条件引用。
        """
        for task_id, task in self.tasks_by_id.items():
            prereq_names = task.get("prerequisites", [])
            if prereq_names:
                prereq_ids = self._resolve_prerequisites(prereq_names)
                task["prerequisite_ids"] = prereq_ids
    
    def _write_tsk_file(self, filepath: str) -> None:
        """
        写入TSK XML文件。
        
        参数:
            filepath: 输出文件路径
        """
        self._resolve_all_prerequisites()
        
        root = ET.Element("tasks")
        
        for task_id, task in self.tasks_by_id.items():
            if not task.get("parent_id"):
                task_element = self._create_task_element(task)
                root.append(task_element)
        
        for cat_id, category in self.categories_by_id.items():
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
        创建任务XML元素。
        
        参数:
            task: 任务字典
            
        返回:
            XML元素
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
        
        if task.get("budget", 0) > 0:
            budget_hours = task["budget"] / 3600.0
            hours = int(budget_hours)
            minutes = int((budget_hours - hours) * 60)
            elem.set("budget", f"{hours}:{minutes}:0")
        
        if task.get("reminder"):
            elem.set("reminder", task["reminder"].strftime("%Y-%m-%d %H:%M:%S"))
        
        if task.get("categories"):
            elem.set("categories", " ".join(task["categories"]))
        
        if task.get("prerequisite_ids"):
            elem.set("prerequisites", " ".join(task["prerequisite_ids"]))
        
        if task.get("description"):
            desc_elem = ET.SubElement(elem, "description")
            desc_elem.text = task["description"]
        
        if task.get("notes"):
            notes_elem = ET.SubElement(elem, "notes")
            notes_elem.text = task["notes"]
        
        if task.get("recurrence"):
            elem.set("recurrence", task["recurrence"])
        
        if task.get("time_spent", 0) > 0:
            effort_elem = self._create_effort_element(task)
            elem.append(effort_elem)
        
        for child in task.get("children", []):
            child_elem = self._create_task_element(child)
            elem.append(child_elem)
        
        return elem
    
    def _create_effort_element(self, task: dict) -> ET.Element:
        """
        创建工时记录XML元素。
        
        参数:
            task: 任务字典
            
        返回:
            XML元素
        """
        time_spent = task.get("time_spent", 0)
        
        effort_id = str(uuid.uuid4())
        
        creation_dt = task.get("creation_datetime")
        if creation_dt:
            end_time = creation_dt
        else:
            end_time = datetime.now()
        
        start_time = end_time
        if time_spent > 0:
            from datetime import timedelta
            start_time = end_time - timedelta(seconds=time_spent)
        
        elem = ET.Element("effort")
        elem.set("id", effort_id)
        elem.set("status", "1")
        elem.set("start", start_time.strftime("%Y-%m-%d %H:%M:%S"))
        elem.set("stop", end_time.strftime("%Y-%m-%d %H:%M:%S"))
        
        return elem
    
    def _create_category_element(self, category: dict) -> ET.Element:
        """
        创建分类XML元素。
        
        参数:
            category: 分类字典
            
        返回:
            XML元素
        """
        elem = ET.Element("category")
        elem.set("id", category["id"])
        elem.set("status", "1")
        
        if category.get("subject"):
            elem.set("subject", category["subject"])
        
        if category.get("tasks"):
            elem.set("categorizables", " ".join(category["tasks"]))
        
        if category.get("description"):
            desc_elem = ET.SubElement(elem, "description")
            desc_elem.text = category["description"]
        
        for child in category.get("children", []):
            child_elem = self._create_category_element(child)
            elem.append(child_elem)
        
        return elem


def import_chinese_csv(
    categories_csv: Optional[str],
    tasks_csv: str,
    output_tsk: str,
    encoding: str = "utf-8-sig"
) -> dict:
    """
    便捷函数：从中文CSV文件导入数据并生成TSK文件。
    
    参数:
        categories_csv: 分类CSV文件路径（可选）
        tasks_csv: 任务CSV文件路径
        output_tsk: 输出TSK文件路径
        encoding: 文件编码
        
    返回:
        包含导入统计的字典
    """
    importer = ChineseCSVImporter()
    return importer.import_from_files(categories_csv, tasks_csv, output_tsk, encoding)
