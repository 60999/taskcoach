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

Task assignment entity for team collaboration.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Assignment(base_object.SynchronizedObject):
    """
    任务分配实体类。
    
    记录任务与用户的分配关系。
    
    Attributes:
        __task: 任务（弱引用）
        __user: 用户（弱引用）
        __assigned_by: 分配者（弱引用）
        __role: 分配角色（负责人、参与者等）
        __status: 分配状态
        __assigned_at: 分配时间
        __accepted_at: 接受时间
        __due_notification_sent: 是否已发送到期通知
    """
    
    ROLE_OWNER = 'owner'
    ROLE_ASSIGNEE = 'assignee'
    ROLE_REVIEWER = 'reviewer'
    ROLE_OBSERVER = 'observer'
    
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'
    STATUS_COMPLETED = 'completed'
    
    def __init__(self, *args, **kwargs):
        task = kwargs.pop('task', None)
        user = kwargs.pop('user', None)
        assigned_by = kwargs.pop('assigned_by', None)
        
        self.__task_ref = weakref.ref(task) if task else lambda: None
        self.__user_ref = weakref.ref(user) if user else lambda: None
        self.__assigned_by_ref = weakref.ref(assigned_by) if assigned_by else lambda: None
        
        self.__role = kwargs.pop('role', self.ROLE_ASSIGNEE)
        self.__status = kwargs.pop('status', self.STATUS_PENDING)
        self.__assigned_at = kwargs.pop('assigned_at', None) or Now()
        self.__accepted_at = kwargs.pop('accepted_at', None)
        self.__due_notification_sent = kwargs.pop('due_notification_sent', False)
        self.__id = kwargs.pop('id', None)
        
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'Assignment(task={self.taskId()}, user={self.userId()}, role={self.__role})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'task_id': self.taskId(),
            'user_id': self.userId(),
            'assigned_by_id': self.assignedById(),
            'role': self.__role,
            'status': self.__status,
            'assigned_at': self.__assigned_at,
            'accepted_at': self.__accepted_at,
            'due_notification_sent': self.__due_notification_sent,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__role = state.get('role', self.ROLE_ASSIGNEE)
        self.__status = state.get('status', self.STATUS_PENDING)
        self.__assigned_at = state.get('assigned_at', Now())
        self.__accepted_at = state.get('accepted_at')
        self.__due_notification_sent = state.get('due_notification_sent', False)
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def task(self):
        """返回任务。"""
        return self.__task_ref()
    
    def taskId(self):
        """返回任务ID。"""
        task = self.task()
        return task.id() if task else ''
    
    def setTask(self, task):
        """设置任务。"""
        self.__task_ref = weakref.ref(task) if task else lambda: None
    
    def user(self):
        """返回用户。"""
        return self.__user_ref()
    
    def userId(self):
        """返回用户ID。"""
        user = self.user()
        return user.id() if user else ''
    
    def setUser(self, user):
        """设置用户。"""
        self.__user_ref = weakref.ref(user) if user else lambda: None
    
    def assignedBy(self):
        """返回分配者。"""
        return self.__assigned_by_ref()
    
    def assignedById(self):
        """返回分配者ID。"""
        assigned_by = self.assignedBy()
        return assigned_by.id() if assigned_by else ''
    
    def setAssignedBy(self, assigned_by):
        """设置分配者。"""
        self.__assigned_by_ref = weakref.ref(assigned_by) if assigned_by else lambda: None
    
    def role(self):
        """返回分配角色。"""
        return self.__role
    
    def setRole(self, role):
        """设置分配角色。"""
        self.__role = role
    
    def isOwner(self):
        """检查是否为负责人。"""
        return self.__role == self.ROLE_OWNER
    
    def isAssignee(self):
        """检查是否为被分配者。"""
        return self.__role == self.ROLE_ASSIGNEE
    
    def isReviewer(self):
        """检查是否为审核者。"""
        return self.__role == self.ROLE_REVIEWER
    
    def status(self):
        """返回分配状态。"""
        return self.__status
    
    def isPending(self):
        """检查是否为待接受状态。"""
        return self.__status == self.STATUS_PENDING
    
    def isAccepted(self):
        """检查是否为已接受状态。"""
        return self.__status == self.STATUS_ACCEPTED
    
    def isDeclined(self):
        """检查是否为已拒绝状态。"""
        return self.__status == self.STATUS_DECLINED
    
    def isCompleted(self):
        """检查是否为已完成状态。"""
        return self.__status == self.STATUS_COMPLETED
    
    def accept(self):
        """接受任务。"""
        self.__status = self.STATUS_ACCEPTED
        self.__accepted_at = Now()
    
    def decline(self):
        """拒绝任务。"""
        self.__status = self.STATUS_DECLINED
    
    def complete(self):
        """完成任务。"""
        self.__status = self.STATUS_COMPLETED
    
    def reopen(self):
        """重新打开任务。"""
        self.__status = self.STATUS_ACCEPTED
    
    def assignedAt(self):
        """返回分配时间。"""
        return self.__assigned_at
    
    def acceptedAt(self):
        """返回接受时间。"""
        return self.__accepted_at
    
    def dueNotificationSent(self):
        """返回是否已发送到期通知。"""
        return self.__due_notification_sent
    
    def markDueNotificationSent(self):
        """标记已发送到期通知。"""
        self.__due_notification_sent = True


