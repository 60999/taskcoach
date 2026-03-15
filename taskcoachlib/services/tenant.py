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

Tenant service for multi-tenant data isolation.
"""

import weakref
from taskcoachlib import patterns


class TenantService:
    """
    多租户数据隔离服务。
    
    负责管理当前用户的组织上下文，确保数据隔离。
    
    Attributes:
        __current_user: 当前登录用户（弱引用）
        __current_organization: 当前组织（弱引用）
        __user_organizations: 用户所属组织映射
        __organization_data: 组织数据存储
    """
    
    def __init__(self):
        self.__current_user_ref = lambda: None
        self.__current_organization_ref = lambda: None
        self.__user_organizations = {}
        self.__organization_data = {}
        self.__listeners = []
    
    def setCurrentUser(self, user):
        """
        设置当前用户。
        
        Args:
            user: 用户对象
        """
        self.__current_user_ref = weakref.ref(user) if user else lambda: None
    
    def currentUser(self):
        """返回当前用户。"""
        return self.__current_user_ref()
    
    def currentUserId(self):
        """返回当前用户ID。"""
        user = self.currentUser()
        return user.id() if user else None
    
    def setCurrentOrganization(self, organization):
        """
        设置当前组织。
        
        Args:
            organization: 组织对象
        """
        old_org = self.currentOrganization()
        self.__current_organization_ref = weakref.ref(organization) if organization else lambda: None
        self._notify_organization_changed(old_org, organization)
    
    def currentOrganization(self):
        """返回当前组织。"""
        return self.__current_organization_ref()
    
    def currentOrganizationId(self):
        """返回当前组织ID。"""
        org = self.currentOrganization()
        return org.id() if org else None
    
    def registerUserOrganization(self, user_id, organization):
        """
        注册用户所属的组织。
        
        Args:
            user_id: 用户ID
            organization: 组织对象
        """
        if user_id not in self.__user_organizations:
            self.__user_organizations[user_id] = []
        if organization not in self.__user_organizations[user_id]:
            self.__user_organizations[user_id].append(organization)
    
    def getUserOrganizations(self, user_id=None):
        """
        获取用户所属的组织列表。
        
        Args:
            user_id: 用户ID，默认为当前用户
            
        Returns:
            组织列表
        """
        if user_id is None:
            user_id = self.currentUserId()
        return self.__user_organizations.get(user_id, [])
    
    def isUserInOrganization(self, user_id, organization_id):
        """
        检查用户是否属于指定组织。
        
        Args:
            user_id: 用户ID
            organization_id: 组织ID
            
        Returns:
            bool: 是否属于该组织
        """
        for org in self.getUserOrganizations(user_id):
            if org.id() == organization_id:
                return True
        return False
    
    def storeOrganizationData(self, organization_id, key, data):
        """
        存储组织数据。
        
        Args:
            organization_id: 组织ID
            key: 数据键
            data: 数据值
        """
        if organization_id not in self.__organization_data:
            self.__organization_data[organization_id] = {}
        self.__organization_data[organization_id][key] = data
    
    def getOrganizationData(self, organization_id, key, default=None):
        """
        获取组织数据。
        
        Args:
            organization_id: 组织ID
            key: 数据键
            default: 默认值
            
        Returns:
            数据值
        """
        org_data = self.__organization_data.get(organization_id, {})
        return org_data.get(key, default)
    
    def getOrganizationTasks(self, organization_id):
        """
        获取组织的任务列表。
        
        Args:
            organization_id: 组织ID
            
        Returns:
            任务列表
        """
        return self.getOrganizationData(organization_id, 'tasks', [])
    
    def getOrganizationBoards(self, organization_id):
        """
        获取组织的看板列表。
        
        Args:
            organization_id: 组织ID
            
        Returns:
            看板列表
        """
        return self.getOrganizationData(organization_id, 'boards', [])
    
    def getOrganizationCategories(self, organization_id):
        """
        获取组织的分类列表。
        
        Args:
            organization_id: 组织ID
            
        Returns:
            分类列表
        """
        return self.getOrganizationData(organization_id, 'categories', [])
    
    def filterByCurrentOrganization(self, items, get_organization_id_func):
        """
        根据当前组织过滤数据。
        
        Args:
            items: 待过滤的项列表
            get_organization_id_func: 获取项组织ID的函数
            
        Returns:
            过滤后的列表
        """
        current_org_id = self.currentOrganizationId()
        if current_org_id is None:
            return list(items)
        return [item for item in items if get_organization_id_func(item) == current_org_id]
    
    def canAccessData(self, data_organization_id):
        """
        检查当前用户是否可以访问指定组织的数据。
        
        Args:
            data_organization_id: 数据所属组织ID
            
        Returns:
            bool: 是否可以访问
        """
        current_org_id = self.currentOrganizationId()
        if current_org_id is None:
            return False
        return current_org_id == data_organization_id
    
    def addOrganizationChangeListener(self, listener):
        """
        添加组织变更监听器。
        
        Args:
            listener: 监听函数，签名为 listener(old_org, new_org)
        """
        self.__listeners.append(listener)
    
    def removeOrganizationChangeListener(self, listener):
        """
        移除组织变更监听器。
        
        Args:
            listener: 监听函数
        """
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_organization_changed(self, old_org, new_org):
        """通知组织变更。"""
        for listener in self.__listeners:
            try:
                listener(old_org, new_org)
            except Exception:
                pass
    
    def clear(self):
        """清除所有数据。"""
        self.__current_user_ref = lambda: None
        self.__current_organization_ref = lambda: None
        self.__user_organizations.clear()
        self.__organization_data.clear()
    
    def exportState(self):
        """
        导出服务状态。
        
        Returns:
            状态字典
        """
        return {
            'user_organizations': {
                user_id: [org.id() for org in orgs]
                for user_id, orgs in self.__user_organizations.items()
            },
            'organization_data_keys': {
                org_id: list(data.keys())
                for org_id, data in self.__organization_data.items()
            },
        }
