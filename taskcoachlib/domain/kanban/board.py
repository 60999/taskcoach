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

Board entity for kanban view.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.base import attribute as attr_module
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import uuid


class Board(base_object.Object):
    """
    看板实体类。
    
    看板是任务管理的可视化视图，包含多个列和可选的泳道。
    
    Attributes:
        __columns: 看板列列表
        __swimlanes: 泳道列表
        __owner_id: 所有者用户ID
        __organization_id: 所属组织ID
    """
    
    def __init__(self, *args, **kwargs):
        self.__columns = kwargs.pop('columns', [])
        self.__swimlanes = kwargs.pop('swimlanes', [])
        self.__owner_id = kwargs.pop('owner_id', '')
        self.__organization_id = kwargs.pop('organization_id', '')
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'columns': [col.__getstate__() for col in self.__columns],
            'swimlanes': [sl.__getstate__() for sl in self.__swimlanes],
            'owner_id': self.__owner_id,
            'organization_id': self.__organization_id,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__owner_id = state.get('owner_id', '')
        self.__organization_id = state.get('organization_id', '')
        self.__columns = []
        self.__swimlanes = []
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Board, class_).monitoredAttributes() + ['columns', 'swimlanes']
    
    def columns(self):
        """返回看板列列表。"""
        return list(self.__columns)
    
    @patterns.eventSource
    def addColumn(self, column, event=None):
        """添加看板列。"""
        self.__columns.append(column)
        event.addSource(self, column, type=self.columnsChangedEventType())
    
    @patterns.eventSource
    def removeColumn(self, column, event=None):
        """移除看板列。"""
        if column in self.__columns:
            self.__columns.remove(column)
            event.addSource(self, column, type=self.columnsChangedEventType())
    
    @patterns.eventSource
    def setColumns(self, columns, event=None):
        """设置看板列列表。"""
        self.__columns = list(columns)
        event.addSource(self, type=self.columnsChangedEventType())
    
    def swimlanes(self):
        """返回泳道列表。"""
        return list(self.__swimlanes)
    
    @patterns.eventSource
    def addSwimlane(self, swimlane, event=None):
        """添加泳道。"""
        self.__swimlanes.append(swimlane)
        event.addSource(self, swimlane, type=self.swimlanesChangedEventType())
    
    @patterns.eventSource
    def removeSwimlane(self, swimlane, event=None):
        """移除泳道。"""
        if swimlane in self.__swimlanes:
            self.__swimlanes.remove(swimlane)
            event.addSource(self, swimlane, type=self.swimlanesChangedEventType())
    
    @patterns.eventSource
    def setSwimlanes(self, swimlanes, event=None):
        """设置泳道列表。"""
        self.__swimlanes = list(swimlanes)
        event.addSource(self, type=self.swimlanesChangedEventType())
    
    def ownerId(self):
        """返回所有者ID。"""
        return self.__owner_id
    
    def setOwnerId(self, owner_id):
        """设置所有者ID。"""
        self.__owner_id = owner_id
    
    def organizationId(self):
        """返回所属组织ID。"""
        return self.__organization_id
    
    def setOrganizationId(self, organization_id):
        """设置所属组织ID。"""
        self.__organization_id = organization_id
    
    def getColumnById(self, column_id):
        """根据ID获取看板列。"""
        for column in self.__columns:
            if column.id() == column_id:
                return column
        return None
    
    def getSwimlaneById(self, swimlane_id):
        """根据ID获取泳道。"""
        for swimlane in self.__swimlanes:
            if swimlane.id() == swimlane_id:
                return swimlane
        return None
    
    @classmethod
    def columnsChangedEventType(class_):
        return '%s.columns' % class_
    
    @classmethod
    def swimlanesChangedEventType(class_):
        return '%s.swimlanes' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Board, class_).modificationEventTypes() + [
            class_.columnsChangedEventType(),
            class_.swimlanesChangedEventType(),
        ]
