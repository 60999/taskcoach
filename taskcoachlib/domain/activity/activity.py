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

Activity entity for tracking user actions.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Activity(base_object.SynchronizedObject):
    """
    活动实体类。
    
    记录用户对实体执行的操作。
    
    Attributes:
        __action: 操作类型
        __actor: 执行操作的用户（弱引用）
        __target: 目标实体（弱引用）
        __target_type: 目标类型
        __target_name: 目标名称
        __details: 操作详情
        __organization: 所属组织（弱引用）
        __created_at: 创建时间
    """
    
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_ASSIGN = 'assign'
    ACTION_UNASSIGN = 'unassign'
    ACTION_COMMENT = 'comment'
    ACTION_MENTION = 'mention'
    ACTION_MOVE = 'move'
    ACTION_COMPLETE = 'complete'
    ACTION_REOPEN = 'reopen'
    ACTION_ARCHIVE = 'archive'
    ACTION_RESTORE = 'restore'
    
    TARGET_TASK = 'task'
    TARGET_BOARD = 'board'
    TARGET_COLUMN = 'column'
    TARGET_COMMENT = 'comment'
    TARGET_USER = 'user'
    TARGET_ORGANIZATION = 'organization'
    TARGET_TEAM = 'team'
    
    ACTION_LABELS = {
        ACTION_CREATE: '创建',
        ACTION_UPDATE: '更新',
        ACTION_DELETE: '删除',
        ACTION_ASSIGN: '分配',
        ACTION_UNASSIGN: '取消分配',
        ACTION_COMMENT: '评论',
        ACTION_MENTION: '提及',
        ACTION_MOVE: '移动',
        ACTION_COMPLETE: '完成',
        ACTION_REOPEN: '重新打开',
        ACTION_ARCHIVE: '归档',
        ACTION_RESTORE: '恢复',
    }
    
    def __init__(self, *args, **kwargs):
        actor = kwargs.pop('actor', None)
        target = kwargs.pop('target', None)
        organization = kwargs.pop('organization', None)
        
        self.__actor_ref = weakref.ref(actor) if actor else lambda: None
        self.__target_ref = weakref.ref(target) if target else lambda: None
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
        
        self.__action = kwargs.pop('action', '')
        self.__target_type = kwargs.pop('target_type', '')
        self.__target_name = kwargs.pop('target_name', '')
        self.__details = kwargs.pop('details', {})
        self.__created_at = kwargs.pop('created_at', None) or Now()
        
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return f'Activity({self.__action}, {self.__target_type}, {self.__target_name})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'action': self.__action,
            'actor_id': self.actorId(),
            'target_id': self.targetId(),
            'target_type': self.__target_type,
            'target_name': self.__target_name,
            'details': self.__details,
            'organization_id': self.organizationId(),
            'created_at': self.__created_at,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__action = state.get('action', '')
        self.__target_type = state.get('target_type', '')
        self.__target_name = state.get('target_name', '')
        self.__details = state.get('details', {})
        self.__created_at = state.get('created_at', Now())
    
    def action(self):
        """返回操作类型。"""
        return self.__action
    
    def actionLabel(self):
        """返回操作标签。"""
        return self.ACTION_LABELS.get(self.__action, self.__action)
    
    def actor(self):
        """返回执行者。"""
        return self.__actor_ref()
    
    def actorId(self):
        """返回执行者ID。"""
        actor = self.actor()
        return actor.id() if actor else ''
    
    def actorName(self):
        """返回执行者名称。"""
        actor = self.actor()
        return actor.displayName() if actor else '未知用户'
    
    def target(self):
        """返回目标实体。"""
        return self.__target_ref()
    
    def targetId(self):
        """返回目标ID。"""
        target = self.target()
        return target.id() if target else ''
    
    def targetType(self):
        """返回目标类型。"""
        return self.__target_type
    
    def targetName(self):
        """返回目标名称。"""
        return self.__target_name
    
    def details(self):
        """返回操作详情。"""
        return dict(self.__details)
    
    def getDetail(self, key, default=None):
        """获取详情项。"""
        return self.__details.get(key, default)
    
    def organization(self):
        """返回所属组织。"""
        return self.__organization_ref()
    
    def organizationId(self):
        """返回组织ID。"""
        org = self.organization()
        return org.id() if org else ''
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
    
    def formatMessage(self):
        """
        格式化活动消息。
        
        Returns:
            格式化的消息字符串
        """
        actor = self.actorName()
        action = self.actionLabel()
        target = self.__target_name or self.__target_type
        
        if self.__action == self.ACTION_ASSIGN:
            assignee = self.__details.get('assignee_name', '')
            return f'{actor} 将 {target} 分配给 {assignee}'
        elif self.__action == self.ACTION_MOVE:
            from_loc = self.__details.get('from', '')
            to_loc = self.__details.get('to', '')
            return f'{actor} 将 {target} 从 {from_loc} 移动到 {to_loc}'
        elif self.__action == self.ACTION_COMMENT:
            return f'{actor} 评论了 {target}'
        elif self.__action == self.ACTION_MENTION:
            return f'{actor} 在 {target} 中提及了你'
        else:
            return f'{actor} {action}了 {target}'


