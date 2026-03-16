# -*- coding: utf-8 -*-
"""
TSK 文件读取器模块
用于读取旧版 TaskCoach 1.4.6 的 .tsk XML 文件，解析任务、分类和笔记数据。

文件功能:
- 解析 XML 格式的 .tsk 文件
- 提取任务、分类、笔记等数据
- 处理任务层次结构和依赖关系
"""

import xml.etree.ElementTree as ET
import re
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class TaskData:
    """
    任务数据类，用于存储解析后的任务信息。
    
    属性:
        id: 任务唯一标识符
        subject: 任务主题/标题
        description: 任务描述
        planned_start_date: 计划开始日期
        due_date: 截止日期
        actual_start_date: 实际开始日期
        completion_date: 完成日期
        priority: 优先级
        percentage_complete: 完成百分比
        budget: 预算时间（秒）
        hourly_fee: 时薪
        fixed_fee: 固定费用
        reminder: 提醒时间
        categories: 所属分类ID列表
        prerequisites: 前置任务ID列表
        parent_id: 父任务ID
        children: 子任务列表
        notes: 备注列表
        efforts: 工时记录列表
        attachments: 附件列表
        creation_datetime: 创建时间
        modification_datetime: 修改时间
        status: 状态标志
    """
    id: str = ""
    subject: str = ""
    description: str = ""
    planned_start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    priority: int = 0
    percentage_complete: int = 0
    budget: int = 0
    hourly_fee: float = 0.0
    fixed_fee: float = 0.0
    reminder: Optional[datetime] = None
    categories: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    parent_id: str = ""
    children: List['TaskData'] = field(default_factory=list)
    notes: List['NoteData'] = field(default_factory=list)
    efforts: List['EffortData'] = field(default_factory=list)
    attachments: List['AttachmentData'] = field(default_factory=list)
    creation_datetime: Optional[datetime] = None
    modification_datetime: Optional[datetime] = None
    status: int = 1
    fg_color: Optional[Tuple[int, int, int, int]] = None
    bg_color: Optional[Tuple[int, int, int, int]] = None
    icon: str = ""
    selected_icon: str = ""


@dataclass
class CategoryData:
    """
    分类数据类，用于存储解析后的分类信息。
    
    属性:
        id: 分类唯一标识符
        subject: 分类名称
        description: 分类描述
        color: 分类颜色
        icon: 分类图标
        categorizables: 关联的可分类对象ID列表
        children: 子分类列表
        notes: 备注列表
    """
    id: str = ""
    subject: str = ""
    description: str = ""
    color: Optional[Tuple[int, int, int, int]] = None
    icon: str = ""
    selected_icon: str = ""
    categorizables: List[str] = field(default_factory=list)
    children: List['CategoryData'] = field(default_factory=list)
    notes: List['NoteData'] = field(default_factory=list)
    filtered: bool = False
    exclusive_subcategories: bool = False


@dataclass
class NoteData:
    """
    笔记数据类，用于存储解析后的笔记信息。
    
    属性:
        id: 笔记唯一标识符
        subject: 笔记主题
        description: 笔记内容
        children: 子笔记列表
    """
    id: str = ""
    subject: str = ""
    description: str = ""
    children: List['NoteData'] = field(default_factory=list)


@dataclass
class EffortData:
    """
    工时记录数据类。
    
    属性:
        id: 工时记录唯一标识符
        start: 开始时间
        stop: 结束时间
        description: 描述
    """
    id: str = ""
    start: Optional[datetime] = None
    stop: Optional[datetime] = None
    description: str = ""


@dataclass
class AttachmentData:
    """
    附件数据类。
    
    属性:
        id: 附件唯一标识符
        subject: 附件名称
        location: 附件位置/路径
        type: 附件类型
        description: 描述
    """
    id: str = ""
    subject: str = ""
    location: str = ""
    type: str = ""
    description: str = ""


