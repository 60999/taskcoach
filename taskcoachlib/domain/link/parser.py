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

Link parser for extracting links from text content.
"""

import re
from abc import ABC, abstractmethod


class LinkParser(ABC):
    """
    链接解析器抽象基类。
    
    定义链接解析的接口。
    """
    
    @abstractmethod
    def parse(self, text):
        """
        解析文本中的链接。
        
        Args:
            text: 文本内容
            
        Returns:
            链接信息列表，每项为字典格式
        """
        pass
    
    @abstractmethod
    def findLinkPositions(self, text):
        """
        查找文本中链接的位置。
        
        Args:
            text: 文本内容
            
        Returns:
            位置列表，每项为 (start, end, link_info)
        """
        pass


class MarkdownLinkParser(LinkParser):
    """
    Markdown链接解析器。
    
    支持解析以下格式的链接：
    - [[任务名称]] - 内部链接
    - [[任务名称|显示文本]] - 带别名的内部链接
    - [显示文本](任务名称) - Markdown格式链接
    - #任务ID - 快捷ID链接
    - task:任务ID - 协议格式链接
    """
    
    WIKI_LINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
    MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    ID_LINK_PATTERN = re.compile(r'#(\w+)')
    PROTOCOL_LINK_PATTERN = re.compile(r'(task|note|category|board):(\w+)')
    URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    
    def __init__(self, entity_lookup_func=None):
        """
        初始化解析器。
        
        Args:
            entity_lookup_func: 实体查找函数，签名为 func(identifier) -> entity
        """
        self._entity_lookup_func = entity_lookup_func
    
    def setEntityLookupFunc(self, func):
        """设置实体查找函数。"""
        self._entity_lookup_func = func
    
    def parse(self, text):
        """
        解析文本中的所有链接。
        
        Args:
            text: 文本内容
            
        Returns:
            链接信息列表，每项包含：
            - type: 链接类型
            - target: 目标标识符
            - display_text: 显示文本
            - start: 起始位置
            - end: 结束位置
        """
        links = []
        
        links.extend(self._parse_wiki_links(text))
        links.extend(self._parse_markdown_links(text))
        links.extend(self._parse_id_links(text))
        links.extend(self._parse_protocol_links(text))
        links.extend(self._parse_url_links(text))
        
        links.sort(key=lambda x: x['start'])
        
        return links
    
    def _parse_wiki_links(self, text):
        """解析Wiki格式链接 [[任务名称]] 或 [[任务名称|显示文本]]。"""
        links = []
        for match in self.WIKI_LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            display_text = match.group(2).strip() if match.group(2) else target
            
            links.append({
                'type': 'wiki',
                'target': target,
                'display_text': display_text,
                'start': match.start(),
                'end': match.end(),
                'raw': match.group(0),
            })
        
        return links
    
    def _parse_markdown_links(self, text):
        """解析Markdown格式链接 [显示文本](目标)。"""
        links = []
        for match in self.MARKDOWN_LINK_PATTERN.finditer(text):
            display_text = match.group(1).strip()
            target = match.group(2).strip()
            
            if target.startswith('http://') or target.startswith('https://'):
                continue
            
            links.append({
                'type': 'markdown',
                'target': target,
                'display_text': display_text,
                'start': match.start(),
                'end': match.end(),
                'raw': match.group(0),
            })
        
        return links
    
    def _parse_id_links(self, text):
        """解析ID格式链接 #任务ID。"""
        links = []
        for match in self.ID_LINK_PATTERN.finditer(text):
            target = match.group(1)
            
            links.append({
                'type': 'id',
                'target': target,
                'display_text': f'#{target}',
                'start': match.start(),
                'end': match.end(),
                'raw': match.group(0),
            })
        
        return links
    
    def _parse_protocol_links(self, text):
        """解析协议格式链接 task:任务ID。"""
        links = []
        for match in self.PROTOCOL_LINK_PATTERN.finditer(text):
            entity_type = match.group(1)
            target = match.group(2)
            
            links.append({
                'type': 'protocol',
                'target': target,
                'entity_type': entity_type,
                'display_text': f'{entity_type}:{target}',
                'start': match.start(),
                'end': match.end(),
                'raw': match.group(0),
            })
        
        return links
    
    def _parse_url_links(self, text):
        """解析URL链接。"""
        links = []
        for match in self.URL_PATTERN.finditer(text):
            url = match.group(0)
            
            links.append({
                'type': 'url',
                'target': url,
                'display_text': url,
                'start': match.start(),
                'end': match.end(),
                'raw': url,
            })
        
        return links
    
    def findLinkPositions(self, text):
        """
        查找文本中链接的位置。
        
        Args:
            text: 文本内容
            
        Returns:
            位置列表，每项为 (start, end, link_info)
        """
        links = self.parse(text)
        return [(link['start'], link['end'], link) for link in links]
    
    def extractTargets(self, text):
        """
        提取文本中的所有目标标识符。
        
        Args:
            text: 文本内容
            
        Returns:
            目标标识符列表
        """
        links = self.parse(text)
        return [link['target'] for link in links if link['type'] != 'url']
    
    def resolveEntity(self, identifier):
        """
        解析标识符对应的实体。
        
        Args:
            identifier: 标识符（名称或ID）
            
        Returns:
            实体对象或None
        """
        if self._entity_lookup_func:
            return self._entity_lookup_func(identifier)
        return None
    
    def renderLink(self, link_info, entity=None):
        """
        渲染链接为显示格式。
        
        Args:
            link_info: 链接信息
            entity: 目标实体（可选）
            
        Returns:
            渲染后的字符串
        """
        if entity:
            display = getattr(entity, 'subject', lambda: link_info['display_text'])()
            return f'[[{entity.id()}|{display}]]'
        else:
            return link_info.get('raw', link_info['display_text'])
    
    def hasLinks(self, text):
        """
        检查文本是否包含链接。
        
        Args:
            text: 文本内容
            
        Returns:
            bool: 是否包含链接
        """
        return bool(
            self.WIKI_LINK_PATTERN.search(text) or
            self.MARKDOWN_LINK_PATTERN.search(text) or
            self.ID_LINK_PATTERN.search(text) or
            self.PROTOCOL_LINK_PATTERN.search(text) or
            self.URL_PATTERN.search(text)
        )
    
    def countLinks(self, text):
        """
        统计文本中的链接数量。
        
        Args:
            text: 文本内容
            
        Returns:
            链接数量
        """
        return len(self.parse(text))
    
    def replaceLinks(self, text, replacement_func):
        """
        替换文本中的链接。
        
        Args:
            text: 文本内容
            replacement_func: 替换函数，签名为 func(link_info) -> str
            
        Returns:
            替换后的文本
        """
        links = self.parse(text)
        if not links:
            return text
        
        result = []
        last_end = 0
        
        for link in links:
            result.append(text[last_end:link['start']])
            result.append(replacement_func(link))
            last_end = link['end']
        
        result.append(text[last_end:])
        
        return ''.join(result)
    
    def stripLinks(self, text):
        """
        移除文本中的链接标记，只保留显示文本。
        
        Args:
            text: 文本内容
            
        Returns:
            清理后的文本
        """
        def strip_link(link_info):
            return link_info['display_text']
        
        return self.replaceLinks(text, strip_link)
