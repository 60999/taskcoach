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

Knowledge search module for full-text search.
"""

import re
from collections import defaultdict


class KnowledgeSearch:
    """
    知识库搜索类。
    
    提供全文搜索和索引功能。
    """
    
    def __init__(self):
        self.__index = defaultdict(list)
        self.__documents = {}
        self.__stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 
                            'be', 'been', 'being', 'have', 'has', 'had',
                            'do', 'does', 'did', 'will', 'would', 'could',
                            'should', 'may', 'might', 'must', 'shall',
                            '的', '是', '在', '有', '和', '与', '或', '了'}
    
    def indexDocument(self, document):
        """
        索引文档。
        
        Args:
            document: Document实例
        """
        doc_id = document.id()
        self.__documents[doc_id] = document
        
        self._removeFromIndex(doc_id)
        
        text = f"{document.subject()} {document.content()}"
        words = self._tokenize(text)
        
        word_positions = defaultdict(list)
        for position, word in enumerate(words):
            if word not in self.__stop_words:
                word_positions[word].append(position)
        
        for word, positions in word_positions.items():
            self.__index[word].append({
                'doc_id': doc_id,
                'positions': positions,
                'frequency': len(positions),
            })
    
    def removeDocument(self, doc_id):
        """
        从索引中移除文档。
        
        Args:
            doc_id: 文档ID
        """
        self._removeFromIndex(doc_id)
        if doc_id in self.__documents:
            del self.__documents[doc_id]
    
    def _removeFromIndex(self, doc_id):
        """从索引中移除文档条目。"""
        for word in list(self.__index.keys()):
            self.__index[word] = [
                entry for entry in self.__index[word] 
                if entry['doc_id'] != doc_id
            ]
            if not self.__index[word]:
                del self.__index[word]
    
    def search(self, query, limit=20):
        """
        搜索文档。
        
        Args:
            query: 搜索查询
            limit: 最大结果数
            
        Returns:
            搜索结果列表，每项包含 document 和 score
        """
        words = self._tokenize(query)
        if not words:
            return []
        
        doc_scores = defaultdict(float)
        
        for word in words:
            if word in self.__index:
                for entry in self.__index[word]:
                    doc_id = entry['doc_id']
                    doc_scores[doc_id] += entry['frequency']
        
        if len(words) > 1:
            phrase_bonus = self._searchPhrase(query)
            for doc_id in phrase_bonus:
                doc_scores[doc_id] += phrase_bonus[doc_id] * 2
        
        sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_results[:limit]:
            if doc_id in self.__documents:
                results.append({
                    'document': self.__documents[doc_id],
                    'score': score,
                })
        
        return results
    
    def _searchPhrase(self, phrase):
        """搜索短语。"""
        words = self._tokenize(phrase)
        if len(words) < 2:
            return {}
        
        doc_phrase_counts = defaultdict(int)
        
        first_word = words[0]
        if first_word not in self.__index:
            return {}
        
        for entry in self.__index[first_word]:
            doc_id = entry['doc_id']
            positions = entry['positions']
            
            for start_pos in positions:
                match = True
                for i, word in enumerate(words[1:], 1):
                    if word not in self.__index:
                        match = False
                        break
                    
                    word_entries = [e for e in self.__index[word] 
                                  if e['doc_id'] == doc_id]
                    if not word_entries:
                        match = False
                        break
                    
                    word_positions = word_entries[0]['positions']
                    if start_pos + i not in word_positions:
                        match = False
                        break
                
                if match:
                    doc_phrase_counts[doc_id] += 1
        
        return doc_phrase_counts
    
    def _tokenize(self, text):
        """
        分词。
        
        Args:
            text: 文本
            
        Returns:
            词列表
        """
        text = text.lower()
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        words = text.split()
        
        words = [w for w in words if w and w not in self.__stop_words]
        
        return words
    
    def getSuggestions(self, prefix, limit=10):
        """
        获取搜索建议。
        
        Args:
            prefix: 前缀
            limit: 最大建议数
            
        Returns:
            建议词列表
        """
        prefix = prefix.lower()
        suggestions = []
        
        for word in self.__index.keys():
            if word.startswith(prefix):
                total_freq = sum(e['frequency'] for e in self.__index[word])
                suggestions.append((word, total_freq))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        return [s[0] for s in suggestions[:limit]]
    
    def getRelatedDocuments(self, doc_id, limit=5):
        """
        获取相关文档。
        
        Args:
            doc_id: 文档ID
            limit: 最大结果数
            
        Returns:
            相关文档列表
        """
        if doc_id not in self.__documents:
            return []
        
        document = self.__documents[doc_id]
        text = f"{document.subject()} {document.content()}"
        words = set(self._tokenize(text))
        
        doc_scores = defaultdict(float)
        
        for word in words:
            if word in self.__index:
                for entry in self.__index[word]:
                    if entry['doc_id'] != doc_id:
                        doc_scores[entry['doc_id']] += entry['frequency']
        
        sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for related_id, score in sorted_results[:limit]:
            if related_id in self.__documents:
                results.append({
                    'document': self.__documents[related_id],
                    'score': score,
                })
        
        return results
    
    def getWordCloud(self, limit=50):
        """
        获取词云数据。
        
        Args:
            limit: 最大词数
            
        Returns:
            词频列表
        """
        word_freq = []
        
        for word, entries in self.__index.items():
            total_freq = sum(e['frequency'] for e in entries)
            word_freq.append((word, total_freq))
        
        word_freq.sort(key=lambda x: x[1], reverse=True)
        
        return word_freq[:limit]
    
    def clear(self):
        """清除索引。"""
        self.__index.clear()
        self.__documents.clear()
    
    def documentCount(self):
        """返回索引文档数。"""
        return len(self.__documents)
    
    def wordCount(self):
        """返回索引词数。"""
        return len(self.__index)
