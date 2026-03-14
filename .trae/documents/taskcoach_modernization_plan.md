# TaskCoach 现代化功能开发计划

> 创建日期：2026-03-15
> 分支名称：feature/modern-workflow-collaboration
> 基于文档：功能差距分析、RDB映射分析、现代化挑战分析、开源项目对比、看板可行性分析、双向链接方案

***

## 一、项目概述

### 1.1 开发目标

基于 TaskCoach 现有架构，实现以下核心功能模块：

| 优先级 | 功能模块        | 说明                 |
| :-: | ----------- | ------------------ |
|  P0 | 工作流可视化显示和编辑 | 看板视图、工作流引擎         |
|  P0 | 核心任务管理增强    | 标签系统、任务模板          |
|  P1 | 团队协作功能      | 多用户、团队管理、权限系统      |
|  P1 | 多租户功能       | 组织管理、数据隔离          |
|  P2 | 评论/讨论功能     | 评论系统、@提及功能         |
|  P2 | 活动日志        | 操作历史记录             |
|  P2 | 任务分配        | 任务指派给用户            |
|  P3 | 双向链接        | Markdown双向链接、知识库管理 |

### 1.2 技术方案

- **存储层**：扩展XML存储格式，新增实体节点
- **域模型**：新增域模型类，保持与现有模型兼容
- **视图层**：新增看板视图、评论面板等UI组件
- **不修改现有数据表结构**：通过新增实体实现功能扩展

***

## 二、开发阶段划分

### 阶段一：基础设施与工作流可视化（P0）

**预计工期**：4周

#### 2.1.1 看板视图模块

**新增文件**：

```
taskcoachlib/domain/kanban/
├── __init__.py
├── board.py          # 看板实体
├── column.py         # 看板列
├── cardposition.py   # 卡片位置
├── swimlane.py       # 泳道
└── sorter.py         # 排序器

taskcoachlib/gui/viewer/
├── kanban.py         # 看板视图
└── kanban_editor.py  # 看板编辑器

taskcoachlib/command/
└── kanbanCommands.py # 看板命令
```

**数据模型设计**：

```python
# Board（看板）
- id: UUID
- name: str
- description: str
- columns: List[BoardColumn]
- swimlanes: List[Swimlane]
- created_at: DateTime
- updated_at: DateTime

# BoardColumn（看板列）
- id: UUID
- board: Board
- name: str
- position: int
- wip_limit: int (可选)
- color: str

# CardPosition（卡片位置）
- id: UUID
- task: Task
- column: BoardColumn
- position: int
- swimlane: Swimlane (可选)

# Swimlane（泳道）
- id: UUID
- board: Board
- name: str
- position: int
```

**实现步骤**：

1. 创建看板域模型类
2. 扩展XML读写器支持看板节点
3. 实现看板视图UI组件
4. 实现拖拽排序功能
5. 实现WIP限制检查

#### 2.1.2 工作流引擎

**新增文件**：

```
taskcoachlib/domain/workflow/
├── __init__.py
├── workflow.py       # 工作流定义
├── state.py          # 状态定义
├── transition.py     # 状态转换
├── rule.py           # 转换规则
└── engine.py         # 工作流引擎
```

**数据模型设计**：

```python
# Workflow（工作流）
- id: UUID
- name: str
- description: str
- states: List[State]
- transitions: List[Transition]
- initial_state: State

# State（状态）
- id: UUID
- name: str
- color: str
- is_initial: bool
- is_final: bool

# Transition（转换）
- id: UUID
- from_state: State
- to_state: State
- name: str
- rules: List[Rule]
```

#### 2.1.3 标签系统

**新增文件**：

```
taskcoachlib/domain/tag/
├── __init__.py
├── tag.py            # 标签实体
└── sorter.py         # 排序器
```

**数据模型设计**：

```python
# Tag（标签）
- id: UUID
- name: str
- color: str
- description: str

# TaskTag（任务-标签关联）
- task_id: UUID
- tag_id: UUID
```

***

### 阶段二：团队协作与多租户（P1）

**预计工期**：6周

#### 2.2.1 用户系统

**新增文件**：

