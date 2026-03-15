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

Link entity for bidirectional linking between tasks and knowledge base.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import Now
from taskcoachlib import patterns
import weakref


class LinkType:
    """
    链接类型枚举类。
    
    定义不同类型的链接关系。
    """
    
    REFERENCE = 'reference'
    DEPENDS_ON = 'depends_on'
    BLOCKS = 'blocks'
    RELATED_TO = 'related_to'
    PARENT_OF = 'parent_of'
    CHILD_OF = 'child_of'
    DUPLICATE_OF = 'duplicate_of'
    MENTIONED_IN = 'mentioned_in'
    
    LABELS = {
        REFERENCE: '引用',
        DEPENDS_ON: '依赖于',
        BLOCKS: '阻塞',
        RELATED_TO: '相关于',
        PARENT_OF: '父任务',
        CHILD_OF: '子任务',
        DUPLICATE_OF: '重复于',
        MENTIONED_IN: '提及于',
    }
    
    INVERSE_TYPES = {
        REFERENCE: REFERENCE,
        DEPENDS_ON: BLOCKS,
        BLOCKS: DEPENDS_ON,
        RELATED_TO: RELATED_TO,
        PARENT_OF: CHILD_OF,
        CHILD_OF: PARENT_OF,
        DUPLICATE_OF: DUPLICATE_OF,
        MENTIONED_IN: REFERENCE,
    }
    
    @classmethod
    def getLabel(cls, link_type):
        """获取链接类型标签。"""
        return cls.LABELS.get(link_type, link_type)
    
    @classmethod
    def getInverseType(cls, link_type):
        """获取反向链接类型。"""
        return cls.INVERSE_TYPES.get(link_type, cls.REFERENCE)


class Link(base_object.SynchronizedObject):
    """
    链接实体类。
    
    表示两个实体之间的双向链接关系。
    
    Attributes:
        __source: 源实体（弱引用）
        __target: 目标实体（弱引用）
        __link_type: 链接类型
        __context: 链接上下文（如文本片段）
        __position: 链接在文本中的位置
        __created_at: 创建时间
        __created_by: 创建者（弱引用）
        __is_active: 是否激活
    """
    
    def __init__(self, *args, **kwargs):
        source = kwargs.pop('source', None)
        target = kwargs.pop('target', None)
        created_by = kwargs.pop('created_by', None)
        
        self.__source_ref = weakref.ref(source) if source else lambda: None
        self.__target_ref = weakref.ref(target) if target else lambda: None
        self.__created_by_ref = weakref.ref(created_by) if created_by else lambda: None
        
        self.__link_type = kwargs.pop('link_type', LinkType.REFERENCE)
        self.__context = kwargs.pop('context', '')
        self.__position = kwargs.pop('position', 0)
        self.__created_at = kwargs.pop('created_at', None) or Now()
        self.__is_active = kwargs.pop('is_active', True)
        self.__id = kwargs.pop('id', None)
        
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        return self.id() == other.id()
    
    def __hash__(self):
        return hash(self.id())
    
    def __repr__(self):
        return f'Link({self.sourceId()} -> {self.targetId()}, type={self.__link_type})'
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'id': self.__id,
            'source_id': self.sourceId(),
            'target_id': self.targetId(),
            'link_type': self.__link_type,
            'context': self.__context,
            'position': self.__position,
            'created_at': self.__created_at,
            'created_by_id': self.createdById(),
            'is_active': self.__is_active,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__id = state.get('id')
        self.__link_type = state.get('link_type', LinkType.REFERENCE)
        self.__context = state.get('context', '')
        self.__position = state.get('position', 0)
        self.__created_at = state.get('created_at', Now())
        self.__is_active = state.get('is_active', True)
    
    def id(self):
        """返回唯一标识符。"""
        return self.__id
    
    def source(self):
        """返回源实体。"""
        return self.__source_ref()
    
    def sourceId(self):
        """返回源实体ID。"""
        source = self.source()
        return source.id() if source else ''
    
    def setSource(self, source):
        """设置源实体。"""
        self.__source_ref = weakref.ref(source) if source else lambda: None
    
    def target(self):
        """返回目标实体。"""
        return self.__target_ref()
    
    def targetId(self):
        """返回目标实体ID。"""
        target = self.target()
        return target.id() if target else ''
    
    def setTarget(self, target):
        """设置目标实体。"""
        self.__target_ref = weakref.ref(target) if target else lambda: None
    
    def linkType(self):
        """返回链接类型。"""
        return self.__link_type
    
    def setLinkType(self, link_type):
        """设置链接类型。"""
        self.__link_type = link_type
    
    def linkTypeLabel(self):
        """返回链接类型标签。"""
        return LinkType.getLabel(self.__link_type)
    
    def inverseLinkType(self):
        """返回反向链接类型。"""
        return LinkType.getInverseType(self.__link_type)
    
    def context(self):
        """返回链接上下文。"""
        return self.__context
    
    def setContext(self, context):
        """设置链接上下文。"""
        self.__context = context
    
    def position(self):
        """返回链接位置。"""
        return self.__position
    
    def setPosition(self, position):
        """设置链接位置。"""
        self.__position = position
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
    
    def createdBy(self):
        """返回创建者。"""
        return self.__created_by_ref()
    
    def createdById(self):
        """返回创建者ID。"""
        created_by = self.createdBy()
        return created_by.id() if created_by else ''
    
    def setCreatedBy(self, created_by):
        """设置创建者。"""
        self.__created_by_ref = weakref.ref(created_by) if created_by else lambda: None
    
    def isActive(self):
        """返回是否激活。"""
        return self.__is_active
    
    def activate(self):
        """激活链接。"""
        self.__is_active = True
    
    def deactivate(self):
        """停用链接。"""
        self.__is_active = False
    
    def createInverse(self):
        """
        创建反向链接。
        
        Returns:
            Link实例（反向链接）
        """
        return Link(
            source=self.target(),
            target=self.source(),
            link_type=self.inverseLinkType(),
            context=self.__context,
            created_by=self.createdBy(),
        )


