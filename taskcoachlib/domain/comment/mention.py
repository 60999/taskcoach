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

Mention entity for @mentions in comments.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import Now
from taskcoachlib import patterns
import weakref
import re


class Mention(base_object.SynchronizedObject):
    """
    提及实体类。
    
    记录评论中对用户的@提及。
    
    Attributes:
        __user: 被提及的用户（弱引用）
        __comment: 所属评论（弱引用）
        __position: 提及在文本中的位置
        __length: 提及长度
        __is_read: 是否已读
        __created_at: 创建时间
    """
    
    MENTION_PATTERN = re.compile(r'@(\w+)')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        comment = kwargs.pop('comment', None)
        
        self.__user_ref = weakref.ref(user) if user else lambda: None
        self.__comment_ref = weakref.ref(comment) if comment else lambda: None
        
        self.__position = kwargs.pop('position', 0)
        self.__length = kwargs.pop('length', 0)
        self.__is_read = kwargs.pop('is_read', False)
        self.__created_at = kwargs.pop('created_at', None) or Now()
        
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'user_id': self.userId(),
            'comment_id': self.commentId(),
            'position': self.__position,
            'length': self.__length,
            'is_read': self.__is_read,
            'created_at': self.__created_at,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__position = state.get('position', 0)
        self.__length = state.get('length', 0)
        self.__is_read = state.get('is_read', False)
        self.__created_at = state.get('created_at', Now())
    
    def user(self):
        """返回被提及的用户。"""
        return self.__user_ref()
    
    def userId(self):
        """返回用户ID。"""
        user = self.user()
        return user.id() if user else ''
    
    def setUser(self, user):
        """设置被提及的用户。"""
        self.__user_ref = weakref.ref(user) if user else lambda: None
    
    def comment(self):
        """返回所属评论。"""
        return self.__comment_ref()
    
    def commentId(self):
        """返回评论ID。"""
        comment = self.comment()
        return comment.id() if comment else ''
    
    def setComment(self, comment):
        """设置所属评论。"""
        self.__comment_ref = weakref.ref(comment) if comment else lambda: None
    
    def position(self):
        """返回提及位置。"""
        return self.__position
    
    def setPosition(self, position):
        """设置提及位置。"""
        self.__position = position
    
    def length(self):
        """返回提及长度。"""
        return self.__length
    
    def setLength(self, length):
        """设置提及长度。"""
        self.__length = length
    
    def isRead(self):
        """返回是否已读。"""
        return self.__is_read
    
    def markAsRead(self):
        """标记为已读。"""
        self.__is_read = True
    
    def markAsUnread(self):
        """标记为未读。"""
        self.__is_read = False
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
    
    @classmethod
    def extractMentions(cls, text):
        """
        从文本中提取提及。
        
        Args:
            text: 文本内容
            
        Returns:
            提及用户名列表
        """
        return cls.MENTION_PATTERN.findall(text)
    
    @classmethod
    def findMentionPositions(cls, text):
        """
        查找文本中所有提及的位置。
        
        Args:
            text: 文本内容
            
        Returns:
            列表，每项为 (username, start, end)
        """
        mentions = []
        for match in cls.MENTION_PATTERN.finditer(text):
            username = match.group(1)
            start = match.start()
            end = match.end()
            mentions.append((username, start, end))
        return mentions


class MentionService:
    """
    提及服务类。
    
    管理提及的创建、查询和通知。
    """
    
    def __init__(self):
        self.__mentions = []
        self.__user_mentions = {}
        self.__listeners = []
    
    def createMention(self, user, comment, position, length):
        """
        创建提及。
        
        Args:
            user: 被提及的用户
            comment: 所属评论
            position: 位置
            length: 长度
            
        Returns:
            Mention实例
        """
        mention = Mention(
            user=user,
            comment=comment,
            position=position,
            length=length
        )
        self.__mentions.append(mention)
        
        user_id = user.id() if user else ''
        if user_id not in self.__user_mentions:
            self.__user_mentions[user_id] = []
        self.__user_mentions[user_id].append(mention)
        
        self._notify_mention_created(mention)
        
        return mention
    
    def parseAndCreateMentions(self, comment, text, user_lookup_func):
        """
        解析文本并创建提及。
        
        Args:
            comment: 所属评论
            text: 文本内容
            user_lookup_func: 用户查找函数，签名为 func(username) -> user
            
        Returns:
            创建的提及列表
        """
        mentions = []
        for username, start, end in Mention.findMentionPositions(text):
            user = user_lookup_func(username)
            if user:
                mention = self.createMention(user, comment, start, end - start)
                mentions.append(mention)
        return mentions
    
    def getMentionsForUser(self, user_id):
        """
        获取用户的所有提及。
        
        Args:
            user_id: 用户ID
            
        Returns:
            提及列表
        """
        return self.__user_mentions.get(user_id, [])
    
    def getUnreadMentionsForUser(self, user_id):
        """
        获取用户的未读提及。
        
        Args:
            user_id: 用户ID
            
        Returns:
            未读提及列表
        """
        return [m for m in self.getMentionsForUser(user_id) if not m.isRead()]
    
    def markAllAsRead(self, user_id):
        """
        将用户的所有提及标记为已读。
        
        Args:
            user_id: 用户ID
        """
        for mention in self.getMentionsForUser(user_id):
            mention.markAsRead()
    
    def removeMention(self, mention):
        """
        移除提及。
        
        Args:
            mention: 要移除的提及
        """
        if mention in self.__mentions:
            self.__mentions.remove(mention)
        
        user_id = mention.userId()
        if user_id in self.__user_mentions:
            if mention in self.__user_mentions[user_id]:
                self.__user_mentions[user_id].remove(mention)
    
    def addMentionListener(self, listener):
        """
        添加提及监听器。
        
        Args:
            listener: 监听函数，签名为 listener(mention, event_type)
        """
        self.__listeners.append(listener)
    
    def removeMentionListener(self, listener):
        """
        移除提及监听器。
        
        Args:
            listener: 监听函数
        """
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_mention_created(self, mention):
        """通知提及创建。"""
        for listener in self.__listeners:
            try:
                listener(mention, 'created')
            except Exception:
                pass
    
    def clear(self):
        """清除所有提及。"""
        self.__mentions.clear()
        self.__user_mentions.clear()
