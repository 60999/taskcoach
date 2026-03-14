# Markdown 双向链接实现方案

## 概述

本文档描述如何在 Markdown 文件中实现类似 Logseq/Obsidian 的双向链接功能，包括：
- `[[页面名]]` - 页面链接
- `((块引用))` - 块引用（自动转换）

---

## 一、语法规范

### 1.1 页面链接 `[[页面名]]`

| 语法 | 说明 | 示例 |
|------|------|------|
| `[[页面名]]` | 基础链接 | `[[项目管理]]` |
| `[[页面名\|显示文本]]` | 带别名 | `[[Python基础\|学习笔记]]` |
| `[[页面名#标题]]` | 链接到标题 | `[[设计模式#单例模式]]` |
| `[[页面名#标题\|别名]]` | 完整语法 | `[[架构设计#MVC\|MVC模式]]` |

### 1.2 块引用 `((块引用ID))`

| 语法 | 说明 | 示例 |
|------|------|------|
| `((块ID))` | 引用特定块 | `((20240101T120000))` |
| `((块ID\|显示文本))` | 带别名引用 | `((abc123\|重要段落))` |

块ID生成规则：使用时间戳或UUID，如 `20240115T143052` 或 `^block-abc123`

---

## 二、技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        应用层 (Application)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  编辑器组件  │  │  预览组件   │  │  反向链接面板            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      服务层 (Service)                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    LinkService                           │    │
│  │  - parseLinks()      解析链接                            │    │
│  │  - resolveLink()     解析链接目标                        │    │
│  │  - getBacklinks()    获取反向链接                        │    │
│  │  - getBlockContent() 获取块内容                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      索引层 (Index)                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐   │
│  │ PageIndex     │  │ LinkIndex     │  │ BlockIndex        │   │
│  │ - 页面元数据   │  │ - 链接关系图   │  │ - 块ID映射        │   │
│  └───────────────┘  └───────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      存储层 (Storage)                            │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐   │
│  │ 文件系统      │  │ 缓存数据库     │  │ 配置文件          │   │
│  │ *.md 文件     │  │ SQLite/JSON   │  │ settings.json     │   │
│  └───────────────┘  └───────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 数据流程

```
用户输入 [[目标页面]]
        │
        ▼
┌───────────────────┐
│ 1. 语法解析       │  ← LinkParser
│    识别链接语法   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ 2. 链接解析       │  ← LinkResolver
│    查找目标文件   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ 3. 索引更新       │  ← IndexManager
│    更新链接关系   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ 4. 渲染/跳转      │  ← UI Component
│    显示或导航     │
└───────────────────┘
```

---

## 三、核心模块设计

### 3.1 模块结构

```
bidirectional_link/
├── __init__.py              # 模块入口
├── parser.py                # 语法解析器
├── resolver.py              # 链接解析器
├── indexer.py               # 索引管理器
├── models.py                # 数据模型
├── cache.py                 # 缓存管理
├── file_watcher.py          # 文件监听器
└── utils.py                 # 工具函数
```

### 3.2 数据模型

```python
# models.py

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class LinkType(Enum):
    """链接类型枚举"""
    PAGE_LINK = "page"        # [[页面名]]
    BLOCK_REF = "block"       # ((块ID))
    HEADING_LINK = "heading"  # [[页面名#标题]]


@dataclass
class Link:
    """链接数据模型"""
    link_type: LinkType                    # 链接类型
    target: str                            # 目标（页面名或块ID）
    display_text: Optional[str] = None     # 显示文本（别名）
    heading: Optional[str] = None          # 标题（如果有）
    source_file: str = ""                  # 来源文件
    line_number: int = 0                   # 行号
    position: tuple = (0, 0)               # (start, end) 字符位置


@dataclass
class Page:
    """页面数据模型"""
    name: str                              # 页面名称
    file_path: str                         # 文件路径
    title: Optional[str] = None            # 标题
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    outgoing_links: list = field(default_factory=list)   # 出链
    incoming_links: list = field(default_factory=list)   # 入链（反向链接）


@dataclass
class Block:
    """块数据模型"""
    block_id: str                          # 块ID
    content: str                           # 块内容
    file_path: str                         # 所属文件
    line_start: int = 0                    # 起始行
    line_end: int = 0                      # 结束行
    heading: Optional[str] = None          # 所属标题
```

