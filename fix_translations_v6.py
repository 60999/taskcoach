# -*- coding: utf-8 -*-
"""
批量修复 zh_CN.po 文件中剩余的多行msgid空翻译
使用精确匹配po文件中的实际文本
"""
import re
import shutil

# 精确匹配po文件中的msgid文本和对应的翻译
TRANSLATION_PAIRS = [
    # (msgid原文, msgstr翻译)
    (
        '"New tasks start with \\"Preset\\" dates and times filled in and checked. "\n'
        '"\\"Proposed\\" dates and times are filled in, but not checked.\\n"\n'
        '"\\n"\n'
        '"\\"Start of day\\" is midnight and \\"End of day\\" is just before midnight. "\n'
        '"When using these, task viewers hide the time and show only the date.\\n"\n'
        '"\\n"\n'
        '"\\"Start of working day\\" and \\"End of working day\\" use the working day as "\n'
        '"set in the Features tab of this preferences dialog."',
        '"新任务以\\"预设\\"日期和时间填充并选中。\\"建议\\"的日期和时间已填充但未选中。\\n"\n'
        '"\\n"\n'
        '"\\"一天开始\\"是午夜，\\"一天结束\\"是午夜前一刻。使用这些时，任务查看器隐藏时间只显示日期。\\n"\n'
        '"\\n"\n'
        '"\\"工作日开始\\"和\\"工作日结束\\"使用此首选项对话框功能选项卡中设置的工作日。"'
    ),
    (
        '"When dropping an e-mail from Mail.app, try to get its subject.\\n"\n'
        '"This takes up to a few seconds per e-mail."',
        '"当从Mail.app拖放邮件时，尝试获取其主题。\\n"\n'
        '"每封邮件可能需要几秒钟。"'
    ),
    (
        '"When opening the task editor, select the task subject and focus it.\\n"\n'
        '"This overwrites the default behavior of focusing the first tab."',
        '"打开任务编辑器时，选择并聚焦任务主题。\\n"\n'
        '"这将覆盖默认的聚焦第一个标签页的行为。"'
    ),
    (
        '"The backup manager will now open to allow you to restore\\n"\n'
        '"an older version of the task file."',
        '"备份管理器现在将打开，允许您恢复\\n"\n'
        '"任务文件的旧版本。"'
    ),
    (
        '"Couldn\'t restore the pane layout from TaskCoach.ini:\\n"\n'
        '"%s\\n\\n"\n'
        '"The default pane layout will be used."',
        '"无法从TaskCoach.ini恢复面板布局：\\n"\n'
        '"%s\\n\\n"\n'
        '"将使用默认面板布局。"'
    ),
    (
        '"When in tree mode, manual ordering is only possible when all selected items are at the same level."',
        '"在树形模式下，只有当所有选中项处于同一级别时才能手动排序。"'
    ),
    (
        '"Effort: %d selected, %d visible, %d total. Time spent: %s selected, %s visible, %s total."',
        '"工作记录：%d 已选，%d 可见，%d 总计。花费时间：%s 已选，%s 可见，%s 总计。"'
    ),
    (
        '"Shift-click on a filter tool to see only tasks belonging to the corresponding status."',
        '"Shift键点击过滤工具可只查看属于相应状态的任务。"'
    ),
    (
        '"Show the \\"Manual ordering\\" column, then drag and drop items from this column to reorder."',
        '"显示\\"手动排序\\"列，然后从此列拖放项目来重新排序。"'
    ),
    (
        '"Tasks are the basic objects that you manipulate. Tasks can\\n"\n'
        '"represent anything from a simple errand to a complex project."',
        '"任务是您操作的基本对象。任务可以\\n"\n'
        '"代表从简单差事到复杂项目的任何事情。"'
    ),
    (
        '"Planned start date: the first date on which the task can be started. \\n"\n'
        '"The planned start date can be in the future; if it is, the task is inactive."',
        '"计划开始日期：可以开始任务的第一个日期。\\n"\n'
        '"计划开始日期可以是未来的；如果是，则任务处于非活动状态。"'
    ),
    (
        '"Completion date: this date is \'None\' as long as the task has \\n"\n'
        '"not been completed. When the task is completed, the completion date is set."',
        '"完成日期：只要任务尚未完成，此日期为\'无\'。\\n"\n'
        '"当任务完成时，完成日期被设置。"'
    ),
    (
        '"Prerequisites: other tasks that need to be completed before\\n"\n'
        '"a task can be started."',
        '"前置任务：在任务开始之前\\n"\n'
        '"需要完成的其他任务。"'
    ),
    (
        '"This all assumes you have not changed the text colors through the \\n"\n'
        '"preferences dialog."',
        '"所有这些都假设您没有通过首选项对话框\\n"\n'
        '"更改文本颜色。"'
    ),
    (
        '"The background color of tasks is determined by the categories the \\n"\n'
        '"task belongs to."',
        '"任务的背景颜色由任务所属的类别决定。"'
    ),
    (
        '"You can set a reminder for a specific date and time. %(name)s will\\n"\n'
        '"show a reminder dialog when that date and time arrives."',
        '"您可以为特定日期和时间设置提醒。%(name)s将在\\n"\n'
        '"该日期和时间到达时显示提醒对话框。"'
    ),
    (
        '"Whenever you spent time on tasks, you can record the amount of time\\n"\n'
        '"spent by tracking effort."',
        '"每当您在任务上花费时间时，您可以通过跟踪工作记录\\n"\n'
        '"来记录花费的时间量。"'
    ),
    (
        '"Stop date/time: stop date and time of the effort. This can be \\n"\n'
        '"\'None\' as long as the effort is still being tracked."',
        '"停止日期/时间：工作记录的停止日期和时间。只要\\n"\n'
        '"工作记录仍在跟踪，这可以是\'无\'。"'
    ),
    (
        '"Tasks and notes may belong to one or more categories. First, you \\n"\n'
        '"need to create the categories you want to use."',
        '"任务和笔记可以属于一个或多个类别。首先，您\\n"\n'
        '"需要创建要使用的类别。"'
    ),
    (
        '"You can limit the items shown in the task and notes viewers to one \\n"\n'
        '"or more categories by checking the category filter."',
        '"您可以通过选中类别过滤器来限制任务和笔记查看器中\\n"\n'
        '"显示的项目为一个或多个类别。"'
    ),
    (
        '"Mutually exclusive subcategories: a check box indicating\\n"\n'
        '"whether the subcategories are mutually exclusive."',
        '"互斥子类别：一个复选框，指示\\n"\n'
        '"子类别是否互斥。"'
    ),
    (
        '"Appearance properties such as icon, font and colors: \\n"\n'
        '"the appearance properties are used when a task or note belongs to the category."',
        '"外观属性如图标、字体和颜色：\\n"\n'
        '"当任务或笔记属于该类别时使用外观属性。"'
    ),
    (
        '"Notes can be used to capture random information that you want\\n"\n'
        '"to keep in your task file."',
        '"笔记可用于捕获您想要\\n"\n'
        '"保留在任务文件中的随机信息。"'
    ),
    (
        '"Both printing and exporting work in the same way: when you print\\n"\n'
        '"or export data, the following steps are taken:"',
        '"打印和导出都以相同的方式工作：当您打印\\n"\n'
        '"或导出数据时，会执行以下步骤："'
    ),
    (
        '"Prepare the contents of a viewer, by putting the items in the \\n"\n'
        '"right order, showing or hiding columns as needed."',
        '"准备查看器的内容，通过将项目按正确顺序排列，\\n"\n'
        '"根据需要显示或隐藏列。"'
    ),
    (
        '"You can preview how the print will look\\n"\n'
        '"using the File -> Print preview menu item."',
        '"您可以使用文件 -> 打印预览菜单项\\n"\n'
        '"预览打印效果。"'
    ),
    (
        '"Next, choose the format you want to export to and whether you\\n"\n'
        '"want to export all items or only selected items."',
        '"接下来，选择您要导出的格式以及\\n"\n'
        '"要导出所有项目还是仅导出所选项目。"'
    ),
    (
        '"You can alter the behaviour of the e-mail command using custom attributes\\n"\n'
        '"in a task description."',
        '"您可以使用任务描述中的自定义属性\\n"\n'
        '"更改电子邮件命令的行为。"'
    ),
    (
        '"A task file may be opened by several instances of %(name)s, either\\n"\n'
        '"running on the same computer or on different computers."',
        '"任务文件可以被%(name)s的多个实例打开，\\n"\n'
        '"无论是在同一台计算机上还是在不同的计算机上运行。"'
    ),
    (
        '"The first case is the most common and the most secure. The second\\n"\n'
        '"case may be dangerous."',
        '"第一种情况最常见也最安全。第二种\\n"\n'
        '"情况可能很危险。"'
    ),
    (
        '"None of the sharing options discussed here work fully. If two users\\n"\n'
        '"save their changes at the same time, data will be lost."',
        '"这里讨论的共享选项都不能完全工作。如果两个用户\\n"\n'
        '"同时保存更改，数据将丢失。"'
    ),
    (
        '"This is the most common protocol: Windows shares and their lookalikes\\n"\n'
        '"(Samba). This protocol works fine on local networks."',
        '"这是最常见的协议：Windows共享及其类似物\\n"\n'
        '"（Samba）。此协议在局域网上工作良好。"'
    ),
    (
        '"A popular way to access files from several computers (also see SpiderOak\\n"\n'
        '"for a secure alternative)."',
        '"一种从多台计算机访问文件的流行方式（也可以看看SpiderOak\\n"\n'
        '"作为安全的替代方案）。"'
    ),
    (
        '"%(name)s integrates with several mail user\\n"\n'
        '"agents, through drag and drop. This allows you to attach e-mails to tasks."',
        '"%(name)s与多个邮件用户代理集成，\\n"\n'
        '"通过拖放。这允许您将电子邮件附加到任务。"'
    ),
    (
        '"Due to a Thunderbird limitation, you can\'t drag and drop several\\n"\n'
        '"e-mails from Thunderbird at once."',
        '"由于Thunderbird的限制，您无法一次从Thunderbird\\n"\n'
        '"拖放多封电子邮件。"'
    ),
    (
        '"Dropping an e-mail on an empty part of the task tree or task list\\n"\n'
        '"creates a new task with the e-mail attached."',
        '"将电子邮件拖放到任务树或任务列表的空白部分\\n"\n'
        '"会创建一个附加了电子邮件的新任务。"'
    ),
    (
        '"SyncML is an XML protocol designed to synchronize several\\n"\n'
        '"applications with a server."',
        '"SyncML是一种XML协议，旨在将多个\\n"\n'
        '"应用程序与服务器同步。"'
    ),
    (
        '"%(name)s has built-in SyncML client support on Windows and Mac OS X\\n"\n'
        '"(provided the Mac has Mac OS X 10.5 or later)."',
        '"%(name)s在Windows和Mac OS X上内置SyncML客户端支持\\n"\n'
        '"（前提是Mac具有Mac OS X 10.5或更高版本）。"'
    ),
    (
        '"On Linux, you must install the SyncML client binding for\\n"\n'
        '"Python yourself. A 64 bits version is available."',
        '"在Linux上，您必须自己安装Python的\\n"\n'
        '"SyncML客户端绑定。有64位版本可用。"'
    ),
    (
        '"This feature is optional and off by default. In order to turn it on,\\n"\n'
        '"go to the SyncML preferences and check \'Enable SyncML\'."',
        '"此功能是可选的，默认关闭。要启用它，\\n"\n'
        '"请转到SyncML首选项并选中\'启用SyncML\'。"'
    ),
    (
        '"To setup SyncML, edit the SyncML preferences in Edit/SyncML \\n"\n'
        '"preferences. Fill in the server URL, username and password."',
        '"要设置SyncML，请在编辑/SyncML首选项中\\n"\n'
        '"编辑SyncML首选项。填写服务器URL、用户名和密码。"'
    ),
    (
        '"Each task file has its own client ID, so that two different task \\n"\n'
        '"files will be synchronized independently."',
        '"每个任务文件都有自己的客户端ID，因此两个不同的任务\\n"\n'
        '"文件将独立同步。"'
    ),
    (
        '"Some limitations are due to the fact that, the underlying data \\n"\n'
        '"type being vcalendar, some features are not supported."',
        '"一些限制是由于底层数据类型是vcalendar，\\n"\n'
        '"某些功能不受支持。"'
    ),
    (
        '"The conflict detection/resolution system is a workaround \\n"\n'
        '"for a Funambol limitation."',
        '"冲突检测/解决系统是\\n"\n'
        '"Funambol限制的变通方法。"'
    ),
    (
        '"You may experience problems under Windows if you don\'t have the \\n"\n'
        '"Microsoft Visual C++ 2008 Redistributable Package installed."',
        '"如果您没有安装Microsoft Visual C++ 2008可再发行组件包，\\n"\n'
        '"您可能会在Windows下遇到问题。"'
    ),
    (
        '"When SyncML is enabled, deleting a task or a note does not actually\\n"\n'
        '"delete it, but marks it as deleted."',
        '"启用SyncML后，删除任务或笔记实际上\\n"\n'
        '"不会删除它，而是将其标记为已删除。"'
    ),
    (
        '"In this case, the \\"Purge deleted items\\" menu item in the File menu \\n"\n'
        '"can be used to permanently delete them."',
        '"在这种情况下，可以使用文件菜单中的\\"清除已删除项目\\"菜单项\\n"\n'
        '"永久删除它们。"'
    ),
    (
        '"There is an iPhone/iPod Touch/iPad companion app for %(name)s, \\n"\n'
        '"available on <a href=\\"http://itunes.com/app/taskcoach/\\">Apple\'s App Store</a>."',
        '"%(name)s有一个iPhone/iPod Touch/iPad伴侣应用，\\n"\n'
        '"可在<a href=\\"http://itunes.com/app/taskcoach/\\">Apple的App Store</a>上获得。"'
    ),
    (
        '"There are some settings for the iPhone/iPod Touch/iPad app in the \\n"\n'
        '"Settings app on your device."',
        '"您设备上的设置应用中有一些\\n"\n'
        '"iPhone/iPod Touch/iPad应用的设置。"'
    ),
    (
        '"Icon position: the LED icon may show up either on the \\n"\n'
        '"left side or the right side of the task."',
        '"图标位置：LED图标可以显示在任务的\\n"\n'
        '"左侧或右侧。"'
    ),
    (
        '"Compact mode: if this is enabled, the task list has smaller \\n"\n'
        '"LEDs and doesn\'t show the task description."',
        '"紧凑模式：如果启用，任务列表有更小的\\n"\n'
        '"LED并且不显示任务描述。"'
    ),
    (
        '"Confirm complete: if enabled, a message box will pop up for \\n"\n'
        '"confirmation when completing a task."',
        '"确认完成：如果启用，完成任务时\\n"\n'
        '"会弹出消息框进行确认。"'
    ),
    (
        '"Before synchronizing, you must also configure %(name)s on the \\n"\n'
        '"desktop; in the preferences, iPhone page."',
        '"同步之前，您还必须在桌面上配置%(name)s；\\n"\n'
        '"在首选项中，iPhone页面。"'
    ),
    (
        '"When you tap the \\"Sync\\" button in the category view, %(name)s\\n"\n'
        '"will automatically try to find a running desktop instance."',
        '"当您在类别视图中点击\\"同步\\"按钮时，%(name)s\\n"\n'
        '"将自动尝试查找正在运行的桌面实例。"'
    ),
    (
        '"%(name)s will remember the chosen instance and try it next time\\n"\n'
        '"you synchronize."',
        '"%(name)s将记住选择的实例，并在下次\\n"\n'
        '"同步时尝试它。"'
    ),
    (
        '"Note that this synchronization happens through the network; there \\n"\n'
        '"is no need for a cable."',
        '"请注意，此同步通过网络进行；\\n"\n'
        '"不需要电缆。"'
    ),
    (
        '"On Windows, you must install <a\\n"\n'
        '"href=\\"http://support.apple.com/kb/dl999\\">Bonjour</a> for this to work."',
        '"在Windows上，您必须安装<a\\n"\n'
        '"href=\\"http://support.apple.com/kb/dl999\\">Bonjour</a>才能使其工作。"'
    ),
    (
        '"On Linux, you must have the <a href=\\"http://avahi.org/\\">Avahi</a> \\n"\n'
        '"daemon installed and running."',
        '"在Linux上，您必须安装并运行\\n"\n'
        '"<a href=\\"http://avahi.org/\\">Avahi</a>守护程序。"'
    ),
    (
        '"You need to have iTunes installed on your computer to browse \\n"\n'
        '"Apple\'s App Store."',
        '"您需要在计算机上安装iTunes才能浏览\\n"\n'
        '"Apple的App Store。"'
    ),
    (
        '"Check that your iPhone/iPod Touch is connected to the same network \\n"\n'
        '"your computer is connected to."',
        '"检查您的iPhone/iPod Touch是否连接到\\n"\n'
        '"您的计算机所连接的同一网络。"'
    ),
    (
        '"No, %(name)s is not available for the Android platform. But,\\n"\n'
        '"<a target=\\"_blank\\" href=\\"http://www.todotodo.com\\">Todo Todo</a> can sync with %(name)s."',
        '"不，%(name)s不适用于Android平台。但是，\\n"\n'
        '"<a target=\\"_blank\\" href=\\"http://www.todotodo.com\\">Todo Todo</a>可以与%(name)s同步。"'
    ),
    (
        '"Todo.txt is an open source todo list manager, created by Gina \\n"\n'
        '"Trapani, that works in a simple text file."',
        '"Todo.txt是一个开源待办事项列表管理器，由Gina \\n"\n'
        '"Trapani创建，在一个简单的文本文件中工作。"'
    ),
    (
        '"When exporting to Todo.txt, %(name)s creates another file alongside\\n"\n'
        '"the target file with extension .idmap."',
        '"导出到Todo.txt时，%(name)s会在目标文件旁边\\n"\n'
        '"创建另一个扩展名为.idmap的文件。"'
    ),
    (
        '"Tip: if you save your task file in the todo folder that Todo.txt\\n"\n'
        '"Touch creates on Dropbox, you can sync your tasks with Todo.txt Touch."',
        '"提示：如果您将任务文件保存在Todo.txt Touch\\n"\n'
        '"在Dropbox上创建的todo文件夹中，您可以将任务与Todo.txt Touch同步。"'
    ),
    (
        '"%(name)s imports task subjects, planned start date, due date, completion \\n"\n'
        '"date, priority, and categories."',
        '"%(name)s导入任务主题、计划开始日期、截止日期、完成\\n"\n'
        '"日期、优先级和类别。"'
    ),
    (
        '"When importing, %(name)s tries to find matching tasks and \\n"\n'
        '"categories and updates them if necessary."',
        '"导入时，%(name)s尝试找到匹配的任务和\\n"\n'
        '"类别，并在必要时更新它们。"'
    ),
    (
        '"%(name)s exports task subjects, planned start date, due date, completion \\n"\n'
        '"date, priority, and categories."',
        '"%(name)s导出任务主题、计划开始日期、截止日期、完成\\n"\n'
        '"日期、优先级和类别。"'
    ),
    (
        '"%(name)s supports dates and times, but Todo.txt only supports \\n"\n'
        '"dates, so the time information is lost."',
        '"%(name)s支持日期和时间，但Todo.txt只支持\\n"\n'
        '"日期，因此时间信息会丢失。"'
    ),
    (
        '"The default Todo.txt format only supports planned start dates and \\n"\n'
        '"completion dates, not due dates."',
        '"默认的Todo.txt格式只支持计划开始日期和\\n"\n'
        '"完成日期，不支持截止日期。"'
    ),
    (
        '"Todo.txt has priorities in the form of a letter (\'A\'-\'Z\'). \\n"\n'
        '"%(name)s has numerical priorities."',
        '"Todo.txt的优先级以字母形式表示（\'A\'-\'Z\'）。\\n"\n'
        '"%(name)s具有数字优先级。"'
    ),
    (
        '"Categories whose subject starts with a \'+\' are exported as projects. \\n"\n'
        '"Categories whose subject starts with a \'@\' are exported as contexts."',
        '"主题以\'+\'开头的类别作为项目导出。\\n"\n'
        '"主题以\'@\'开头的类别作为上下文导出。"'
    ),
    (
        '"Templates are blueprints for new tasks. Right now, the only task \\n"\n'
        '"properties that can be templated are dates."',
        '"模板是新任务的蓝图。目前，唯一可以\\n"\n'
        '"模板化的任务属性是日期。"'
    ),
    (
        '"One can create a template by selecting a task (only one) and click \\n"\n'
        '"on the \\"Save as template\\" menu item."',
        '"可以通过选择一个任务（只有一个）并点击\\n"\n'
        '"\\"保存为模板\\"菜单项来创建模板。"'
    ),
    (
        '"You can also create a new template from a pre-made template file \\n"\n'
        '"(.tsktmpl); just drag it onto the task list."',
        '"您也可以从预制模板文件\\n"\n'
        '"（.tsktmpl）创建新模板；只需将其拖到任务列表上。"'
    ),
    (
        '"In order to instantiate a task template, use the \\"New task from \\n"\n'
        '"template\\" menu item."',
        '"要实例化任务模板，请使用\\"从模板新建任务\\"\\n"\n'
        '"菜单项。"'
    ),
    (
        '"You can also add templates from the template editor (File/Edit\\n"\n'
        '"templates), as well as remove templates."',
        '"您也可以从模板编辑器（文件/编辑\\n"\n'
        '"模板）添加模板，以及删除模板。"'
    ),
    (
        '"You can drag and drop viewers to create almost any user interface \\n"\n'
        '"layout you want."',
        '"您可以拖放查看器来创建几乎任何您想要的\\n"\n'
        '"用户界面布局。"'
    ),
    (
        '"In the edit dialogs, you can drag and drop tabs to rearrange \\n"\n'
        '"the order or to create new tabs."',
        '"在编辑对话框中，您可以拖放标签页来重新排列\\n"\n'
        '"顺序或创建新标签页。"'
    ),
    (
        '"Subjects and descriptions of tasks, notes and categories can be\\n"\n'
        '"edited without opening the editor dialog."',
        '"任务、笔记和类别的主题和描述可以\\n"\n'
        '"在不打开编辑器对话框的情况下编辑。"'
    ),
    (
        '"%(name)s has several keyboard shortcuts, listed below. Keyboard \\n"\n'
        '"shortcuts are not configurable."',
        '"%(name)s有几个键盘快捷键，如下所列。键盘\\n"\n'
        '"快捷键不可配置。"'
    ),
    (
        '"<h4>%(name)s - %(description)s</h4>\\n"\n'
        '"<h5>Version %(version)s, %(date)s</h5>\\n"\n'
        '"<p>%(copyright)s</p>\\n"\n'
        '"<p>%(website)s</p>"',
        '"<h4>%(name)s - %(description)s</h4>\\n"\n'
        '"<h5>版本 %(version)s, %(date)s</h5>\\n"\n'
        '"<p>%(copyright)s</p>\\n"\n'
        '"<p>%(website)s</p>"'
    ),
    (
        '"An iPhone or iPod Touch tried to connect to Task Coach,\\n"\n'
        '"but no password is set. Please set a password in the preferences."',
        '"iPhone或iPod Touch尝试连接到Task Coach，\\n"\n'
        '"但未设置密码。请在首选项中设置密码。"'
    ),
    (
        '"Could not open an IMAP connection to %(server)s:%(port)s\\n"\n'
        '"to retrieve Thunderbird message."',
        '"无法打开到%(server)s:%(port)s的IMAP连接\\n"\n'
        '"以检索Thunderbird消息。"'
    ),
]


def fix_translations(input_file, output_file):
    """修复po文件中的空翻译"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_count = 0
    
    for msgid_text, msgstr_text in TRANSLATION_PAIRS:
        # 构建搜索模式
        search_pattern = f'msgid ""\n{msgid_text}\nmsgstr ""'
        
        # 构建替换模式
        replace_pattern = f'msgid ""\n{msgid_text}\nmsgstr ""\n{msgstr_text}'
        
        if search_pattern in content:
            content = content.replace(search_pattern, replace_pattern)
            fixed_count += 1
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixed_count


if __name__ == '__main__':
    input_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    output_file = r'd:\Development\taskcoach\taskcoachlib\i18n\locales\zh_CN.po'
    
    # 先备份
    backup_file = input_file + '.bak6'
    shutil.copy(input_file, backup_file)
    print(f"已备份到: {backup_file}")
    
    # 修复翻译
    count = fix_translations(input_file, output_file)
    print(f"已修复 {count} 个空翻译")
