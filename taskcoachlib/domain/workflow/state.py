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

State entity for workflow.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns
import weakref


class State(base_object.Object):
    """
    工作流状态实体类。
    
    状态代表任务在工作流中的一个阶段，如"新建"、"进行中"、"已完成"。
    
    Attributes:
        __workflow: 所属工作流（弱引用）
        __color: 状态颜色
        __is_initial: 是否为初始状态
        __is_final: 是否为最终状态
    """
    
    def __init__(self, *args, **kwargs):
        workflow = kwargs.pop('workflow', None)
        self.__workflow_ref = weakref.ref(workflow) if workflow else lambda: None
        self.__color = kwargs.pop('color', '#808080')
        self.__is_initial = kwargs.pop('is_initial', False)
        self.__is_final = kwargs.pop('is_final', False)
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'color': self.__color,
            'is_initial': self.__is_initial,
            'is_final': self.__is_final,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__color = state.get('color', '#808080')
        self.__is_initial = state.get('is_initial', False)
        self.__is_final = state.get('is_final', False)
    
    @classmethod
    def monitoredAttributes(class_):
        return super(State, class_).monitoredAttributes() + ['color', 'is_initial', 'is_final']
    
    def workflow(self):
        """返回所属工作流。"""
        return self.__workflow_ref()
    
    def setWorkflow(self, workflow):
        """设置所属工作流。"""
        self.__workflow_ref = weakref.ref(workflow) if workflow else lambda: None
    
    def color(self):
        """返回状态颜色。"""
        return self.__color
    
    @patterns.eventSource
    def setColor(self, color, event=None):
        """设置状态颜色。"""
        self.__color = color
        event.addSource(self, color, type=self.colorChangedEventType())
    
    def isInitial(self):
        """返回是否为初始状态。"""
        return self.__is_initial
    
    @patterns.eventSource
    def setIsInitial(self, is_initial, event=None):
        """设置是否为初始状态。"""
        self.__is_initial = is_initial
        event.addSource(self, is_initial, type=self.initialChangedEventType())
    
    def isFinal(self):
        """返回是否为最终状态。"""
        return self.__is_final
    
    @patterns.eventSource
    def setIsFinal(self, is_final, event=None):
        """设置是否为最终状态。"""
        self.__is_final = is_final
        event.addSource(self, is_final, type=self.finalChangedEventType())
    
    @classmethod
    def colorChangedEventType(class_):
        return '%s.color' % class_
    
    @classmethod
    def initialChangedEventType(class_):
        return '%s.is_initial' % class_
    
    @classmethod
    def finalChangedEventType(class_):
        return '%s.is_final' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(State, class_).modificationEventTypes() + [
            class_.colorChangedEventType(),
            class_.initialChangedEventType(),
            class_.finalChangedEventType(),
        ]
