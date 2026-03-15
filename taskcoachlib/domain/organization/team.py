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

Team entity for multi-tenant support.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Team(base_object.Object):
    """
    团队实体类。
    
    团队是组织内的分组单位，包含多个成员。
    
    Attributes:
        __organization: 所属组织（弱引用）
        __members: 成员列表
    """
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
        self.__members = kwargs.pop('members', [])
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'members': [m.__getstate__() for m in self.__members],
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__members = []
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Team, class_).monitoredAttributes() + ['members']
    
    def organization(self):
        """返回所属组织。"""
        return self.__organization_ref()
    
    def setOrganization(self, organization):
        """设置所属组织。"""
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
    
    def members(self):
        """返回成员列表。"""
        return list(self.__members)
    
    @patterns.eventSource
    def addMember(self, member, event=None):
        """添加成员。"""
        self.__members.append(member)
        event.addSource(self, member, type=self.membersChangedEventType())
    
    @patterns.eventSource
    def removeMember(self, member, event=None):
        """移除成员。"""
        if member in self.__members:
            self.__members.remove(member)
            event.addSource(self, member, type=self.membersChangedEventType())
    
    @patterns.eventSource
    def setMembers(self, members, event=None):
        """设置成员列表。"""
        self.__members = list(members)
        event.addSource(self, type=self.membersChangedEventType())
    
    def getMemberByUserId(self, user_id):
        """根据用户ID获取成员。"""
        for member in self.__members:
            if member.userId() == user_id:
                return member
        return None
    
    def memberCount(self):
        """返回成员数量。"""
        return len(self.__members)
    
    @classmethod
    def membersChangedEventType(class_):
        return '%s.members' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Team, class_).modificationEventTypes() + [
            class_.membersChangedEventType(),
        ]