### 3.3 语法解析器

```python
# parser.py

import re
from typing import List, Optional
from .models import Link, LinkType


class LinkParser:
    """
    双向链接语法解析器。
    
    支持解析以下语法：
    - [[页面名]]
    - [[页面名|显示文本]]
    - [[页面名#标题]]
    - ((块ID))
    - ((块ID|显示文本))
    """
    
    PAGE_LINK_PATTERN = re.compile(
        r'\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]'
    )
    
    BLOCK_REF_PATTERN = re.compile(
        r'\(\(([^)|]+)(?:\|([^)]+))?\)\)'
    )
    
    def parse(self, content: str, source_file: str = "") -> List[Link]:
        """
        解析文本中的所有链接。
        
        Args:
            content: 要解析的文本内容
            source_file: 来源文件路径
            
        Returns:
            解析出的链接列表
        """
        links = []
        links.extend(self._parse_page_links(content, source_file))
        links.extend(self._parse_block_refs(content, source_file))
        return links
    
    def _parse_page_links(self, content: str, source_file: str) -> List[Link]:
        """解析页面链接 [[页面名]]"""
        links = []
        for match in self.PAGE_LINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            heading = match.group(2).strip() if match.group(2) else None
            display_text = match.group(3).strip() if match.group(3) else None
            
            link_type = LinkType.HEADING_LINK if heading else LinkType.PAGE_LINK
            
            links.append(Link(
                link_type=link_type,
                target=target,
                display_text=display_text,
                heading=heading,
                source_file=source_file,
                position=(match.start(), match.end())
            ))
        return links
    
    def _parse_block_refs(self, content: str, source_file: str) -> List[Link]:
        """解析块引用 ((块ID))"""
        links = []
        for match in self.BLOCK_REF_PATTERN.finditer(content):
            block_id = match.group(1).strip()
            display_text = match.group(2).strip() if match.group(2) else None
            
            links.append(Link(
                link_type=LinkType.BLOCK_REF,
                target=block_id,
                display_text=display_text,
                source_file=source_file,
                position=(match.start(), match.end())
            ))
        return links
    
    def extract_block_ids(self, content: str) -> List[str]:
        """提取内容中的所有块ID"""
        return [m.group(1).strip() for m in self.BLOCK_REF_PATTERN.finditer(content)]
```

### 3.4 索引管理器

```python
# indexer.py

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict
from .models import Link, Page, Block, LinkType
from .parser import LinkParser


class LinkIndex:
    """
    双向链接索引管理器。
    
    维护三种索引：
    1. 页面索引：页面名 -> 页面信息
    2. 正向链接索引：页面名 -> 链接目标列表
    3. 反向链接索引：页面名 -> 被引用来源列表
    """
    
    def __init__(self, vault_path: str):
        """
        初始化索引管理器。
        
        Args:
            vault_path: Markdown 文件夹路径
        """
        self.vault_path = Path(vault_path)
        self.parser = LinkParser()
        
        self.pages: Dict[str, Page] = {}
        self.blocks: Dict[str, Block] = {}
        self.forward_links: Dict[str, List[Link]] = defaultdict(list)
        self.backlinks: Dict[str, List[Link]] = defaultdict(list)
    
    def build_index(self) -> None:
        """构建完整索引"""
        for md_file in self.vault_path.rglob('*.md'):
            self._index_file(md_file)
    
    def _index_file(self, file_path: Path) -> None:
        """索引单个文件"""
        content = file_path.read_text(encoding='utf-8')
        page_name = file_path.stem
        
        page = Page(
            name=page_name,
            file_path=str(file_path),
            title=self._extract_title(content)
        )
        
        links = self.parser.parse(content, str(file_path))
        page.outgoing_links = links
        self.pages[page_name] = page
        
        for link in links:
            self.forward_links[page_name].append(link)
            self.backlinks[link.target].append(link)
        
        self._extract_blocks(content, str(file_path), page_name)
    
    def get_backlinks(self, page_name: str) -> List[Link]:
        """
        获取页面的反向链接。
        
        Args:
            page_name: 页面名称
            
        Returns:
            指向该页面的所有链接列表
        """
        return self.backlinks.get(page_name, [])
    
    def get_forward_links(self, page_name: str) -> List[Link]:
        """
        获取页面的正向链接。
        
        Args:
            page_name: 页面名称
            
        Returns:
            该页面指向的所有链接列表
        """
        return self.forward_links.get(page_name, [])
    
    def get_block_content(self, block_id: str) -> Optional[Block]:
        """
        获取块内容。
        
        Args:
            block_id: 块ID
            
        Returns:
            块对象，如果不存在返回 None
        """
        return self.blocks.get(block_id)
    
    def _extract_title(self, content: str) -> Optional[str]:
        """提取文件标题（第一个 # 标题）"""
        for line in content.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()
        return None
    
    def _extract_blocks(self, content: str, file_path: str, page_name: str) -> None:
        """提取文件中的块（带块ID的段落）"""
        block_id_pattern = r'\^([a-zA-Z0-9-]+)'
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            match = re.search(block_id_pattern, line)
            if match:
                block_id = match.group(1)
                self.blocks[block_id] = Block(
                    block_id=block_id,
                    content=line.replace(f'^{block_id}', '').strip(),
                    file_path=file_path,
                    line_start=i + 1,
                    line_end=i + 1
                )
```

