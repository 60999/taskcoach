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

Organization container for managing organization collections.
"""

from taskcoachlib.domain import base
from taskcoachlib import patterns


class OrganizationContainer(base.Collection):
    """
    组织容器类。
    
    用于管理组织对象的集合。
    """
    
    def findOrganizationByName(self, name):
        """
        根据名称查找组织。
        
        Args:
            name: 组织名称
            
        Returns:
            Organization对象或None
        """
        for org in self:
            if org.subject() == name:
                return org
        return None
    
    def getOrganizationsByOwner(self, owner_id):
        """
        获取指定用户拥有的组织。
        
        Args:
            owner_id: 所有者ID
            
        Returns:
            组织列表
        """
        return [org for org in self if org.ownerId() == owner_id]


class TeamContainer(base.Collection):
    """
    团队容器类。
    
    用于管理团队对象的集合。
    """
    
    def findTeamByName(self, name):
        """
        根据名称查找团队。
        
        Args:
            name: 团队名称
            
        Returns:
            Team对象或None
        """
        for team in self:
            if team.subject() == name:
                return team
        return None
    
    def getTeamsByOrganization(self, organization):
        """
        获取指定组织的团队。
        
        Args:
            organization: 组织对象
            
        Returns:
            团队列表
        """
        return [team for team in self if team.organization() == organization]
