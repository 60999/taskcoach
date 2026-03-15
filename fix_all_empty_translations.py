# -*- coding: utf-8 -*-
"""
批量修复 zh_CN.po 文件中的空翻译
包含所有425个空翻译的中文翻译
"""
import re
import os

TRANSLATIONS = {
    "This setting can be overridden for individual tasks\nin the task edit dialog.": 
        "此设置可以在任务编辑对话框中为单个任务覆盖。",
    
    "If there is no user input for this amount of time\n(in minutes), %(name)s will ask what to do about current efforts.": 
        "如果用户在此时间内（以分钟计）没有输入，%(name)s 将询问如何处理当前的工作记录。",
    
    "Use decimal times for effort entries.": 
        "使用小数时间表示工作记录。",
    
    "Display one hour, fifteen minutes as 1.25 instead of 1:15\nThis is useful when calculating fees.": 
        "将一小时十五分钟显示为1.25而不是1:15\n这在计算费用时很有用。",
    
    "New tasks start with \"Preset\" dates and times filled in and checked. \"Proposed\" dates and times are not used.": 
        "新任务以\"预设\"日期和时间填充并选中。\"建议\"的日期和时间不被使用。",
    
    "When synchronizing, enter this password on the iPhone to authorize it": 
        "同步时，在iPhone上输入此密码进行授权",
    
    "Font to use in the description field of edit dialogs": 
        "编辑对话框中描述字段使用的字体",
    
    "Get e-mail subject from Mail.app": 
        "从Mail.app获取邮件主题",
    
    "When dropping an e-mail from Mail.app, try to get its subject.\nThis takes up to a few seconds per e-mail.": 
        "当从Mail.app拖放邮件时，尝试获取其主题。\n每封邮件可能需要几秒钟。",
    
    "Focus task subject in task editor": 
        "在任务编辑器中聚焦任务主题",
    
    "When opening the task editor, select the task subject and focus it.\nThis overwrites the default behavior of focusing the first tab.": 
        "打开任务编辑器时，选择并聚焦任务主题。\n这将覆盖默认的聚焦第一个标签页的行为。",
    
    "Also make this the default snooze time for future reminders": 
        "同时将此设为未来提醒的默认贪睡时间",
    
    "Horde-based": 
        "基于Horde",
    
    "Available tools": 
        "可用工具",
    
    "Make this tool visible in the toolbar": 
        "在工具栏中显示此工具",
    
    "Hide this tool from the toolbar": 
        "在工具栏中隐藏此工具",
    
    "Tools": 
        "工具",
    
    "Move the tool up (to the left of the toolbar)": 
        "上移工具（到工具栏左侧）",
    
    "Move the tool down (to the right of the toolbar)": 
        "下移工具（到工具栏右侧）",
    
    "Reorder toolbar buttons by drag and dropping them in this list.": 
        "通过在此列表中拖放来重新排列工具栏按钮。",
    
    "The backup manager will now open to allow you to restore\nan older version of the task file.": 
        "备份管理器现在将打开，允许您恢复\n任务文件的旧版本。",
    
    "Couldn't restore the pane layout from TaskCoach.ini:\n%s\n\nThe default pane layout will be used.": 
        "无法从TaskCoach.ini恢复面板布局：\n%s\n\n将使用默认面板布局。",
    
    "%s settings error": 
        "%s 设置错误",
    
    "&Mode": 
        "模式(&M)",
    
    "&Hierarchical calendar": 
        "层次日历(&H)",
    
    "Open a new tab with a viewer that displays task hierarchy in a calendar": 
        "打开一个新标签页，在日历中显示任务层次结构",
    
    "Eff&ort for selected task(s)": 
        "所选任务的工作记录(&O)",
    
    "Merge &disk changes\tShift-Ctrl-M": 
        "合并磁盘更改(&D)\tShift-Ctrl-M",
    
    "Sa&ve selected tasks to new taskfile...": 
        "保存所选任务到新任务文件(&V)...",
    
    "Save the selected tasks to a separate taskfile": 
        "将所选任务保存到单独的任务文件",
    
    "Manage backups...": 
        "管理备份...",
    
    "Manage all task file backups": 
        "管理所有任务文件备份",
    
    "Customize toolbar": 
        "自定义工具栏",
    
    "Customize": 
        "自定义",
    
    "New task with selected tasks as &dependents...": 
        "新建任务并将所选任务作为依赖项(&D)...",
    
    "Search": 
        "搜索",
    
    "Aggregation mode": 
        "聚合模式",
    
    "List": 
        "列表",
    
    "Tree": 
        "树形",
    
    "When checked, show tasks as tree, otherwise show tasks as list": 
        "选中时以树形显示任务，否则以列表显示",
    
    "Order choice": 
        "排序选择",
    
    "Configure the hierarchical calendar viewer": 
        "配置层次日历查看器",
    
    "Set pie chart angle": 
        "设置饼图角度",
    
    "Rounding precision": 
        "舍入精度",
    
    "&Creation date": 
        "创建日期(&C)",
    
    "Sort by creation date": 
        "按创建日期排序",
    
    "&Modification date": 
        "修改日期(&M)",
    
    "Sort by last modification date": 
        "按最后修改日期排序",
    
    "Show/hide creation date column": 
        "显示/隐藏创建日期列",
    
    "Show/hide last modification date column": 
        "显示/隐藏最后修改日期列",
    
    "Toolbars are customizable": 
        "工具栏可自定义",
    
    "Click on the gear icon on the right to add buttons and rearrange them.": 
        "点击右侧的齿轮图标添加按钮并重新排列。",
    
    "Reordering in tree mode": 
        "树形模式下的重新排序",
    
    "When in tree mode, manual ordering is only possible when all selected items are at the same level.": 
        "在树形模式下，只有当所有选中项处于同一级别时才能手动排序。",
    
    "When in tree mode, you can only put objects at the same level (parent).": 
        "在树形模式下，您只能将对象放在同一级别（父级）。",
    
    "&Manual ordering": 
        "手动排序(&M)",
    
    "Show/hide the manual ordering column": 
        "显示/隐藏手动排序列",
    
    "Effort aggregation": 
        "工作记录聚合",
    
    "Effort: %d selected, %d visible, %d total. Time spent: %s selected, %s visible, %s total.": 
        "工作记录：%d 已选，%d 可见，%d 总计。花费时间：%s 已选，%s 可见，%s 总计。",
    
    "Details:": 
        "详情：",
    
    "Effort for selected task(s)": 
        "所选任务的工作记录",
    
    "Sort categories by creation date": 
        "按创建日期排序分类",
    
    "Sort categories by last modification date": 
        "按最后修改日期排序分类",
    
    "Sort categories manually": 
        "手动排序分类",
    
    "Sort attachments by creation date": 
        "按创建日期排序附件",
    
    "Sort attachments by last modification date": 
        "按最后修改日期排序附件",
    
    "Sort notes by creation date": 
        "按创建日期排序笔记",
    
    "Sort notes by last modification date": 
        "按最后修改日期排序笔记",
    
    "Sort notes manually": 
        "手动排序笔记",
    
    "Sort tasks by creation date": 
        "按创建日期排序任务",
    
    "Sort tasks by last modification date": 
        "按最后修改日期排序任务",
    
    "Sort tasks manually": 
        "手动排序任务",
    
    "&Dependents": 
        "依赖项(&D)",
    
    "Shift-click on a filter tool to see only tasks belonging to the corresponding status.": 
        "Shift键点击过滤工具可只查看属于相应状态的任务。",
    
    "Lay out tasks by": 
        "任务布局方式",
    
    "Hierarchical calendar": 
        "层次日历",
    
    "Hierarchical calendar viewer configuration": 
        "层次日历查看器配置",
    
    "Manual ordering": 
        "手动排序",
    
    "Show the \"Manual ordering\" column, then drag and drop items from this column to reorder.": 
        "显示\"手动排序\"列，然后从此列拖放项目来重新排序。",
    
    "Dependents": 
        "依赖项",
    
    "% complete": 
        "完成百分比",
    
    "&Budget left": 
        "剩余预算(&B)",
    
    "&All financial columns": 
        "所有财务列(&A)",
    
    "Show/hide dependents column": 
        "显示/隐藏依赖项列",
    
    "Show tasks as": 
        "任务显示方式",
    
    "Tab": 
        "Tab键",
    
    "Space": 
        "空格",
    
    "Colon": 
        "冒号",
    
    "Semicolon": 
        "分号",
    
    "Pipe": 
        "竖线",
    
    "Double it": 
        "双写",
    
    "Escape with": 
        "转义符",
    
    "First line describes fields": 
        "首行描述字段",
    
    "Quote character": 
        "引号字符",
    
    "Escape quote": 
        "转义引号",
    
    "Field #%d": 
        "字段 #%d",
    
    "ID": 
        "ID",
    
    "No field mapping.": 
        "无字段映射。",
    
    "About effort": 
        "关于工作记录",
    
    "Effort properties": 
        "工作记录属性",
    
    "Printing": 
        "打印",
    
    "Exporting": 
        "导出",
    
    "Multi-user usage": 
        "多用户使用",
    
    "About multi-user": 
        "关于多用户",
    
    "Storage options": 
        "存储选项",
    
    "E-mailing tasks": 
        "通过电子邮件发送任务",
    
    "Custom attributes for e-mailing": 
        "电子邮件的自定义属性",
    
    "E-mail integration": 
        "电子邮件集成",
    
    "Attaching an e-mail to a task": 
        "将电子邮件附加到任务",
    
    "Setup": 
        "设置",
    
    "Limitations": 
        "限制",
    
    "Troubleshooting": 
        "故障排除",
    
    "%(name)s on the iPhone": 
        "%(name)s 在iPhone上",
    
    "%(name)s on Android?": 
        "%(name)s 在Android上？",
    
    "Todo.txt and Todo.txt Touch": 
        "Todo.txt 和 Todo.txt Touch",
    
    "Importing todo.txt": 
        "导入todo.txt",
    
    "Tasks are the basic objects that you manipulate. Tasks can\nrepresent anything from a simple errand to a complex project.": 
        "任务是您操作的基本对象。任务可以\n代表从简单差事到复杂项目的任何事情。",
    
    "Planned start date: the first date on which the task can be started. \nThe planned start date can be in the future; if it is, the task is inactive.": 
        "计划开始日期：可以开始任务的第一个日期。\n计划开始日期可以是未来的；如果是，则任务处于非活动状态。",
    
    "Completion date: this date is 'None' as long as the task has \nnot been completed. When the task is completed, the completion date is set.": 
        "完成日期：只要任务尚未完成，此日期为'无'。\n当任务完成时，完成日期被设置。",
    
    "Prerequisites: other tasks that need to be completed before\na task can be started.": 
        "前置任务：在任务开始之前\n需要完成的其他任务。",
    
    "Budget: amount of hours available for the task.": 
        "预算：任务可用的小时数。",
    
    "Hourly fee: the amount of money earned with the task per hour.": 
        "时薪：任务每小时赚取的金额。",
    
    "Fixed fee: the amount of money earned with the task \nregardless of the time spent.": 
        "固定费用：无论花费多少时间\n任务赚取的金额。",
    
    "The following properties are calculated from the properties above:": 
        "以下属性由上述属性计算得出：",
    
    "Days left: the number of days left until the due date.": 
        "剩余天数：距离截止日期的天数。",
    
    "Dependents: other tasks that can be started when the \nprerequisite task has been completed.": 
        "依赖项：前置任务完成后\n可以开始的其他任务。",
    
    "Time spent: effort spent on the task.": 
        "花费时间：任务上花费的工作记录。",
    
    "Budget left: task budget minus time spent on the task.": 
        "剩余预算：任务预算减去任务上花费的时间。",
    
    "Revenue: hourly fee times hours spent plus fixed fee.": 
        "收入：时薪乘以花费的小时数加上固定费用。",
    
    "Tasks always have exactly one of the following states:": 
        "任务始终处于以下状态之一：",
    
    "Active: the actual start date is in the past;": 
        "活动：实际开始日期在过去；",
    
    "Inactive: the task has not been started and/or not all \nprerequisite tasks have been completed;": 
        "非活动：任务尚未开始和/或并非所有\n前置任务都已完成；",
    
    "Completed: the task has been completed.": 
        "已完成：任务已完成。",
    
    "In addition, tasks can be referenced as:": 
        "此外，任务可以被引用为：",
    
    "Overdue: the due date is in the past;": 
        "逾期：截止日期在过去；",
    
    "Due soon: the due date is soon (what 'soon' is, can be \nchanged in the preferences);": 
        "即将到期：截止日期很快（什么是'很快'\n可以在首选项中更改）；",
    
    "Late: the planned start is in the past and the task has \nnot been started;": 
        "迟到：计划开始在过去但任务\n尚未开始；",
    
    "Over budget: no budget left;": 
        "超预算：没有剩余预算；",
    
    "Under budget: still budget left;": 
        "预算内：仍有剩余预算；",
    
    "No budget: the task has no budget.": 
        "无预算：任务没有预算。",
    
    "The text of tasks is colored according to the following rules:": 
        "任务文本根据以下规则着色：",
    
    "Overdue tasks are red;": 
        "逾期任务为红色；",
    
    "Tasks due soon are orange;": 
        "即将到期的任务为橙色；",
    
    "Active tasks are black text with a blue icon;": 
        "活动任务为黑色文本带蓝色图标；",
    
    "Late tasks are purple;": 
        "迟到任务为紫色；",
    
    "Future tasks are gray, and": 
        "未来任务为灰色，以及",
    
    "Completed tasks are green.": 
        "已完成任务为绿色。",
    
    "This all assumes you have not changed the text colors through the \npreferences dialog.": 
        "所有这些都假设您没有通过首选项对话框\n更改文本颜色。",
    
    "The background color of tasks is determined by the categories the \ntask belongs to.": 
        "任务的背景颜色由任务所属的类别决定。",
    
    "You can set a reminder for a specific date and time. %(name)s will\nshow a reminder dialog when that date and time arrives.": 
        "您可以为特定日期和时间设置提醒。%(name)s将在\n该日期和时间到达时显示提醒对话框。",
    
    "Whenever you spent time on tasks, you can record the amount of time\nspent by tracking effort.": 
        "每当您在任务上花费时间时，您可以通过跟踪工作记录\n来记录花费的时间量。",
    
    "Effort records have the following properties you can change:": 
        "工作记录具有以下可以更改的属性：",
    
    "Task: the task the effort belongs to.": 
        "任务：工作记录所属的任务。",
    
    "Start date/time: start date and time of the effort.": 
        "开始日期/时间：工作记录的开始日期和时间。",
    
    "Stop date/time: stop date and time of the effort. This can be \n'None' as long as the effort is still being tracked.": 
        "停止日期/时间：工作记录的停止日期和时间。只要\n工作记录仍在跟踪，这可以是'无'。",
    
    "Description: a multi-line description of the effort.": 
        "描述：工作记录的多行描述。",
    
    "Time spent: how much time you have spent working on the task.": 
        "花费时间：您在任务上花费了多少时间。",
    
    "Revenue: money earned with the time spent.": 
        "收入：花费时间赚取的钱。",
    
    "Tasks and notes may belong to one or more categories. First, you \nneed to create the categories you want to use.": 
        "任务和笔记可以属于一个或多个类别。首先，您\n需要创建要使用的类别。",
    
    "You can limit the items shown in the task and notes viewers to one \nor more categories by checking the category filter.": 
        "您可以通过选中类别过滤器来限制任务和笔记查看器中\n显示的项目为一个或多个类别。",
    
    "Categories have the following properties you can change:": 
        "类别具有以下可以更改的属性：",
    
    "Subject: a single line that summarizes the category.": 
        "主题：总结类别的单行文本。",
    
    "Description: a multi-line description of the category.": 
        "描述：类别的多行描述。",
    
    "Mutually exclusive subcategories: a check box indicating\nwhether the subcategories are mutually exclusive.": 
        "互斥子类别：一个复选框，指示\n子类别是否互斥。",
    
    "Appearance properties such as icon, font and colors: \nthe appearance properties are used when a task or note belongs to the category.": 
        "外观属性如图标、字体和颜色：\n当任务或笔记属于该类别时使用外观属性。",
    
    "Notes can be used to capture random information that you want\nto keep in your task file.": 
        "笔记可用于捕获您想要\n保留在任务文件中的随机信息。",
    
    "Notes have the following properties you can change:": 
        "笔记具有以下可以更改的属性：",
    
    "Subject: a single line that summarizes the note.": 
        "主题：总结笔记的单行文本。",
    
    "Description: a multi-line description of the note.": 
        "描述：笔记的多行描述。",
    
    "Appearance properties such as icon, font and colors.": 
        "外观属性如图标、字体和颜色。",
    
    "Both printing and exporting work in the same way: when you print\nor export data, the following steps are taken:": 
        "打印和导出都以相同的方式工作：当您打印\n或导出数据时，会执行以下步骤：",
    
    "Prepare the contents of a viewer, by putting the items in the \nright order, showing or hiding columns as needed.": 
        "准备查看器的内容，通过将项目按正确顺序排列，\n根据需要显示或隐藏列。",
    
    "You can preview how the print will look\nusing the File -> Print preview menu item.": 
        "您可以使用文件 -> 打印预览菜单项\n预览打印效果。",
    
    "Next, choose the format you want to export to and whether you\nwant to export all items or only selected items.": 
        "接下来，选择您要导出的格式以及\n要导出所有项目还是仅导出所选项目。",
    
    "Custom attributes for e-mailing tasks": 
        "电子邮件发送任务的自定义属性",
    
    "You can alter the behaviour of the e-mail command using custom attributes\nin a task description.": 
        "您可以使用任务描述中的自定义属性\n更改电子邮件命令的行为。",
    
    "[email:to=foo@spam.com]": 
        "[email:to=foo@spam.com]",
    
    "[email:cc=bar@spam.com]": 
        "[email:cc=bar@spam.com]",
    
    "A task file may be opened by several instances of %(name)s, either\nrunning on the same computer or on different computers.": 
        "任务文件可以被%(name)s的多个实例打开，\n无论是在同一台计算机上还是在不同的计算机上运行。",
    
    "A single user, opening the task file on several computers (work,\nhome, laptop).": 
        "单个用户，在多台计算机上打开任务文件（工作、\n家庭、笔记本电脑）。",
    
    "Several users working on the same task file.": 
        "多个用户在同一任务文件上工作。",
    
    "The first case is the most common and the most secure. The second\ncase may be dangerous.": 
        "第一种情况最常见也最安全。第二种\n情况可能很危险。",
    
    "None of the sharing options discussed here work fully. If two users\nsave their changes at the same time, data will be lost.": 
        "这里讨论的共享选项都不能完全工作。如果两个用户\n同时保存更改，数据将丢失。",
    
    "SMB/CIFS": 
        "SMB/CIFS",
    
    "This is the most common protocol: Windows shares and their lookalikes\n(Samba). This protocol works fine on local networks.": 
        "这是最常见的协议：Windows共享及其类似物\n（Samba）。此协议在局域网上工作良好。",
    
    "NFS": 
        "NFS",
    
    "Not tested yet.": 
        "尚未测试。",
    
    "DropBox": 
        "DropBox",
    
    "A popular way to access files from several computers (also see SpiderOak\nfor a secure alternative).": 
        "一种从多台计算机访问文件的流行方式（也可以看看SpiderOak\n作为安全的替代方案）。",
    
    "%(name)s integrates with several mail user\nagents, through drag and drop. This allows you to attach e-mails to tasks.": 
        "%(name)s与多个邮件用户代理集成，\n通过拖放。这允许您将电子邮件附加到任务。",
    
    "Mail user agents supported include:": 
        "支持的邮件用户代理包括：",
    
    "Mozilla Thunderbird": 
        "Mozilla Thunderbird",
    
    "Microsoft Outlook": 
        "Microsoft Outlook",
    
    "Claws Mail": 
        "Claws Mail",
    
    "Apple Mail": 
        "Apple Mail",
    
    "Due to a Thunderbird limitation, you can't drag and drop several\ne-mails from Thunderbird at once.": 
        "由于Thunderbird的限制，您无法一次从Thunderbird\n拖放多封电子邮件。",
    
    "There are two ways to attach an e-mail to a task; you can:": 
        "有两种方法可以将电子邮件附加到任务；您可以：",
    
    "Drop it on a task either in the task tree or the task list.": 
        "将其拖放到任务树或任务列表中的任务上。",
    
    "Drop it in the attachment pane in the task editor.": 
        "将其拖放到任务编辑器的附件面板中。",
    
    "Dropping an e-mail on an empty part of the task tree or task list\ncreates a new task with the e-mail attached.": 
        "将电子邮件拖放到任务树或任务列表的空白部分\n会创建一个附加了电子邮件的新任务。",
    
    "SyncML is an XML protocol designed to synchronize several\napplications with a server.": 
        "SyncML是一种XML协议，旨在将多个\n应用程序与服务器同步。",
    
    "%(name)s has built-in SyncML client support on Windows and Mac OS X\n(provided the Mac has Mac OS X 10.5 or later).": 
        "%(name)s在Windows和Mac OS X上内置SyncML客户端支持\n（前提是Mac具有Mac OS X 10.5或更高版本）。",
    
    "On Linux, you must install the SyncML client binding for\nPython yourself. A 64 bits version is available.": 
        "在Linux上，您必须自己安装Python的\nSyncML客户端绑定。有64位版本可用。",
    
    "This feature is optional and off by default. In order to turn it on,\ngo to the SyncML preferences and check 'Enable SyncML'.": 
        "此功能是可选的，默认关闭。要启用它，\n请转到SyncML首选项并选中'启用SyncML'。",
    
    "To setup SyncML, edit the SyncML preferences in Edit/SyncML \npreferences. Fill in the server URL, username and password.": 
        "要设置SyncML，请在编辑/SyncML首选项中\n编辑SyncML首选项。填写服务器URL、用户名和密码。",
    
    "The database names are pretty standard; the default values \nshould work.": 
        "数据库名称相当标准；默认值\n应该可以工作。",
    
    "Each task file has its own client ID, so that two different task \nfiles will be synchronized independently.": 
        "每个任务文件都有自己的客户端ID，因此两个不同的任务\n文件将独立同步。",
    
    "Some limitations are due to the fact that, the underlying data \ntype being vcalendar, some features are not supported.": 
        "一些限制是由于底层数据类型是vcalendar，\n某些功能不受支持。",
    
    "Task and category hierarchy are lost to the server.": 
        "任务和类别层次结构在服务器上丢失。",
    
    "Recurrence and reminders are not supported yet.": 
        "尚不支持重复和提醒。",
    
    "Note categories are lost to the server.": 
        "笔记类别在服务器上丢失。",
    
    "The conflict detection/resolution system is a workaround \nfor a Funambol limitation.": 
        "冲突检测/解决系统是\nFunambol限制的变通方法。",
    
    "Probably some others...": 
        "可能还有其他...",
    
    "The SyncML menu items are only present if your platform is \nsupported. Currently supported platforms are:": 
        "SyncML菜单项仅在您的平台\n受支持时才存在。目前支持的平台是：",
    
    "Windows, 32 bits (see below)": 
        "Windows，32位（见下文）",
    
    "Linux, 32 bits": 
        "Linux，32位",
    
    "Mac OS 10.3 and later, both Intel and PPC": 
        "Mac OS 10.3及更高版本，Intel和PPC",
    
    "You may experience problems under Windows if you don't have the \nMicrosoft Visual C++ 2008 Redistributable Package installed.": 
        "如果您没有安装Microsoft Visual C++ 2008可再发行组件包，\n您可能会在Windows下遇到问题。",
    
    "When SyncML is enabled, deleting a task or a note does not actually\ndelete it, but marks it as deleted.": 
        "启用SyncML后，删除任务或笔记实际上\n不会删除它，而是将其标记为已删除。",
    
    "In this case, the \"Purge deleted items\" menu item in the File menu \ncan be used to permanently delete them.": 
        "在这种情况下，可以使用文件菜单中的\"清除已删除项目\"菜单项\n永久删除它们。",
    
    "iPhone, iPod Touch and iPad": 
        "iPhone、iPod Touch和iPad",
    
    "%(name)s on the iPhone/iPod Touch/iPad": 
        "%(name)s 在iPhone/iPod Touch/iPad上",
    
    "There is an iPhone/iPod Touch/iPad companion app for %(name)s, \navailable on <a href=\"http://itunes.com/app/taskcoach/\">Apple's App Store</a>.": 
        "%(name)s有一个iPhone/iPod Touch/iPad伴侣应用，\n可在<a href=\"http://itunes.com/app/taskcoach/\">Apple的App Store</a>上获得。",
    
    "Basic task attributes: subject, description, dates (with \nrecurrence)...": 
        "基本任务属性：主题、描述、日期（带重复）...",
    
    "Hierarchical tasks and categories": 
        "层次任务和类别",
    
    "Time tracking": 
        "时间跟踪",
    
    "Multiple task files": 
        "多个任务文件",
    
    "Two-way synchronization with %(name)s on the desktop": 
        "与桌面上的%(name)s双向同步",
    
    "The application is universal and has a custom iPad UI.": 
        "该应用程序是通用的，并具有自定义iPad UI。",
    
    "Configuration on the iPhone/iPod Touch/iPad": 
        "iPhone/iPod Touch/iPad上的配置",
    
    "There are some settings for the iPhone/iPod Touch/iPad app in the \nSettings app on your device.": 
        "您设备上的设置应用中有一些\niPhone/iPod Touch/iPad应用的设置。",
    
    "Show completed: whether to show completed tasks.": 
        "显示已完成：是否显示已完成的任务。",
    
    "Show inactive: whether to show inactive tasks (planned start date \nin the future).": 
        "显示非活动：是否显示非活动任务（计划开始日期\n在未来）。",
    
    "Icon position: the LED icon may show up either on the \nleft side or the right side of the task.": 
        "图标位置：LED图标可以显示在任务的\n左侧或右侧。",
    
    "Compact mode: if this is enabled, the task list has smaller \nLEDs and doesn't show the task description.": 
        "紧凑模式：如果启用，任务列表有更小的\nLED并且不显示任务描述。",
    
    "Confirm complete: if enabled, a message box will pop up for \nconfirmation when completing a task.": 
        "确认完成：如果启用，完成任务时\n会弹出消息框进行确认。",
    
    "# days due soon: How many days in the future is \nconsidered \"soon\".": 
        "即将到期天数：未来多少天\n被认为是\"很快\"。",
    
    "Configuration on the desktop, all platforms": 
        "桌面上的配置，所有平台",
    
    "Before synchronizing, you must also configure %(name)s on the \ndesktop; in the preferences, iPhone page.": 
        "同步之前，您还必须在桌面上配置%(name)s；\n在首选项中，iPhone页面。",
    
    "When you tap the \"Sync\" button in the category view, %(name)s\nwill automatically try to find a running desktop instance.": 
        "当您在类别视图中点击\"同步\"按钮时，%(name)s\n将自动尝试查找正在运行的桌面实例。",
    
    "%(name)s will remember the chosen instance and try it next time\nyou synchronize.": 
        "%(name)s将记住选择的实例，并在下次\n同步时尝试它。",
    
    "Note that this synchronization happens through the network; there \nis no need for a cable.": 
        "请注意，此同步通过网络进行；\n不需要电缆。",
    
    "Configuration on Windows": 
        "Windows上的配置",
    
    "On Windows, you must install <a\nhref=\"http://support.apple.com/kb/dl999\">Bonjour</a> for this to work.": 
        "在Windows上，您必须安装<a\nhref=\"http://support.apple.com/kb/dl999\">Bonjour</a>才能使其工作。",
    
    "Configuration on Linux": 
        "Linux上的配置",
    
    "On Linux, you must have the <a href=\"http://avahi.org/\">Avahi</a> \ndaemon installed and running.": 
        "在Linux上，您必须安装并运行\n<a href=\"http://avahi.org/\">Avahi</a>守护程序。",
    
    "I can't seem to find the iPhone/iPod Touch app on Apple's \nwebsite": 
        "我似乎在Apple网站上\n找不到iPhone/iPod Touch应用",
    
    "You need to have iTunes installed on your computer to browse \nApple's App Store.": 
        "您需要在计算机上安装iTunes才能浏览\nApple的App Store。",
    
    "My computer doesn't appear in the list when trying to sync": 
        "尝试同步时我的计算机没有出现在列表中",
    
    "Check that your iPhone/iPod Touch is connected to the same network \nyour computer is connected to.": 
        "检查您的iPhone/iPod Touch是否连接到\n您的计算机所连接的同一网络。",
    
    "The iPhone can't connect to my computer": 
        "iPhone无法连接到我的计算机",
    
    "If you have a firewall, check that ports 4096-4100 are open.": 
        "如果您有防火墙，请检查端口4096-4100是否打开。",
    
    "No, %(name)s is not available for the Android platform. But,\n<a target=\"_blank\" href=\"http://www.todotodo.com\">Todo Todo</a> can sync with %(name)s.": 
        "不，%(name)s不适用于Android平台。但是，\n<a target=\"_blank\" href=\"http://www.todotodo.com\">Todo Todo</a>可以与%(name)s同步。",
    
    "Todo.txt is an open source todo list manager, created by Gina \nTrapani, that works in a simple text file.": 
        "Todo.txt是一个开源待办事项列表管理器，由Gina \nTrapani创建，在一个简单的文本文件中工作。",
    
    "When exporting to Todo.txt, %(name)s creates another file alongside\nthe target file with extension .idmap.": 
        "导出到Todo.txt时，%(name)s会在目标文件旁边\n创建另一个扩展名为.idmap的文件。",
    
    "Tip: if you save your task file in the todo folder that Todo.txt\nTouch creates on Dropbox, you can sync your tasks with Todo.txt Touch.": 
        "提示：如果您将任务文件保存在Todo.txt Touch\n在Dropbox上创建的todo文件夹中，您可以将任务与Todo.txt Touch同步。",
    
    "%(name)s imports task subjects, planned start date, due date, completion \ndate, priority, and categories.": 
        "%(name)s导入任务主题、计划开始日期、截止日期、完成\n日期、优先级和类别。",
    
    "When importing, %(name)s tries to find matching tasks and \ncategories and updates them if necessary.": 
        "导入时，%(name)s尝试找到匹配的任务和\n类别，并在必要时更新它们。",
    
    "%(name)s exports task subjects, planned start date, due date, completion \ndate, priority, and categories.": 
        "%(name)s导出任务主题、计划开始日期、截止日期、完成\n日期、优先级和类别。",
    
    "%(name)s supports dates and times, but Todo.txt only supports \ndates, so the time information is lost.": 
        "%(name)s支持日期和时间，但Todo.txt只支持\n日期，因此时间信息会丢失。",
    
    "The default Todo.txt format only supports planned start dates and \ncompletion dates, not due dates.": 
        "默认的Todo.txt格式只支持计划开始日期和\n完成日期，不支持截止日期。",
    
    "Todo.txt has priorities in the form of a letter ('A'-'Z'). \n%(name)s has numerical priorities.": 
        "Todo.txt的优先级以字母形式表示（'A'-'Z'）。\n%(name)s具有数字优先级。",
    
    "Categories whose subject starts with a '+' are exported as projects. \nCategories whose subject starts with a '@' are exported as contexts.": 
        "主题以'+'开头的类别作为项目导出。\n主题以'@'开头的类别作为上下文导出。",
    
    "Templates are blueprints for new tasks. Right now, the only task \nproperties that can be templated are dates.": 
        "模板是新任务的蓝图。目前，唯一可以\n模板化的任务属性是日期。",
    
    "One can create a template by selecting a task (only one) and click \non the \"Save as template\" menu item.": 
        "可以通过选择一个任务（只有一个）并点击\n\"保存为模板\"菜单项来创建模板。",
    
    "You can also create a new template from a pre-made template file \n(.tsktmpl); just drag it onto the task list.": 
        "您也可以从预制模板文件\n（.tsktmpl）创建新模板；只需将其拖到任务列表上。",
    
    "In order to instantiate a task template, use the \"New task from \ntemplate\" menu item.": 
        "要实例化任务模板，请使用\"从模板新建任务\"\n菜单项。",
    
    "You can also add templates from the template editor (File/Edit\ntemplates), as well as remove templates.": 
        "您也可以从模板编辑器（文件/编辑\n模板）添加模板，以及删除模板。",
    
    "Please note that this system is not localized; you must enter\nthe dates in english.": 
        "请注意，此系统未本地化；您必须\n以英语输入日期。",
    
    "You can drag and drop viewers to create almost any user interface \nlayout you want.": 
        "您可以拖放查看器来创建几乎任何您想要的\n用户界面布局。",
    
    "In the edit dialogs, you can drag and drop tabs to rearrange \nthe order or to create new tabs.": 
        "在编辑对话框中，您可以拖放标签页来重新排列\n顺序或创建新标签页。",
    
    "Subjects and descriptions of tasks, notes and categories can be\nedited without opening the editor dialog.": 
        "任务、笔记和类别的主题和描述可以\n在不打开编辑器对话框的情况下编辑。",
    
    "%(name)s has several keyboard shortcuts, listed below. Keyboard \nshortcuts are not configurable.": 
        "%(name)s有几个键盘快捷键，如下所列。键盘\n快捷键不可配置。",
    
    "Ctrl-A": "Ctrl-A",
    "Shift-Ctrl-A": "Shift-Ctrl-A",
    "Ctrl-B": "Ctrl-B",
    "Shift-Ctrl-B": "Shift-Ctrl-B",
    "Ctrl-C": "Ctrl-C",
    "Shift-Ctrl-C": "Shift-Ctrl-C",
    "Ctrl-D": "Ctrl-D",
    "Shift-Ctrl-D": "Shift-Ctrl-D",
    "Ctrl-E": "Ctrl-E",
    "Shift-Ctrl-E": "Shift-Ctrl-E",
    "Ctrl-F": "Ctrl-F",
    "Ctrl-G": "Ctrl-G",
    "Ctrl-H": "Ctrl-H",
    "Ctrl-I": "Ctrl-I",
    "Shift-Ctrl-I": "Shift-Ctrl-I",
    "Ctrl-J": "Ctrl-J",
    "Ctrl-M (Linux and Windows)": "Ctrl-M（Linux和Windows）",
    "Shift-Ctrl-M (Mac OS X)": "Shift-Ctrl-M（Mac OS X）",
    "Shift-Ctrl-M": "Shift-Ctrl-M",
    "Ctrl-N (Linux and Mac OS X)": "Ctrl-N（Linux和Mac OS X）",
    "Shift-Ctrl-N (Linux and Mac OS X)": "Shift-Ctrl-N（Linux和Mac OS X）",
    "Insert a new subitem": "插入新的子项目",
    "Ctrl-O": "Ctrl-O",
    "Shift-Ctrl-O": "Shift-Ctrl-O",
    "Alt-P": "Alt-P",
    "Ctrl-P": "Ctrl-P",
    "Shift-Ctrl-P": "Shift-Ctrl-P",
    "Ctrl-Q": "Ctrl-Q",
    "Ctrl-R": "Ctrl-R",
    "Shift-Ctrl-R": "Shift-Ctrl-R",
    "Ctrl-S": "Ctrl-S",
    "Shift-Ctrl-S": "Shift-Ctrl-S",
    "Ctrl-T": "Ctrl-T",
    "Shift-Ctrl-T": "Shift-Ctrl-T",
    "Ctrl-V": "Ctrl-V",
    "Shift-Ctrl-V": "Shift-Ctrl-V",
    "Ctrl-W": "Ctrl-W",
    "Ctrl-X": "Ctrl-X",
    "Ctrl-Y": "Ctrl-Y",
    "Ctrl-Z": "Ctrl-Z",
    
    "Edit the selected item(s) or close a dialog": 
        "编辑所选项目或关闭对话框",
    
    "Enter": 
        "回车",
    
    "Ctrl-Enter": 
        "Ctrl-回车",
    
    "Mark the selected task(s) (un)completed": 
        "将所选任务标记为（未）完成",
    
    "Cancel a dialog or move keyboard focus from search control back to viewer": 
        "取消对话框或将键盘焦点从搜索控件移回查看器",
    
    "Escape": 
        "Esc键",
    
    "Move keyboard focus to the next field in the dialog": 
        "将键盘焦点移到对话框中的下一个字段",
    
    "Move keyboard focus to the previous field in the dialog": 
        "将键盘焦点移到对话框中的上一个字段",
    
    "Shift-Tab": 
        "Shift-Tab",
    
    "Ctrl-Tab": 
        "Ctrl-Tab",
    
    "Move keyboard focus to the next tab in a notebook control": 
        "将键盘焦点移到笔记本控件中的下一个标签页",
    
    "Move keyboard focus to the previous tab in a notebook control": 
        "将键盘焦点移到笔记本控件中的上一个标签页",
    
    "Shift-Ctrl-Tab": 
        "Shift-Ctrl-Tab",
    
    "DELETE": 
        "删除键",
    
    "INSERT (Windows)": 
        "插入键（Windows）",
    
    "Shift-INSERT (Windows)": 
        "Shift-插入键（Windows）",
    
    "Ctrl-PgDn": 
        "Ctrl-PgDn",
    
    "Ctrl-PgUp": 
        "Ctrl-PgUp",
    
    "Alt-Down": 
        "Alt-下",
    
    "Pop up menu or drop down box": 
        "弹出菜单或下拉框",
    
    "Edit the subject of the selected item in a viewer": 
        "在查看器中编辑所选项目的主题",
    
    "F2": 
        "F2",
    
    "<h4>%(name)s - %(description)s</h4>\n<h5>Version %(version)s, %(date)s</h5>\n<p>%(copyright)s</p>\n<p>%(website)s</p>": 
        "<h4>%(name)s - %(description)s</h4>\n<h5>版本 %(version)s, %(date)s</h5>\n<p>%(copyright)s</p>\n<p>%(website)s</p>",
    
    "Browse for files to add as attachment to the selected item(s)": 
        "浏览要作为附件添加到所选项目的文件",
    
    "Add a note to the selected item(s)": 
        "向所选项目添加笔记",
    
    "Paste item(s) from the clipboard as subitem of the selected item": 
        "从剪贴板粘贴项目作为所选项目的子项目",
    
    "Stop tracking effort or resume tracking effort": 
        "停止跟踪工作记录或恢复跟踪工作记录",
    
    "Load what has changed on disk": 
        "加载磁盘上的更改",
    
    "Mail the selected item(s), using your default mailer": 
        "使用默认邮件程序发送所选项目",
    
    "Open all attachments of the selected item(s)": 
        "打开所选项目的所有附件",
    
    "Open all notes of the selected item(s)": 
        "打开所选项目的所有笔记",
    
    "Show all items regardless of category": 
        "显示所有项目，无论类别如何",
    
    "Move keyboard focus from viewer to search control": 
        "将键盘焦点从查看器移到搜索控件",
    
    "An iPhone or iPod Touch tried to connect to Task Coach,\nbut no password is set. Please set a password in the preferences.": 
        "iPhone或iPod Touch尝试连接到Task Coach，\n但未设置密码。请在首选项中设置密码。",
    
    "Protocol version: %d": 
        "协议版本：%d",
    
    "Rejected protocol version %d": 
        "拒绝的协议版本 %d",
    
    "Hash OK.": 
        "哈希正确。",
    
    "Hash KO.": 
        "哈希错误。",
    
    "Device name: %s": 
        "设备名称：%s",
    
    "GUID: %s": 
        "GUID：%s",
    
    "Sending file name: %s": 
        "发送文件名：%s",
    
    "Full from desktop.": 
        "从桌面完整同步。",
    
    "%d categories": 
        "%d 个类别",
    
    "Send category %s": 
        "发送类别 %s",
    
    "Response: %d": 
        "响应：%d",
    
    "%d tasks": 
        "%d 个任务",
    
    "Send task %s": 
        "发送任务 %s",
    
    "%d efforts": 
        "%d 个工作记录",
    
    "Send effort %s": 
        "发送工作记录 %s",
    
    "Finished.": 
        "完成。",
    
    "%d new categories": 
        "%d 个新类别",
    
    "%d new tasks": 
        "%d 个新任务",
    
    "%d new efforts": 
        "%d 个新工作记录",
    
    "%d modified categories": 
        "%d 个修改的类别",
    
    "%d modified tasks": 
        "%d 个修改的任务",
    
    "%d modified efforts": 
        "%d 个修改的工作记录",
    
    "%d deleted categories": 
        "%d 个删除的类别",
    
    "%d deleted tasks": 
        "%d 个删除的任务",
    
    "%d deleted efforts": 
        "%d 个删除的工作记录",
    
    "New category (parent: %s)": 
        "新类别（父级：%s）",
    
    "Delete category %s": 
        "删除类别 %s",
    
    "Modify category %s": 
        "修改类别 %s",
    
    "End of task synchronization.": 
        "任务同步结束。",
    
    "Could not find task %s for effort.": 
        "找不到工作记录的任务 %s。",
    
    "Sending GUID: %s": 
        "发送GUID：%s",
    
    "Reading mail info...": 
        "正在读取邮件信息...",
    
    "Reading mail information. Please wait.": 
        "正在读取邮件信息。请稍候。",
    
    "Could not find Thunderbird data dir": 
        "找不到Thunderbird数据目录",
    
    "Could not find Thunderbird profile.": 
        "找不到Thunderbird配置文件。",
    
    "No default section in profiles.ini": 
        "profiles.ini中没有默认部分",
    
    "Malformed Thunderbird internal ID:\n%s. Please file a bug report.": 
        "Thunderbird内部ID格式错误：\n%s。请提交错误报告。",
    
    "Could not find directory for ID\n%s.\nPlease file a bug report.": 
        "找不到ID的目录\n%s。\n请提交错误报告。",
    
    "Unrecognized URL scheme: \"%s\"": 
        "无法识别的URL方案：\"%s\"",
    
    "Could not open an IMAP connection to %(server)s:%(port)s\nto retrieve Thunderbird message.": 
        "无法打开到%(server)s:%(port)s的IMAP连接\n以检索Thunderbird消息。",
    
    "Please enter the domain for user %s": 
        "请输入用户%s的域",
    
    "Could not select inbox \"%s\"\n(%s)": 
        "无法选择收件箱\"%s\"\n(%s)",
    
    "No such mail: %d": 
        "没有这样的邮件：%d",
    
    "Actual start time": 
        "实际开始时间",
    
    "Planned start time": 
        "计划开始时间",
    
    "Due time": 
        "截止时间",
    
    "Completion time": 
        "完成时间",
    
    "Reminder time": 
        "提醒时间",
    
    "Creation time": 
        "创建时间",
    
    "Period end date": 
        "周期结束日期",
    
    "Period end time": 
        "周期结束时间",
    
    "The synchronization for source %s": 
        "源%s的同步",
    
    "will be a refresh from server. All local items will\nbe deleted. Do you wish to continue?": 
        "将从服务器刷新。所有本地项目将\n被删除。您要继续吗？",
    
    "will be a refresh from client. All remote items will\nbe deleted. Do you wish to continue?": 
        "将从客户端刷新。所有远程项目将\n被删除。您要继续吗？",
    
    "Synchronization": 
        "同步",
    
    "Synchronizing. Please wait.\n\n\n": 
        "正在同步。请稍候。\n\n\n",
    
    "%d items added.\n%d items updated.\n%d items deleted.": 
        "添加了%d个项目。\n更新了%d个项目。\n删除了%d个项目。",
    
    "An error occurred in the synchronization.\nError code: %d; message: %s": 
        "同步过程中发生错误。\n错误代码：%d；消息：%s",
    
    "You must first edit your SyncML Settings, in Edit/SyncML preferences.": 
        "您必须先在编辑/SyncML首选项中编辑您的SyncML设置。",
    
    "Pane Switcher": 
        "面板切换器",
    
    "\"><b>": 
        "\"><b>",
    
    "</b>": 
        "</b>",
    
    "<body bgcolor=\"#": 
        "<body bgcolor=\"#",
    
    "<p>": 
        "<p>",
    
    "</body>": 
        "</body>",
    
    "Restore %s": 
        "恢复 %s",
    
    "Pane Preview": 
        "面板预览",
    
    "Cl&ose": 
        "关闭(&O)",
    
    "Close All": 
        "全部关闭",
    
    "&Next": 
        "下一个(&N)",
    
    "&Previous": 
        "上一个(&P)",
    
    "&Window": 
        "窗口(&W)",
    
    "Edit": 
        "编辑",
    
    "%d weeks": 
        "%d 周",
    
    "%d hours": 
        "%d 小时",
    
    "Done": 
        "完成",
    
    "Viewer not searchable": 
        "查看器不可搜索",
    
    "Compatibility warning": 
        "兼容性警告",
}


