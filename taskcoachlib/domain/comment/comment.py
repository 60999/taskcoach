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

Comment entity for task discussions.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Comment(base_object.Object):
    """
    评论实体类。
    
    评论可以附加到任务或其他实体上，支持嵌套回复。
    
    Attributes:
        __content: 评论内容
        __author: 评论作者（弱引用）
        __target: 评论目标实体（弱引用）
        __parent: 父评论（弱引用）
        __replies: 回复列表
        __created_at: 创建时间
        __updated_at: 更新时间
        __is_edited: 是否已编辑
        __is_deleted: 是否已删除
    """
    
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        target = kwargs.pop('target', None)
        parent = kwargs.pop('parent', None)
        
        self.__author_ref = weakref.ref(author) if author else lambda: None
        self.__target_ref = weakref.ref(target) if target else lambda: None
        self.__parent_ref = weakref.ref(parent) if parent else lambda: None
        
        self.__content = kwargs.pop('content', '')
        self.__replies = kwargs.pop('replies', [])
        self.__created_at = kwargs.pop('created_at', None) or Now()
        self.__updated_at = kwargs.pop('updated_at', None) or self.__created_at
        self.__is_edited = kwargs.pop('is_edited', False)
        self.__is_deleted = kwargs.pop('is_deleted', False)
        
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'content': self.__content,
            'author_id': self.authorId(),
            'target_id': self.targetId(),
            'parent_id': self.parentId(),
            'replies': [r.__getstate__() for r in self.__replies],
            'created_at': self.__created_at,
            'updated_at': self.__updated_at,
            'is_edited': self.__is_edited,
            'is_deleted': self.__is_deleted,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__content = state.get('content', '')
        self.__replies = []
        self.__created_at = state.get('created_at', Now())
        self.__updated_at = state.get('updated_at', self.__created_at)
        self.__is_edited = state.get('is_edited', False)
        self.__is_deleted = state.get('is_deleted', False)
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Comment, class_).monitoredAttributes() + ['content', 'replies']
    
    def content(self):
        """返回评论内容。"""
        return self.__content
    
    @patterns.eventSource
    def setContent(self, content, event=None):
        """设置评论内容。"""
        self.__content = content
        self.__updated_at = Now()
        self.__is_edited = True
        event.addSource(self, content, type=self.contentChangedEventType())
    
    def author(self):
        """返回评论作者。"""
        return self.__author_ref()
    
    def authorId(self):
        """返回作者ID。"""
        author = self.author()
        return author.id() if author else ''
    
    def setAuthor(self, author):
        """设置评论作者。"""
        self.__author_ref = weakref.ref(author) if author else lambda: None
    
    def target(self):
        """返回评论目标。"""
        return self.__target_ref()
    
    def targetId(self):
        """返回目标ID。"""
        target = self.target()
        return target.id() if target else ''
    
    def setTarget(self, target):
        """设置评论目标。"""
        self.__target_ref = weakref.ref(target) if target else lambda: None
    
    def parent(self):
        """返回父评论。"""
        return self.__parent_ref()
    
    def parentId(self):
        """返回父评论ID。"""
        parent = self.parent()
        return parent.id() if parent else ''
    
    def setParent(self, parent):
        """设置父评论。"""
        self.__parent_ref = weakref.ref(parent) if parent else lambda: None
    
    def isReply(self):
        """检查是否为回复。"""
        return self.parent() is not None
    
    def replies(self):
        """返回回复列表。"""
        return list(self.__replies)
    
    @patterns.eventSource
    def addReply(self, reply, event=None):
        """添加回复。"""
        self.__replies.append(reply)
        reply.setParent(self)
        event.addSource(self, reply, type=self.repliesChangedEventType())
    
    @patterns.eventSource
    def removeReply(self, reply, event=None):
        """移除回复。"""
        if reply in self.__replies:
            self.__replies.remove(reply)
            reply.setParent(None)
            event.addSource(self, reply, type=self.repliesChangedEventType())
    
    def replyCount(self):
        """返回回复数量。"""
        return len(self.__replies)
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
    
    def updatedAt(self):
        """返回更新时间。"""
        return self.__updated_at
    
    def isEdited(self):
        """返回是否已编辑。"""
        return self.__is_edited
    
    def isDeleted(self):
        """返回是否已删除。"""
        return self.__is_deleted
    
    def delete(self):
        """软删除评论。"""
        self.__is_deleted = True
    
    def restore(self):
        """恢复评论。"""
        self.__is_deleted = False
    
    def getVisibleContent(self):
        """获取可见内容（已删除时显示占位符）。"""
        if self.__is_deleted:
            return '[已删除]'
        return self.__content
    
    def getAllReplies(self):
        """递归获取所有回复。"""
        all_replies = []
        for reply in self.__replies:
            all_replies.append(reply)
            all_replies.extend(reply.getAllReplies())
        return all_replies
    
    @classmethod
    def contentChangedEventType(class_):
        return '%s.content' % class_
    
    @classmethod
    def repliesChangedEventType(class_):
        return '%s.replies' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Comment, class_).modificationEventTypes() + [
            class_.contentChangedEventType(),
            class_.repliesChangedEventType(),
        ]


class CommentThread(base_object.SynchronizedObject):
    """
    评论线程类。
    
    管理一个目标实体的所有评论。
    
    Attributes:
        __target: 目标实体（弱引用）
        __comments: 评论列表
    """
    
    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target', None)
        self.__target_ref = weakref.ref(target) if target else lambda: None
        self.__comments = kwargs.pop('comments', [])
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'target_id': self.targetId(),
            'comments': [c.__getstate__() for c in self.__comments],
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__comments = []
    
    def target(self):
        """返回目标实体。"""
        return self.__target_ref()
    
    def targetId(self):
        """返回目标ID。"""
        target = self.target()
        return target.id() if target else ''
    
    def setTarget(self, target):
        """设置目标实体。"""
        self.__target_ref = weakref.ref(target) if target else lambda: None
    
    def comments(self):
        """返回评论列表。"""
        return list(self.__comments)
    
    @patterns.eventSource
    def addComment(self, comment, event=None):
        """添加评论。"""
        self.__comments.append(comment)
        comment.setTarget(self.target())
        event.addSource(self, comment, type=self.commentsChangedEventType())
    
    @patterns.eventSource
    def removeComment(self, comment, event=None):
        """移除评论。"""
        if comment in self.__comments:
            self.__comments.remove(comment)
            event.addSource(self, comment, type=self.commentsChangedEventType())
    
    def commentCount(self):
        """返回评论数量。"""
        return len(self.__comments)
    
    def getRootComments(self):
        """获取根评论（非回复）。"""
        return [c for c in self.__comments if not c.isReply()]
    
    def getCommentById(self, comment_id):
        """根据ID获取评论。"""
        for comment in self.__comments:
            if comment.id() == comment_id:
                return comment
            for reply in comment.getAllReplies():
                if reply.id() == comment_id:
                    return reply
        return None
    
    def getCommentsByAuthor(self, author_id):
        """根据作者获取评论。"""
        return [c for c in self.__comments if c.authorId() == author_id]
    
    def sortCommentsByTime(self, ascending=True):
        """按时间排序评论。"""
        self.__comments.sort(key=lambda c: c.createdAt(), reverse=not ascending)
    
    @classmethod
    def commentsChangedEventType(class_):
        return '%s.comments' % class_