```
taskcoachlib/domain/user/
├── __init__.py
├── user.py           # 用户实体
├── role.py           # 角色定义
├── permission.py     # 权限定义
└── session.py        # 会话管理
```

**数据模型设计**：

```python
# User（用户）
- id: UUID
- username: str
- email: str
- password_hash: str
- display_name: str
- avatar: str
- created_at: DateTime
- last_login: DateTime
- is_active: bool

# Role（角色）
- id: UUID
- name: str
- permissions: List[Permission]

# Permission（权限）
- id: UUID
- name: str
- resource: str
- action: str
```

#### 2.2.2 组织与团队管理

**新增文件**：

```
taskcoachlib/domain/organization/
├── __init__.py
├── organization.py   # 组织实体
├── team.py           # 团队实体
├── membership.py     # 成员关系
└── invitation.py     # 邀请管理
```

**数据模型设计**：

```python
# Organization（组织）
- id: UUID
- name: str
- description: str
- owner: User
- teams: List[Team]
- created_at: DateTime
- settings: dict

# Team（团队）
- id: UUID
- organization: Organization
- name: str
- description: str
- members: List[Membership]

# Membership（成员关系）
- id: UUID
- user: User
- team: Team
- role: Role
- joined_at: DateTime
```

#### 2.2.3 多租户数据隔离

**实现方案**：

1. 所有实体添加 `organization_id` 字段
2. 实现租户上下文管理器
3. 数据访问层自动过滤租户数据
4. 权限检查中间件

***

### 阶段三：协作功能（P2）

**预计工期**：4周

#### 2.3.1 评论系统

**新增文件**：

```
taskcoachlib/domain/comment/
├── __init__.py
├── comment.py        # 评论实体
├── mention.py        # 提及功能
└── thread.py         # 评论线程
```

**数据模型设计**：

```python
# Comment（评论）
- id: UUID
- content: str
- author: User
- target_type: str  # 'task', 'project', etc.
- target_id: UUID
- parent: Comment (可选，支持回复)
- mentions: List[Mention]
- created_at: DateTime
- updated_at: DateTime

# Mention（提及）
- id: UUID
- comment: Comment
- user: User
- position_start: int
- position_end: int
- is_read: bool
```

#### 2.3.2 活动日志

**新增文件**：

```
taskcoachlib/domain/activity/
├── __init__.py
├── activity_log.py   # 活动日志
├── activity_type.py  # 活动类型
└── feed.py           # 活动流
```

**数据模型设计**：

```python
# ActivityLog（活动日志）
- id: UUID
- actor: User
- action: str  # 'created', 'updated', 'deleted', 'commented', etc.
- target_type: str
- target_id: UUID
- details: dict  # JSON格式的详细信息
- created_at: DateTime
- organization: Organization
```

#### 2.3.3 任务分配

**扩展 Task 模型**：

```python
# Task 新增属性
- assignees: List[User]  # 任务分配的用户列表
- watchers: List[User]   # 关注者列表
```

**新增文件**：

```
taskcoachlib/domain/assignment/
├── __init__.py
├── assignment.py     # 分配关系
└── notification.py   # 通知管理
```

***

### 阶段四：双向链接与知识库（P3）

**预计工期**：4周

#### 2.4.1 双向链接模块

**新增文件**：

```
taskcoachlib/domain/bidirectional_link/
├── __init__.py
├── parser.py         # 语法解析器
├── resolver.py       # 链接解析器
├── indexer.py        # 索引管理器
├── models.py         # 数据模型
├── cache.py          # 缓存管理
└── utils.py          # 工具函数
```

**支持的语法**：

- `[[页面名]]` - 页面链接
- `[[页面名|显示文本]]` - 带别名
- `[[页面名#标题]]` - 链接到标题
- `((块ID))` - 块引用

**数据模型设计**：

```python
# Link（链接）
- link_type: Enum  # PAGE_LINK, BLOCK_REF, HEADING_LINK
- target: str
- display_text: str (可选)
- heading: str (可选)
- source_file: str
- position: tuple

# Page（页面）
- name: str
- file_path: str
- outgoing_links: List[Link]
- incoming_links: List[Link]

# Block（块）
- block_id: str
- content: str
- file_path: str
- line_start: int
- line_end: int
```

