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

Permission service for access control.
"""

import weakref
from taskcoachlib.domain.user.permission import Permission


class PermissionService:
    """
    权限检查服务。
    
    负责检查用户对资源的访问权限。
    
    Attributes:
        __role_permissions: 角色-权限映射
        __user_roles: 用户-角色映射
        __superuser_bypass: 超级用户是否绕过权限检查
    """
    
    DEFAULT_ADMIN_PERMISSIONS = [
        (Permission.RESOURCE_TASK, Permission.ACTION_CREATE),
        (Permission.RESOURCE_TASK, Permission.ACTION_READ),
        (Permission.RESOURCE_TASK, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_TASK, Permission.ACTION_DELETE),
        (Permission.RESOURCE_TASK, Permission.ACTION_ASSIGN),
        (Permission.RESOURCE_BOARD, Permission.ACTION_CREATE),
        (Permission.RESOURCE_BOARD, Permission.ACTION_READ),
        (Permission.RESOURCE_BOARD, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_BOARD, Permission.ACTION_DELETE),
        (Permission.RESOURCE_USER, Permission.ACTION_READ),
        (Permission.RESOURCE_USER, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_ORGANIZATION, Permission.ACTION_READ),
        (Permission.RESOURCE_ORGANIZATION, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_ORGANIZATION, Permission.ACTION_MANAGE),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_CREATE),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_READ),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_DELETE),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_CREATE),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_READ),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_DELETE),
    ]
    
    DEFAULT_MEMBER_PERMISSIONS = [
        (Permission.RESOURCE_TASK, Permission.ACTION_CREATE),
        (Permission.RESOURCE_TASK, Permission.ACTION_READ),
        (Permission.RESOURCE_TASK, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_TASK, Permission.ACTION_ASSIGN),
        (Permission.RESOURCE_BOARD, Permission.ACTION_READ),
        (Permission.RESOURCE_BOARD, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_USER, Permission.ACTION_READ),
        (Permission.RESOURCE_ORGANIZATION, Permission.ACTION_READ),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_CREATE),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_READ),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_UPDATE),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_DELETE),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_READ),
    ]
    
    DEFAULT_GUEST_PERMISSIONS = [
        (Permission.RESOURCE_TASK, Permission.ACTION_READ),
        (Permission.RESOURCE_BOARD, Permission.ACTION_READ),
        (Permission.RESOURCE_USER, Permission.ACTION_READ),
        (Permission.RESOURCE_ORGANIZATION, Permission.ACTION_READ),
        (Permission.RESOURCE_COMMENT, Permission.ACTION_READ),
        (Permission.RESOURCE_WORKFLOW, Permission.ACTION_READ),
    ]
    
    def __init__(self):
        self.__role_permissions = {}
        self.__user_roles = {}
        self.__superuser_bypass = True
        self._initialize_default_permissions()
    
    def _initialize_default_permissions(self):
        """初始化默认权限。"""
        self.__role_permissions['admin'] = set(self.DEFAULT_ADMIN_PERMISSIONS)
        self.__role_permissions['member'] = set(self.DEFAULT_MEMBER_PERMISSIONS)
        self.__role_permissions['guest'] = set(self.DEFAULT_GUEST_PERMISSIONS)
    
    def grantPermission(self, role_name, resource, action):
        """
        授予角色权限。
        
        Args:
            role_name: 角色名称
            resource: 资源类型
            action: 操作类型
        """
        if role_name not in self.__role_permissions:
            self.__role_permissions[role_name] = set()
        self.__role_permissions[role_name].add((resource, action))
    
    def revokePermission(self, role_name, resource, action):
        """
        撤销角色权限。
        
        Args:
            role_name: 角色名称
            resource: 资源类型
            action: 操作类型
        """
        if role_name in self.__role_permissions:
            self.__role_permissions[role_name].discard((resource, action))
    
    def getRolePermissions(self, role_name):
        """
        获取角色的所有权限。
        
        Args:
            role_name: 角色名称
            
        Returns:
            权限集合
        """
        return self.__role_permissions.get(role_name, set()).copy()
    
    def assignRoleToUser(self, user_id, role_name, organization_id=None):
        """
        为用户分配角色。
        
        Args:
            user_id: 用户ID
            role_name: 角色名称
            organization_id: 组织ID（可选）
        """
        key = (user_id, organization_id) if organization_id else user_id
        if key not in self.__user_roles:
            self.__user_roles[key] = set()
        self.__user_roles[key].add(role_name)
    
    def removeRoleFromUser(self, user_id, role_name, organization_id=None):
        """
        移除用户的角色。
        
        Args:
            user_id: 用户ID
            role_name: 角色名称
            organization_id: 组织ID（可选）
        """
        key = (user_id, organization_id) if organization_id else user_id
        if key in self.__user_roles:
            self.__user_roles[key].discard(role_name)
    
    def getUserRoles(self, user_id, organization_id=None):
        """
        获取用户的角色列表。
        
        Args:
            user_id: 用户ID
            organization_id: 组织ID（可选）
            
        Returns:
            角色集合
        """
        roles = set()
        if user_id in self.__user_roles:
            roles.update(self.__user_roles[user_id])
        if organization_id:
            key = (user_id, organization_id)
            if key in self.__user_roles:
                roles.update(self.__user_roles[key])
        return roles
    
    def hasPermission(self, user, resource, action, organization_id=None):
        """
        检查用户是否有指定权限。
        
        Args:
            user: 用户对象
            resource: 资源类型
            action: 操作类型
            organization_id: 组织ID（可选）
            
        Returns:
            bool: 是否有权限
        """
        if user is None:
            return False
        
        if self.__superuser_bypass and user.isSuperuser():
            return True
        
        user_id = user.id()
        roles = self.getUserRoles(user_id, organization_id)
        
        for role_name in roles:
            if self._checkRolePermission(role_name, resource, action):
                return True
        
        return False
    
    def _checkRolePermission(self, role_name, resource, action):
        """
        检查角色是否有指定权限。
        
        Args:
            role_name: 角色名称
            resource: 资源类型
            action: 操作类型
            
        Returns:
            bool: 是否有权限
        """
        permissions = self.__role_permissions.get(role_name, set())
        return (resource, action) in permissions
    
    def checkPermission(self, user, resource, action, organization_id=None):
        """
        检查权限并抛出异常（用于装饰器）。
        
        Args:
            user: 用户对象
            resource: 资源类型
            action: 操作类型
            organization_id: 组织ID（可选）
            
        Raises:
            PermissionDeniedError: 权限不足时抛出
        """
        if not self.hasPermission(user, resource, action, organization_id):
            raise PermissionDeniedError(user, resource, action)
    
    def filterByPermission(self, user, items, resource, action, 
                          organization_id=None, get_organization_id_func=None):
        """
        根据权限过滤数据。
        
        Args:
            user: 用户对象
            items: 待过滤的项列表
            resource: 资源类型
            action: 操作类型
            organization_id: 组织ID（可选）
            get_organization_id_func: 获取项组织ID的函数
            
        Returns:
            过滤后的列表
        """
        if user is None:
            return []
        
        if self.__superuser_bypass and user.isSuperuser():
            return list(items)
        
        if not self.hasPermission(user, resource, action, organization_id):
            return []
        
        if get_organization_id_func and organization_id:
            return [item for item in items 
                   if get_organization_id_func(item) == organization_id]
        
        return list(items)
    
    def setSuperuserBypass(self, enabled):
        """
        设置超级用户是否绕过权限检查。
        
        Args:
            enabled: 是否启用
        """
        self.__superuser_bypass = enabled
    
    def clearUserRoles(self, user_id=None):
        """
        清除用户角色映射。
        
        Args:
            user_id: 用户ID，为None时清除所有
        """
        if user_id is None:
            self.__user_roles.clear()
        else:
            keys_to_remove = [k for k in self.__user_roles 
                            if k == user_id or (isinstance(k, tuple) and k[0] == user_id)]
            for k in keys_to_remove:
                del self.__user_roles[k]
    
    def exportState(self):
        """
        导出服务状态。
        
        Returns:
            状态字典
        """
        return {
            'role_permissions': {
                role: list(perms) 
                for role, perms in self.__role_permissions.items()
            },
            'user_roles': {
                str(k): list(v) for k, v in self.__user_roles.items()
            },
            'superuser_bypass': self.__superuser_bypass,
        }


class PermissionDeniedError(Exception):
    """权限拒绝异常。"""
    
    def __init__(self, user, resource, action):
        self.user = user
        self.resource = resource
        self.action = action
        message = f"User '{user.subject() if user else 'None'}' denied {action} on {resource}"
        super().__init__(message)


def require_permission(resource, action, get_organization_id=None):
    """
    权限检查装饰器。
    
    Args:
        resource: 资源类型
        action: 操作类型
        get_organization_id: 获取组织ID的函数
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            permission_service = getattr(self, '_permission_service', None)
            if permission_service is None:
                return func(self, *args, **kwargs)
            
            user = getattr(self, '_current_user', None)
            if user is None:
                raise PermissionDeniedError(None, resource, action)
            
            org_id = None
            if get_organization_id:
                org_id = get_organization_id(self, *args, **kwargs)
            
            permission_service.checkPermission(user, resource, action, org_id)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
