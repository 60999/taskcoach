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

User container for managing user collections.
"""

from taskcoachlib.domain import base
from taskcoachlib import patterns


class UserContainer(base.Collection):
    """
    用户容器类。
    
    用于管理用户对象的集合。
    """
    
    def findUserByUsername(self, username):
        """
        根据用户名查找用户。
        
        Args:
            username: 用户名
            
        Returns:
            User对象或None
        """
        for user in self:
            if user.username() == username:
                return user
        return None
    
    def findUserByEmail(self, email):
        """
        根据邮箱查找用户。
        
        Args:
            email: 电子邮箱
            
        Returns:
            User对象或None
        """
        for user in self:
            if user.email() == email:
                return user
        return None
    
    def getActiveUsers(self):
        """
        获取所有活跃用户。
        
        Returns:
            活跃用户列表
        """
        return [user for user in self if user.isActive()]
    
    def getSuperusers(self):
        """
        获取所有超级用户。
        
        Returns:
            超级用户列表
        """
        return [user for user in self if user.isSuperuser()]
