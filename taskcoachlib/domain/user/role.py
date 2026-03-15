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

Role entity for team collaboration.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib import patterns


class Role(base_object.Object):
    """
    角色实体类。
    
    角色定义一组权限，可以分配给用户。
    
    Attributes:
        __description: 角色描述
        __organization_id: 所属组织ID
        __is_system: 是否系统角色
    """
    
    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'
    ROLE_GUEST = 'guest'
    
    def __init__(self, *args, **kwargs):
        self.__description = kwargs.pop('description', '')
        self.__organization_id = kwargs.pop('organization_id', '')
        self.__is_system = kwargs.pop('is_system', False)
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'description': self.__description,
            'organization_id': self.__organization_id,
            'is_system': self.__is_system,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__description = state.get('description', '')
        self.__organization_id = state.get('organization_id', '')
        self.__is_system = state.get('is_system', False)
    
    def description(self):
        """返回角色描述。"""
        return self.__description
    
    def setDescription(self, description):
        """设置角色描述。"""
        self.__description = description
    
    def organizationId(self):
        """返回所属组织ID。"""
        return self.__organization_id
    
    def setOrganizationId(self, organization_id):
        """设置所属组织ID。"""
        self.__organization_id = organization_id
    
    def isSystem(self):
        """返回是否系统角色。"""
        return self.__is_system
    
    def setIsSystem(self, is_system):
        """设置是否系统角色。"""
        self.__is_system = is_system
    
    def isAdmin(self):
        """检查是否为管理员角色。"""
        return self.subject() == self.ROLE_ADMIN
    
    def isMember(self):
        """检查是否为成员角色。"""
        return self.subject() == self.ROLE_MEMBER
    
    def isGuest(self):
        """检查是否为访客角色。"""
        return self.subject() == self.ROLE_GUEST
