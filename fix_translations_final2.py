# -*- coding: utf-8 -*-
"""
修复 zh_CN.po 文件中所有剩余空翻译
"""
import shutil

TRANSLATIONS = {
    "When dropping an e-mail from Mail.app, try to get its subject.\nThis takes up to a few seconds per e-mail.": 
        "当从Mail.app拖放邮件时，尝试获取其主题。\n每封邮件可能需要几秒钟。",
    
    "When opening the task editor, select the task subject and focus it.\nThis overwrites the default behavior of focusing the first tab.": 
        "打开任务编辑器时，选择并聚焦任务主题。\n这将覆盖默认的聚焦第一个标签页的行为。",
    
    "The backup manager will now open to allow you to restore\nan older version of the task file.": 
        "备份管理器现在将打开，允许您恢复\n任务文件的旧版本。",
    
    "Couldn't restore the pane layout from TaskCoach.ini:\n%s\n\nThe default pane layout will be used.": 
        "无法从TaskCoach.ini恢复面板布局：\n%s\n\n将使用默认面板布局。",
    
    "Merge &disk changes\tShift-Ctrl-M": 
        "合并磁盘更改(&D)\tShift-Ctrl-M",
    
    "When in tree mode, manual ordering is only possible when all selected items are at the same level.": 
        "在树形模式下，只有当所有选中项处于同一级别时才能手动排序。",
    
    "Effort: %d selected, %d visible, %d total. Time spent: %s selected, %s visible, %s total.": 
        "工作记录：%d 已选，%d 可见，%d 总计。花费时间：%s 已选，%s 可见，%s 总计。",
    
    "Shift-click on a filter tool to see only tasks belonging to the corresponding status.": 
        "Shift键点击过滤工具可只查看属于相应状态的任务。",
    
    "Show the \"Manual ordering\" column, then drag and drop items from this column to reorder.": 
        "显示\"手动排序\"列，然后从此列拖放项目来重新排序。",
    
    "Tasks are the basic objects that you manipulate. Tasks can\nrepresent anything from a simple errand to a complex project.": 
        "任务是您操作的基本对象。任务可以\n代表从简单差事到复杂项目的任何事情。",
    
    "Planned start date: the first date on which the task can be started. \nThe planned start date can be in the future; if it is, the task is inactive.": 
        "计划开始日期：可以开始任务的第一个日期。\n计划开始日期可以是未来的；如果是，则任务处于非活动状态。",
    
    "Completion date: this date is 'None' as long as the task has \nnot been completed. When the task is completed, the completion date is set.": 
        "完成日期：只要任务尚未完成，此日期为'无'。\n当任务完成时，完成日期被设置。",
    
    "Prerequisites: other tasks that need to be completed before\na task can be started.": 
        "前置任务：在任务开始之前\n需要完成的其他任务。",
    
    "This all assumes you have not changed the text colors through the \npreferences dialog.": 
        "所有这些都假设您没有通过首选项对话框\n更改文本颜色。",
    
    "The background color of tasks is determined by the categories the \ntask belongs to.": 
        "任务的背景颜色由任务所属的类别决定。",
    
    "You can set a reminder for a specific date and time. %(name)s will\nshow a reminder dialog when that date and time arrives.": 
        "您可以为特定日期和时间设置提醒。%(name)s将在\n该日期和时间到达时显示提醒对话框。",
    
    "Whenever you spent time on tasks, you can record the amount of time\nspent by tracking effort.": 
        "每当您在任务上花费时间时，您可以通过跟踪工作记录\n来记录花费的时间量。",
    
    "Stop date/time: stop date and time of the effort. This can be \n'None' as long as the effort is still being tracked.": 
        "停止日期/时间：工作记录的停止日期和时间。只要\n工作记录仍在跟踪，这可以是'无'。",
    
    "Tasks and notes may belong to one or more categories. First, you \nneed to create the categories you want to use.": 
        "任务和笔记可以属于一个或多个类别。首先，您\n需要创建要使用的类别。",
    
    "You can limit the items shown in the task and notes viewers to one \nor more categories by checking the category filter.": 
        "您可以通过选中类别过滤器来限制任务和笔记查看器中\n显示的项目为一个或多个类别。",
    
    "Mutually exclusive subcategories: a check box indicating\nwhether the subcategories are mutually exclusive.": 
        "互斥子类别：一个复选框，指示\n子类别是否互斥。",
    
    "Appearance properties such as icon, font and colors: \nthe appearance properties are used when a task or note belongs to the category.": 
        "外观属性如图标、字体和颜色：\n当任务或笔记属于该类别时使用外观属性。",
    
    "Notes can be used to capture random information that you want\nto keep in your task file.": 
        "笔记可用于捕获您想要\n保留在任务文件中的随机信息。",
    
    "Both printing and exporting work in the same way: when you print\nor export data, the following steps are taken:": 
        "打印和导出都以相同的方式工作：当您打印\n或导出数据时，会执行以下步骤：",
    
    "Prepare the contents of a viewer, by putting the items in the \nright order, showing or hiding columns as needed.": 
        "准备查看器的内容，通过将项目按正确顺序排列，\n根据需要显示或隐藏列。",
    
    "You can preview how the print will look\nusing the File -> Print preview menu item.": 
        "您可以使用文件 -> 打印预览菜单项\n预览打印效果。",
    
    "Next, choose the format you want to export to and whether you\nwant to export all items or only selected items.": 
        "接下来，选择您要导出的格式以及\n要导出所有项目还是仅导出所选项目。",
    
    "You can alter the behaviour of the e-mail command using custom attributes\nin a task description.": 
        "您可以使用任务描述中的自定义属性\n更改电子邮件命令的行为。",
    
    "A task file may be opened by several instances of %(name)s, either\nrunning on the same computer or on different computers.": 
        "任务文件可以被%(name)s的多个实例打开，\n无论是在同一台计算机上还是在不同的计算机上运行。",
    
    "The first case is the most common and the most secure. The second\ncase may be dangerous.": 
        "第一种情况最常见也最安全。第二种\n情况可能很危险。",
    
    "None of the sharing options discussed here work fully. If two users\nsave their changes at the same time, data will be lost.": 
        "这里讨论的共享选项都不能完全工作。如果两个用户\n同时保存更改，数据将丢失。",
    
    "This is the most common protocol: Windows shares and their lookalikes\n(Samba). This protocol works fine on local networks.": 
        "这是最常见的协议：Windows共享及其类似物\n（Samba）。此协议在局域网上工作良好。",
    
    "A popular way to access files from several computers (also see SpiderOak\nfor a secure alternative).": 
        "一种从多台计算机访问文件的流行方式（也可以看看SpiderOak\n作为安全的替代方案）。",
    
    "%(name)s integrates with several mail user\nagents, through drag and drop. This allows you to attach e-mails to tasks.": 
        "%(name)s与多个邮件用户代理集成，\n通过拖放。这允许您将电子邮件附加到任务。",
    
    "Due to a Thunderbird limitation, you can't drag and drop several\ne-mails from Thunderbird at once.": 
        "由于Thunderbird的限制，您无法一次从Thunderbird\n拖放多封电子邮件。",
    
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
    
    "Each task file has its own client ID, so that two different task \nfiles will be synchronized independently.": 
        "每个任务文件都有自己的客户端ID，因此两个不同的任务\n文件将独立同步。",
    
    "Some limitations are due to the fact that, the underlying data \ntype being vcalendar, some features are not supported.": 
        "一些限制是由于底层数据类型是vcalendar，\n某些功能不受支持。",
    
    "The conflict detection/resolution system is a workaround \nfor a Funambol limitation.": 
        "冲突检测/解决系统是\nFunambol限制的变通方法。",
    
    "You may experience problems under Windows if you don't have the \nMicrosoft Visual C++ 2008 Redistributable Package installed.": 
        "如果您没有安装Microsoft Visual C++ 2008可再发行组件包，\n您可能会在Windows下遇到问题。",
    
    "When SyncML is enabled, deleting a task or a note does not actually\ndelete it, but marks it as deleted.": 
        "启用SyncML后，删除任务或笔记实际上\n不会删除它，而是将其标记为已删除。",
    
    "In this case, the \"Purge deleted items\" menu item in the File menu \ncan be used to permanently delete them.": 
        "在这种情况下，可以使用文件菜单中的\"清除已删除项目\"菜单项\n永久删除它们。",
    
    "There is an iPhone/iPod Touch/iPad companion app for %(name)s, \navailable on <a href=\"http://itunes.com/app/taskcoach/\">Apple's App Store</a>.": 
        "%(name)s有一个iPhone/iPod Touch/iPad伴侣应用，\n可在<a href=\"http://itunes.com/app/taskcoach/\">Apple的App Store</a>上获得。",
    
    "There are some settings for the iPhone/iPod Touch/iPad app in the \nSettings app on your device.": 
        "您设备上的设置应用中有一些\niPhone/iPod Touch/iPad应用的设置。",
    
    "Icon position: the LED icon may show up either on the \nleft side or the right side of the task.": 
        "图标位置：LED图标可以显示在任务的\n左侧或右侧。",
    
    "Compact mode: if this is enabled, the task list has smaller \nLEDs and doesn't show the task description.": 
        "紧凑模式：如果启用，任务列表有更小的\nLED并且不显示任务描述。",
    
    "Confirm complete: if enabled, a message box will pop up for \nconfirmation when completing a task.": 
        "确认完成：如果启用，完成任务时\n会弹出消息框进行确认。",
    
    "Before synchronizing, you must also configure %(name)s on the \ndesktop; in the preferences, iPhone page.": 
        "同步之前，您还必须在桌面上配置%(name)s；\n在首选项中，iPhone页面。",
    
    "When you tap the \"Sync\" button in the category view, %(name)s\nwill automatically try to find a running desktop instance.": 
        "当您在类别视图中点击\"同步\"按钮时，%(name)s\n将自动尝试查找正在运行的桌面实例。",
    
    "On Linux, you must have the <a href=\"http://avahi.org/\">Avahi</a> \ndaemon installed and running.": 
        "在Linux上，您必须安装并运行\n<a href=\"http://avahi.org/\">Avahi</a>守护程序。",
    
    "You need to have iTunes installed on your computer to browse \nApple's App Store.": 
        "您需要在计算机上安装iTunes才能浏览\nApple的App Store。",
    
    "Check that your iPhone/iPod Touch is connected to the same network \nyour computer is connected to.": 
        "检查您的iPhone/iPod Touch是否连接到\n您的计算机所连接的同一网络。",
    
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
    
    "You can drag and drop viewers to create almost any user interface \nlayout you want.": 
        "您可以拖放查看器来创建几乎任何您想要的\n用户界面布局。",
    
    "In the edit dialogs, you can drag and drop tabs to rearrange \nthe order or to create new tabs.": 
        "在编辑对话框中，您可以拖放标签页来重新排列\n顺序或创建新标签页。",
    
    "Subjects and descriptions of tasks, notes and categories can be\nedited without opening the editor dialog.": 
        "任务、笔记和类别的主题和描述可以\n在不打开编辑器对话框的情况下编辑。",
    
    "%(name)s has several keyboard shortcuts, listed below. Keyboard \nshortcuts are not configurable.": 
        "%(name)s有几个键盘快捷键，如下所列。键盘\n快捷键不可配置。",
    
    "<h4>%(name)s - %(description)s</h4>\n<h5>Version %(version)s, %(date)s</h5>\n<p>%(copyright)s</p>\n<p>%(website)s</p>": 
        "<h4>%(name)s - %(description)s</h4>\n<h5>版本 %(version)s, %(date)s</h5>\n<p>%(copyright)s</p>\n<p>%(website)s</p>",
    
    "An iPhone or iPod Touch tried to connect to Task Coach,\nbut no password is set. Please set a password in the preferences.": 
        "iPhone或iPod Touch尝试连接到Task Coach，\n但未设置密码。请在首选项中设置密码。",
    
    "Unrecognized URL scheme: \"%s\"": 
        "无法识别的URL方案：\"%s\"",
    
    "Could not open an IMAP connection to %(server)s:%(port)s\nto retrieve Thunderbird message.": 
        "无法打开到%(server)s:%(port)s的IMAP连接\n以检索Thunderbird消息。",
    
    "\"><b>": 
        "\"><b>",
    
    "<body bgcolor=\"#": 
        "<body bgcolor=\"#",
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
        
        if line.strip() == 'msgid ""':
            msgid_lines = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('"') and not lines[j].strip().startswith('msgstr'):
                msgid_lines.append(lines[j].strip())
                j += 1
            
            msgid_text = ''
            for ml in msgid_lines:
                if ml.startswith('"') and ml.endswith('"'):
                    content_part = ml[1:-1]
                    content_part = content_part.replace('\\n', '\n')
                    content_part = content_part.replace('\\t', '\t')
                    content_part = content_part.replace('\\"', '"')
                    content_part = content_part.replace('\\\\', '\\')
                    msgid_text += content_part
            
            k = j
            while k < len(lines) and not lines[k].strip().startswith('msgstr'):
                k += 1
            
            is_empty = False
            if k < len(lines) and lines[k].strip() == 'msgstr ""':
                next_line = k + 1
                has_content = False
                while next_line < len(lines) and lines[next_line].strip().startswith('"'):
                    if lines[next_line].strip() != '""':
                        has_content = True
                        break
                    next_line += 1
                is_empty = not has_content
            
            if is_empty and msgid_text in TRANSLATIONS:
                translation = TRANSLATIONS[msgid_text]
                
                result.append(line)
                for ml in msgid_lines:
                    result.append(ml)
                
                result.append('msgstr ""')
                for trans_line in translation.split('\n'):
                    result.append(f'"{trans_line}"')
                
                fixed_count += 1
                i = k + 1
                while i < len(lines) and lines[i].strip().startswith('"') and lines[i].strip() == '""':
                    i += 1
                continue
            
            result.append(line)
        else:
            result.append(line)
        
        i += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    return fixed_count


if __name__ == '__main__':
    input_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    output_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    backup_file = input_file + '.bak_final2'
    shutil.copy(input_file, backup_file)
    print(f"已备份到: {backup_file}")
    
    count = fix_translations(input_file, output_file)
    print(f"已修复 {count} 个空翻译")