---

## 四、实现方案对比

### 4.1 方案对比表

| 方案 | 适用场景 | 优点 | 缺点 | 复杂度 |
|------|----------|------|------|--------|
| **方案A: 纯Python解析** | 独立应用、CLI工具 | 无依赖、易集成 | 性能一般 | ⭐⭐ |
| **方案B: SQLite缓存** | 大型笔记库 | 查询快、持久化 | 需要数据库 | ⭐⭐⭐ |
| **方案C: 图数据库** | 复杂关系分析 | 关系查询强 | 依赖重 | ⭐⭐⭐⭐ |
| **方案D: 实时解析** | 编辑器插件 | 实时响应 | 每次重新解析 | ⭐ |

### 4.2 推荐方案

**对于 TaskCoach 项目，推荐方案A + 方案B 的组合：**

1. 使用纯 Python 解析器处理语法
2. 使用 JSON 文件缓存索引（轻量级）
3. 增量更新策略（只重新索引变化的文件）

---

## 五、与 TaskCoach 集成方案

### 5.1 集成点分析

TaskCoach 作为任务管理软件，可在以下位置集成双向链接：

| 集成位置 | 功能描述 |
|----------|----------|
| 任务描述 | 支持 `[[任务名]]` 链接到其他任务 |
| 笔记功能 | 支持 Markdown 双向链接 |
| 分类系统 | 使用 `[[分类名]]` 关联分类 |
| 文档导出 | 导出时保留链接关系 |

### 5.2 文件放置位置

```
taskcoachlib/
├── bidirectional_link/          # 新增模块
│   ├── __init__.py
│   ├── parser.py
│   ├── indexer.py
│   ├── models.py
│   └── utils.py
├── domain/
│   └── note/
│       └── note.py              # 修改：添加链接支持
└── gui/
    └── viewer/
        └── note.py              # 修改：渲染链接
```

---

## 六、测试用例

### 6.1 语法解析测试

```python
# test_parser.py

import unittest
from bidirectional_link.parser import LinkParser
from bidirectional_link.models import LinkType


class TestLinkParser(unittest.TestCase):
    """链接解析器测试"""
    
    def setUp(self):
        self.parser = LinkParser()
    
    def test_simple_page_link(self):
        """测试简单页面链接 [[页面名]]"""
        content = "这是一个 [[目标页面]] 链接"
        links = self.parser.parse(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "目标页面")
        self.assertEqual(links[0].link_type, LinkType.PAGE_LINK)
    
    def test_page_link_with_alias(self):
        """测试带别名的页面链接 [[页面名|显示文本]]"""
        content = "参见 [[Python基础|学习笔记]]"
        links = self.parser.parse(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "Python基础")
        self.assertEqual(links[0].display_text, "学习笔记")
    
    def test_page_link_with_heading(self):
        """测试带标题的页面链接 [[页面名#标题]]"""
        content = "参考 [[设计模式#单例模式]]"
        links = self.parser.parse(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "设计模式")
        self.assertEqual(links[0].heading, "单例模式")
        self.assertEqual(links[0].link_type, LinkType.HEADING_LINK)
    
    def test_block_reference(self):
        """测试块引用 ((块ID))"""
        content = "引用 ((20240115T143052))"
        links = self.parser.parse(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "20240115T143052")
        self.assertEqual(links[0].link_type, LinkType.BLOCK_REF)
    
    def test_multiple_links(self):
        """测试多个链接"""
        content = """
        这是 [[页面A]] 和 [[页面B|别名]] 
        以及 ((block123)) 的混合内容
        """
        links = self.parser.parse(content)
        self.assertEqual(len(links), 3)


if __name__ == '__main__':
    unittest.main()
```

