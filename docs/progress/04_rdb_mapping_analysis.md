# TaskCoach 数据模型关系数据库映射分析报告

> 分析日期：2026-03-15  
> 分析目标：评估 TaskCoach 实体属性和关系能否使用传统关系数据库保存

---

## 一、实体属性分析表

### 1. Task（任务）实体

| 属性名 | 类型 | Python类型 | RDB映射 | 说明 |
|--------|------|------------|---------|------|
| id | 简单 | str (UUID) | VARCHAR(36) PRIMARY KEY | 唯一标识符 |
| subject | 简单 | str | VARCHAR(255) | 任务标题 |
| description | 简单 | str | TEXT | 任务描述 |
| priority | 简单 | int | INTEGER | 优先级 |
| percentageComplete | 简单 | int | INTEGER | 完成百分比(0-100) |
| hourlyFee | 简单 | float | DECIMAL(10,2) | 时薪 |
| fixedFee | 简单 | float | DECIMAL(10,2) | 固定费用 |
| ordering | 简单 | long | BIGINT | 排序字段 |
| creationDateTime | 日期 | DateTime | TIMESTAMP | 创建时间 |
| modificationDateTime | 日期 | DateTime | TIMESTAMP | 修改时间 |
| dueDateTime | 日期 | DateTime | TIMESTAMP | 截止日期 |
| plannedStartDateTime | 日期 | DateTime | TIMESTAMP | 计划开始时间 |
| actualStartDateTime | 日期 | DateTime | TIMESTAMP | 实际开始时间 |
| completionDateTime | 日期 | DateTime | TIMESTAMP | 完成时间 |
| reminder | 日期 | DateTime | TIMESTAMP | 提醒时间 |
| budget | 时间间隔 | TimeDelta | BIGINT (毫秒) | 预算时间 |
| plannedDuration | 时间间隔 | TimeDelta | BIGINT (毫秒) | 计划持续时间 |
| recurrence | 复杂对象 | Recurrence | JSON/多字段 | 重复规则 |
| fgColor | 简单 | wx.Colour | VARCHAR(50) | 前景色 |
| bgColor | 简单 | wx.Colour | VARCHAR(50) | 背景色 |
| font | 简单 | wx.Font | TEXT | 字体 |
| icon | 简单 | str | VARCHAR(100) | 图标ID |
| efforts | 集合 | List[Effort] | 外键关联 | 工时记录 |
| categories | 集合 | Set[Category] | 中间表 | 多对多关系 |
| prerequisites | 集合 | WeakSet[Task] | 中间表 | 前置任务 |
| dependencies | 集合 | WeakSet[Task] | 中间表 | 依赖任务 |
| parent | 自引用 | Task | 外键 | 父任务 |
| children | 自引用 | List[Task] | 外键反向 | 子任务列表 |
| notes | 集合 | List[Note] | 外键关联 | 笔记 |
| attachments | 集合 | List[Attachment] | 外键关联 | 附件 |

### 2. Category（类别）实体

| 属性名 | 类型 | Python类型 | RDB映射 | 说明 |
|--------|------|------------|---------|------|
| id | 简单 | str (UUID) | VARCHAR(36) PRIMARY KEY | 唯一标识符 |
| subject | 简单 | str | VARCHAR(255) | 类别名称 |
| description | 简单 | str | TEXT | 类别描述 |
| filtered | 简单 | bool | BOOLEAN | 是否过滤 |
| exclusiveSubcategories | 简单 | bool | BOOLEAN | 子类别是否互斥 |
| stylePriority | 简单 | int | INTEGER | 样式优先级 |
| categorizables | 集合 | Set[Categorizable] | 中间表 | 关联的任务/笔记 |
| parent | 自引用 | Category | 外键 | 父类别 |
| children | 自引用 | List[Category] | 外键反向 | 子类别列表 |
| notes | 集合 | List[Note] | 外键关联 | 笔记 |
| attachments | 集合 | List[Attachment] | 外键关联 | 附件 |

### 3. Effort（工时）实体

| 属性名 | 类型 | Python类型 | RDB映射 | 说明 |
|--------|------|------------|---------|------|
| id | 简单 | str (UUID) | VARCHAR(36) PRIMARY KEY | 唯一标识符 |
| task | 关系 | Task (weakref) | VARCHAR(36) FK | 所属任务 |
| start | 日期 | DateTime | TIMESTAMP | 开始时间 |
| stop | 日期 | DateTime (可空) | TIMESTAMP NULL | 结束时间 |
| entryMode | 简单 | str | VARCHAR(20) | 录入模式 |
| duration | 时间间隔 | TimeDelta (可空) | BIGINT (毫秒) NULL | 持续时间 |

### 4. Note（笔记）实体

| 属性名 | 类型 | Python类型 | RDB映射 | 说明 |
|--------|------|------------|---------|------|
| id | 简单 | str (UUID) | VARCHAR(36) PRIMARY KEY | 唯一标识符 |
| subject | 简单 | str | VARCHAR(255) | 笔记标题 |
| description | 简单 | str | TEXT | 笔记内容 |
| categories | 集合 | Set[Category] | 中间表 | 多对多关系 |
| attachments | 集合 | List[Attachment] | 外键关联 | 附件 |

