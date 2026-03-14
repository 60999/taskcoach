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

Transition entity for workflow.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns
import weakref


class Transition(base_object.Object):
    """
    状态转换实体类。
    
    转换定义从一个状态到另一个状态的流转规则。
    
    Attributes:
        __workflow: 所属工作流（弱引用）
        __from_state_id: 源状态ID
        __to_state_id: 目标状态ID
        __rules: 转换规则列表
    """
    
    def __init__(self, *args, **kwargs):
        workflow = kwargs.pop('workflow', None)
        self.__workflow_ref = weakref.ref(workflow) if workflow else lambda: None
        self.__from_state_id = kwargs.pop('from_state_id', '')
        self.__to_state_id = kwargs.pop('to_state_id', '')
        self.__rules = kwargs.pop('rules', [])
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'from_state_id': self.__from_state_id,
            'to_state_id': self.__to_state_id,
            'rules': [r.__getstate__() for r in self.__rules],
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__from_state_id = state.get('from_state_id', '')
        self.__to_state_id = state.get('to_state_id', '')
        self.__rules = []
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Transition, class_).monitoredAttributes() + ['from_state_id', 'to_state_id', 'rules']
    
    def workflow(self):
        """返回所属工作流。"""
        return self.__workflow_ref()
    
    def setWorkflow(self, workflow):
        """设置所属工作流。"""
        self.__workflow_ref = weakref.ref(workflow) if workflow else lambda: None
    
    def fromStateId(self):
        """返回源状态ID。"""
        return self.__from_state_id
    
    @patterns.eventSource
    def setFromStateId(self, state_id, event=None):
        """设置源状态ID。"""
        self.__from_state_id = state_id
        event.addSource(self, state_id, type=self.fromStateChangedEventType())
    
    def toStateId(self):
        """返回目标状态ID。"""
        return self.__to_state_id
    
    @patterns.eventSource
    def setToStateId(self, state_id, event=None):
        """设置目标状态ID。"""
        self.__to_state_id = state_id
        event.addSource(self, state_id, type=self.toStateChangedEventType())
    
    def rules(self):
        """返回转换规则列表。"""
        return list(self.__rules)
    
    @patterns.eventSource
    def addRule(self, rule, event=None):
        """添加转换规则。"""
        self.__rules.append(rule)
        event.addSource(self, rule, type=self.rulesChangedEventType())
    
    @patterns.eventSource
    def removeRule(self, rule, event=None):
        """移除转换规则。"""
        if rule in self.__rules:
            self.__rules.remove(rule)
            event.addSource(self, rule, type=self.rulesChangedEventType())
    
    @classmethod
    def fromStateChangedEventType(class_):
        return '%s.from_state' % class_
    
    @classmethod
    def toStateChangedEventType(class_):
        return '%s.to_state' % class_
    
    @classmethod
    def rulesChangedEventType(class_):
        return '%s.rules' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Transition, class_).modificationEventTypes() + [
            class_.fromStateChangedEventType(),
            class_.toStateChangedEventType(),
            class_.rulesChangedEventType(),
        ]