### 6.2 索引测试

```python
# test_indexer.py

import unittest
import tempfile
import os
from pathlib import Path
from bidirectional_link.indexer import LinkIndex


class TestLinkIndex(unittest.TestCase):
    """索引管理器测试"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.index = LinkIndex(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_backlinks(self):
        """测试反向链接"""
        page_a = Path(self.temp_dir) / "PageA.md"
        page_b = Path(self.temp_dir) / "PageB.md"
        
        page_a.write_text("链接到 [[PageB]]", encoding='utf-8')
        page_b.write_text("这是 PageB", encoding='utf-8')
        
        self.index.build_index()
        
        backlinks = self.index.get_backlinks("PageB")
        self.assertEqual(len(backlinks), 1)
        self.assertEqual(backlinks[0].source_file, str(page_a))


if __name__ == '__main__':
    unittest.main()
```

---

## 七、性能优化策略

### 7.1 增量索引

```python
def update_index(self, changed_file: str) -> None:
    """
    增量更新索引。
    
    只重新处理变化的文件，而非全部重建。
    """
    page_name = Path(changed_file).stem
    
    if page_name in self.pages:
        old_links = self.forward_links.get(page_name, [])
        for link in old_links:
            self.backlinks[link.target] = [
                l for l in self.backlinks[link.target] 
                if l.source_file != changed_file
            ]
    
    self._index_file(Path(changed_file))
```

### 7.2 缓存策略

```python
# cache.py

import json
import hashlib
from pathlib import Path


class IndexCache:
    """
    索引缓存管理器。
    
    使用 JSON 文件存储索引，支持：
    - 快速加载
    - 增量更新
    - 文件哈希校验
    """
    
    CACHE_FILE = ".link_index_cache.json"
    
    def __init__(self, vault_path: str):
        self.cache_path = Path(vault_path) / self.CACHE_FILE
        self.file_hashes: Dict[str, str] = {}
    
    def get_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        content = Path(file_path).read_bytes()
        return hashlib.md5(content).hexdigest()
    
    def is_changed(self, file_path: str) -> bool:
        """检查文件是否变化"""
        current_hash = self.get_file_hash(file_path)
        stored_hash = self.file_hashes.get(file_path)
        return current_hash != stored_hash
    
    def save(self, index: 'LinkIndex') -> None:
        """保存索引到缓存"""
        data = {
            'pages': {k: {'name': v.name, 'file_path': v.file_path} 
                     for k, v in index.pages.items()},
            'backlinks': {k: [{'target': l.target, 'source_file': l.source_file} 
                             for l in v] 
                         for k, v in index.backlinks.items()},
            'file_hashes': self.file_hashes
        }
        self.cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    def load(self) -> Optional[dict]:
        """从缓存加载索引"""
        if self.cache_path.exists():
            return json.loads(self.cache_path.read_text())
        return None
```

---

## 八、总结

### 8.1 实现要点

1. **语法解析**：使用正则表达式匹配 `[[页面名]]` 和 `((块ID))`
2. **索引构建**：扫描所有文件，建立正向/反向链接映射
3. **增量更新**：监听文件变化，只更新变化的部分
4. **缓存机制**：使用 JSON 或 SQLite 存储索引，避免重复解析

### 8.2 扩展方向

| 扩展功能 | 描述 |
|----------|------|
| 图谱可视化 | 使用 D3.js 或 Cytoscape.js 展示链接关系图 |
| 全文搜索 | 结合 Whoosh 或 Elasticsearch 实现链接内容搜索 |
| 自动补全 | 输入 `[[` 时自动提示已有页面名 |
| 链接检测 | 检测断裂链接（目标不存在） |

### 8.3 参考资料

- [Wikilink 规范](https://github.com/tgrosinger/wikilink-spec)
- [Obsidian 开发文档](https://docs.obsidian.md/)
- [Logseq 开发文档](https://logseq.github.io/)
