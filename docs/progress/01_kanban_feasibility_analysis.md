# TaskCoach 看板视图等功能数据模型可行性分析报告

> 分析日期：2026-03-15  
> 分析目标：评估 TaskCoach 缺失功能是否可以在新增数据表、不修改现有数据表的情况下实现

---

## 一、现有数据表结构概述

### 1.1 核心域模型

TaskCoach 使用 **XML 文件存储**（`.tsk` 格式），而非传统关系数据库。数据模型基于 Python 类的继承体系：

```
Object (基类)
├── CompositeObject (组合对象，支持树形结构)
│   ├── Category (分类)
│   └── CategorizableCompositeObject (可分类的组合对象)
│       ├── Task (任务) - 核心实体
│       └── Note (笔记)
├── Effort (工作记录)
└── Attachment (附件)
    ├── FileAttachment
    ├── URIAttachment
    └── MailAttachment
```

### 1.2 现有实体属性详情

#### Task (任务)

| 属性类别 | 属性名 | 类型 | 说明 |
|---------|--------|------|------|
| **标识** | id | UUID | 唯一标识符 |
| | subject | String | 任务标题 |
| | description | String | 详细描述 |
| **日期时间** | plannedStartDateTime | DateTime | 计划开始时间 |
| | actualStartDateTime | DateTime | 实际开始时间 |
| | dueDateTime | DateTime | 截止时间 |
| | completionDateTime | DateTime | 完成时间 |
| | creationDateTime | DateTime | 创建时间 |
| | modificationDateTime | DateTime | 修改时间 |
| **进度** | percentageComplete | Integer | 完成百分比 (0-100) |
| | priority | Integer | 优先级 |
| | status | Enum | 状态 |
| **时间预算** | budget | TimeDelta | 预算时间 |
| | plannedDuration | TimeDelta | 计划持续时间 |
| **费用** | hourlyFee | Decimal | 时薪 |
| | fixedFee | Decimal | 固定费用 |
| **提醒** | reminder | DateTime | 提醒时间 |
| | recurrence | Recurrence | 重复规则 |
| **关系** | parent/children | Tree | 父子任务（已支持子任务嵌套） |
| | prerequisites | Set[Task] | 前置任务 |
| | dependencies | Set[Task] | 依赖任务 |
| | categories | Set[Category] | 所属分类（多对多） |
| | efforts | List[Effort] | 工作记录 |
| | notes | List[Note] | 备注 |
| | attachments | List[Attachment] | 附件 |

#### Category (分类)

| 属性名 | 类型 | 说明 |
|--------|------|------|
| id | UUID | 唯一标识符 |
| subject | String | 分类名称 |
| description | String | 描述 |
| parent/children | Tree | 树形结构 |
| categorizables | Set | 关联的任务/笔记 |
| filtered | Boolean | 是否过滤 |
| exclusiveSubcategories | Boolean | 互斥子分类 |
| stylePriority | Integer | 样式优先级 |
| fgColor/bgColor/font/icon | Style | 外观样式 |

#### Effort (工作记录)

| 属性名 | 类型 | 说明 |
|--------|------|------|
| id | UUID | 唯一标识符 |
| task | Task (外键) | 所属任务 |
| start | DateTime | 开始时间 |
| stop | DateTime | 结束时间 |
| entryMode | Enum | 记录模式 |
| description | String | 描述 |

#### Note (笔记)

| 属性名 | 类型 | 说明 |
|--------|------|------|
| id | UUID | 唯一标识符 |
| subject | String | 标题 |
| description | String | 内容 |
| categories | Set[Category] | 所属分类 |
| attachments | List[Attachment] | 附件 |

#### Attachment (附件)

| 属性名 | 类型 | 说明 |
|--------|------|------|
| id | UUID | 唯一标识符 |
| type_ | Enum | 类型 |
| location | String | 位置/路径 |
| subject | String | 标题 |
| description | String | 描述 |
| notes | List[Note] | 备注 |

---

## 二、看板视图功能所需的数据结构

### 2.1 看板核心概念

典型的看板视图包含以下核心元素：

```
看板
├── 列表/列 - 如：待办、进行中、已完成
│   └── 卡片 - 任务的可视化表示
└── 泳道 - 可选的横向分组
```

### 2.2 需要新增的数据表

#### 方案A：独立看板系统（推荐）

| 新增实体 | 属性 | 说明 |
|----------|------|------|
| **Board** | id, name, description, owner, created_at | 看板定义 |
| **BoardColumn** | id, board_id, name, position, wip_limit, color | 列定义 |
| **CardPosition** | id, task_id, column_id, position, swimlane_id | 卡片位置 |
| **Swimlane** | id, board_id, name, position | 泳道定义 |

#### 方案B：基于现有 Category 扩展（最小改动）

利用现有的 Category 系统实现看板：
- 每个 Board 对应一个 Category
- 每个 Column 对应一个子 Category
- 卡片位置通过 `ordering` 属性存储

---

## 三、缺失功能的数据需求分析

### 3.1 已支持的功能（无需新增）

| 功能 | 现有支持 | 实现方式 |
|------|----------|----------|
| **子任务嵌套** | ✅ 已支持 | Task.parent/children 树形结构 |
| **附件** | ✅ 已支持 | Attachment 类 + AttachmentOwner 混入 |
| **备注/评论** | ✅ 已支持 | Note 类 + NoteOwner 混入 |
| **提醒** | ✅ 已支持 | Task.reminder + scheduler |
| **时间跟踪** | ✅ 已支持 | Effort 类 |
| **分类/标签** | ✅ 已支持 | Category 类（可模拟标签） |
| **任务依赖** | ✅ 已支持 | Task.prerequisites/dependencies |
| **重复任务** | ✅ 已支持 | Task.recurrence |

