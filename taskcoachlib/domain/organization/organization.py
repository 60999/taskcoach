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

Organization entity for multi-tenant support.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns


class Organization(base_object.Object):
    """
    组织实体类。
    
    组织是多租户系统的顶级实体，包含多个团队和成员。
    
    Attributes:
        __owner_id: 所有者用户ID
        __teams: 团队列表
        __settings: 组织设置
    """
    
    def __init__(self, *args, **kwargs):
        self.__owner_id = kwargs.pop('owner_id', '')
        self.__teams = kwargs.pop('teams', [])
        self.__settings = kwargs.pop('settings', {})
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'owner_id': self.__owner_id,
            'teams': [t.__getstate__() for t in self.__teams],
            'settings': self.__settings,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__owner_id = state.get('owner_id', '')
        self.__teams = []
        self.__settings = state.get('settings', {})
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Organization, class_).monitoredAttributes() + ['teams']
    
    def ownerId(self):
        """返回所有者ID。"""
        return self.__owner_id
    
    def setOwnerId(self, owner_id):
        """设置所有者ID。"""
        self.__owner_id = owner_id
    
    def teams(self):
        """返回团队列表。"""
        return list(self.__teams)
    
    @patterns.eventSource
    def addTeam(self, team, event=None):
        """添加团队。"""
        self.__teams.append(team)
        event.addSource(self, team, type=self.teamsChangedEventType())
    
    @patterns.eventSource
    def removeTeam(self, team, event=None):
        """移除团队。"""
        if team in self.__teams:
            self.__teams.remove(team)
            event.addSource(self, team, type=self.teamsChangedEventType())
    
    @patterns.eventSource
    def setTeams(self, teams, event=None):
        """设置团队列表。"""
        self.__teams = list(teams)
        event.addSource(self, type=self.teamsChangedEventType())
    
    def settings(self):
        """返回组织设置。"""
        return dict(self.__settings)
    
    def setSettings(self, settings):
        """设置组织设置。"""
        self.__settings = dict(settings)
    
    def getSetting(self, key, default=None):
        """获取设置项。"""
        return self.__settings.get(key, default)
    
    def setSetting(self, key, value):
        """设置设置项。"""
        self.__settings[key] = value
    
    def getTeamById(self, team_id):
        """根据ID获取团队。"""
        for team in self.__teams:
            if team.id() == team_id:
                return team
        return None
    
    def memberCount(self):
        """返回成员总数。"""
        count = 0
        for team in self.__teams:
            count += len(team.members())
        return count
    
    @classmethod
    def teamsChangedEventType(class_):
        return '%s.teams' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Organization, class_).modificationEventTypes() + [
            class_.teamsChangedEventType(),
        ]
