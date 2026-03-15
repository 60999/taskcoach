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

Permission entity for team collaboration.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns


class Permission(base_object.Object):
    """
    权限实体类。
    
    权限定义对特定资源的操作许可。
    
    Attributes:
        __resource: 资源类型
        __action: 操作类型
        __description: 权限描述
    """
    
    RESOURCE_TASK = 'task'
    RESOURCE_BOARD = 'board'
    RESOURCE_USER = 'user'
    RESOURCE_ORGANIZATION = 'organization'
    RESOURCE_COMMENT = 'comment'
    RESOURCE_WORKFLOW = 'workflow'
    
    ACTION_CREATE = 'create'
    ACTION_READ = 'read'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_ASSIGN = 'assign'
    ACTION_MANAGE = 'manage'
    
    def __init__(self, *args, **kwargs):
        self.__resource = kwargs.pop('resource', '')
        self.__action = kwargs.pop('action', '')
        self.__description = kwargs.pop('description', '')
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'resource': self.__resource,
            'action': self.__action,
            'description': self.__description,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__resource = state.get('resource', '')
        self.__action = state.get('action', '')
        self.__description = state.get('description', '')
    
    def resource(self):
        """返回资源类型。"""
        return self.__resource
    
    def setResource(self, resource):
        """设置资源类型。"""
        self.__resource = resource
    
    def action(self):
        """返回操作类型。"""
        return self.__action
    
    def setAction(self, action):
        """设置操作类型。"""
        self.__action = action
    
    def description(self):
        """返回权限描述。"""
        return self.__description
    
    def setDescription(self, description):
        """设置权限描述。"""
        self.__description = description
    
    def matches(self, resource, action):
        """检查是否匹配指定的资源和操作。"""
        return self.__resource == resource and self.__action == action
    
    @classmethod
    def create_task_permissions(cls):
        """创建任务相关权限。"""
        return [
            cls(subject='task_create', resource=cls.RESOURCE_TASK, action=cls.ACTION_CREATE, description='创建任务'),
            cls(subject='task_read', resource=cls.RESOURCE_TASK, action=cls.ACTION_READ, description='查看任务'),
            cls(subject='task_update', resource=cls.RESOURCE_TASK, action=cls.ACTION_UPDATE, description='更新任务'),
            cls(subject='task_delete', resource=cls.RESOURCE_TASK, action=cls.ACTION_DELETE, description='删除任务'),
            cls(subject='task_assign', resource=cls.RESOURCE_TASK, action=cls.ACTION_ASSIGN, description='分配任务'),
        ]
    
    @classmethod
    def create_board_permissions(cls):
        """创建看板相关权限。"""
        return [
            cls(subject='board_create', resource=cls.RESOURCE_BOARD, action=cls.ACTION_CREATE, description='创建看板'),
            cls(subject='board_read', resource=cls.RESOURCE_BOARD, action=cls.ACTION_READ, description='查看看板'),
            cls(subject='board_update', resource=cls.RESOURCE_BOARD, action=cls.ACTION_UPDATE, description='更新看板'),
            cls(subject='board_delete', resource=cls.RESOURCE_BOARD, action=cls.ACTION_DELETE, description='删除看板'),
        ]


class UserRole(base_object.SynchronizedObject):
    """
    用户-角色关联实体类。
    
    记录用户在特定组织中的角色分配。
    
    Attributes:
        __user_id: 用户ID
        __role_id: 角色ID
        __organization_id: 组织ID
        __assigned_at: 分配时间
    """
    
    def __init__(self, *args, **kwargs):
        self.__id = kwargs.pop('id', None)
        self.__user_id = kwargs.pop('user_id', '')
        self.__role_id = kwargs.pop('role_id', '')
        self.__organization_id = kwargs.pop('organization_id', '')
        self.__assigned_at = kwargs.pop('assigned_at', None) or Now()
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, UserRole):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'UserRole(user_id={self.__user_id}, role_id={self.__role_id}, org_id={self.__organization_id})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'user_id': self.__user_id,
            'role_id': self.__role_id,
            'organization_id': self.__organization_id,
            'assigned_at': self.__assigned_at,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__user_id = state.get('user_id', '')
        self.__role_id = state.get('role_id', '')
        self.__organization_id = state.get('organization_id', '')
        self.__assigned_at = state.get('assigned_at', Now())
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def userId(self):
        """返回用户ID。"""
        return self.__user_id
    
    def setUserId(self, user_id):
        """设置用户ID。"""
        self.__user_id = user_id
    
    def roleId(self):
        """返回角色ID。"""
        return self.__role_id
    
    def setRoleId(self, role_id):
        """设置角色ID。"""
        self.__role_id = role_id
    
    def organizationId(self):
        """返回组织ID。"""
        return self.__organization_id
    
    def setOrganizationId(self, organization_id):
        """设置组织ID。"""
        self.__organization_id = organization_id
    
    def assignedAt(self):
        """返回分配时间。"""
        return self.__assigned_at