class TSKReader:
    """
    TSK 文件读取器类。
    
    用于读取和解析旧版 TaskCoach 的 .tsk XML 文件。
    支持解析 tskversion 30 及以下版本的文件。
    
    使用示例:
        reader = TSKReader()
        tasks, categories, notes = reader.read("path/to/file.tsk")
    """
    
    def __init__(self):
        """初始化读取器。"""
        self.tsk_version: int = 0
        self.release_version: str = ""
        self._prerequisites_map: Dict[str, List[str]] = {}
        self._categorizables_map: Dict[str, List[str]] = {}
        
    def read(self, filepath: str) -> Tuple[List[TaskData], List[CategoryData], List[NoteData]]:
        """
        读取并解析 TSK 文件。
        
        参数:
            filepath: TSK 文件路径
            
        返回:
            包含任务列表、分类列表和独立笔记列表的元组
            
        异常:
            FileNotFoundError: 文件不存在
            ET.ParseError: XML 解析错误
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        self._parse_header(root)
        
        tasks = self._parse_tasks(root)
        self._resolve_prerequisites(tasks)
        
        categories = self._parse_categories(root)
        self._resolve_categories(categories, tasks)
        
        notes = self._parse_standalone_notes(root)
        
        return tasks, categories, notes
    
    def _parse_header(self, root: ET.Element) -> None:
        """
        解析文件头部信息，提取版本号。
        
        参数:
            root: XML 根元素
        """
        header = root.attrib.get("{http://www.w3.org/2001/XInclude}href", "")
        
        for child in root:
            if child.tag == ET.ProcessingInstruction and child.target == "taskcoach":
                match = re.search(r'tskversion="(\d+)"', child.text or "")
                if match:
                    self.tsk_version = int(match.group(1))
                match = re.search(r'release="([^"]+)"', child.text or "")
                if match:
                    self.release_version = match.group(1)
                break
        
        if self.tsk_version == 0:
            self.tsk_version = 30
    
    def _parse_tasks(self, node: ET.Element) -> List[TaskData]:
        """
        递归解析任务节点。
        
        参数:
            node: XML 节点
            
        返回:
            任务数据列表
        """
        tasks = []
        for task_node in node.findall("task"):
            task = self._parse_task_node(task_node)
            tasks.append(task)
        return tasks
    
    def _parse_task_node(self, node: ET.Element) -> TaskData:
        """
        解析单个任务节点。
        
        参数:
            node: 任务 XML 节点
            
        返回:
            TaskData 对象
        """
        task = TaskData()
        
        task.id = node.attrib.get("id", "")
        task.subject = node.attrib.get("subject", "")
        task.status = int(node.attrib.get("status", "1"))
        
        start_attr = "startdate" if self.tsk_version <= 33 else "plannedstartdate"
        task.planned_start_date = self._parse_datetime(node.attrib.get(start_attr, ""))
        task.due_date = self._parse_datetime(node.attrib.get("duedate", ""))
        task.actual_start_date = self._parse_datetime(node.attrib.get("actualstartdate", ""))
        task.completion_date = self._parse_datetime(node.attrib.get("completiondate", ""))
        
        task.priority = int(node.attrib.get("priority", "0"))
        task.percentage_complete = int(node.attrib.get("percentageComplete", "0"))
        
        budget_str = node.attrib.get("budget", "")
        if budget_str:
            task.budget = self._parse_timedelta(budget_str)
        
        task.hourly_fee = float(node.attrib.get("hourlyFee", "0"))
        task.fixed_fee = float(node.attrib.get("fixedFee", "0"))
        
        task.reminder = self._parse_datetime(node.attrib.get("reminder", ""))
        
        task.creation_datetime = self._parse_datetime(
            node.attrib.get("creationDateTime", "1-1-1 0:0")
        )
        task.modification_datetime = self._parse_datetime(
            node.attrib.get("modificationDateTime", "1-1-1 0:0")
        )
        
        task.fg_color = self._parse_color(node.attrib.get("fgColor", ""))
        bg_attr = "color" if self.tsk_version <= 27 else "bgColor"
        task.bg_color = self._parse_color(node.attrib.get(bg_attr, ""))
        
        task.icon = node.attrib.get("icon", "")
        task.selected_icon = node.attrib.get("selectedIcon", "")
        
        prereq_str = node.attrib.get("prerequisites", "")
        if prereq_str:
            self._prerequisites_map[task.id] = [
                p for p in prereq_str.split(" ") if p
            ]
        
        desc_node = node.find("description")
        if desc_node is not None and desc_node.text:
            task.description = desc_node.text.strip()
        
        task.children = self._parse_tasks(node)
        task.notes = self._parse_notes(node)
        task.efforts = self._parse_efforts(node)
        task.attachments = self._parse_attachments(node)
        
        return task
    
    def _parse_categories(self, root: ET.Element) -> List[CategoryData]:
        """
        解析分类节点。
        
        参数:
            root: XML 根元素
            
        返回:
            分类数据列表
        """
        categories = []
        for cat_node in root.findall("category"):
            category = self._parse_category_node(cat_node)
            categories.append(category)
        return categories
    
    def _parse_category_node(self, node: ET.Element) -> CategoryData:
        """
        解析单个分类节点。
        
        参数:
            node: 分类 XML 节点
            
        返回:
            CategoryData 对象
        """
        category = CategoryData()
        
        category.id = node.attrib.get("id", "")
        category.subject = node.attrib.get("subject", "")
        category.status = int(node.attrib.get("status", "1"))
        
        category.color = self._parse_color(node.attrib.get("bgColor", ""))
        category.icon = node.attrib.get("icon", "")
        category.selected_icon = node.attrib.get("selectedIcon", "")
        
        category.filtered = node.attrib.get("filtered", "False").lower() == "true"
        category.exclusive_subcategories = node.attrib.get(
            "exclusiveSubcategories", "False"
        ).lower() == "true"
        
        categorizables_attr = "categorizables" if self.tsk_version >= 19 else "tasks"
        categorizables_str = node.attrib.get(categorizables_attr, "")
        if categorizables_str:
            self._categorizables_map[category.id] = categorizables_str.split(" ")
        
        desc_node = node.find("description")
        if desc_node is not None and desc_node.text:
            category.description = desc_node.text.strip()
        
        category.children = [
            self._parse_category_node(child) 
            for child in node.findall("category")
        ]
        category.notes = self._parse_notes(node)
        
        return category
    
    def _parse_notes(self, node: ET.Element) -> List[NoteData]:
        """
        解析笔记节点。
        
        参数:
            node: XML 节点
            
        返回:
            笔记数据列表
        """
        notes = []
        for note_node in node.findall("note"):
            note = self._parse_note_node(note_node)
            notes.append(note)
        return notes
    
    def _parse_note_node(self, node: ET.Element) -> NoteData:
        """
        解析单个笔记节点。
        
        参数:
            node: 笔记 XML 节点
            
        返回:
            NoteData 对象
        """
        note = NoteData()
        
        note.id = node.attrib.get("id", "")
        note.subject = node.attrib.get("subject", "")
        
        desc_node = node.find("description")
        if desc_node is not None and desc_node.text:
            note.description = desc_node.text.strip()
        
        note.children = [
            self._parse_note_node(child) 
            for child in node.findall("note")
        ]
        
        return note
    
    def _parse_efforts(self, node: ET.Element) -> List[EffortData]:
        """
        解析工时记录节点。
        
        参数:
            node: XML 节点
            
        返回:
            工时记录数据列表
        """
        efforts = []
        for effort_node in node.findall("effort"):
            effort = EffortData()
            effort.id = effort_node.attrib.get("id", "")
            effort.start = self._parse_datetime(effort_node.attrib.get("start", ""))
            effort.stop = self._parse_datetime(effort_node.attrib.get("stop", ""))
            
            desc_node = effort_node.find("description")
            if desc_node is not None and desc_node.text:
                effort.description = desc_node.text.strip()
            
            efforts.append(effort)
        return efforts
    
    def _parse_attachments(self, node: ET.Element) -> List[AttachmentData]:
        """
        解析附件节点。
        
        参数:
            node: XML 节点
            
        返回:
            附件数据列表
        """
        attachments = []
        for att_node in node.findall("attachment"):
            att = AttachmentData()
            att.id = att_node.attrib.get("id", "")
            att.subject = att_node.attrib.get("subject", "")
            att.location = att_node.attrib.get("location", "")
            att.type = att_node.attrib.get("type", "")
            
            desc_node = att_node.find("description")
            if desc_node is not None and desc_node.text:
                att.description = desc_node.text.strip()
            
            attachments.append(att)
        return attachments
    
    def _parse_standalone_notes(self, root: ET.Element) -> List[NoteData]:
        """
        解析独立的笔记节点（不属于任务或分类的笔记）。
        
        参数:
            root: XML 根元素
            
        返回:
            独立笔记数据列表
        """
        notes = []
        for note_node in root.findall("note"):
            note = self._parse_note_node(note_node)
            notes.append(note)
        return notes
    
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
    
    def _parse_timedelta(self, timedelta_str: str) -> int:
        """
        解析时间增量字符串，返回秒数。
        
        参数:
            timedelta_str: 时间增量字符串
            
        返回:
            秒数
        """
        if not timedelta_str:
            return 0
        
        match = re.match(r"(\d+):(\d+):(\d+)", timedelta_str)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            return hours * 3600 + minutes * 60 + seconds
        
        return 0
    
    def _parse_color(self, color_str: str) -> Optional[Tuple[int, int, int, int]]:
        """
        解析颜色字符串。
        
        参数:
            color_str: 颜色字符串，格式如 "(255, 255, 255, 255)"
            
        返回:
            RGBA 元组或 None
        """
        if not color_str:
            return None
        
        match = re.match(r"\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)", color_str)
        if match:
            return (
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
            )
        return None
    
    def _resolve_prerequisites(self, tasks: List[TaskData]) -> None:
        """
        解析任务的前置任务依赖关系。
        
        参数:
            tasks: 任务列表
        """
        tasks_by_id: Dict[str, TaskData] = {}
        
        def collect_tasks(task_list: List[TaskData]) -> None:
            for task in task_list:
                tasks_by_id[task.id] = task
                collect_tasks(task.children)
        
        collect_tasks(tasks)
        
        for task_id, prereq_ids in self._prerequisites_map.items():
            if task_id in tasks_by_id:
                tasks_by_id[task_id].prerequisites = [
                    pid for pid in prereq_ids if pid in tasks_by_id
                ]
    
    def _resolve_categories(
        self, 
        categories: List[CategoryData], 
        tasks: List[TaskData]
    ) -> None:
        """
        解析任务与分类的关联关系。
        
        参数:
            categories: 分类列表
            tasks: 任务列表
        """
        tasks_by_id: Dict[str, TaskData] = {}
        
        def collect_tasks(task_list: List[TaskData]) -> None:
            for task in task_list:
                tasks_by_id[task.id] = task
                collect_tasks(task.children)
        
        collect_tasks(tasks)
        
        for cat_id, categorizable_ids in self._categorizables_map.items():
            for obj_id in categorizable_ids:
                if obj_id in tasks_by_id:
                    tasks_by_id[obj_id].categories.append(cat_id)


def flatten_tasks(tasks: List[TaskData]) -> List[TaskData]:
    """
    将嵌套的任务列表扁平化。
    
    参数:
        tasks: 嵌套的任务列表
        
    返回:
        扁平化的任务列表
    """
    result = []
    for task in tasks:
        result.append(task)
        result.extend(flatten_tasks(task.children))
    return result


def flatten_categories(categories: List[CategoryData]) -> List[CategoryData]:
    """
    将嵌套的分类列表扁平化。
    
    参数:
        categories: 嵌套的分类列表
        
    返回:
        扁平化的分类列表
    """
    result = []
    for category in categories:
        result.append(category)
        result.extend(flatten_categories(category.children))
    return result
