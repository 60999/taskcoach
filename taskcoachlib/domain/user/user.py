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

User entity for team collaboration.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns


class User(base_object.Object):
    """
    用户实体类。
    
    用户代表系统中的一个账户，可以属于多个组织并拥有不同的角色。
    
    Attributes:
        __username: 用户名（唯一）
        __email: 电子邮箱
        __password_hash: 密码哈希
        __display_name: 显示名称
        __avatar: 头像路径
        __last_login: 最后登录时间
        __is_active: 是否激活
        __is_superuser: 是否超级用户
    """
    
    def __init__(self, *args, **kwargs):
        self.__username = kwargs.pop('username', '')
        self.__email = kwargs.pop('email', '')
        self.__password_hash = kwargs.pop('password_hash', '')
        self.__display_name = kwargs.pop('display_name', '')
        self.__avatar = kwargs.pop('avatar', None)
        self.__last_login = kwargs.pop('last_login', None)
        self.__is_active = kwargs.pop('is_active', True)
        self.__is_superuser = kwargs.pop('is_superuser', False)
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'username': self.__username,
            'email': self.__email,
            'password_hash': self.__password_hash,
            'display_name': self.__display_name,
            'avatar': self.__avatar,
            'last_login': self.__last_login,
            'is_active': self.__is_active,
            'is_superuser': self.__is_superuser,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__username = state.get('username', '')
        self.__email = state.get('email', '')
        self.__password_hash = state.get('password_hash', '')
        self.__display_name = state.get('display_name', '')
        self.__avatar = state.get('avatar')
        self.__last_login = state.get('last_login')
        self.__is_active = state.get('is_active', True)
        self.__is_superuser = state.get('is_superuser', False)
    
    @classmethod
    def monitoredAttributes(class_):
        return super(User, class_).monitoredAttributes() + ['username', 'email', 'display_name']
    
    def username(self):
        """返回用户名。"""
        return self.__username
    
    @patterns.eventSource
    def setUsername(self, username, event=None):
        """设置用户名。"""
        self.__username = username
        event.addSource(self, username, type=self.usernameChangedEventType())
    
    def email(self):
        """返回电子邮箱。"""
        return self.__email
    
    @patterns.eventSource
    def setEmail(self, email, event=None):
        """设置电子邮箱。"""
        self.__email = email
        event.addSource(self, email, type=self.emailChangedEventType())
    
    def passwordHash(self):
        """返回密码哈希。"""
        return self.__password_hash
    
    def setPasswordHash(self, password_hash):
        """设置密码哈希。"""
        self.__password_hash = password_hash
    
    def displayName(self):
        """返回显示名称。"""
        return self.__display_name or self.__username
    
    @patterns.eventSource
    def setDisplayName(self, display_name, event=None):
        """设置显示名称。"""
        self.__display_name = display_name
        event.addSource(self, display_name, type=self.displayNameChangedEventType())
    
    def avatar(self):
        """返回头像路径。"""
        return self.__avatar
    
    def setAvatar(self, avatar):
        """设置头像路径。"""
        self.__avatar = avatar
    
    def lastLogin(self):
        """返回最后登录时间。"""
        return self.__last_login
    
    def setLastLogin(self, last_login):
        """设置最后登录时间。"""
        self.__last_login = last_login
    
    def isActive(self):
        """返回是否激活。"""
        return self.__is_active
    
    def setIsActive(self, is_active):
        """设置是否激活。"""
        self.__is_active = is_active
    
    def isSuperuser(self):
        """返回是否超级用户。"""
        return self.__is_superuser
    
    def setIsSuperuser(self, is_superuser):
        """设置是否超级用户。"""
        self.__is_superuser = is_superuser
    
    def check_password(self, password, password_hasher):
        """检查密码是否正确。"""
        return password_hasher.verify(password, self.__password_hash)
    
    def set_password(self, password, password_hasher):
        """设置密码。"""
        self.__password_hash = password_hasher.hash(password)
    
    @classmethod
    def usernameChangedEventType(class_):
        return '%s.username' % class_
    
    @classmethod
    def emailChangedEventType(class_):
        return '%s.email' % class_
    
    @classmethod
    def displayNameChangedEventType(class_):
        return '%s.display_name' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(User, class_).modificationEventTypes() + [
            class_.usernameChangedEventType(),
            class_.emailChangedEventType(),
            class_.displayNameChangedEventType(),
        ]