#### 2.4.2 知识库管理

**新增文件**：

```
taskcoachlib/domain/knowledge/
├── __init__.py
├── document.py       # 文档实体
├── folder.py         # 文件夹
├── search.py         # 搜索引擎
└── export.py         # 导出功能
```

***

## 三、XML存储扩展

### 3.1 新增XML节点结构

```xml
<?xml version="1.0" encoding="utf-8"?>
<taskcoach version="3.0">
  <!-- 现有节点保持不变 -->
  <tasks>
    <task id="..." subject="...">
      <!-- 新增属性 -->
      <assignees>
        <assignee user_id="..."/>
      </assignees>
      <watchers>
        <watcher user_id="..."/>
      </watchers>
    </task>
  </tasks>
  
  <categories>...</categories>
  <notes>...</notes>
  <efforts>...</efforts>
  <attachments>...</attachments>
  
  <!-- 新增节点 -->
  <boards>
    <board id="..." name="项目看板">
      <columns>
        <column id="..." name="待办" position="0" wip_limit="5"/>
        <column id="..." name="进行中" position="1"/>
        <column id="..." name="已完成" position="2"/>
      </columns>
      <swimlanes>
        <swimlane id="..." name="优先级高" position="0"/>
      </swimlanes>
    </board>
  </boards>
  
  <cardPositions>
    <cardPosition id="..." taskId="..." columnId="..." position="0"/>
  </cardPositions>
  
  <tags>
    <tag id="..." name="紧急" color="#FF0000"/>
  </tags>
  
  <taskTags>
    <taskTag taskId="..." tagId="..."/>
  </taskTags>
  
  <workflows>
    <workflow id="..." name="任务工作流">
      <states>
        <state id="..." name="新建" is_initial="true"/>
        <state id="..." name="进行中"/>
        <state id="..." name="已完成" is_final="true"/>
      </states>
      <transitions>
        <transition id="..." from_state="..." to_state="..." name="开始"/>
      </transitions>
    </workflow>
  </workflows>
  
  <users>
    <user id="..." username="..." email="..." display_name="..."/>
  </users>
  
  <organizations>
    <organization id="..." name="...">
      <teams>
        <team id="..." name="开发团队">
          <memberships>
            <membership user_id="..." role="admin"/>
          </memberships>
        </team>
      </teams>
    </organization>
  </organizations>
  
  <comments>
    <comment id="..." target_type="task" target_id="..." author_id="...">
      <content>这是评论内容，@user1 请查看</content>
      <mentions>
        <mention user_id="..." position_start="8" position_end="14"/>
      </mentions>
    </comment>
  </comments>
  
  <activityLogs>
    <activityLog id="..." actor_id="..." action="created" target_type="task" target_id="...">
      <details>{"field": "subject", "value": "新任务"}</details>
    </activityLog>
  </activityLogs>
  
  <links>
    <link id="..." source_type="task" source_id="..." target_type="note" target_id="..."/>
  </links>
</taskcoach>
```

### 3.2 XML读写器扩展

**修改文件**：

- `taskcoachlib/persistence/xml/writer.py` - 添加新节点写入
- `taskcoachlib/persistence/xml/reader.py` - 添加新节点解析

***

## 四、GUI组件开发

### 4.1 看板视图

**新增文件**：`taskcoachlib/gui/viewer/kanban.py`

**功能特性**：

- 拖拽卡片移动
- 列间拖拽
- WIP限制显示
- 泳道分组
- 快速添加任务
- 卡片详情预览

### 4.2 评论面板

**新增文件**：`taskcoachlib/gui/viewer/comment.py`

**功能特性**：

- 评论列表显示
- 富文本编辑器
- @提及自动完成
- 回复嵌套显示
- 时间线展示

### 4.3 活动流面板

**新增文件**：`taskcoachlib/gui/viewer/activity.py`

**功能特性**：

- 活动时间线
- 过滤器（按用户、类型、时间）
- 详情展开

### 4.4 用户管理界面

