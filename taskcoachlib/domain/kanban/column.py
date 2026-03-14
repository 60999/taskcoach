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

BoardColumn entity for kanban view.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.base import attribute as attr_module
from taskcoachlib import patterns
import weakref


class BoardColumn(base_object.Object):
    """
    看板列实体类。
    
    看板列代表任务的一个状态或阶段，如"待办"、"进行中"、"已完成"。
    
    Attributes:
        __board: 所属看板（弱引用）
        __position: 列位置（从0开始）
        __wip_limit: WIP（在制品）限制
        __color: 列颜色
        __task_status: 关联的任务状态
    """
    
    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        self.__board_ref = weakref.ref(board) if board else lambda: None
        self.__position = kwargs.pop('position', 0)
        self.__wip_limit = kwargs.pop('wip_limit', None)
        self.__color = kwargs.pop('color', '#E8E8E8')
        self.__task_status = kwargs.pop('task_status', None)
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'position': self.__position,
            'wip_limit': self.__wip_limit,
            'color': self.__color,
            'task_status': self.__task_status,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__position = state.get('position', 0)
        self.__wip_limit = state.get('wip_limit')
        self.__color = state.get('color', '#E8E8E8')
        self.__task_status = state.get('task_status')
    
    @classmethod
    def monitoredAttributes(class_):
        return super(BoardColumn, class_).monitoredAttributes() + ['position', 'wip_limit', 'color']
    
    def board(self):
        """返回所属看板。"""
        return self.__board_ref()
    
    def setBoard(self, board):
        """设置所属看板。"""
        self.__board_ref = weakref.ref(board) if board else lambda: None
    
    def position(self):
        """返回列位置。"""
        return self.__position
    
    @patterns.eventSource
    def setPosition(self, position, event=None):
        """设置列位置。"""
        self.__position = position
        event.addSource(self, position, type=self.positionChangedEventType())
    
    def wipLimit(self):
        """返回WIP限制。"""
        return self.__wip_limit
    
    @patterns.eventSource
    def setWipLimit(self, wip_limit, event=None):
        """设置WIP限制。"""
        self.__wip_limit = wip_limit
        event.addSource(self, wip_limit, type=self.wipLimitChangedEventType())
    
    def color(self):
        """返回列颜色。"""
        return self.__color
    
    @patterns.eventSource
    def setColor(self, color, event=None):
        """设置列颜色。"""
        self.__color = color
        event.addSource(self, color, type=self.colorChangedEventType())
    
    def taskStatus(self):
        """返回关联的任务状态。"""
        return self.__task_status
    
    @patterns.eventSource
    def setTaskStatus(self, task_status, event=None):
        """设置关联的任务状态。"""
        self.__task_status = task_status
    
    def hasWipLimit(self):
        """检查是否设置了WIP限制。"""
        return self.__wip_limit is not None and self.__wip_limit > 0
    
    @classmethod
    def positionChangedEventType(class_):
        return '%s.position' % class_
    
    @classmethod
    def wipLimitChangedEventType(class_):
        return '%s.wip_limit' % class_
    
    @classmethod
    def colorChangedEventType(class_):
        return '%s.color' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(BoardColumn, class_).modificationEventTypes() + [
            class_.positionChangedEventType(),
            class_.wipLimitChangedEventType(),
            class_.colorChangedEventType(),
        ]
