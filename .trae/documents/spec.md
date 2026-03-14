# TaskCoach 现代化功能开发规格说明书

> 版本：1.0
> 创建日期：2026-03-15
> 分支名称：feature/modern-workflow-collaboration

---

## 一、项目概述

### 1.1 项目背景

TaskCoach 是一个成熟的桌面任务管理应用，拥有完善的任务管理核心功能。然而，在现代任务管理软件的核心趋势——云端化、协作化、智能化方面，TaskCoach 面临着重大挑战。本规格说明书定义了 TaskCoach 现代化升级的详细技术规格。

### 1.2 项目目标

| 目标类型 | 具体目标 |
|----------|----------|
| 核心功能 | 实现工作流可视化显示和编辑 |
| 协作功能 | 实现团队协作、多租户功能 |
| 交互功能 | 实现评论/讨论、@提及、活动日志、任务分配 |
| 知识管理 | 实现双向链接功能 |

### 1.3 项目范围

**包含范围**：
- 看板视图模块
- 工作流引擎
- 标签系统
- 用户与权限系统
- 组织与团队管理
- 评论系统
- 活动日志
- 任务分配
- 双向链接

**不包含范围**：
- Web版本开发
- 移动端应用
- 云同步服务
- AI功能

### 1.4 技术约束

| 约束类型 | 约束内容 |
|----------|----------|
| 存储格式 | 必须兼容现有XML存储格式 |
| 向后兼容 | 旧版本数据文件必须能正常打开 |
| 架构限制 | 不修改现有核心域模型结构 |
| 平台支持 | Windows, macOS, Linux |

---

## 二、功能规格

### 2.1 看板视图模块

#### 2.1.1 功能描述

看板视图提供可视化的任务管理界面，支持拖拽操作、泳道分组、WIP限制等功能。

#### 2.1.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| KB-001 | 创建、编辑、删除看板 | 高 |
| KB-002 | 创建、编辑、删除看板列 | 高 |
| KB-003 | 拖拽卡片在列间移动 | 高 |
| KB-004 | 拖拽卡片在列内排序 | 高 |
| KB-005 | 创建、编辑、删除泳道 | 中 |
| KB-006 | 按泳道分组显示卡片 | 中 |
| KB-007 | 设置列的WIP限制 | 中 |
| KB-008 | WIP超限警告显示 | 中 |
| KB-009 | 快速添加任务卡片 | 高 |
| KB-010 | 卡片详情预览 | 中 |
| KB-011 | 看板过滤功能 | 中 |
| KB-012 | 看板搜索功能 | 低 |

#### 2.1.3 数据模型

```python
@dataclass
class Board:
    """
    看板实体。
    
    Attributes:
        id: 唯一标识符 (UUID)
        name: 看板名称
        description: 看板描述
        columns: 看板列列表
        swimlanes: 泳道列表
        created_at: 创建时间
        updated_at: 更新时间
        owner_id: 所有者ID
        organization_id: 所属组织ID
    """
    id: str
    name: str
    description: str
    columns: List['BoardColumn']
    swimlanes: List['Swimlane']
    created_at: DateTime
    updated_at: DateTime
    owner_id: str
    organization_id: str


@dataclass
class BoardColumn:
    """
    看板列实体。
    
    Attributes:
        id: 唯一标识符
        board: 所属看板
        name: 列名称
        position: 列位置（从0开始）
        wip_limit: WIP限制（可选）
        color: 列颜色
        task_status: 关联的任务状态（可选）
    """
    id: str
    board: Board
    name: str
    position: int
    wip_limit: Optional[int]
    color: str
    task_status: Optional[str]


@dataclass
class CardPosition:
    """
    卡片位置实体。
    
    Attributes:
        id: 唯一标识符
        task: 关联的任务
        column: 所在列
        position: 卡片位置
        swimlane: 所在泳道（可选）
    """
    id: str
    task: Task
    column: BoardColumn
    position: int
    swimlane: Optional['Swimlane']


@dataclass
class Swimlane:
    """
    泳道实体。
    
    Attributes:
        id: 唯一标识符
        board: 所属看板
        name: 泳道名称
        position: 泳道位置
    """
    id: str
    board: Board
    name: str
    position: int
```

#### 2.1.4 XML存储格式