### 3.2 需要新增数据表的功能

| 功能 | 数据需求 | 可行性 |
|------|----------|--------|
| **看板视图** | Board, BoardColumn, CardPosition, Swimlane | ✅ 完全可行 |
| **标签系统** | Tag, TaskTag 关联表 | ✅ 完全可行 |
| **评论系统** | Comment（独立于 Note） | ✅ 完全可行 |
| **自定义字段** | CustomField, CustomFieldValue | ✅ 完全可行 |
| **任务模板** | TaskTemplate | ✅ 完全可行 |
| **历史记录/审计** | HistoryLog | ✅ 完全可行 |
| **多看板支持** | Board 实体 | ✅ 完全可行 |

---

## 四、可行性结论和建议方案

### 4.1 核心结论

> **所有缺失功能都可以在新增数据表、不修改现有数据表结构的情况下实现。**

原因：
1. **XML 存储格式灵活**：新增实体只需添加新的 XML 节点类型，不影响现有节点
2. **UUID 标识系统**：所有实体使用 UUID，新增实体不会产生 ID 冲突
3. **松耦合架构**：域模型使用混入模式，新增功能通过新类实现
4. **外键关联**：新增表通过 UUID 引用现有实体，无需修改被引用表

### 4.2 推荐实现方案

#### 方案一：扩展 XML 存储格式

```xml
<!-- 现有结构保持不变 -->
<tasks>
  <task id="..." subject="...">...</task>
</tasks>

<!-- 新增看板节点 -->
<boards>
  <board id="..." name="项目看板">
    <column id="..." name="待办" position="0" wip_limit="5"/>
    <column id="..." name="进行中" position="1"/>
    <column id="..." name="已完成" position="2"/>
    <swimlane id="..." name="优先级高"/>
  </board>
</boards>

<!-- 新增卡片位置节点 -->
<cardPositions>
  <cardPosition taskId="..." columnId="..." position="0"/>
</cardPositions>

<!-- 新增标签节点 -->
<tags>
  <tag id="..." name="紧急" color="#FF0000"/>
</tags>

<!-- 新增任务-标签关联 -->
<taskTags>
  <taskTag taskId="..." tagId="..."/>
</taskTags>
```

#### 方案二：新增域模型类

```python
# 新增文件：taskcoachlib/domain/kanban/board.py
class Board(base.Object):
    """看板实体"""
    def __init__(self, name, description=None, ...):
        self.__columns = []  # BoardColumn 列表
        self.__swimlanes = []  # Swimlane 列表

class BoardColumn(base.Object):
    """看板列"""
    def __init__(self, board, name, position, wip_limit=None, ...):
        self.__board = board
        self.__name = name
        self.__position = position
        self.__wip_limit = wip_limit

class CardPosition(base.Object):
    """卡片位置"""
    def __init__(self, task, column, position, swimlane=None, ...):
        self.__task = task  # 引用现有 Task
        self.__column = column
        self.__position = position
        self.__swimlane = swimlane

# 新增文件：taskcoachlib/domain/tag/tag.py
class Tag(base.Object):
    """标签实体"""
    def __init__(self, name, color=None, ...):
        self.__name = name
        self.__color = color
        self.__tasks = set()  # 关联的任务
```

### 4.3 数据迁移影响

| 操作 | 影响 |
|------|------|
| 新增实体类 | 无影响，新类独立 |
| 新增 XML 节点 | 无影响，旧版本忽略未知节点 |
| 新增关联关系 | 无影响，通过 UUID 引用 |
| 修改现有类 | **不需要** |

### 4.4 实现优先级建议

| 优先级 | 功能 | 理由 |
|--------|------|------|
| **P0** | 看板视图 | 核心缺失功能，用户需求高 |
| **P1** | 标签系统 | 与 Category 互补，更灵活 |
| **P2** | 任务模板 | 提高效率 |
| **P3** | 评论系统 | 增强协作 |
| **P4** | 自定义字段 | 高级定制需求 |

### 4.5 技术实现路径

```
1. 创建新的域模型类
   ├── taskcoachlib/domain/kanban/
   │   ├── board.py
   │   ├── column.py
   │   ├── cardposition.py
   │   └── swimlane.py
   └── taskcoachlib/domain/tag/
       └── tag.py

2. 扩展 XML 读写器
   ├── persistence/xml/writer.py - 添加新节点写入
   └── persistence/xml/reader.py - 添加新节点解析

3. 扩展 TaskFile
   └── 添加 boards(), tags() 等容器

4. 创建看板视图
   └── gui/viewer/kanban.py

5. 添加 UI 命令
   └── command/kanbanCommands.py
```

---

## 五、总结

| 问题 | 答案 |
|------|------|
| 看板视图是否可以新增数据表实现？ | **是** |
| 是否需要修改现有数据表？ | **否** |
| 其他缺失功能是否同样可行？ | **是** |
| 推荐的实现方式？ | 新增域模型类 + 扩展 XML 存储 |

TaskCoach 的架构设计具有良好的扩展性，通过新增域模型类和扩展 XML 存储格式，可以在完全不修改现有数据结构的前提下实现看板视图、标签系统、评论系统等缺失功能。
