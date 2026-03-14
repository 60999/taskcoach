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

CardPosition entity for kanban view.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns
import weakref


class CardPosition(base_object.SynchronizedObject):
    """
    卡片位置实体类。
    
    记录任务在看板中的位置信息，包括所在列、位置索引和泳道。
    
    Attributes:
        __task: 关联的任务（弱引用）
        __column: 所在列（弱引用）
        __position: 卡片位置索引
        __swimlane: 所在泳道（弱引用，可选）
    """
    
    def __init__(self, *args, **kwargs):
        task = kwargs.pop('task', None)
        column = kwargs.pop('column', None)
        swimlane = kwargs.pop('swimlane', None)
        self.__task_ref = weakref.ref(task) if task else lambda: None
        self.__column_ref = weakref.ref(column) if column else lambda: None
        self.__swimlane_ref = weakref.ref(swimlane) if swimlane else lambda: None
        self.__position = kwargs.pop('position', 0)
        self.__id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, CardPosition):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        task = self.task()
        column = self.column()
        return f'CardPosition(task={task.id() if task else None}, column={column.id() if column else None}, position={self.__position})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'position': self.__position,
            'task_id': self.taskId(),
            'column_id': self.columnId(),
            'swimlane_id': self.swimlaneId(),
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__position = state.get('position', 0)
        self.__task_ref = lambda: None
        self.__column_ref = lambda: None
        self.__swimlane_ref = lambda: None
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def taskId(self):
        """返回任务ID。"""
        task = self.task()
        return task.id() if task else None
    
    def columnId(self):
        """返回列ID。"""
        column = self.column()
        return column.id() if column else None
    
    def swimlaneId(self):
        """返回泳道ID。"""
        swimlane = self.swimlane()
        return swimlane.id() if swimlane else None
    
    def task(self):
        """返回关联的任务。"""
        return self.__task_ref()
    
    def setTask(self, task):
        """设置关联的任务。"""
        self.__task_ref = weakref.ref(task) if task else lambda: None
    
    def column(self):
        """返回所在列。"""
        return self.__column_ref()
    
    @patterns.eventSource
    def setColumn(self, column, event=None):
        """设置所在列。"""
        self.__column_ref = weakref.ref(column) if column else lambda: None
        event.addSource(self, column, type=self.columnChangedEventType())
    
    def position(self):
        """返回卡片位置索引。"""
        return self.__position
    
    @patterns.eventSource
    def setPosition(self, position, event=None):
        """设置卡片位置索引。"""
        self.__position = position
        event.addSource(self, position, type=self.positionChangedEventType())
    
    def swimlane(self):
        """返回所在泳道。"""
        return self.__swimlane_ref()
    
    @patterns.eventSource
    def setSwimlane(self, swimlane, event=None):
        """设置所在泳道。"""
        self.__swimlane_ref = weakref.ref(swimlane) if swimlane else lambda: None
        event.addSource(self, swimlane, type=self.swimlaneChangedEventType())
    
    @classmethod
    def columnChangedEventType(class_):
        return '%s.column' % class_
    
    @classmethod
    def positionChangedEventType(class_):
        return '%s.position' % class_
    
    @classmethod
    def swimlaneChangedEventType(class_):
        return '%s.swimlane' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return [
            class_.columnChangedEventType(),
            class_.positionChangedEventType(),
            class_.swimlaneChangedEventType(),
        ]