```xml
<boards>
  <board id="uuid-here" name="项目看板" description="主要项目看板" 
         owner_id="user-uuid" organization_id="org-uuid"
         created_at="2026-03-15T10:00:00" updated_at="2026-03-15T10:00:00">
    <columns>
      <column id="col-1" name="待办" position="0" wip_limit="5" color="#E8E8E8"/>
      <column id="col-2" name="进行中" position="1" color="#FFE4B5"/>
      <column id="col-3" name="已完成" position="2" color="#90EE90"/>
    </columns>
    <swimlanes>
      <swimlane id="sl-1" name="高优先级" position="0"/>
      <swimlane id="sl-2" name="普通" position="1"/>
    </swimlanes>
  </board>
</boards>

<cardPositions>
  <cardPosition id="cp-1" taskId="task-uuid" columnId="col-1" position="0" swimlaneId="sl-1"/>
</cardPositions>
```

---

### 2.2 工作流引擎

#### 2.2.1 功能描述

工作流引擎提供任务状态流转的定义和执行能力，支持自定义工作流、状态转换规则。

#### 2.2.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| WF-001 | 创建、编辑、删除工作流 | 高 |
| WF-002 | 定义工作流状态 | 高 |
| WF-003 | 定义状态转换 | 高 |
| WF-004 | 设置初始状态和最终状态 | 高 |
| WF-005 | 状态转换规则配置 | 中 |
| WF-006 | 工作流可视化编辑器 | 中 |
| WF-007 | 工作流执行日志 | 低 |

#### 2.2.3 数据模型

```python
@dataclass
class Workflow:
    """
    工作流实体。
    
    Attributes:
        id: 唯一标识符
        name: 工作流名称
        description: 工作流描述
        states: 状态列表
        transitions: 转换列表
        initial_state: 初始状态
        organization_id: 所属组织ID
    """
    id: str
    name: str
    description: str
    states: List['State']
    transitions: List['Transition']
    initial_state: 'State'
    organization_id: str


@dataclass
class State:
    """
    工作流状态实体。
    
    Attributes:
        id: 唯一标识符
        workflow: 所属工作流
        name: 状态名称
        color: 状态颜色
        is_initial: 是否为初始状态
        is_final: 是否为最终状态
    """
    id: str
    workflow: Workflow
    name: str
    color: str
    is_initial: bool
    is_final: bool


@dataclass
class Transition:
    """
    状态转换实体。
    
    Attributes:
        id: 唯一标识符
        workflow: 所属工作流
        from_state: 源状态
        to_state: 目标状态
        name: 转换名称
        rules: 转换规则列表
    """
    id: str
    workflow: Workflow
    from_state: State
    to_state: State
    name: str
    rules: List['TransitionRule']


@dataclass
class TransitionRule:
    """
    转换规则实体。
    
    Attributes:
        id: 唯一标识符
        transition: 所属转换
        rule_type: 规则类型
        condition: 规则条件
        action: 规则动作
    """
    id: str
    transition: Transition
    rule_type: str  # 'condition', 'action', 'validator'
    condition: str
    action: str
```

---

### 2.3 标签系统

#### 2.3.1 功能描述

标签系统提供灵活的任务分类方式，与现有Category系统互补，支持多标签、颜色自定义。

#### 2.3.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| TG-001 | 创建、编辑、删除标签 | 高 |
| TG-002 | 为任务添加/移除标签 | 高 |
| TG-003 | 标签颜色自定义 | 高 |
| TG-004 | 按标签过滤任务 | 高 |
| TG-005 | 标签自动补全 | 中 |
| TG-006 | 标签使用统计 | 低 |

#### 2.3.3 数据模型

```python
@dataclass
class Tag:
    """
    标签实体。
    
    Attributes:
        id: 唯一标识符
        name: 标签名称
        color: 标签颜色 (十六进制)
        description: 标签描述
        organization_id: 所属组织ID
    """
    id: str
    name: str
    color: str
    description: str
    organization_id: str


@dataclass
class TaskTag:
    """
    任务-标签关联实体。
    
    Attributes:
        task_id: 任务ID
        tag_id: 标签ID
        created_at: 创建时间
    """
    task_id: str
    tag_id: str
    created_at: DateTime
```

---