class ActivityLog:
    """
    活动日志类。
    
    管理活动的存储和查询。
    """
    
    def __init__(self):
        self.__activities = []
        self.__by_actor = {}
        self.__by_target = {}
        self.__by_organization = {}
        self.__listeners = []
    
    def logActivity(self, action, actor, target, target_type=None, 
                   target_name=None, details=None, organization=None):
        """
        记录活动。
        
        Args:
            action: 操作类型
            actor: 执行者
            target: 目标实体
            target_type: 目标类型
            target_name: 目标名称
            details: 操作详情
            organization: 所属组织
            
        Returns:
            Activity实例
        """
        if target_type is None and target is not None:
            target_type = type(target).__name__.lower()
        
        if target_name is None and target is not None:
            target_name = getattr(target, 'subject', lambda: '')()
        
        activity = Activity(
            action=action,
            actor=actor,
            target=target,
            target_type=target_type or '',
            target_name=target_name or '',
            details=details or {},
            organization=organization,
        )
        
        self.__activities.append(activity)
        
        actor_id = actor.id() if actor else ''
        if actor_id not in self.__by_actor:
            self.__by_actor[actor_id] = []
        self.__by_actor[actor_id].append(activity)
        
        target_id = target.id() if target else ''
        if target_id not in self.__by_target:
            self.__by_target[target_id] = []
        self.__by_target[target_id].append(activity)
        
        org_id = organization.id() if organization else ''
        if org_id not in self.__by_organization:
            self.__by_organization[org_id] = []
        self.__by_organization[org_id].append(activity)
        
        self._notify_activity_logged(activity)
        
        return activity
    
    def getActivities(self, limit=None, offset=0):
        """
        获取活动列表。
        
        Args:
            limit: 最大数量
            offset: 偏移量
            
        Returns:
            活动列表
        """
        activities = self.__activities[offset:]
        if limit:
            activities = activities[:limit]
        return activities
    
    def getActivitiesByActor(self, actor_id, limit=None):
        """
        获取指定用户的活动。
        
        Args:
            actor_id: 用户ID
            limit: 最大数量
            
        Returns:
            活动列表
        """
        activities = self.__by_actor.get(actor_id, [])
        if limit:
            activities = activities[:limit]
        return activities
    
    def getActivitiesByTarget(self, target_id, limit=None):
        """
        获取指定目标的活动。
        
        Args:
            target_id: 目标ID
            limit: 最大数量
            
        Returns:
            活动列表
        """
        activities = self.__by_target.get(target_id, [])
        if limit:
            activities = activities[:limit]
        return activities
    
    def getActivitiesByOrganization(self, organization_id, limit=None):
        """
        获取指定组织的活动。
        
        Args:
            organization_id: 组织ID
            limit: 最大数量
            
        Returns:
            活动列表
        """
        activities = self.__by_organization.get(organization_id, [])
        if limit:
            activities = activities[:limit]
        return activities
    
    def getRecentActivities(self, count=20):
        """
        获取最近的活动。
        
        Args:
            count: 数量
            
        Returns:
            活动列表
        """
        return self.__activities[-count:] if self.__activities else []
    
    def getActivitiesByType(self, action, limit=None):
        """
        获取指定类型的活动。
        
        Args:
            action: 操作类型
            limit: 最大数量
            
        Returns:
            活动列表
        """
        activities = [a for a in self.__activities if a.action() == action]
        if limit:
            activities = activities[:limit]
        return activities
    
    def clearOldActivities(self, days=30):
        """
        清除旧活动。
        
        Args:
            days: 保留天数
            
        Returns:
            删除的活动数量
        """
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        old_activities = [a for a in self.__activities if a.createdAt() < cutoff]
        
        for activity in old_activities:
            self.__activities.remove(activity)
            
            actor_id = activity.actorId()
            if actor_id in self.__by_actor and activity in self.__by_actor[actor_id]:
                self.__by_actor[actor_id].remove(activity)
            
            target_id = activity.targetId()
            if target_id in self.__by_target and activity in self.__by_target[target_id]:
                self.__by_target[target_id].remove(activity)
            
            org_id = activity.organizationId()
            if org_id in self.__by_organization and activity in self.__by_organization[org_id]:
                self.__by_organization[org_id].remove(activity)
        
        return len(old_activities)
    
    def addActivityListener(self, listener):
        """
        添加活动监听器。
        
        Args:
            listener: 监听函数，签名为 listener(activity)
        """
        self.__listeners.append(listener)
    
    def removeActivityListener(self, listener):
        """
        移除活动监听器。
        
        Args:
            listener: 监听函数
        """
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_activity_logged(self, activity):
        """通知活动记录。"""
        for listener in self.__listeners:
            try:
                listener(activity)
            except Exception:
                pass
    
    def count(self):
        """返回活动总数。"""
        return len(self.__activities)
    
    def clear(self):
        """清除所有活动。"""
        self.__activities.clear()
        self.__by_actor.clear()
        self.__by_target.clear()
        self.__by_organization.clear()
