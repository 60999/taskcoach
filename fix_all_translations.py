#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch translate all empty msgstr entries in zh_CN.po file.
Handles both single-line and multi-line translations.
"""

import re

TRANSLATIONS = {
    # Multi-line translations
    "If there is no user input for this amount of time\n(in minutes), %(name)s will ask what to do about current efforts.":
        "如果用户在此时间内（以分钟计）没有输入，%(name)s 将询问如何处理当前的工作记录。",
    "Use decimal times for effort entries.":
        "使用小数时间表示工作记录。",
    "Display one hour, fifteen minutes as 1.25 instead of 1:15\nThis is useful when creating invoices.":
        "将一小时十五分钟显示为 1.25 而不是 1:15\n这在创建发票时很有用。",
    "Include deleted items in export. Note that this does not work for the html export.":
        "在导出中包含已删除的项目。注意这不适用于 HTML 导出。",
    "When turned on, deleted items are moved to the Trash. When turned off, deleted items are permanently deleted.":
        "开启后，已删除的项目将移到回收站。关闭后，已删除的项目将被永久删除。",
    "When turned on, attachments are stored in the task file. When turned off, attachments are stored as links.":
        "开启后，附件将存储在任务文件中。关闭后，附件将存储为链接。",
    "When turned on, you can drag and drop attachments. When turned off, you can only browse for attachments.":
        "开启后，您可以拖放附件。关闭后，您只能浏览附件。",
    "This allows you to take screen shots which are attached to tasks.":
        "这允许您截取屏幕截图并附加到任务中。",
    "When turned on, the time spent on a task is shown in the task tooltip (not in the task editor).":
        "开启后，任务花费的时间将显示在任务提示中（不在任务编辑器中）。",
    "When turned on, notifications are shown when tasks become active.":
        "开启后，任务变为活动状态时将显示通知。",
    "When turned on, notifications are shown when tasks become due soon.":
        "开启后，任务即将到期时将显示通知。",
    "When turned on, notifications are shown when tasks become overdue.":
        "开启后，任务过期时将显示通知。",
    "This is the minimum time in minutes before the due date on which the due soon notification is shown.":
        "这是到期日前显示即将到期通知的最短时间（以分钟计）。",
    "This is the minimum time in minutes after the due date on which the overdue notification is shown.":
        "这是到期日后显示过期通知的最短时间（以分钟计）。",
    "When turned on, the start date of tasks is automatically updated when the task is set to completed.":
        "开启后，任务完成时自动更新任务的开始日期。",
    "When turned on, child tasks inherit the categories of their parent.":
        "开启后，子任务继承父任务的分类。",
    "When turned on, you can create new tasks by\n-dragging a selection box\n-dropping an email on the task list\n-dropping a selection of emails on the task list":
        "开启后，您可以通过以下方式创建新任务：\n- 拖动选择框\n- 将邮件拖放到任务列表\n- 将选中的邮件拖放到任务列表",
    "The file is automatically loaded when the file changes on disk.":
        "文件在磁盘上更改时自动加载。",
    "You can select one or more categories. Only tasks with at least one of these categories are shown.":
        "您可以选择一个或多个分类。只显示至少属于这些分类之一的任务。",
    "You can select one or more categories. Only tasks with these categories are shown.":
        "您可以选择一个或多个分类。只显示具有这些分类的任务。",
    "You can select one or more categories. All tasks except those with these categories are shown.":
        "您可以选择一个或多个分类。除了具有这些分类的任务外，显示所有任务。",
    "The text entered here will be used as search text.":
        "在此输入的文本将用作搜索文本。",
    "Searches are case sensitive by default.":
        "默认情况下搜索是区分大小写的。",
    "Tasks with a budget larger than zero are not hidden from any viewer.":
        "预算大于零的任务不会在任何查看器中被隐藏。",
    "Turn this option off if you want to hide tasks without budget from all viewers.":
        "如果您想从所有查看器中隐藏没有预算的任务，请关闭此选项。",
    "Turn this option on if you want to hide tasks without hourly fee from all viewers.":
        "如果您想从所有查看器中隐藏没有时薪的任务，请打开此选项。",
    "Turn this option off if you want to hide tasks without fixed fee from all viewers.":
        "如果您想从所有查看器中隐藏没有固定费用的任务，请关闭此选项。",
    "When turned on, the time spent is not shown in the task list.":
        "开启后，时间花费不会显示在任务列表中。",
    "When turned on, the budget is not shown in the task list.":
        "开启后，预算不会显示在任务列表中。",
    "When turned on, the hourly fee is not shown in the task list.":
        "开启后，时薪不会显示在任务列表中。",
    "When turned on, the fixed fee is not shown in the task list.":
        "开启后，固定费用不会显示在任务列表中。",
    "When turned on, the percentage complete is not shown in the task list.":
        "开启后，完成百分比不会显示在任务列表中。",
    "When turned on, the priority is not shown in the task list.":
        "开启后，优先级不会显示在任务列表中。",
    "When turned on, the start date is not shown in the task list.":
        "开启后，开始日期不会显示在任务列表中。",
    "When turned on, the due date is not shown in the task list.":
        "开启后，到期日期不会显示在任务列表中。",
    "When turned on, the completion date is not shown in the task list.":
        "开启后，完成日期不会显示在任务列表中。",
    "When turned on, the reminder is not shown in the task list.":
        "开启后，提醒不会显示在任务列表中。",
    "When turned on, the attachment indicator is not shown in the task list.":
        "开启后，附件指示器不会显示在任务列表中。",
    "When turned on, the note indicator is not shown in the task list.":
        "开启后，笔记指示器不会显示在任务列表中。",
    "When turned on, the category indicator is not shown in the task list.":
        "开启后，分类指示器不会显示在任务列表中。",
    "When turned on, the recurrence indicator is not shown in the task list.":
        "开启后，重复指示器不会显示在任务列表中。",
    "When turned on, the dependency indicator is not shown in the task list.":
        "开启后，依赖关系指示器不会显示在任务列表中。",
    "When turned on, the effort is not shown in the task list.":
        "开启后，工作记录不会显示在任务列表中。",
    "When turned on, the parent is not shown in the task list.":
        "开启后，父任务不会显示在任务列表中。",
    "When turned on, the children are not shown in the task list.":
        "开启后，子任务不会显示在任务列表中。",
    "When turned on, the children are shown in the task list.":
        "开启后，子任务将显示在任务列表中。",
    "When turned on, the total effort is shown in the task list.":
        "开启后，总工作记录将显示在任务列表中。",
    "When turned on, the total budget is shown in the task list.":
        "开启后，总预算将显示在任务列表中。",
    "When turned on, the total budget is not shown in the task list.":
        "开启后，总预算不会显示在任务列表中。",
    "When turned on, the total fee is shown in the task list.":
        "开启后，总费用将显示在任务列表中。",
    "When turned on, the total fee is not shown in the task list.":
        "开启后，总费用不会显示在任务列表中。",
    "When turned on, the date the task was created is shown in the task list.":
        "开启后，任务创建日期将显示在任务列表中。",
    "When turned on, the date the task was last modified is shown in the task list.":
        "开启后，任务最后修改日期将显示在任务列表中。",
    "When turned on, the date the task was created is not shown in the task list.":
        "开启后，任务创建日期不会显示在任务列表中。",
    "When turned on, the date the task was last modified is not shown in the task list.":
        "开启后，任务最后修改日期不会显示在任务列表中。",
    "When turned on, the icon of tasks is shown in the task list.":
        "开启后，任务图标将显示在任务列表中。",
    "When turned on, the icon of categories is shown in the category list.":
        "开启后，分类图标将显示在分类列表中。",
    "Turn this option on to make the columns wider so that the whole text fits.":
        "打开此选项使列更宽，以便显示完整文本。",
    "Turn this option on to show the categories of tasks.":
        "打开此选项以显示任务的分类。",
    "Turn this option on to show the start date of tasks.":
        "打开此选项以显示任务的开始日期。",
    "Turn this option on to show the due date of tasks.":
        "打开此选项以显示任务的到期日期。",
    "Turn this option on to show the completion date of tasks.":
        "打开此选项以显示任务的完成日期。",
    "Turn this option on to show the priority of tasks.":
        "打开此选项以显示任务的优先级。",
    "Turn this option on to show the budget of tasks.":
        "打开此选项以显示任务的预算。",
    "Turn this option on to show the hourly fee of tasks.":
        "打开此选项以显示任务的时薪。",
    "Turn this option on to show the fixed fee of tasks.":
        "打开此选项以显示任务的固定费用。",
    "Turn this option on to show the percentage complete of tasks.":
        "打开此选项以显示任务的完成百分比。",
    "Turn this option on to show the reminders of tasks.":
        "打开此选项以显示任务的提醒。",
    "Turn this option on to show the attachments of tasks.":
        "打开此选项以显示任务的附件。",
    "Turn this option on to show the notes of tasks.":
        "打开此选项以显示任务的笔记。",
    "Turn this option on to show the categories of tasks.":
        "打开此选项以显示任务的分类。",
    "Turn this option on to show the recurrence of tasks.":
        "打开此选项以显示任务的重复。",
    "Turn this option on to show the dependencies of tasks.":
        "打开此选项以显示任务的依赖关系。",
    "Turn this option on to show the effort of tasks.":
        "打开此选项以显示任务的工作记录。",
    "Turn this option on to show the time the effort started.":
        "打开此选项以显示工作记录的开始时间。",
    "Turn this option on to show the time the effort ended.":
        "打开此选项以显示工作记录的结束时间。",
    "Turn this option on to show the description of tasks.":
        "打开此选项以显示任务的描述。",
    "Turn this option on to show the description of categories.":
        "打开此选项以显示分类的描述。",
    "Turn this option on to show the description of notes.":
        "打开此选项以显示笔记的描述。",
    "Turn this option on to use a dark theme.":
        "打开此选项以使用深色主题。",
    "Turn this option on to show icons in the menu bar.":
        "打开此选项以在菜单栏中显示图标。",
    "Turn this option on to show the viewer toolbar.":
        "打开此选项以显示查看器工具栏。",
    "Turn this option on to show the taskbar icon.":
        "打开此选项以显示任务栏图标。",
    "Turn this option on to show notifications.":
        "打开此选项以显示通知。",
    "Turn this option on to show balloon tips.":
        "打开此选项以显示气球提示。",
    "Turn this option on to play a sound when a reminder is shown.":
        "打开此选项以在显示提醒时播放声音。",
    "Turn this option on to start minimized.":
        "打开此选项以最小化启动。",
    "Turn this option on to start with an empty task file.":
        "打开此选项以空任务文件启动。",
    "Turn this option on to let the window appear on top of other windows.":
        "打开此选项使窗口显示在其他窗口之上。",
    "Turn this option on to show a tip when the program starts.":
        "打开此选项以在程序启动时显示提示。",
    "Turn this option on to automatically save the task file after each change.":
        "打开此选项以在每次更改后自动保存任务文件。",
    "Turn this option on to automatically save the task file.":
        "打开此选项以自动保存任务文件。",
    "Turn this option on to notify the user when the task file changes.":
        "打开此选项以在任务文件更改时通知用户。",
    "Turn this option on to backup the task file automatically.":
        "打开此选项以自动备份任务文件。",
    "Turn this option on to hide the task in the system tray when minimized.":
        "打开此选项以在最小化时将任务隐藏在系统托盘中。",
    "Turn this option on to hide the main window when minimized.":
        "打开此选项以在最小化时隐藏主窗口。",
    "Turn this option on to hide the main window when closed.":
        "打开此选项以在关闭时隐藏主窗口。",
    "Turn this option on to keep the window always on top.":
        "打开此选项以保持窗口始终置顶。",
    "Turn this option on to show notifications.":
        "打开此选项以显示通知。",
    "Turn this option on to let the window fill the whole screen.":
        "打开此选项使窗口填充整个屏幕。",
    "Turn this option on to let the window appear in the middle of the screen.":
        "打开此选项使窗口出现在屏幕中央。",
    "Turn this option on to let the window remember its position.":
        "打开此选项使窗口记住其位置。",
    "Turn this option on to let the window remember its size.":
        "打开此选项使窗口记住其大小。",
    "Turn this option on to start with an empty task file when you start %s.":
        "打开此选项以在启动 %s 时使用空任务文件。",
    "Turn this option on to automatically save the task file when you close a viewer.":
        "打开此选项以在关闭查看器时自动保存任务文件。",
    "Turn this option on to restore the last opened task file when you start %s.":
        "打开此选项以在启动 %s 时恢复上次打开的任务文件。",
    "Turn this option on to show a warning when a task becomes overdue.":
        "打开此选项以在任务过期时显示警告。",
    "Turn this option on to show a warning when you try to close a viewer while there are unsaved changes.":
        "打开此选项以在尝试关闭有未保存更改的查看器时显示警告。",
    "Turn this option on to restore the last opened task file when you start %(name)s.":
        "打开此选项以在启动 %(name)s 时恢复上次打开的任务文件。",
    "When turned on, you can add new items by pressing Ctrl+N.":
        "开启后，您可以按 Ctrl+N 添加新项目。",
    "When turned on, you can add new items by pressing Ctrl+Shift+N.":
        "开启后，您可以按 Ctrl+Shift+N 添加新项目。",
    "When turned on, you can delete items by pressing Delete.":
        "开启后，您可以按 Delete 删除项目。",
    "When turned on, you can delete items permanently by pressing Shift+Delete.":
        "开启后，您可以按 Shift+Delete 永久删除项目。",
    "When turned on, items will be indented when you press Tab.":
        "开启后，按 Tab 键时项目将缩进。",
    "When turned on, items will be outdented when you press Shift+Tab.":
        "开启后，按 Shift+Tab 键时项目将取消缩进。",
    "When turned on, you can select items by pressing the Space key.":
        "开启后，您可以按空格键选择项目。",
    "When turned on, you can expand/collapse items by pressing the Space key.":
        "开启后，您可以按空格键展开/折叠项目。",
    "When turned on, you can select items by pressing the Enter key.":
        "开启后，您可以按 Enter 键选择项目。",
    "When turned on, the selection is extended when selecting.":
        "开启后，选择时将扩展选区。",
    "When turned on, selected items are dragged automatically.":
        "开启后，选中的项目将自动开始拖动。",
    "When turned on, a popup menu is shown when you right click.":
        "开启后，右键单击时将显示弹出菜单。",
    "When turned on, the viewer has the focus when it is opened.":
        "开启后，打开查看器时它将获得焦点。",
    "When turned on, deleted items are moved to the Trash.":
        "开启后，已删除的项目将移到回收站。",
    "When turned on, attachments are stored in the task file.":
        "开启后，附件将存储在任务文件中。",
    "When turned on, you can take screen shots.":
        "开启后，您可以截取屏幕截图。",
    "When turned on, the time spent is shown in the task tooltip.":
        "开启后，花费的时间将显示在任务提示中。",
    "When turned on, notifications are shown when tasks become active.":
        "开启后，任务变为活动状态时将显示通知。",
    "Turn this option on to let the window remember its position on the screen.":
        "打开此选项使窗口记住其在屏幕上的位置。",
    "Turn this option on to let the window remember its size on the screen.":
        "打开此选项使窗口记住其在屏幕上的大小。",
    "Turn this option on to automatically load the task file when it changes on disk.":
        "打开此选项以在磁盘上的任务文件更改时自动加载。",
    "Turn this option on to hide the toolbar when it is not focused.":
        "打开此选项以在工具栏失去焦点时隐藏它。",
    "Turn this option on to show the status bar.":
        "打开此选项以显示状态栏。",
    "Turn this option on to let the window fill the whole screen when maximized.":
        "打开此选项使窗口最大化时填充整个屏幕。",
    "Turn this option on to show icons in the toolbar.":
        "打开此选项以在工具栏中显示图标。",
    "Turn this option on to show small icons in the toolbar.":
        "打开此选项以在工具栏中显示小图标。",
    "Turn this option on to show the description of effort.":
        "打开此选项以显示工作记录的描述。",
    "Turn this option on to show the categories of tasks in the tree.":
        "打开此选项以在树中显示任务的分类。",
    "Turn this option on to automatically mark tasks as completed when all subtasks are completed.":
        "打开此选项以在所有子任务完成时自动标记任务为完成。",
    "Turn this option on to hide completed tasks from the viewer.":
        "打开此选项以从查看器中隐藏已完成的任务。",
    "Turn this option on to hide inactive tasks from the viewer.":
        "打开此选项以从查看器中隐藏非活动的任务。",
    "Turn this option on to hide tasks in the future from the viewer.":
        "打开此选项以从查看器中隐藏未来的任务。",
    "Turn this option on to hide tasks that have a start date in the future.":
        "打开此选项以隐藏开始日期在未来的任务。",
    "Turn this option on to hide tasks that have a due date in the past.":
        "打开此选项以隐藏到期日期在过去任务。",
    "Turn this option on to sort items in the viewer.":
        "打开此选项以在查看器中对项目进行排序。",
    "Turn this option on to sort items in descending order.":
        "打开此选项以按降序对项目进行排序。",
    "Turn this option on to sort by status.":
        "打开此选项以按状态排序。",
    "Turn this option on to sort by priority.":
        "打开此选项以按优先级排序。",
    "Turn this option on to sort by start date.":
        "打开此选项以按开始日期排序。",
    "Turn this option on to sort by due date.":
        "打开此选项以按到期日期排序。",
    "Turn this option on to sort by completion date.":
        "打开此选项以按完成日期排序。",
    "Turn this option on to sort by budget.":
        "打开此选项以按预算排序。",
    "Turn this option on to sort by hourly fee.":
        "打开此选项以按时薪排序。",
    "Turn this option on to sort by fixed fee.":
        "打开此选项以按固定费用排序。",
    "Turn this option on to sort by effort.":
        "打开此选项以按工作记录排序。",
    "Turn this option on to sort by creation date.":
        "打开此选项以按创建日期排序。",
    "Turn this option on to sort by modification date.":
        "打开此选项以按修改日期排序。",
    "Turn this option on to sort by subject.":
        "打开此选项以按主题排序。",
    "Turn this option on to sort by description.":
        "打开此选项以按描述排序。",
    "Turn this option on to sort by categories.":
        "打开此选项以按分类排序。",
    "Turn this option on to sort by effort per budget.":
        "打开此选项以按每预算工作记录排序。",
    "Turn this option on to sort by revenue.":
        "打开此选项以按收入排序。",
    "Turn this option on to show revenue in the viewer.":
        "打开此选项以在查看器中显示收入。",
    "Turn this option on to show effort per budget in the viewer.":
        "打开此选项以在查看器中显示每预算工作记录。",
    "Turn this option on to hide revenue in the viewer.":
        "打开此选项以在查看器中隐藏收入。",
    "Turn this option on to hide effort per budget in the viewer.":
        "打开此选项以在查看器中隐藏每预算工作记录。",
    "Turn this option on to hide overdue tasks.":
        "打开此选项以隐藏过期任务。",
    "Turn this option on to hide tasks that are due soon.":
        "打开此选项以隐藏即将到期的任务。",
    "Turn this option on to show the parent in the viewer.":
        "打开此选项以在查看器中显示父任务。",
    "Turn this option on to show the children in the viewer.":
        "打开此选项以在查看器中显示子任务。",
    "Turn this option on to show the total effort in the viewer.":
        "打开此选项以在查看器中显示总工作记录。",
    "Turn this option on to show the total budget in the viewer.":
        "打开此选项以在查看器中显示总预算。",
    "Turn this option on to show the total fee in the viewer.":
        "打开此选项以在查看器中显示总费用。",
    "Turn this option on to show the creation date in the viewer.":
        "打开此选项以在查看器中显示创建日期。",
    "Turn this option on to show the modification date in the viewer.":
        "打开此选项以在查看器中显示修改日期。",
    "Turn this option on to show the icon in the viewer.":
        "打开此选项以在查看器中显示图标。",
    "Turn this option on to show the categories in the viewer.":
        "打开此选项以在查看器中显示分类。",
    "Turn this option on to show the start date in the viewer.":
        "打开此选项以在查看器中显示开始日期。",
    "Turn this option on to show the due date in the viewer.":
        "打开此选项以在查看器中显示到期日期。",
    "Turn this option on to show the completion date in the viewer.":
        "打开此选项以在查看器中显示完成日期。",
    "Turn this option on to show the priority in the viewer.":
        "打开此选项以在查看器中显示优先级。",
    "Turn this option on to show the budget in the viewer.":
        "打开此选项以在查看器中显示预算。",
    "Turn this option on to show the hourly fee in the viewer.":
        "打开此选项以在查看器中显示时薪。",
    "Turn this option on to show the fixed fee in the viewer.":
        "打开此选项以在查看器中显示固定费用。",
    "Turn this option on to show the percentage complete in the viewer.":
        "打开此选项以在查看器中显示完成百分比。",
    "Turn this option on to show the reminder in the viewer.":
        "打开此选项以在查看器中显示提醒。",
    "Turn this option on to show the attachment indicator in the viewer.":
        "打开此选项以在查看器中显示附件指示器。",
    "Turn this option on to show the note indicator in the viewer.":
        "打开此选项以在查看器中显示笔记指示器。",
    "Turn this option on to show the recurrence indicator in the viewer.":
        "打开此选项以在查看器中显示重复指示器。",
    "Turn this option on to show the dependency indicator in the viewer.":
        "打开此选项以在查看器中显示依赖关系指示器。",
    "Turn this option on to show the effort in the viewer.":
        "打开此选项以在查看器中显示工作记录。",
    "Turn this option on to show the description in the viewer.":
        "打开此选项以在查看器中显示描述。",
    "Turn this option on to make the columns wider so that the whole text fits.":
        "打开此选项使列更宽，以便完整显示文本。",
    "Turn this option on to hide the parent from the viewer.":
        "打开此选项以从查看器中隐藏父任务。",
    "Turn this option on to hide the children from the viewer.":
        "打开此选项以从查看器中隐藏子任务。",
    "Turn this option on to hide the total effort from the viewer.":
        "打开此选项以从查看器中隐藏总工作记录。",
    "Turn this option on to hide the total budget from the viewer.":
        "打开此选项以从查看器中隐藏总预算。",
    "Turn this option on to hide the total fee from the viewer.":
        "打开此选项以从查看器中隐藏总费用。",
    "Turn this option on to hide the creation date from the viewer.":
        "打开此选项以从查看器中隐藏创建日期。",
    "Turn this option on to hide the modification date from the viewer.":
        "打开此选项以从查看器中隐藏修改日期。",
    "Turn this option on to hide the icon from the viewer.":
        "打开此选项以从查看器中隐藏图标。",
    "Turn this option on to hide the categories from the viewer.":
        "打开此选项以从查看器中隐藏分类。",
    "Turn this option on to hide the start date from the viewer.":
        "打开此选项以从查看器中隐藏开始日期。",
    "Turn this option on to hide the due date from the viewer.":
        "打开此选项以从查看器中隐藏到期日期。",
    "Turn this option on to hide the completion date from the viewer.":
        "打开此选项以从查看器中隐藏完成日期。",
    "Turn this option on to hide the priority from the viewer.":
        "打开此选项以从查看器中隐藏优先级。",
    "Turn this option on to hide the budget from the viewer.":
        "打开此选项以从查看器中隐藏预算。",
    "Turn this option on to hide the hourly fee from the viewer.":
        "打开此选项以从查看器中隐藏时薪。",
    "Turn this option on to hide the fixed fee from the viewer.":
        "打开此选项以从查看器中隐藏固定费用。",
    "Turn this option on to hide the percentage complete from the viewer.":
        "打开此选项以从查看器中隐藏完成百分比。",
    "Turn this option on to hide the reminder from the viewer.":
        "打开此选项以从查看器中隐藏提醒。",
    "Turn this option on to hide the attachment indicator from the viewer.":
        "打开此选项以从查看器中隐藏附件指示器。",
    "Turn this option on to hide the note indicator from the viewer.":
        "打开此选项以从查看器中隐藏笔记指示器。",
    "Turn this option on to hide the recurrence indicator from the viewer.":
        "打开此选项以从查看器中隐藏重复指示器。",
    "Turn this option on to hide the dependency indicator from the viewer.":
        "打开此选项以从查看器中隐藏依赖关系指示器。",
    "Turn this option on to hide the effort from the viewer.":
        "打开此选项以从查看器中隐藏工作记录。",
    "Turn this option on to hide the description from the viewer.":
        "打开此选项以从查看器中隐藏描述。",
    "Turn this option on to show the categories in a column in the viewer.":
        "打开此选项以在查看器的列中显示分类。",
    "Turn this option on to use auto text.":
        "打开此选项以使用自动文本。",
    "Turn this option on to wrap the text in the viewer.":
        "打开此选项以在查看器中换行文本。",
    "Turn this option on to show the column headers in the viewer.":
        "打开此选项以在查看器中显示列标题。",
    "Turn this option on to show the header in printed reports.":
        "打开此选项以在打印报告中显示页眉。",
    "Turn this option on to show the footer in printed reports.":
        "打开此选项以在打印报告中显示页脚。",
    "Turn this option on to show the page number in printed reports.":
        "打开此选项以在打印报告中显示页码。",
    "Turn this option on to show the title in printed reports.":
        "打开此选项以在打印报告中显示标题。",
    "Turn this option on to let printed reports fit on one page.":
        "打开此选项使打印报告在一页上显示。",
    "Turn this option on to let printed reports be expanded to fit the page.":
        "打开此选项使打印报告展开以适应页面。",
    "Turn this option on to show line numbers in printed reports.":
        "打开此选项以在打印报告中显示行号。",
    "Turn this option on to show lines in printed reports.":
        "打开此选项以在打印报告中显示线条。",
    "Turn this option on to auto-complete text in the subject and description fields.":
        "打开此选项以在主题和描述字段中自动完成文本。",
    "Turn this option on to use notification sounds.":
        "打开此选项以使用通知声音。",
    "Turn this option on to play a sound when the due soon notification is shown.":
        "打开此选项以在显示即将到期通知时播放声音。",
    "Turn this option on to play a sound when the overdue notification is shown.":
        "打开此选项以在显示过期通知时播放声音。",
    "Turn this option on to play a sound when the task becomes active.":
        "打开此选项以在任务变为活动状态时播放声音。",
    "Turn this option on to save the window position on exit.":
        "打开此选项以在退出时保存窗口位置。",
    "Turn this option on to save the window size on exit.":
        "打开此选项以在退出时保存窗口大小。",
    "Turn this option on to start with an empty task file when you start %(name)s.":
        "打开此选项以在启动 %(name)s 时使用空任务文件。",
    "Turn this option on to start with the last opened task file when you start %(name)s.":
        "打开此选项以在启动 %(name)s 时打开上次打开的任务文件。",
    "Turn this option on to hide the task list.":
        "打开此选项以隐藏任务列表。",
    "Turn this option on to hide the task tree.":
        "打开此选项以隐藏任务树。",
    "Turn this option on to hide the category list.":
        "打开此选项以隐藏分类列表。",
    "Turn this option on to hide the category tree.":
        "打开此选项以隐藏分类树。",
    "Turn this option on to hide the effort list.":
        "打开此选项以隐藏工作记录列表。",
    "Turn this option on to show the effort list.":
        "打开此选项以显示工作记录列表。",
    "Turn this option on to show the category list.":
        "打开此选项以显示分类列表。",
    "Turn this option on to show the category tree.":
        "打开此选项以显示分类树。",
    "Turn this option on to show the task list.":
        "打开此选项以显示任务列表。",
    "Turn this option on to show the task tree.":
        "打开此选项以显示任务树。",
    "Turn this option on to show the toolbar.":
        "打开此选项以显示工具栏。",
    "Turn this option on to show the menubar.":
        "打开此选项以显示菜单栏。",
    "Turn this option on to use tabs.":
        "打开此选项以使用标签页。",
    "Turn this option on to show the main window.":
        "打开此选项以显示主窗口。",
    "Turn this option on to maximize the window.":
        "打开此选项以最大化窗口。",
    "Turn this option on to iconify the window.":
        "打开此选项以最小化窗口为图标。",
    "Turn this option on to show a tip of the day.":
        "打开此选项以显示每日提示。",
    "Turn this option on to show the taskbar icon.":
        "打开此选项以显示任务栏图标。",
    "Turn this option on to show notifications.":
        "打开此选项以显示通知。",
    "Turn this option on to show balloon tips.":
        "打开此选项以显示气球提示。",
    "When turned on, a sound is played when the due soon notification is shown.":
        "开启后，显示即将到期通知时将播放声音。",
    "When turned on, a sound is played when the overdue notification is shown.":
        "开启后，显示过期通知时将播放声音。",
    "When turned on, a sound is played when the task becomes active.":
        "开启后，任务变为活动状态时将播放声音。",
    "Turn this option on to save the columns automatically.":
        "打开此选项以自动保存列。",
    "Turn this option on to save the sort order automatically.":
        "打开此选项以自动保存排序顺序。",
    "Turn this option on to save the filter automatically.":
        "打开此选项以自动保存过滤器。",
    "Turn this option on to automatically load the last opened file.":
        "打开此选项以自动加载上次打开的文件。",
    "When turned on, categories are shown in the task tree.":
        "开启后，分类将显示在任务树中。",
    "When turned on, the effort of subtasks is added to the effort of the parent.":
        "开启后，子任务的工作记录将添加到父任务的工作记录中。",
    "When turned on, the budget of subtasks is added to the budget of the parent.":
        "开启后，子任务的预算将添加到父任务的预算中。",
    "When turned on, the fee of subtasks is added to the fee of the parent.":
        "开启后，子任务的费用将添加到父任务的费用中。",
    "When turned on, the effort of subtasks is not added to the effort of the parent.":
        "开启后，子任务的工作记录不会添加到父任务的工作记录中。",
    "When turned on, the budget of subtasks is not added to the budget of the parent.":
        "开启后，子任务的预算不会添加到父任务的预算中。",
    "When turned on, the fee of subtasks is not added to the fee of the parent.":
        "开启后，子任务的费用不会添加到父任务的费用中。",
    "When turned on, the total effort of completed subtasks is shown in the task.":
        "开启后，已完成子任务的总工作记录将显示在任务中。",
    "When turned on, the total budget of completed subtasks is shown in the task.":
        "开启后，已完成子任务的总预算将显示在任务中。",
    "When turned on, the total fee of completed subtasks is shown in the task.":
        "开启后，已完成子任务的总费用将显示在任务中。",
    "When turned on, the total effort of completed subtasks is not shown in the task.":
        "开启后，已完成子任务的总工作记录不会显示在任务中。",
    "When turned on, the total budget of completed subtasks is not shown in the task.":
        "开启后，已完成子任务的总预算不会显示在任务中。",
    "When turned on, the total fee of completed subtasks is not shown in the task.":
        "开启后，已完成子任务的总费用不会显示在任务中。",
    "Turn this option on to show the revenue in the viewer.":
        "打开此选项以在查看器中显示收入。",
    "Turn this option on to show the effort per budget in the viewer.":
        "打开此选项以在查看器中显示每预算工作记录。",
    "Turn this option on to hide the revenue in the viewer.":
        "打开此选项以在查看器中隐藏收入。",
    "Turn this option on to hide the effort per budget in the viewer.":
        "打开此选项以在查看器中隐藏每预算工作记录。",
    "Turn this option on to show this settings page.":
        "打开此选项以显示此设置页面。",
    "Turn this option on to hide this settings page.":
        "打开此选项以隐藏此设置页面。",
    "Turn this option on to use a different color for the weekend.":
        "打开此选项以使用不同的周末颜色。",
    "Turn this option on to use a different color for days in the past.":
        "打开此选项以使用不同的过去日期颜色。",
    "Turn this option on to use a different color for today.":
        "打开此选项以使用不同的今天颜色。",
    "Turn this option on to use a different color for days in the future.":
        "打开此选项以使用不同的未来日期颜色。",
    "Turn this option on to use a different color for overdue tasks.":
        "打开此选项以使用不同的过期任务颜色。",
    "Turn this option on to use a different color for due soon tasks.":
        "打开此选项以使用不同的即将到期任务颜色。",
    "Turn this option on to use a different color for completed tasks.":
        "打开此选项以使用不同的已完成任务颜色。",
    "Turn this option on to use a different color for inactive tasks.":
        "打开此选项以使用不同的非活动任务颜色。",
    "Turn this option on to use a different color for tasks with no start date.":
        "打开此选项以使用不同的没有开始日期的任务颜色。",
    "Turn this option on to use a different color for tasks with no due date.":
        "打开此选项以使用不同的没有到期日期的任务颜色。",
    "Turn this option on to use a different color for tasks with a budget.":
        "打开此选项以使用不同的有预算的任务颜色。",
    "Turn this option on to use a different color for tasks with an hourly fee.":
        "打开此选项以使用不同的有时薪的任务颜色。",
    "Turn this option on to use a different color for tasks with a fixed fee.":
        "打开此选项以使用不同的有固定费用的任务颜色。",
    "Turn this option on to use a different color for tasks with attachments.":
        "打开此选项以使用不同的有附件的任务颜色。",
    "Turn this option on to use a different color for tasks with notes.":
        "打开此选项以使用不同的有笔记的任务颜色。",
    "Turn this option on to use a different color for tasks with categories.":
        "打开此选项以使用不同的有分类的任务颜色。",
    "Turn this option on to use a different color for tasks with recurrences.":
        "打开此选项以使用不同的有重复的任务颜色。",
    "Turn this option on to use a different color for tasks with prerequisites.":
        "打开此选项以使用不同的有前置条件的任务颜色。",
    "Turn this option on to use a different color for tasks with effort.":
        "打开此选项以使用不同的有工作记录的任务颜色。",
    "Turn this option on to use a different color for tasks with dependencies.":
        "打开此选项以使用不同的有依赖关系的任务颜色。",
    "Turn this option on to use a different color for overdue items.":
        "打开此选项以使用不同的过期项目颜色。",
    "Turn this option on to use a different color for the current time.":
        "打开此选项以使用不同的当前时间颜色。",
    "Turn this option on to use a different color for the current day.":
        "打开此选项以使用不同的当前日期颜色。",
    "Turn this option on to show the time spent in the task list.":
        "打开此选项以在任务列表中显示花费的时间。",
    "Turn this option on to show the budget in the task list.":
        "打开此选项以在任务列表中显示预算。",
    "Turn this option on to show the hourly fee in the task list.":
        "打开此选项以在任务列表中显示时薪。",
    "Turn this option on to show the fixed fee in the task list.":
        "打开此选项以在任务列表中显示固定费用。",
    "Turn this option on to show the percentage complete in the task list.":
        "打开此选项以在任务列表中显示完成百分比。",
    "Turn this option on to show the priority in the task list.":
        "打开此选项以在任务列表中显示优先级。",
    "Turn this option on to show the start date in the task list.":
        "打开此选项以在任务列表中显示开始日期。",
    "Turn this option on to show the due date in the task list.":
        "打开此选项以在任务列表中显示到期日期。",
    "Turn this option on to show the completion date in the task list.":
        "打开此选项以在任务列表中显示完成日期。",
    "Turn this option on to show the reminder in the task list.":
        "打开此选项以在任务列表中显示提醒。",
    "Turn this option on to show the attachment indicator in the task list.":
        "打开此选项以在任务列表中显示附件指示器。",
    "Turn this option on to show the note indicator in the task list.":
        "打开此选项以在任务列表中显示笔记指示器。",
    "Turn this option on to show the category indicator in the task list.":
        "打开此选项以在任务列表中显示分类指示器。",
    "Turn this option on to show the recurrence indicator in the task list.":
        "打开此选项以在任务列表中显示重复指示器。",
    "Turn this option on to show the dependency indicator in the task list.":
        "打开此选项以在任务列表中显示依赖关系指示器。",
    "Turn this option on to show the effort in the task list.":
        "打开此选项以在任务列表中显示工作记录。",
    "Turn this option on to show the parent in the task list.":
        "打开此选项以在任务列表中显示父任务。",
    "Turn this option on to show the children in the task list.":
        "打开此选项以在任务列表中显示子任务。",
    "Turn this option on to show the total effort in the task list.":
        "打开此选项以在任务列表中显示总工作记录。",
    "Turn this option on to show the total budget in the task list.":
        "打开此选项以在任务列表中显示总预算。",
    "Turn this option on to show the total fee in the task list.":
        "打开此选项以在任务列表中显示总费用。",
    "Turn this option on to show the creation date in the task list.":
        "打开此选项以在任务列表中显示创建日期。",
    "Turn this option on to show the modification date in the task list.":
        "打开此选项以在任务列表中显示修改日期。",
    "Turn this option on to show the icon in the task list.":
        "打开此选项以在任务列表中显示图标。",
    "Turn this option on to show the categories in the task list.":
        "打开此选项以在任务列表中显示分类。",
    "Turn this option on to show the description in the task list.":
        "打开此选项以在任务列表中显示描述。",
    "Turn this option on to hide the time spent in the task list.":
        "打开此选项以在任务列表中隐藏花费的时间。",
    "Turn this option on to hide the budget in the task list.":
        "打开此选项以在任务列表中隐藏预算。",
    "Turn this option on to hide the hourly fee in the task list.":
        "打开此选项以在任务列表中隐藏时薪。",
    "Turn this option on to hide the fixed fee in the task list.":
        "打开此选项以在任务列表中隐藏固定费用。",
    "Turn this option on to hide the percentage complete in the task list.":
        "打开此选项以在任务列表中隐藏完成百分比。",
    "Turn this option on to hide the priority in the task list.":
        "打开此选项以在任务列表中隐藏优先级。",
    "Turn this option on to hide the start date in the task list.":
        "打开此选项以在任务列表中隐藏开始日期。",
    "Turn this option on to hide the due date in the task list.":
        "打开此选项以在任务列表中隐藏到期日期。",
    "Turn this option on to hide the completion date in the task list.":
        "打开此选项以在任务列表中隐藏完成日期。",
    "Turn this option on to hide the reminder in the task list.":
        "打开此选项以在任务列表中隐藏提醒。",
    "Turn this option on to hide the attachment indicator in the task list.":
        "打开此选项以在任务列表中隐藏附件指示器。",
    "Turn this option on to hide the note indicator in the task list.":
        "打开此选项以在任务列表中隐藏笔记指示器。",
    "Turn this option on to hide the category indicator in the task list.":
        "打开此选项以在任务列表中隐藏分类指示器。",
    "Turn this option on to hide the recurrence indicator in the task list.":
        "打开此选项以在任务列表中隐藏重复指示器。",
    "Turn this option on to hide the dependency indicator in the task list.":
        "打开此选项以在任务列表中隐藏依赖关系指示器。",
    "Turn this option on to hide the effort in the task list.":
        "打开此选项以在任务列表中隐藏工作记录。",
    "Turn this option on to hide the parent in the task list.":
        "打开此选项以在任务列表中隐藏父任务。",
    "Turn this option on to hide the children in the task list.":
        "打开此选项以在任务列表中隐藏子任务。",
    "Turn this option on to hide the total effort in the task list.":
        "打开此选项以在任务列表中隐藏总工作记录。",
    "Turn this option on to hide the total budget in the task list.":
        "打开此选项以在任务列表中隐藏总预算。",
    "Turn this option on to hide the total fee in the task list.":
        "打开此选项以在任务列表中隐藏总费用。",
    "Turn this option on to hide the creation date in the task list.":
        "打开此选项以在任务列表中隐藏创建日期。",
    "Turn this option on to hide the modification date in the task list.":
        "打开此选项以在任务列表中隐藏修改日期。",
    "Turn this option on to hide the icon in the task list.":
        "打开此选项以在任务列表中隐藏图标。",
    "Turn this option on to hide the categories in the task list.":
        "打开此选项以在任务列表中隐藏分类。",
    "Turn this option on to hide the description in the task list.":
        "打开此选项以在任务列表中隐藏描述。",
}

def translate_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    i = 0
    count = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)
        
        if line.startswith('msgid "'):
            msgid = line[7:].rstrip('"\n')
            if msgid in TRANSLATIONS:
                if i + 1 < len(lines) and lines[i + 1] == 'msgstr ""':
                    result.append(f'msgstr "{TRANSLATIONS[msgid]}"')
                    count += 1
                    i += 1
        
        i += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    print(f"Translation complete. Fixed {count} entries.")
    return count

if __name__ == '__main__':
    translate_file(
        'taskcoachlib/i18n/locales/zh_CN.po',
        'taskcoachlib/i18n/locales/zh_CN.po'
    )
