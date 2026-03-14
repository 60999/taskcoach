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

Workflow entity for task status management.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns


class Workflow(base_object.Object):
    """
    工作流实体类。
    
    工作流定义任务状态流转的规则，包含状态列表和状态转换列表。
    
    Attributes:
        __states: 状态列表
        __transitions: 转换列表
        __initial_state_id: 初始状态ID
        __organization_id: 所属组织ID
    """
    
    def __init__(self, *args, **kwargs):
        self.__states = kwargs.pop('states', [])
        self.__transitions = kwargs.pop('transitions', [])
        self.__initial_state_id = kwargs.pop('initial_state_id', None)
        self.__organization_id = kwargs.pop('organization_id', '')
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'states': [s.__getstate__() for s in self.__states],
            'transitions': [t.__getstate__() for t in self.__transitions],
            'initial_state_id': self.__initial_state_id,
            'organization_id': self.__organization_id,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__states = []
        self.__transitions = []
        self.__initial_state_id = state.get('initial_state_id')
        self.__organization_id = state.get('organization_id', '')
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Workflow, class_).monitoredAttributes() + ['states', 'transitions']
    
    def states(self):
        """返回状态列表。"""
        return list(self.__states)
    
    @patterns.eventSource
    def addState(self, state, event=None):
        """添加状态。"""
        self.__states.append(state)
        event.addSource(self, state, type=self.statesChangedEventType())
    
    @patterns.eventSource
    def removeState(self, state, event=None):
        """移除状态。"""
        if state in self.__states:
            self.__states.remove(state)
            event.addSource(self, state, type=self.statesChangedEventType())
    
    @patterns.eventSource
    def setStates(self, states, event=None):
        """设置状态列表。"""
        self.__states = list(states)
        event.addSource(self, type=self.statesChangedEventType())
    
    def transitions(self):
        """返回转换列表。"""
        return list(self.__transitions)
    
    @patterns.eventSource
    def addTransition(self, transition, event=None):
        """添加转换。"""
        self.__transitions.append(transition)
        event.addSource(self, transition, type=self.transitionsChangedEventType())
    
    @patterns.eventSource
    def removeTransition(self, transition, event=None):
        """移除转换。"""
        if transition in self.__transitions:
            self.__transitions.remove(transition)
            event.addSource(self, transition, type=self.transitionsChangedEventType())
    
    @patterns.eventSource
    def setTransitions(self, transitions, event=None):
        """设置转换列表。"""
        self.__transitions = list(transitions)
        event.addSource(self, type=self.transitionsChangedEventType())
    
    def initialStateId(self):
        """返回初始状态ID。"""
        return self.__initial_state_id
    
    def initialState(self):
        """返回初始状态对象。"""
        for state in self.__states:
            if state.id() == self.__initial_state_id:
                return state
        return None
    
    @patterns.eventSource
    def setInitialStateId(self, state_id, event=None):
        """设置初始状态ID。"""
        self.__initial_state_id = state_id
        event.addSource(self, state_id, type=self.initialStateChangedEventType())
    
    def organizationId(self):
        """返回所属组织ID。"""
        return self.__organization_id
    
    def setOrganizationId(self, organization_id):
        """设置所属组织ID。"""
        self.__organization_id = organization_id
    
    def getStateById(self, state_id):
        """根据ID获取状态。"""
        for state in self.__states:
            if state.id() == state_id:
                return state
        return None
    
    def getTransitionsFromState(self, state_id):
        """获取从指定状态出发的所有转换。"""
        return [t for t in self.__transitions if t.fromStateId() == state_id]
    
    def getTransitionsToState(self, state_id):
        """获取到达指定状态的所有转换。"""
        return [t for t in self.__transitions if t.toStateId() == state_id]
    
    def canTransition(self, from_state_id, to_state_id):
        """检查是否可以从一个状态转换到另一个状态。"""
        for transition in self.__transitions:
            if transition.fromStateId() == from_state_id and transition.toStateId() == to_state_id:
                return True
        return False
    
    @classmethod
    def statesChangedEventType(class_):
        return '%s.states' % class_
    
    @classmethod
    def transitionsChangedEventType(class_):
        return '%s.transitions' % class_
    
    @classmethod
    def initialStateChangedEventType(class_):
        return '%s.initial_state' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Workflow, class_).modificationEventTypes() + [
            class_.statesChangedEventType(),
            class_.transitionsChangedEventType(),
            class_.initialStateChangedEventType(),
        ]