class AssignmentService:
    """
    任务分配服务类。
    
    管理任务的分配、查询和通知。
    """
    
    def __init__(self):
        self.__assignments = []
        self.__by_task = {}
        self.__by_user = {}
        self.__listeners = []
    
    def assignTask(self, task, user, assigned_by=None, role=Assignment.ROLE_ASSIGNEE):
        """
        分配任务给用户。
        
        Args:
            task: 任务对象
            user: 用户对象
            assigned_by: 分配者
            role: 分配角色
            
        Returns:
            Assignment实例
        """
        existing = self.getAssignment(task.id() if task else '', user.id() if user else '')
        if existing:
            existing.setRole(role)
            return existing
        
        assignment = Assignment(
            task=task,
            user=user,
            assigned_by=assigned_by,
            role=role,
        )
        
        self.__assignments.append(assignment)
        
        task_id = task.id() if task else ''
        if task_id not in self.__by_task:
            self.__by_task[task_id] = []
        self.__by_task[task_id].append(assignment)
        
        user_id = user.id() if user else ''
        if user_id not in self.__by_user:
            self.__by_user[user_id] = []
        self.__by_user[user_id].append(assignment)
        
        self._notify_assignment_created(assignment)
        
        return assignment
    
    def unassignTask(self, task, user):
        """
        取消任务分配。
        
        Args:
            task: 任务对象
            user: 用户对象
            
        Returns:
            bool: 是否成功取消
        """
        task_id = task.id() if task else ''
        user_id = user.id() if user else ''
        
        assignment = self.getAssignment(task_id, user_id)
        if assignment:
            self.__assignments.remove(assignment)
            
            if task_id in self.__by_task:
                self.__by_task[task_id].remove(assignment)
            if user_id in self.__by_user:
                self.__by_user[user_id].remove(assignment)
            
            self._notify_assignment_removed(assignment)
            return True
        
        return False
    
    def getAssignment(self, task_id, user_id):
        """
        获取特定任务和用户的分配。
        
        Args:
            task_id: 任务ID
            user_id: 用户ID
            
        Returns:
            Assignment实例或None
        """
        for assignment in self.__by_task.get(task_id, []):
            if assignment.userId() == user_id:
                return assignment
        return None
    
    def getAssignmentsForTask(self, task_id):
        """
        获取任务的所有分配。
        
        Args:
            task_id: 任务ID
            
        Returns:
            分配列表
        """
        return self.__by_task.get(task_id, [])
    
    def getAssignmentsForUser(self, user_id, status=None):
        """
        获取用户的所有分配。
        
        Args:
            user_id: 用户ID
            status: 状态过滤（可选）
            
        Returns:
            分配列表
        """
        assignments = self.__by_user.get(user_id, [])
        if status:
            assignments = [a for a in assignments if a.status() == status]
        return assignments
    
    def getPendingAssignmentsForUser(self, user_id):
        """
        获取用户的待接受分配。
        
        Args:
            user_id: 用户ID
            
        Returns:
            待接受分配列表
        """
        return self.getAssignmentsForUser(user_id, Assignment.STATUS_PENDING)
    
    def getAcceptedAssignmentsForUser(self, user_id):
        """
        获取用户的已接受分配。
        
        Args:
            user_id: 用户ID
            
        Returns:
            已接受分配列表
        """
        return self.getAssignmentsForUser(user_id, Assignment.STATUS_ACCEPTED)
    
    def getTaskAssignees(self, task_id):
        """
        获取任务的被分配者列表。
        
        Args:
            task_id: 任务ID
            
        Returns:
            用户列表
        """
        assignments = self.getAssignmentsForTask(task_id)
        return [a.user() for a in assignments if a.user() and a.isAccepted()]
    
    def getTaskOwner(self, task_id):
        """
        获取任务的负责人。
        
        Args:
            task_id: 任务ID
            
        Returns:
            用户对象或None
        """
        assignments = self.getAssignmentsForTask(task_id)
        for assignment in assignments:
            if assignment.isOwner() and assignment.isAccepted():
                return assignment.user()
        return None
    
    def isUserAssigned(self, task_id, user_id):
        """
        检查用户是否被分配到任务。
        
        Args:
            task_id: 任务ID
            user_id: 用户ID
            
        Returns:
            bool: 是否已分配
        """
        assignment = self.getAssignment(task_id, user_id)
        return assignment is not None and assignment.isAccepted()
    
    def acceptAssignment(self, task_id, user_id):
        """
        接受任务分配。
        
        Args:
            task_id: 任务ID
            user_id: 用户ID
            
        Returns:
            bool: 是否成功
        """
        assignment = self.getAssignment(task_id, user_id)
        if assignment:
            assignment.accept()
            self._notify_assignment_accepted(assignment)
            return True
        return False
    
    def declineAssignment(self, task_id, user_id):
        """
        拒绝任务分配。
        
        Args:
            task_id: 任务ID
            user_id: 用户ID
            
        Returns:
            bool: 是否成功
        """
        assignment = self.getAssignment(task_id, user_id)
        if assignment:
            assignment.decline()
            self._notify_assignment_declined(assignment)
            return True
        return False
    
    def addAssignmentListener(self, listener):
        """
        添加分配监听器。
        
        Args:
            listener: 监听函数，签名为 listener(assignment, event_type)
        """
        self.__listeners.append(listener)
    
    def removeAssignmentListener(self, listener):
        """
        移除分配监听器。
        
        Args:
            listener: 监听函数
        """
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_assignment_created(self, assignment):
        """通知分配创建。"""
        for listener in self.__listeners:
            try:
                listener(assignment, 'created')
            except Exception:
                pass
    
    def _notify_assignment_removed(self, assignment):
        """通知分配移除。"""
        for listener in self.__listeners:
            try:
                listener(assignment, 'removed')
            except Exception:
                pass
    
    def _notify_assignment_accepted(self, assignment):
        """通知分配接受。"""
        for listener in self.__listeners:
            try:
                listener(assignment, 'accepted')
            except Exception:
                pass
    
    def _notify_assignment_declined(self, assignment):
        """通知分配拒绝。"""
        for listener in self.__listeners:
            try:
                listener(assignment, 'declined')
            except Exception:
                pass
    
    def count(self):
        """返回分配总数。"""
        return len(self.__assignments)
    
    def clear(self):
        """清除所有分配。"""
        self.__assignments.clear()
        self.__by_task.clear()
        self.__by_user.clear()
