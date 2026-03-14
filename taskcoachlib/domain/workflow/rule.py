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

TransitionRule entity for workflow.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns
import weakref


class TransitionRule(base_object.SynchronizedObject):
    """
    转换规则实体类。
    
    规则定义状态转换的条件和动作。
    
    Attributes:
        __transition: 所属转换（弱引用）
        __rule_type: 规则类型 ('condition', 'action', 'validator')
        __condition: 规则条件表达式
        __action: 规则动作
    """
    
    TYPE_CONDITION = 'condition'
    TYPE_ACTION = 'action'
    TYPE_VALIDATOR = 'validator'
    
    def __init__(self, *args, **kwargs):
        transition = kwargs.pop('transition', None)
        self.__transition_ref = weakref.ref(transition) if transition else lambda: None
        self.__rule_type = kwargs.pop('rule_type', self.TYPE_CONDITION)
        self.__condition = kwargs.pop('condition', '')
        self.__action = kwargs.pop('action', '')
        self.__id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, TransitionRule):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'TransitionRule(type={self.__rule_type}, condition={self.__condition})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'rule_type': self.__rule_type,
            'condition': self.__condition,
            'action': self.__action,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__rule_type = state.get('rule_type', self.TYPE_CONDITION)
        self.__condition = state.get('condition', '')
        self.__action = state.get('action', '')
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def transition(self):
        """返回所属转换。"""
        return self.__transition_ref()
    
    def setTransition(self, transition):
        """设置所属转换。"""
        self.__transition_ref = weakref.ref(transition) if transition else lambda: None
    
    def ruleType(self):
        """返回规则类型。"""
        return self.__rule_type
    
    @patterns.eventSource
    def setRuleType(self, rule_type, event=None):
        """设置规则类型。"""
        self.__rule_type = rule_type
        event.addSource(self, rule_type, type=self.ruleTypeChangedEventType())
    
    def condition(self):
        """返回规则条件。"""
        return self.__condition
    
    @patterns.eventSource
    def setCondition(self, condition, event=None):
        """设置规则条件。"""
        self.__condition = condition
        event.addSource(self, condition, type=self.conditionChangedEventType())
    
    def action(self):
        """返回规则动作。"""
        return self.__action
    
    @patterns.eventSource
    def setAction(self, action, event=None):
        """设置规则动作。"""
        self.__action = action
        event.addSource(self, action, type=self.actionChangedEventType())
    
    def isCondition(self):
        """检查是否为条件规则。"""
        return self.__rule_type == self.TYPE_CONDITION
    
    def isAction(self):
        """检查是否为动作规则。"""
        return self.__rule_type == self.TYPE_ACTION
    
    def isValidator(self):
        """检查是否为验证规则。"""
        return self.__rule_type == self.TYPE_VALIDATOR
    
    @classmethod
    def ruleTypeChangedEventType(class_):
        return '%s.rule_type' % class_
    
    @classmethod
    def conditionChangedEventType(class_):
        return '%s.condition' % class_
    
    @classmethod
    def actionChangedEventType(class_):
        return '%s.action' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return [
            class_.ruleTypeChangedEventType(),
            class_.conditionChangedEventType(),
            class_.actionChangedEventType(),
        ]