### 2.4 用户与权限系统

#### 2.4.1 功能描述

用户与权限系统提供用户管理、角色定义、权限控制功能，为团队协作提供基础支持。

#### 2.4.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| US-001 | 用户注册 | 高 |
| US-002 | 用户登录/登出 | 高 |
| US-003 | 用户资料编辑 | 高 |
| US-004 | 密码修改 | 高 |
| US-005 | 角色定义 | 高 |
| US-006 | 权限分配 | 高 |
| US-007 | 用户头像上传 | 中 |
| US-008 | 用户状态管理（启用/禁用） | 中 |

#### 2.4.3 数据模型

```python
@dataclass
class User:
    """
    用户实体。
    
    Attributes:
        id: 唯一标识符
        username: 用户名
        email: 电子邮箱
        password_hash: 密码哈希
        display_name: 显示名称
        avatar: 头像路径
        created_at: 创建时间
        updated_at: 更新时间
        last_login: 最后登录时间
        is_active: 是否激活
        is_superuser: 是否超级用户
    """
    id: str
    username: str
    email: str
    password_hash: str
    display_name: str
    avatar: Optional[str]
    created_at: DateTime
    updated_at: DateTime
    last_login: Optional[DateTime]
    is_active: bool
    is_superuser: bool


@dataclass
class Role:
    """
    角色实体。
    
    Attributes:
        id: 唯一标识符
        name: 角色名称
        description: 角色描述
        permissions: 权限列表
        organization_id: 所属组织ID
    """
    id: str
    name: str
    description: str
    permissions: List['Permission']
    organization_id: str


@dataclass
class Permission:
    """
    权限实体。
    
    Attributes:
        id: 唯一标识符
        name: 权限名称
        resource: 资源类型
        action: 操作类型
        description: 权限描述
    """
    id: str
    name: str
    resource: str  # 'task', 'board', 'user', 'organization', etc.
    action: str    # 'create', 'read', 'update', 'delete', 'assign', etc.
    description: str


@dataclass
class UserRole:
    """
    用户-角色关联实体。
    
    Attributes:
        user_id: 用户ID
        role_id: 角色ID
        organization_id: 组织ID
        assigned_at: 分配时间
    """
    user_id: str
    role_id: str
    organization_id: str
    assigned_at: DateTime
```

#### 2.4.4 预定义权限

| 权限名称 | 资源 | 操作 | 说明 |
|----------|------|------|------|
| task_create | task | create | 创建任务 |
| task_read | task | read | 查看任务 |
| task_update | task | update | 更新任务 |
| task_delete | task | delete | 删除任务 |
| task_assign | task | assign | 分配任务 |
| board_create | board | create | 创建看板 |
| board_read | board | read | 查看看板 |
| board_update | board | update | 更新看板 |
| board_delete | board | delete | 删除看板 |
| user_manage | user | manage | 管理用户 |
| org_manage | organization | manage | 管理组织 |

---

### 2.5 组织与团队管理

#### 2.5.1 功能描述

组织与团队管理提供多租户支持，实现数据隔离和团队协作。

#### 2.5.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| ORG-001 | 创建、编辑、删除组织 | 高 |
| ORG-002 | 组织设置管理 | 中 |
| ORG-003 | 创建、编辑、删除团队 | 高 |
| ORG-004 | 团队成员管理 | 高 |
| ORG-005 | 成员邀请 | 中 |
| ORG-006 | 成员角色分配 | 高 |
| ORG-007 | 组织数据隔离 | 高 |

#### 2.5.3 数据模型