class LinkRegistry:
    """
    链接注册表类。
    
    管理所有链接的存储、查询和索引。
    """
    
    def __init__(self):
        self.__links = []
        self.__by_source = {}
        self.__by_target = {}
        self.__listeners = []
    
    def registerLink(self, source, target, link_type=LinkType.REFERENCE, 
                    context='', position=0, created_by=None):
        """
        注册链接。
        
        Args:
            source: 源实体
            target: 目标实体
            link_type: 链接类型
            context: 上下文
            position: 位置
            created_by: 创建者
            
        Returns:
            Link实例
        """
        link = Link(
            source=source,
            target=target,
            link_type=link_type,
            context=context,
            position=position,
            created_by=created_by,
        )
        
        self.__links.append(link)
        
        source_id = source.id() if source else ''
        if source_id not in self.__by_source:
            self.__by_source[source_id] = []
        self.__by_source[source_id].append(link)
        
        target_id = target.id() if target else ''
        if target_id not in self.__by_target:
            self.__by_target[target_id] = []
        self.__by_target[target_id].append(link)
        
        self._notify_link_registered(link)
        
        return link
    
    def unregisterLink(self, link):
        """
        注销链接。
        
        Args:
            link: 要注销的链接
            
        Returns:
            bool: 是否成功
        """
        if link in self.__links:
            self.__links.remove(link)
            
            source_id = link.sourceId()
            if source_id in self.__by_source and link in self.__by_source[source_id]:
                self.__by_source[source_id].remove(link)
            
            target_id = link.targetId()
            if target_id in self.__by_target and link in self.__by_target[target_id]:
                self.__by_target[target_id].remove(link)
            
            self._notify_link_unregistered(link)
            return True
        
        return False
    
    def getLinksFromSource(self, source_id, link_type=None):
        """
        获取从指定源发出的链接。
        
        Args:
            source_id: 源实体ID
            link_type: 链接类型过滤（可选）
            
        Returns:
            链接列表
        """
        links = self.__by_source.get(source_id, [])
        if link_type:
            links = [l for l in links if l.linkType() == link_type]
        return links
    
    def getLinksToTarget(self, target_id, link_type=None):
        """
        获取指向指定目标的链接。
        
        Args:
            target_id: 目标实体ID
            link_type: 链接类型过滤（可选）
            
        Returns:
            链接列表
        """
        links = self.__by_target.get(target_id, [])
        if link_type:
            links = [l for l in links if l.linkType() == link_type]
        return links
    
    def getBidirectionalLinks(self, entity_id):
        """
        获取实体的所有双向链接。
        
        Args:
            entity_id: 实体ID
            
        Returns:
            链接列表
        """
        outgoing = self.getLinksFromSource(entity_id)
        incoming = self.getLinksToTarget(entity_id)
        return outgoing + incoming
    
    def getLinkedEntities(self, entity_id, direction='both'):
        """
        获取链接的实体列表。
        
        Args:
            entity_id: 实体ID
            direction: 方向 ('outgoing', 'incoming', 'both')
            
        Returns:
            实体列表
        """
        entities = []
        
        if direction in ('outgoing', 'both'):
            for link in self.getLinksFromSource(entity_id):
                target = link.target()
                if target and target not in entities:
                    entities.append(target)
        
        if direction in ('incoming', 'both'):
            for link in self.getLinksToTarget(entity_id):
                source = link.source()
                if source and source not in entities:
                    entities.append(source)
        
        return entities
    
    def getLinkedEntityIds(self, entity_id, direction='both'):
        """
        获取链接的实体ID列表。
        
        Args:
            entity_id: 实体ID
            direction: 方向
            
        Returns:
            实体ID列表
        """
        ids = set()
        
        if direction in ('outgoing', 'both'):
            for link in self.getLinksFromSource(entity_id):
                ids.add(link.targetId())
        
        if direction in ('incoming', 'both'):
            for link in self.getLinksToTarget(entity_id):
                ids.add(link.sourceId())
        
        return list(ids)
    
    def areLinked(self, source_id, target_id):
        """
        检查两个实体是否有链接。
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            
        Returns:
            bool: 是否有链接
        """
        for link in self.getLinksFromSource(source_id):
            if link.targetId() == target_id:
                return True
        return False
    
    def getLinkBetween(self, source_id, target_id):
        """
        获取两个实体之间的链接。
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            
        Returns:
            Link实例或None
        """
        for link in self.getLinksFromSource(source_id):
            if link.targetId() == target_id:
                return link
        return None
    
    def count(self):
        """返回链接总数。"""
        return len(self.__links)
    
    def clear(self):
        """清除所有链接。"""
        self.__links.clear()
        self.__by_source.clear()
        self.__by_target.clear()
    
    def addLinkListener(self, listener):
        """
        添加链接监听器。
        
        Args:
            listener: 监听函数，签名为 listener(link, event_type)
        """
        self.__listeners.append(listener)
    
    def removeLinkListener(self, listener):
        """
        移除链接监听器。
        
        Args:
            listener: 监听函数
        """
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_link_registered(self, link):
        """通知链接注册。"""
        for listener in self.__listeners:
            try:
                listener(link, 'registered')
            except Exception:
                pass
    
    def _notify_link_unregistered(self, link):
        """通知链接注销。"""
        for listener in self.__listeners:
            try:
                listener(link, 'unregistered')
            except Exception:
                pass