**新增文件**：

```
taskcoachlib/gui/dialog/
├── user_management.py    # 用户管理
├── organization.py       # 组织管理
├── team.py               # 团队管理
└── permissions.py        # 权限管理
```

***

## 五、测试计划

### 5.1 单元测试

**测试目录结构**：

```
tests/unittests/
├── domainTests/
│   ├── KanbanTest.py
│   ├── TagTest.py
│   ├── UserTest.py
│   ├── OrganizationTest.py
│   ├── CommentTest.py
│   ├── ActivityLogTest.py
│   └── BidirectionalLinkTest.py
├── guiTests/
│   ├── KanbanViewerTest.py
│   ├── CommentViewerTest.py
│   └── ActivityViewerTest.py
└── persistenceTests/
    ├── KanbanXMLTest.py
    └── UserXMLTest.py
```

### 5.2 集成测试

- 看板与任务同步测试
- 用户权限集成测试
- 多租户数据隔离测试
- 双向链接索引测试

***

## 六、实施步骤详细计划

### 第1周：项目初始化与看板基础

| 任务               | 说明                                    | 文件                            |
| ---------------- | ------------------------------------- | ----------------------------- |
| 创建新分支            | feature/modern-workflow-collaboration | -                             |
| 创建域模型目录          | kanban, tag, workflow                 | taskcoachlib/domain/          |
| 实现Board实体        | 看板基础类                                 | domain/kanban/board.py        |
| 实现BoardColumn实体  | 看板列类                                  | domain/kanban/column.py       |
| 实现CardPosition实体 | 卡片位置类                                 | domain/kanban/cardposition.py |

### 第2周：看板视图与XML扩展

| 任务       | 说明     | 文件                        |
| -------- | ------ | ------------------------- |
| 扩展XML写入器 | 支持看板节点 | persistence/xml/writer.py |
| 扩展XML读取器 | 支持看板节点 | persistence/xml/reader.py |
| 实现看板视图   | 基础UI组件 | gui/viewer/kanban.py      |
| 实现拖拽功能   | 卡片拖拽移动 | gui/viewer/kanban.py      |

### 第3周：标签系统与工作流

| 任务             | 说明      | 文件                            |
| -------------- | ------- | ----------------------------- |
| 实现Tag实体        | 标签基础类   | domain/tag/tag.py             |
| 实现TaskTag关联    | 任务-标签关联 | domain/tag/tag.py             |
| 实现Workflow实体   | 工作流定义   | domain/workflow/workflow\.py  |
| 实现State实体      | 状态定义    | domain/workflow/state.py      |
| 实现Transition实体 | 状态转换    | domain/workflow/transition.py |

### 第4周：看板完善与测试

| 任务      | 说明     | 文件                                        |
| ------- | ------ | ----------------------------------------- |
| 实现泳道功能  | 泳道分组   | domain/kanban/swimlane.py                 |
| 实现WIP限制 | WIP检查  | gui/viewer/kanban.py                      |
| 编写单元测试  | 看板模块测试 | tests/unittests/domainTests/KanbanTest.py |
| Git提交   | 阶段一完成  | -                                         |

### 第5-6周：用户系统

| 任务             | 说明    | 文件                        |
| -------------- | ----- | ------------------------- |
| 实现User实体       | 用户基础类 | domain/user/user.py       |
| 实现Role实体       | 角色定义  | domain/user/role.py       |
| 实现Permission实体 | 权限定义  | domain/user/permission.py |
| 实现密码加密         | 安全存储  | domain/user/auth.py       |
| 实现会话管理         | 登录状态  | domain/user/session.py    |

### 第7-8周：组织与团队

| 任务               | 说明    | 文件                                  |
| ---------------- | ----- | ----------------------------------- |
| 实现Organization实体 | 组织基础类 | domain/organization/organization.py |
| 实现Team实体         | 团队基础类 | domain/organization/team.py         |
| 实现Membership实体   | 成员关系  | domain/organization/membership.py   |
| 实现多租户隔离          | 数据过滤  | domain/organization/context.py      |
| 实现权限检查           | 访问控制  | domain/user/permission.py           |