```python
@dataclass
class Organization:
    """
    组织实体。
    
    Attributes:
        id: 唯一标识符
        name: 组织名称
        description: 组织描述
        owner_id: 所有者ID
        teams: 团队列表
        settings: 组织设置
        created_at: 创建时间
        updated_at: 更新时间
    """
    id: str
    name: str
    description: str
    owner_id: str
    teams: List['Team']
    settings: dict
    created_at: DateTime
    updated_at: DateTime


@dataclass
class Team:
    """
    团队实体。
    
    Attributes:
        id: 唯一标识符
        organization: 所属组织
        name: 团队名称
        description: 团队描述
        members: 成员列表
        created_at: 创建时间
    """
    id: str
    organization: Organization
    name: str
    description: str
    members: List['Membership']
    created_at: DateTime


@dataclass
class Membership:
    """
    成员关系实体。
    
    Attributes:
        id: 唯一标识符
        user: 用户
        team: 团队
        role: 角色
        joined_at: 加入时间
        status: 成员状态
    """
    id: str
    user: User
    team: Team
    role: Role
    joined_at: DateTime
    status: str  # 'active', 'pending', 'inactive'


@dataclass
class Invitation:
    """
    邀请实体。
    
    Attributes:
        id: 唯一标识符
        organization: 组织
        team: 团队（可选）
        email: 邀请邮箱
        role: 分配角色
        invited_by: 邀请人
        invited_at: 邀请时间
        expires_at: 过期时间
        status: 邀请状态
    """
    id: str
    organization: Organization
    team: Optional[Team]
    email: str
    role: Role
    invited_by: User
    invited_at: DateTime
    expires_at: DateTime
    status: str  # 'pending', 'accepted', 'declined', 'expired'
```

---

### 2.6 评论系统

#### 2.6.1 功能描述

评论系统提供任务评论、回复、@提及功能，支持团队讨论。

#### 2.6.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| CM-001 | 创建评论 | 高 |
| CM-002 | 编辑评论 | 高 |
| CM-003 | 删除评论 | 高 |
| CM-004 | 回复评论 | 高 |
| CM-005 | @提及用户 | 高 |
| CM-006 | 评论排序 | 中 |
| CM-007 | 评论搜索 | 低 |
| CM-008 | 富文本支持 | 中 |

#### 2.6.3 数据模型

```python
@dataclass
class Comment:
    """
    评论实体。
    
    Attributes:
        id: 唯一标识符
        content: 评论内容
        author: 作者
        target_type: 目标类型
        target_id: 目标ID
        parent: 父评论（回复时使用）
        mentions: 提及列表
        created_at: 创建时间
        updated_at: 更新时间
        is_edited: 是否已编辑
    """
    id: str
    content: str
    author: User
    target_type: str  # 'task', 'board', 'project'
    target_id: str
    parent: Optional['Comment']
    mentions: List['Mention']
    created_at: DateTime
    updated_at: DateTime
    is_edited: bool


@dataclass
class Mention:
    """
    提及实体。
    
    Attributes:
        id: 唯一标识符
        comment: 所属评论
        user: 被提及的用户
        position_start: 起始位置
        position_end: 结束位置
        is_read: 是否已读
        created_at: 创建时间
    """
    id: str
    comment: Comment
    user: User
    position_start: int
    position_end: int
    is_read: bool
    created_at: DateTime
```

---

### 2.7 活动日志

#### 2.7.1 功能描述

活动日志记录系统中所有重要操作，提供操作追溯和审计功能。

#### 2.7.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| AL-001 | 记录任务创建 | 高 |
| AL-002 | 记录任务更新 | 高 |
| AL-003 | 记录任务删除 | 高 |
| AL-004 | 记录评论创建 | 高 |
| AL-005 | 记录任务分配 | 高 |
| AL-006 | 记录状态变更 | 高 |
| AL-007 | 活动流展示 | 高 |
| AL-008 | 活动过滤 | 中 |
| AL-009 | 活动导出 | 低 |

#### 2.7.3 数据模型

```python
@dataclass
class ActivityLog:
    """
    活动日志实体。
    
    Attributes:
        id: 唯一标识符
        actor: 操作者
        action: 操作类型
        target_type: 目标类型
        target_id: 目标ID
        target_name: 目标名称
        details: 详细信息
        organization: 所属组织
        created_at: 创建时间
        ip_address: IP地址（可选）
    """
    id: str
    actor: User
    action: str  # 'created', 'updated', 'deleted', 'commented', 'assigned', etc.
    target_type: str
    target_id: str
    target_name: str
    details: dict
    organization: Organization
    created_at: DateTime
    ip_address: Optional[str]
```

#### 2.7.4 预定义活动类型

| 活动类型 | 说明 | 记录内容 |
|----------|------|----------|
| task.created | 任务创建 | 任务名称 |
| task.updated | 任务更新 | 变更字段 |
| task.deleted | 任务删除 | 任务名称 |
| task.assigned | 任务分配 | 分配给谁 |
| task.status_changed | 状态变更 | 旧状态、新状态 |
| comment.created | 评论创建 | 评论摘要 |
| board.created | 看板创建 | 看板名称 |
| user.joined | 用户加入 | 用户名 |

