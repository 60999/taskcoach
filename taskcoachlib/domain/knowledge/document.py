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

Document entity for knowledge base.
"""

from taskcoachlib.domain.base import object as base_object
from taskcoachlib.domain.date import DateTime, Now
from taskcoachlib import patterns
import weakref


class Document(base_object.Object):
    """
    文档实体类。
    
    知识库中的文档，支持Markdown格式和双向链接。
    
    Attributes:
        __content: 文档内容（Markdown格式）
        __author: 作者（弱引用）
        __tags: 标签列表
        __category: 分类
        __organization: 所属组织（弱引用）
        __created_at: 创建时间
        __updated_at: 更新时间
        __version: 版本号
        __is_published: 是否发布
        __linked_tasks: 关联任务ID列表
        __linked_documents: 关联文档ID列表
    """
    
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        organization = kwargs.pop('organization', None)
        
        self.__author_ref = weakref.ref(author) if author else lambda: None
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
        
        self.__content = kwargs.pop('content', '')
        self.__tags = kwargs.pop('tags', [])
        self.__category = kwargs.pop('category', '')
        self.__created_at = kwargs.pop('created_at', None) or Now()
        self.__updated_at = kwargs.pop('updated_at', None) or self.__created_at
        self.__version = kwargs.pop('version', 1)
        self.__is_published = kwargs.pop('is_published', False)
        self.__linked_tasks = kwargs.pop('linked_tasks', [])
        self.__linked_documents = kwargs.pop('linked_documents', [])
        
        super().__init__(*args, **kwargs)
    
    def __getstate__(self):
        state = super().__getstate__()
        state.update({
            'content': self.__content,
            'author_id': self.authorId(),
            'tags': self.__tags,
            'category': self.__category,
            'organization_id': self.organizationId(),
            'created_at': self.__created_at,
            'updated_at': self.__updated_at,
            'version': self.__version,
            'is_published': self.__is_published,
            'linked_tasks': self.__linked_tasks,
            'linked_documents': self.__linked_documents,
        })
        return state
    
    @patterns.eventSource
    def __setstate__(self, state, event=None):
        super().__setstate__(state, event=event)
        self.__content = state.get('content', '')
        self.__tags = state.get('tags', [])
        self.__category = state.get('category', '')
        self.__created_at = state.get('created_at', Now())
        self.__updated_at = state.get('updated_at', self.__created_at)
        self.__version = state.get('version', 1)
        self.__is_published = state.get('is_published', False)
        self.__linked_tasks = state.get('linked_tasks', [])
        self.__linked_documents = state.get('linked_documents', [])
    
    @classmethod
    def monitoredAttributes(class_):
        return super(Document, class_).monitoredAttributes() + ['content', 'tags']
    
    def content(self):
        """返回文档内容。"""
        return self.__content
    
    @patterns.eventSource
    def setContent(self, content, event=None):
        """设置文档内容。"""
        self.__content = content
        self.__updated_at = Now()
        self.__version += 1
        event.addSource(self, content, type=self.contentChangedEventType())
    
    def author(self):
        """返回作者。"""
        return self.__author_ref()
    
    def authorId(self):
        """返回作者ID。"""
        author = self.author()
        return author.id() if author else ''
    
    def setAuthor(self, author):
        """设置作者。"""
        self.__author_ref = weakref.ref(author) if author else lambda: None
    
    def tags(self):
        """返回标签列表。"""
        return list(self.__tags)
    
    @patterns.eventSource
    def addTag(self, tag, event=None):
        """添加标签。"""
        if tag not in self.__tags:
            self.__tags.append(tag)
            event.addSource(self, tag, type=self.tagsChangedEventType())
    
    @patterns.eventSource
    def removeTag(self, tag, event=None):
        """移除标签。"""
        if tag in self.__tags:
            self.__tags.remove(tag)
            event.addSource(self, tag, type=self.tagsChangedEventType())
    
    def hasTag(self, tag):
        """检查是否有指定标签。"""
        return tag in self.__tags
    
    def category(self):
        """返回分类。"""
        return self.__category
    
    def setCategory(self, category):
        """设置分类。"""
        self.__category = category
    
    def organization(self):
        """返回所属组织。"""
        return self.__organization_ref()
    
    def organizationId(self):
        """返回组织ID。"""
        org = self.organization()
        return org.id() if org else ''
    
    def setOrganization(self, organization):
        """设置所属组织。"""
        self.__organization_ref = weakref.ref(organization) if organization else lambda: None
    
    def createdAt(self):
        """返回创建时间。"""
        return self.__created_at
    
    def updatedAt(self):
        """返回更新时间。"""
        return self.__updated_at
    
    def version(self):
        """返回版本号。"""
        return self.__version
    
    def isPublished(self):
        """返回是否发布。"""
        return self.__is_published
    
    def publish(self):
        """发布文档。"""
        self.__is_published = True
    
    def unpublish(self):
        """取消发布。"""
        self.__is_published = False
    
    def linkedTasks(self):
        """返回关联任务ID列表。"""
        return list(self.__linked_tasks)
    
    def addLinkedTask(self, task_id):
        """添加关联任务。"""
        if task_id not in self.__linked_tasks:
            self.__linked_tasks.append(task_id)
    
    def removeLinkedTask(self, task_id):
        """移除关联任务。"""
        if task_id in self.__linked_tasks:
            self.__linked_tasks.remove(task_id)
    
    def linkedDocuments(self):
        """返回关联文档ID列表。"""
        return list(self.__linked_documents)
    
    def addLinkedDocument(self, doc_id):
        """添加关联文档。"""
        if doc_id not in self.__linked_documents:
            self.__linked_documents.append(doc_id)
    
    def removeLinkedDocument(self, doc_id):
        """移除关联文档。"""
        if doc_id in self.__linked_documents:
            self.__linked_documents.remove(doc_id)
    
    def wordCount(self):
        """返回字数统计。"""
        return len(self.__content.split())
    
    def excerpt(self, length=200):
        """返回文档摘要。"""
        if len(self.__content) <= length:
            return self.__content
        return self.__content[:length] + '...'
    
    @classmethod
    def contentChangedEventType(class_):
        return '%s.content' % class_
    
    @classmethod
    def tagsChangedEventType(class_):
        return '%s.tags' % class_
    
    @classmethod
    def modificationEventTypes(class_):
        return super(Document, class_).modificationEventTypes() + [
            class_.contentChangedEventType(),
            class_.tagsChangedEventType(),
        ]


class DocumentCollection:
    """
    文档集合类。
    
    管理文档的存储、查询和索引。
    """
    
    def __init__(self):
        self.__documents = []
        self.__by_id = {}
        self.__by_author = {}
        self.__by_category = {}
        self.__by_tag = {}
        self.__listeners = []
    
    def addDocument(self, document):
        """
        添加文档。
        
        Args:
            document: Document实例
        """
        self.__documents.append(document)
        self.__by_id[document.id()] = document
        
        author_id = document.authorId()
        if author_id not in self.__by_author:
            self.__by_author[author_id] = []
        self.__by_author[author_id].append(document)
        
        category = document.category()
        if category:
            if category not in self.__by_category:
                self.__by_category[category] = []
            self.__by_category[category].append(document)
        
        for tag in document.tags():
            if tag not in self.__by_tag:
                self.__by_tag[tag] = []
            self.__by_tag[tag].append(document)
        
        self._notify_document_added(document)
    
    def removeDocument(self, document):
        """
        移除文档。
        
        Args:
            document: Document实例
        """
        if document in self.__documents:
            self.__documents.remove(document)
            del self.__by_id[document.id()]
            
            author_id = document.authorId()
            if author_id in self.__by_author and document in self.__by_author[author_id]:
                self.__by_author[author_id].remove(document)
            
            category = document.category()
            if category in self.__by_category and document in self.__by_category[category]:
                self.__by_category[category].remove(document)
            
            for tag in document.tags():
                if tag in self.__by_tag and document in self.__by_tag[tag]:
                    self.__by_tag[tag].remove(document)
            
            self._notify_document_removed(document)
    
    def getDocument(self, doc_id):
        """根据ID获取文档。"""
        return self.__by_id.get(doc_id)
    
    def getDocumentsByAuthor(self, author_id):
        """根据作者获取文档。"""
        return self.__by_author.get(author_id, [])
    
    def getDocumentsByCategory(self, category):
        """根据分类获取文档。"""
        return self.__by_category.get(category, [])
    
    def getDocumentsByTag(self, tag):
        """根据标签获取文档。"""
        return self.__by_tag.get(tag, [])
    
    def getAllDocuments(self):
        """获取所有文档。"""
        return list(self.__documents)
    
    def getPublishedDocuments(self):
        """获取已发布文档。"""
        return [d for d in self.__documents if d.isPublished()]
    
    def count(self):
        """返回文档总数。"""
        return len(self.__documents)
    
    def getAllCategories(self):
        """获取所有分类。"""
        return list(self.__by_category.keys())
    
    def getAllTags(self):
        """获取所有标签。"""
        return list(self.__by_tag.keys())
    
    def addDocumentListener(self, listener):
        """添加文档监听器。"""
        self.__listeners.append(listener)
    
    def removeDocumentListener(self, listener):
        """移除文档监听器。"""
        if listener in self.__listeners:
            self.__listeners.remove(listener)
    
    def _notify_document_added(self, document):
        """通知文档添加。"""
        for listener in self.__listeners:
            try:
                listener(document, 'added')
            except Exception:
                pass
    
    def _notify_document_removed(self, document):
        """通知文档移除。"""
        for listener in self.__listeners:
            try:
                listener(document, 'removed')
            except Exception:
                pass
    
    def clear(self):
        """清除所有文档。"""
        self.__documents.clear()
        self.__by_id.clear()
        self.__by_author.clear()
        self.__by_category.clear()
        self.__by_tag.clear()