### 第9-10周：评论与活动日志

| 任务              | 说明    | 文件                               |
| --------------- | ----- | -------------------------------- |
| 实现Comment实体     | 评论基础类 | domain/comment/comment.py        |
| 实现@提及解析         | 提及功能  | domain/comment/mention.py        |
| 实现ActivityLog实体 | 活动日志  | domain/activity/activity\_log.py |
| 实现活动订阅          | 事件监听  | domain/activity/feed.py          |
| 实现评论视图          | UI组件  | gui/viewer/comment.py            |

### 第11-12周：任务分配与通知

| 任务       | 说明          | 文件                                |
| -------- | ----------- | --------------------------------- |
| 扩展Task模型 | 添加assignees | domain/task/task.py               |
| 实现分配逻辑   | 任务指派        | domain/assignment/assignment.py   |
| 实现通知系统   | 通知推送        | domain/assignment/notification.py |
| 实现活动流视图  | UI组件        | gui/viewer/activity.py            |

### 第13-14周：双向链接

| 任务      | 说明   | 文件                                     |
| ------- | ---- | -------------------------------------- |
| 实现链接解析器 | 语法解析 | domain/bidirectional\_link/parser.py   |
| 实现链接索引  | 索引管理 | domain/bidirectional\_link/indexer.py  |
| 实现反向链接  | 反向查询 | domain/bidirectional\_link/resolver.py |
| 实现缓存机制  | 性能优化 | domain/bidirectional\_link/cache.py    |

### 第15-16周：知识库与整合测试

| 任务           | 说明   | 文件                           |
| ------------ | ---- | ---------------------------- |
| 实现Document实体 | 文档管理 | domain/knowledge/document.py |
| 实现全文搜索       | 搜索功能 | domain/knowledge/search.py   |
| 整合测试         | 功能测试 | tests/integrationtests/      |
| 文档更新         | 进度文档 | docs/progress/               |
| Git提交        | 项目完成 | -                            |

***

## 七、风险与缓解措施

| 风险      | 影响     | 缓解措施           |
| ------- | ------ | -------------- |
| XML文件过大 | 性能下降   | 实现增量保存、压缩存储    |
| 多租户数据泄露 | 安全问题   | 严格的权限检查、数据隔离测试 |
| 向后兼容性   | 用户数据丢失 | 版本迁移脚本、兼容性测试   |
| GUI性能   | 用户体验差  | 虚拟滚动、懒加载       |

***

## 八、验收标准

### 8.1 功能验收

- [ ] 看板视图可正常创建、编辑、删除
- [ ] 卡片可拖拽移动，位置正确保存
- [ ] 标签系统可正常使用
- [ ] 用户可注册、登录
- [ ] 组织和团队可正常管理
- [ ] 评论和@提及功能正常
- [ ] 活动日志正确记录
- [ ] 任务分配功能正常
- [ ] 双向链接正确解析和跳转

### 8.2 性能验收

- [ ] 看板加载时间 < 2秒
- [ ] 拖拽响应时间 < 100ms
- [ ] 搜索响应时间 < 500ms

### 8.3 兼容性验收

- [ ] 旧版本数据文件可正常打开

  <br />

***

## 九、参考文档

1. [功能差距分析报告](docs/progress/05_feature_gap_analysis.md)
2. [RDB映射分析报告](docs/progress/04_rdb_mapping_analysis.md)
3. [现代化挑战分析报告](docs/progress/03_modernization_challenges.md)
4. [开源项目对比分析](docs/progress/02_opensource_projects_comparison.md)
5. [看板可行性分析报告](docs/progress/01_kanban_feasibility_analysis.md)
6. [双向链接实现方案](docs/MARKDOWN_BIDIRECTIONAL_LINK.md)
7. [Plane项目管理工具介绍](docs/progress/plane_introduction.md)
8. [Camunda工作流引擎介绍](docs/CAMUNDA_INTRODUCTION.md)
9. [Zapier自动化平台介绍](docs/ZAPIER_INTRODUCTION.md)
10. [Make自动化平台介绍](docs/MAKE_INTRODUCTION.md)