---

### 2.8 任务分配

#### 2.8.1 功能描述

任务分配功能允许将任务指派给一个或多个用户，支持分配通知和状态跟踪。

#### 2.8.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| TA-001 | 分配任务给用户 | 高 |
| TA-002 | 移除任务分配 | 高 |
| TA-003 | 批量分配任务 | 中 |
| TA-004 | 分配通知 | 高 |
| TA-005 | 我的任务视图 | 高 |
| TA-006 | 任务关注功能 | 中 |

#### 2.8.3 数据模型扩展

```python
# Task 实体扩展属性
@dataclass
class TaskExtension:
    """
    任务扩展属性。
    
    Attributes:
        task_id: 任务ID
        assignees: 分配用户列表
        watchers: 关注者列表
    """
    task_id: str
    assignees: List[User]
    watchers: List[User]


@dataclass
class Assignment:
    """
    任务分配实体。
    
    Attributes:
        id: 唯一标识符
        task: 任务
        user: 用户
        assigned_by: 分配人
        assigned_at: 分配时间
        status: 分配状态
    """
    id: str
    task: Task
    user: User
    assigned_by: User
    assigned_at: DateTime
    status: str  # 'pending', 'accepted', 'declined'


@dataclass
class Watcher:
    """
    任务关注者实体。
    
    Attributes:
        id: 唯一标识符
        task: 任务
        user: 用户
        created_at: 关注时间
    """
    id: str
    task: Task
    user: User
    created_at: DateTime
```

---

### 2.9 双向链接

#### 2.9.1 功能描述

双向链接功能实现类似 Logseq/Obsidian 的链接能力，支持任务、笔记之间的关联。

#### 2.9.2 功能需求

| 需求ID | 需求描述 | 优先级 |
|--------|----------|:------:|
| BL-001 | 解析[[页面链接]]语法 | 高 |
| BL-002 | 解析((块引用))语法 | 高 |
| BL-003 | 解析带别名链接 | 中 |
| BL-004 | 解析带标题链接 | 中 |
| BL-005 | 反向链接查询 | 高 |
| BL-006 | 链接索引构建 | 高 |
| BL-007 | 链接自动补全 | 中 |
| BL-008 | 断链检测 | 中 |

#### 2.9.3 数据模型

```python
class LinkType(Enum):
    """链接类型枚举。"""
    PAGE_LINK = "page"
    BLOCK_REF = "block"
    HEADING_LINK = "heading"


@dataclass
class Link:
    """
    链接实体。
    
    Attributes:
        link_type: 链接类型
        target: 目标（页面名或块ID）
        display_text: 显示文本（别名）
        heading: 标题（如果有）
        source_type: 来源类型
        source_id: 来源ID
        position: 字符位置
    """
    link_type: LinkType
    target: str
    display_text: Optional[str]
    heading: Optional[str]
    source_type: str
    source_id: str
    position: tuple


@dataclass
class Page:
    """
    页面实体。
    
    Attributes:
        name: 页面名称
        entity_type: 实体类型
        entity_id: 实体ID
        outgoing_links: 出链列表
        incoming_links: 入链列表
    """
    name: str
    entity_type: str
    entity_id: str
    outgoing_links: List[Link]
    incoming_links: List[Link]


@dataclass
class Block:
    """
    块实体。
    
    Attributes:
        block_id: 块ID
        content: 块内容
        entity_type: 所属实体类型
        entity_id: 所属实体ID
        line_start: 起始行
        line_end: 结束行
    """
    block_id: str
    content: str
    entity_type: str
    entity_id: str
    line_start: int
    line_end: int
```

---

## 三、非功能需求

### 3.1 性能需求

| 指标 | 要求 | 说明 |
|------|------|------|
| 看板加载时间 | < 2秒 | 100个任务以内 |
| 拖拽响应时间 | < 100ms | 卡片拖拽操作 |
| 搜索响应时间 | < 500ms | 全文搜索 |
| 评论加载时间 | < 1秒 | 50条评论以内 |
| XML文件保存 | < 3秒 | 1000个任务 |

