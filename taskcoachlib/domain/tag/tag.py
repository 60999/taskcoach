# -*- coding: utf-8 -*-

"""
Task Coach - Your friendly task manager
Copyright (C) 2004-2024 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Tag entity for flexible task categorization.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns


class Tag(base_object.Object):
    """
    标签实体类。
    
    标签提供灵活的任务分类方式，与现有Category系统互补。
    支持多标签、颜色自定义。
    
    Attributes:
        __color: 标签颜色（十六进制格式）
        __organization_id: 所属组织ID
    """
    
    def __init__(self, *args, **kwargs):
        self.__color = kwargs.pop('color', '#3498db')
        self.__organization_id = kwargs.pop('organization_id', '')
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'color': self.__color,
            'organization_id': self.__organization_id,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__color = state.get('color', '#3498db')
        self.__organization_id = state.get('organization_id', '')
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Tag, class_).monitoredAttributes() + ['color']
    
    def color(self):
        """返回标签颜色。"""
        return self.__color
    
    @patterns.eventSource
    def setColor(self, color, event=None):
        """设置标签颜色。"""
        self.__color = color
        event.addSource(self, color, type=self.colorChangedEventType())
    
    def organizationId(self):
        """返回所属组织ID。"""
        return self.__organization_id
    
    def setOrganizationId(self, organization_id):
        """设置所属组织ID。"""
        self.__organization_id = organization_id
    
    @classmethod
    def colorChangedEventType(class_):
        return '%s.color' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Tag, class_).modificationEventTypes() + [
            class_.colorChangedEventType(),
        ]


class TaskTag(base_object.SynchronizedObject):
    """
    任务-标签关联实体类。
    
    记录任务与标签之间的多对多关系。
    
    Attributes:
        __task_id: 任务ID
        __tag_id: 标签ID
        __created_at: 创建时间
    """
    
    def __init__(self, *args, **kwargs):
        self.__task_id = kwargs.pop('task_id', '')
        self.__tag_id = kwargs.pop('tag_id', '')
        self.__created_at = kwargs.pop('created_at', None) or Now()
        self.__id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, TaskTag):
            return NotImplemented
        return self.taskId() == other.taskId() and self.tagId() == other.tagId()
    
    def __hash__(self):
        return hash((self.__task_id, self.__tag_id))
    
    def __repr__(self):
        return f'TaskTag(task_id={self.__task_id}, tag_id={self.__tag_id})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'task_id': self.__task_id,
            'tag_id': self.__tag_id,
            'created_at': self.__created_at,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__task_id = state.get('task_id', '')
        self.__tag_id = state.get('tag_id', '')
        self.__created_at = state.get('created_at', Now())
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def taskId(self):
        """返回任务ID。"""
        return self.__task_id
    
    def setTaskId(self, task_id):
        """设置任务ID。"""
        self.__task_id = task_id
    
    def tagId(self):
        """返回标签ID。"""
        return self.__tag_id
    
    def setTagId(self, tag_id):
        """设置标签ID。"""
        self.__tag_id = tag_id
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