def fix_translations(input_file, output_file):
    """修复po文件中的空翻译"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    i = 0
    fixed_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是 msgid 行
        if line.startswith('msgid "'):
            # 提取 msgid
            msgid = line[7:].rstrip('"')
            
            # 处理多行 msgid
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('"') and not lines[j].strip().startswith('msgstr'):
                msgid += lines[j].strip().strip('"')
                j += 1
            
            # 检查是否有翻译
            if msgid in TRANSLATIONS:
                # 找到 msgstr 行
                k = j
                while k < len(lines) and not lines[k].strip().startswith('msgstr'):
                    k += 1
                
                if k < len(lines):
                    msgstr_line = lines[k].strip()
                    
                    # 检查是否是空翻译
                    if msgstr_line == 'msgstr ""':
                        # 检查下一行是否是翻译内容（多行翻译）
                        next_line_idx = k + 1
                        has_content = False
                        while next_line_idx < len(lines) and lines[next_line_idx].strip().startswith('"'):
                            if lines[next_line_idx].strip() != '""':
                                has_content = True
                                break
                            next_line_idx += 1
                        
                        if not has_content:
                            # 添加所有行直到 msgstr
                            for idx in range(i, k):
                                result.append(lines[idx])
                            
                            # 添加翻译
                            translation = TRANSLATIONS[msgid]
                            if '\n' in translation:
                                # 多行翻译
                                result.append('msgstr ""')
                                for trans_line in translation.split('\n'):
                                    result.append(f'"{trans_line}"')
                            else:
                                result.append(f'msgstr "{translation}"')
                            
                            fixed_count += 1
                            i = next_line_idx
                            continue
        
        result.append(line)
        i += 1
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    return fixed_count


if __name__ == '__main__':
    input_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    output_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    # 先备份
    import shutil
    backup_file = input_file + '.bak'
    shutil.copy(input_file, backup_file)
    print(f"已备份到: {backup_file}")
    
    # 修复翻译
    count = fix_translations(input_file, output_file)
    print(f"已修复 {count} 个空翻译")
