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

Swimlane entity for kanban view.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns
import weakref


class Swimlane(base_object.Object):
    """
    泳道实体类。
    
    泳道用于在看板中横向分组卡片，例如按优先级、负责人等分组。
    
    Attributes:
        __board: 所属看板（弱引用）
        __position: 泳道位置（从0开始）
    """
    
    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        self.__board_ref = weakref.ref(board) if board else lambda: None
        self.__position = kwargs.pop('position', 0)
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'position': self.__position,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__position = state.get('position', 0)
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Swimlane, class_).monitoredAttributes() + ['position']
    
    def board(self):
        """返回所属看板。"""
        return self.__board_ref()
    
    def setBoard(self, board):
        """设置所属看板。"""
        self.__board_ref = weakref.ref(board) if board else lambda: None
    
    def position(self):
        """返回泳道位置。"""
        return self.__position
    
    @patterns.eventSource
    def setPosition(self, position, event=None):
        """设置泳道位置。"""
        self.__position = position
        event.addSource(self, position, type=self.positionChangedEventType())
    
    @classmethod
    def positionChangedEventType(class_):
        return '%s.position' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Swimlane, class_).modificationEventTypes() + [
            class_.positionChangedEventType(),
        ]