### 5. Attachment（附件）实体

| 属性名 | 类型 | Python类型 | RDB映射 | 说明 |
|--------|------|------------|---------|------|
| id | 简单 | str (UUID) | VARCHAR(36) PRIMARY KEY | 唯一标识符 |
| location | 简单 | str | VARCHAR(1024) | 文件路径/URI |
| type_ | 简单 | str | VARCHAR(20) | 类型 |
| subject | 简单 | str | VARCHAR(255) | 标题 |
| description | 简单 | str | TEXT | 描述 |

---

## 二、实体关系分析表

| 关系名称 | 源实体 | 目标实体 | 关系类型 | RDB实现方式 |
|----------|--------|----------|----------|-------------|
| Task-Category | Task | Category | 多对多 | 中间表 task_category |
| Task-Effort | Task | Effort | 一对多 | effort.task_id 外键 |
| Task-Task(parent) | Task | Task | 自引用(树形) | task.parent_id 外键 |
| Task-Task(prereq) | Task | Task | 多对多自引用 | 中间表 task_prerequisite |
| Task-Task(deps) | Task | Task | 多对多自引用 | 中间表 task_dependency |
| Task-Note | Task | Note | 一对多 | note.owner_id, owner_type |
| Task-Attachment | Task | Attachment | 一对多 | attachment.owner_id, owner_type |
| Category-Categorizable | Category | Task/Note | 多对多 | 中间表 category_categorizable |
| Category-Category | Category | Category | 自引用(树形) | category.parent_id 外键 |
| Category-Note | Category | Note | 一对多 | note.owner_id, owner_type |
| Category-Attachment | Category | Attachment | 一对多 | attachment.owner_id, owner_type |
| Note-Category | Note | Category | 多对多 | 中间表 note_category |
| Note-Attachment | Note | Attachment | 一对多 | attachment.owner_id, owner_type |

---

## 三、需要特殊处理的属性

### 1. Recurrence（重复规则）对象

Recurrence 是一个复杂对象，包含多个字段：

```
Recurrence:
  - unit: str (daily/weekly/monthly/yearly/"")
  - amount: int
  - sameWeekday: bool
  - max: int (最大重复次数，0=无限)
  - count: int (已重复次数)
  - stop_datetime: DateTime
  - recurBasedOnCompletion: bool
  - weekdays: List[int] (周几，0-6)
```

**RDB存储方案：**
- 方案A：使用 JSON 字段存储（MySQL 5.7+, PostgreSQL）
- 方案B：拆分为多个独立字段
- 方案C：创建独立的 recurrence 表（推荐）

### 2. 树形结构

树形结构需要特殊处理：

**RDB存储方案：**
- 使用 parent_id 外键实现
- 可选：添加 path 或 nested set 模型优化查询性能

### 3. 多态关联

Note 和 Attachment 可以关联到 Task 或 Category：

**RDB存储方案：**
- 方案A：使用 owner_id + owner_type 双字段（推荐）
- 方案B：创建多个关联表（task_notes, category_notes 等）

### 4. WeakSet（弱引用集合）

prerequisites 和 dependencies 使用 WeakSet：

**RDB存储方案：**
- 使用中间表存储，不依赖对象引用

---

## 四、关系数据库映射可行性结论

### 结论：**✅ 完全可以使用传统关系数据库保存**

TaskCoach 的数据模型完全可以用传统关系数据库保存，原因如下：

| 类型 | 映射方式 | 可行性 |
|------|----------|:------:|
| 简单类型属性 | 直接映射到RDB字段 | ✅ |
| 日期时间类型 | TIMESTAMP / BIGINT | ✅ |
| 一对多关系 | 外键实现 | ✅ |
| 多对多关系 | 中间表实现 | ✅ |
| 树形结构 | parent_id 外键 | ✅ |
| 复杂对象 | 拆分字段或JSON | ✅ |

### 需要注意的问题：

| 问题 | 说明 | 解决方案 |
|------|------|----------|
| 对象图遍历 | 当前依赖内存引用 | RDB通过查询实现 |
| 事件系统 | 当前使用pubsub | 需要重新设计 |
| 缓存策略 | 无缓存 | 实现对象缓存 |
| 事务管理 | 无并发控制 | 处理并发更新 |

---

## 五、推荐的数据库表结构设计

### 5.1 核心实体表