### 3.2 安全需求

| 需求 | 说明 |
|------|------|
| 密码存储 | 使用bcrypt加密，成本因子12 |
| 权限检查 | 所有操作必须进行权限验证 |
| 数据隔离 | 多租户数据严格隔离 |
| 审计日志 | 记录所有敏感操作 |

### 3.3 兼容性需求

| 需求 | 说明 |
|------|------|
| 向后兼容 | 旧版本XML文件可正常打开 |
| 平台兼容 | Windows 10+, macOS 10.14+, Linux |
| Python版本 | Python 3.8+ |
| wxPython版本 | wxPython 4.1+ |

---

## 四、接口规格

### 4.1 域模型接口

```python
class BoardRepository:
    """看板仓储接口。"""
    
    def find_by_id(self, board_id: str) -> Optional[Board]:
        """根据ID查找看板。"""
        pass
    
    def find_by_organization(self, org_id: str) -> List[Board]:
        """查找组织下的所有看板。"""
        pass
    
    def save(self, board: Board) -> None:
        """保存看板。"""
        pass
    
    def delete(self, board_id: str) -> None:
        """删除看板。"""
        pass


class UserRepository:
    """用户仓储接口。"""
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """根据ID查找用户。"""
        pass
    
    def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户。"""
        pass
    
    def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户。"""
        pass
    
    def save(self, user: User) -> None:
        """保存用户。"""
        pass
```

### 4.2 服务接口

```python
class KanbanService:
    """看板服务接口。"""
    
    def create_board(self, name: str, description: str) -> Board:
        """创建看板。"""
        pass
    
    def add_column(self, board_id: str, name: str, position: int) -> BoardColumn:
        """添加列。"""
        pass
    
    def move_card(self, card_id: str, target_column_id: str, position: int) -> None:
        """移动卡片。"""
        pass
    
    def get_backlinks(self, page_name: str) -> List[Link]:
        """获取反向链接。"""
        pass


class AuthService:
    """认证服务接口。"""
    
    def register(self, username: str, email: str, password: str) -> User:
        """用户注册。"""
        pass
    
    def login(self, username: str, password: str) -> Session:
        """用户登录。"""
        pass
    
    def logout(self, session_id: str) -> None:
        """用户登出。"""
        pass
    
    def validate_token(self, token: str) -> Optional[User]:
        """验证令牌。"""
        pass


class PermissionService:
    """权限服务接口。"""
    
    def check_permission(self, user: User, resource: str, action: str) -> bool:
        """检查权限。"""
        pass
    
    def grant_permission(self, role: Role, permission: Permission) -> None:
        """授予权限。"""
        pass
    
    def revoke_permission(self, role: Role, permission: Permission) -> None:
        """撤销权限。"""
        pass
```

---

## 五、验收标准

### 5.1 功能验收标准

| 功能模块 | 验收标准 |
|----------|----------|
| 看板视图 | 可创建、编辑、删除看板；卡片可拖拽移动；位置正确保存 |
| 工作流引擎 | 可定义工作流；状态转换正确执行 |
| 标签系统 | 可创建标签；任务可添加/移除标签 |
| 用户系统 | 用户可注册、登录；密码正确加密存储 |
| 组织管理 | 可创建组织、团队；成员可加入团队 |
| 评论系统 | 可创建评论、回复；@提及正确解析 |
| 活动日志 | 所有操作正确记录；活动流正确展示 |
| 任务分配 | 任务可分配给用户；分配通知正确发送 |
| 双向链接 | 链接正确解析；反向链接正确查询 |

### 5.2 性能验收标准

| 测试项 | 验收标准 |
|--------|----------|
| 看板加载 | 100任务看板加载时间 < 2秒 |
| 拖拽操作 | 卡片拖拽响应时间 < 100ms |
| 搜索功能 | 1000任务中搜索响应 < 500ms |
| 文件保存 | 1000任务文件保存 < 3秒 |

### 5.3 兼容性验收标准

| 测试项 | 验收标准 |
|--------|----------|
| 旧版本数据 | 旧版本XML文件可正常打开 |
| 新功能数据 | 新功能数据不影响旧版本读取 |
| 跨平台 | Windows/macOS/Linux功能一致 |
