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

Membership and Invitation entities for multi-tenant support.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Membership(base_object.SynchronizedObject):
    """
    成员关系实体类。
    
    记录用户与团队的关系，以及用户在团队中的角色。
    
    Attributes:
        __user: 用户（弱引用）
        __team: 团队（弱引用）
        __role: 角色
        __status: 成员状态
    """
    
    STATUS_ACTIVE = 'active'
    STATUS_PENDING = 'pending'
    STATUS_INACTIVE = 'inactive'
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        team = kwargs.pop('team', None)
        self.__user_ref = weakref.ref(user) if user else lambda: None
        self.__team_ref = weakref.ref(team) if team else lambda: None
        self.__role_id = kwargs.pop('role_id', '')
        self.__joined_at = kwargs.pop('joined_at', None) or Now()
        self.__status = kwargs.pop('status', self.STATUS_ACTIVE)
        self.__id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, Membership):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'Membership(user_id={self.userId()}, team_id={self.teamId()}, status={self.__status})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'user_id': self.userId(),
            'team_id': self.teamId(),
            'role_id': self.__role_id,
            'joined_at': self.__joined_at,
            'status': self.__status,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__role_id = state.get('role_id', '')
        self.__joined_at = state.get('joined_at', Now())
        self.__status = state.get('status', self.STATUS_ACTIVE)
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def user(self):
        """返回用户。"""
        return self.__user_ref()
    
    def setUser(self, user):
        """设置用户。"""
        self.__user_ref = weakref.ref(user) if user else lambda: None
    
    def userId(self):
        """返回用户ID。"""
        user = self.user()
        return user.id() if user else ''
    
    def team(self):
        """返回团队。"""
        return self.__team_ref()
    
    def setTeam(self, team):
        """设置团队。"""
        self.__team_ref = weakref.ref(team) if team else lambda: None
    
    def teamId(self):
        """返回团队ID。"""
        team = self.team()
        return team.id() if team else ''
    
    def roleId(self):
        """返回角色ID。"""
        return self.__role_id
    
    def setRoleId(self, role_id):
        """设置角色ID。"""
        self.__role_id = role_id
    
    def joinedAt(self):
        """返回加入时间。"""
        return self.__joined_at
    
    def status(self):
        """返回成员状态。"""
        return self.__status
    
    def setStatus(self, status):
        """设置成员状态。"""
        self.__status = status
    
    def isActive(self):
        """检查是否为活跃状态。"""
        return self.__status == self.STATUS_ACTIVE
    
    def isPending(self):
        """检查是否为待确认状态。"""
        return self.__status == self.STATUS_PENDING
    
    def activate(self):
        """激活成员。"""
        self.__status = self.STATUS_ACTIVE
    
    def deactivate(self):
        """停用成员。"""
        self.__status = self.STATUS_INACTIVE


class Invitation(base_object.SynchronizedObject):
    """
    邀请实体类。
    
    记录组织或团队对用户的邀请。
    
    Attributes:
        __organization: 组织（弱引用）
        __team: 团队（弱引用，可选）
        __email: 邀请邮箱
        __role_id: 分配角色ID
        __invited_by: 邀请人（弱引用）
        __expires_at: 过期时间
        __status: 邀请状态
    """
    
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'
    STATUS_EXPIRED = 'expired'
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        team = kwargs.pop('team', None)
        invited_by = kwargs.pop('invited_by', None)
        
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
        self.__team_ref = weakref.ref(team) if team else lambda: None
        self.__invited_by_ref = weakref.ref(invited_by) if invited_by else lambda: None
        
        self.__email = kwargs.pop('email', '')
        self.__role_id = kwargs.pop('role_id', '')
        self.__invited_at = kwargs.pop('invited_at', None) or Now()
        self.__expires_at = kwargs.pop('expires_at', None)
        self.__status = kwargs.pop('status', self.STATUS_PENDING)
        self.__id = kwargs.pop('id', None)
        
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, Invitation):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'Invitation(email={self.__email}, status={self.__status})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'organization_id': self.organizationId(),
            'team_id': self.teamId(),
            'email': self.__email,
            'role_id': self.__role_id,
            'invited_by_id': self.invitedById(),
            'invited_at': self.__invited_at,
            'expires_at': self.__expires_at,
            'status': self.__status,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__email = state.get('email', '')
        self.__role_id = state.get('role_id', '')
        self.__invited_at = state.get('invited_at', Now())
        self.__expires_at = state.get('expires_at')
        self.__status = state.get('status', self.STATUS_PENDING)
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def organization(self):
        """返回组织。"""
        return self.__organization_ref()
    
    def organizationId(self):
        """返回组织ID。"""
        org = self.organization()
        return org.id() if org else ''
    
    def team(self):
        """返回团队。"""
        return self.__team_ref()
    
    def teamId(self):
        """返回团队ID。"""
        team = self.team()
        return team.id() if team else ''
    
    def email(self):
        """返回邀请邮箱。"""
        return self.__email
    
    def roleId(self):
        """返回角色ID。"""
        return self.__role_id
    
    def invitedBy(self):
        """返回邀请人。"""
        return self.__invited_by_ref()
    
    def invitedById(self):
        """返回邀请人ID。"""
        inviter = self.invitedBy()
        return inviter.id() if inviter else ''
    
    def invitedAt(self):
        """返回邀请时间。"""
        return self.__invited_at
    
    def expiresAt(self):
        """返回过期时间。"""
        return self.__expires_at
    
    def status(self):
        """返回邀请状态。"""
        return self.__status
    
    def isPending(self):
        """检查是否为待处理状态。"""
        return self.__status == self.STATUS_PENDING
    
    def isExpired(self):
        """检查是否已过期。"""
        if self.__expires_at and Now() > self.__expires_at:
            return True
        return self.__status == self.STATUS_EXPIRED
    
    def accept(self):
        """接受邀请。"""
        self.__status = self.STATUS_ACCEPTED
    
    def decline(self):
        """拒绝邀请。"""
        self.__status = self.STATUS_DECLINED
    
    def expire(self):
        """标记为过期。"""
        self.__status = self.STATUS_EXPIRED