```sql
-- 任务表
CREATE TABLE task (
    id VARCHAR(36) PRIMARY KEY,
    subject VARCHAR(255) NOT NULL DEFAULT '',
    description TEXT,
    priority INTEGER DEFAULT 0,
    percentage_complete INTEGER DEFAULT 0,
    hourly_fee DECIMAL(10,2) DEFAULT 0,
    fixed_fee DECIMAL(10,2) DEFAULT 0,
    ordering BIGINT DEFAULT 0,
    
    -- 日期时间字段
    creation_date_time TIMESTAMP NOT NULL,
    modification_date_time TIMESTAMP,
    due_date_time TIMESTAMP,
    planned_start_date_time TIMESTAMP,
    actual_start_date_time TIMESTAMP,
    completion_date_time TIMESTAMP,
    reminder TIMESTAMP,
    
    -- 时间预算（存储为毫秒）
    budget BIGINT DEFAULT 0,
    planned_duration BIGINT DEFAULT 0,
    
    -- 外观属性
    fg_color VARCHAR(50),
    bg_color VARCHAR(50),
    font TEXT,
    icon VARCHAR(100),
    
    -- 树形结构
    parent_id VARCHAR(36),
    
    FOREIGN KEY (parent_id) REFERENCES task(id) ON DELETE SET NULL
);

-- 重复规则表
CREATE TABLE recurrence (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    unit VARCHAR(20) NOT NULL DEFAULT '',
  -- daily/weekly/monthly/yearly/''
    amount INTEGER DEFAULT 1,
    same_weekday BOOLEAN DEFAULT FALSE,
    max_count INTEGER DEFAULT 0,
    current_count INTEGER DEFAULT 0,
    stop_date_time TIMESTAMP,
    recur_based_on_completion BOOLEAN DEFAULT FALSE,
    weekdays VARCHAR(20),
    
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- 类别表
CREATE TABLE category (
    id VARCHAR(36) PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    description TEXT,
    filtered BOOLEAN DEFAULT FALSE,
    exclusive_subcategories BOOLEAN DEFAULT FALSE,
    style_priority INTEGER DEFAULT 0,
    fg_color VARCHAR(50),
    bg_color VARCHAR(50),
    font TEXT,
    icon VARCHAR(100),
    parent_id VARCHAR(36),
    
    FOREIGN KEY (parent_id) REFERENCES category(id) ON DELETE SET NULL
);

-- 工时表
CREATE TABLE effort (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    start_date_time TIMESTAMP NOT NULL,
    stop_date_time TIMESTAMP,
    entry_mode VARCHAR(20) DEFAULT 'standard',
    duration BIGINT,
    
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- 笔记表
CREATE TABLE note (
    id VARCHAR(36) PRIMARY KEY,
    subject VARCHAR(255) NOT NULL DEFAULT '',
    description TEXT,
    owner_id VARCHAR(36) NOT NULL,
    owner_type VARCHAR(50) NOT NULL,  -- 'task' 或 'category'
    fg_color VARCHAR(50),
    bg_color VARCHAR(50),
    icon VARCHAR(100)
);

-- 附件表
CREATE TABLE attachment (
    id VARCHAR(36) PRIMARY KEY,
    location VARCHAR(1024) NOT NULL,
    type VARCHAR(20) DEFAULT 'file',
    subject VARCHAR(255),
    description TEXT,
    owner_id VARCHAR(36) NOT NULL,
    owner_type VARCHAR(50) NOT NULL
);
```

### 5.2 关系表（多对多）

```sql
-- 任务-类别 关联表
CREATE TABLE task_category (
    task_id VARCHAR(36) NOT NULL,
    category_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (task_id, category_id),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- 笔记-类别 关联表
CREATE TABLE note_category (
    note_id VARCHAR(36) NOT NULL,
    category_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (note_id, category_id),
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- 任务前置任务 关联表
CREATE TABLE task_prerequisite (
    task_id VARCHAR(36) NOT NULL,
    prerequisite_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (task_id, prerequisite_id),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_id) REFERENCES task(id) ON DELETE CASCADE
);

-- 任务依赖任务 关联表
CREATE TABLE task_dependency (
    task_id VARCHAR(36) NOT NULL,
    dependency_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (task_id, dependency_id),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE,
    FOREIGN KEY (dependency_id) REFERENCES task(id) ON DELETE CASCADE
);
```

### 5.3 索引设计

```sql
CREATE INDEX idx_task_parent ON task(parent_id);
CREATE INDEX idx_task_due_date ON task(due_date_time);
CREATE INDEX idx_category_parent ON category(parent_id);
CREATE INDEX idx_effort_task ON effort(task_id);
CREATE INDEX idx_effort_start ON effort(start_date_time);
CREATE INDEX idx_note_owner ON note(owner_id, owner_type);
CREATE INDEX idx_attachment_owner ON attachment(owner_id, owner_type);
```

---

## 六、总结

| 问题 | 答案 |
|------|------|
| 能否使用关系数据库保存？ | **✅ 完全可以** |
| 所有属性都能映射吗？ | **✅ 是** |
| 所有关系都能实现吗？ | **✅ 是** |
| 推荐的数据库？ | SQLite（轻量级）或 PostgreSQL（功能完整） |

TaskCoach 的数据模型设计良好，完全可以映射到传统关系数据库。建议使用 SQLAlchemy 等 ORM 框架实现数据持久化，保持与现有 XML 存储的兼容性。
