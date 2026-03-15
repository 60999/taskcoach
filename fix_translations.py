#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch translate empty msgstr entries in zh_CN.po file.
This script reads the .po file, extracts empty msgstr entries,
and translates them using a comprehensive translation dictionary.
"""

import re

# Comprehensive translation dictionary
TRANSLATIONS = {
    # Preferences
    "Auto load when the file changes on disk": "文件在磁盘上更改时自动加载",
    "Smart filesystem monitoring": "智能文件系统监控",
    
    # Backup manager
    "File": "文件",
    "Full path": "完整路径",
    "Date": "日期",
    "Restore": "恢复",
    "close": "关闭",
    "Choose the restoration destination": "选择恢复目标",
    
    # Entry dialog
    "previous planned start and/or due date": "上一次计划开始和/或到期日期",
    "last completion date": "上次完成日期",
    
    # Priority commands
    "Decrease priority": "降低优先级",
    "Decrease priority of \"%s\"": "降低 \"%s\" 的优先级",
    "Change priority": "更改优先级",
    "Change priority of \"%s\"": "更改 \"%s\" 的优先级",
    
    # Task commands
    "Add note to tasks": "添加笔记到任务",
    "Change planned start date": "更改计划开始日期",
    "Change planned start date of \"%s\"": "更改 \"%s\" 的计划开始日期",
    "Change due date": "更改到期日期",
    "Change due date of \"%s\"": "更改 \"%s\" 的到期日期",
    "Change actual start date": "更改实际开始日期",
    "Change actual start date of \"%s\"": "更改 \"%s\" 的实际开始日期",
    "Change completion date": "更改完成日期",
    "Change completion date of \"%s\"": "更改 \"%s\" 的完成日期",
    "Change reminder dates/times": "更改提醒日期/时间",
    "Change reminder date/time of \"%s\"": "更改 \"%s\" 的提醒日期/时间",
    "Change recurrences": "更改重复",
    "Change recurrence of \"%s\"": "更改 \"%s\" 的重复",
    "Change percentage complete of \"%s\"": "更改 \"%s\" 的完成百分比",
    "Change when tasks are marked completed": "更改任务标记完成时的行为",
    "Change when \"%s\" is marked completed": "更改 \"%s\" 标记完成时的行为",
    "Change budgets": "更改预算",
    "Change budget of \"%s\"": "更改 \"%s\" 的预算",
    "Change hourly fees": "更改时薪",
    "Change hourly fee of \"%s\"": "更改 \"%s\" 的时薪",
    "Change fixed fees": "更改固定费用",
    "Change fixed fee of \"%s\"": "更改 \"%s\" 的固定费用",
    "Change planned durations": "更改计划时长",
    "Change planned duration of \"%s\"": "更改 \"%s\" 的计划时长",
    "Change planned duration modes": "更改计划时长模式",
    "Change planned duration mode of \"%s\"": "更改 \"%s\" 的计划时长模式",
    "Toggle prerequisite": "切换前置条件",
    "Toggle prerequisite of \"%s\"": "切换 \"%s\" 的前置条件",
    
    # Render
    "Mon": "周一",
    "Tue": "周二",
    "Wed": "周三",
    "Thu": "周四",
    "Fri": "周五",
    "Sat": "周六",
    "Sun": "周日",
    "Today": "今天",
    "yesterday": "昨天",
    "tomorrow": "明天",
    "now": "现在",
    "Every other day": "每隔一天",
    "Every other week": "每隔一周",
    "Every other month": "每隔一月",
    "Every other year": "每隔一年",
    "Daily": "每天",
    "Weekly": "每周",
    "Monthly": "每月",
    "Yearly": "每年",
    
    # Calendar config
    "Day(s)": "天",
    "Week(s)": "周",
    "Month": "月",
    "Horizontal": "水平",
    "Vertical": "垂直",
    "Which tasks to display": "显示哪些任务",
    "Tasks with a planned start date and a due date": "有计划开始日期和到期日期的任务",
    "Tasks with a planned start date": "有计划开始日期的任务",
    "Tasks with a due date": "有到期日期的任务",
    "All tasks, except unplanned tasks": "所有任务，除未计划任务外",
    "All tasks": "所有任务",
    "Draw a line showing the current time": "绘制显示当前时间的线",
    "Color used to highlight the current day": "用于突出显示当前日期的颜色",
    "Kind of period displayed and its count": "显示的周期类型及其数量",
    "Calendar orientation": "日历方向",
    
    # Widgets
    "Tasks": "任务",
    "days": "天",
    "hours": "小时",
    "mins": "分钟",
    "secs": "秒",
    "d": "天",
    "Label": "标签",
    "Hints": "提示",
    "Theme": "主题",
    "Context": "上下文",
    "Key": "键",
    "Choose Icon": "选择图标",
    "Search icons...": "搜索图标...",
    "Clear": "清除",
    "All files (*.*)|*": "所有文件(*.*)|*",
    
    # Effort commands
    "Change effort stop date and time": "更改工作记录停止日期和时间",
    "Change effort stop date and time of \"%s\"": "更改 \"%s\" 工作记录的停止日期和时间",
    "Change effort durations": "更改工作记录时长",
    "Change effort duration of \"%s\"": "更改 \"%s\" 工作记录的时长",
    "Change effort entry modes": "更改工作记录录入模式",
    "Change effort entry mode of \"%s\"": "更改 \"%s\" 工作记录的录入模式",
    
    # Note commands
    "Drag and drop note \"%s\"": "拖放笔记 \"%s\"",
    "Drag and drop notes": "拖放笔记",
    "Add note": "添加笔记",
    "Add note to \"%s\"": "添加笔记到 \"%s\"",
    "Add subnote": "添加子笔记",
    "Add subnote to \"%s\"": "添加子笔记到 \"%s\"",
    "Remove note": "移除笔记",
    "Remove note from \"%s\"": "从 \"%s\" 移除笔记",
    "New note": "新建笔记",
    "New subnote": "新建子笔记",
    "New subnote of \"%s\"": "\"%s\" 的新子笔记",
    "Delete note \"%s\"": "删除笔记 \"%s\"",
    "Delete notes": "删除笔记",
    
    # Category commands
    "New category": "新建分类",
    "New subcategory": "新建子分类",
    "New subcategory of \"%s\"": "\"%s\" 的新子分类",
    "Edit exclusive subcategories": "编辑互斥子分类",
    "Edit exclusive subcategories of \"%s\"": "编辑 \"%s\" 的互斥子分类",
    "Edit style priority": "编辑样式优先级",
    "Edit style priority of \"%s\"": "编辑 \"%s\" 的样式优先级",
    
    # Effort commands
    "New efforts": "新建工作记录",
    "New effort of \"%s\"": "\"%s\" 的新工作记录",
    "Add efforts": "添加工作记录",
    "Add effort to \"%s\"": "添加工作记录到 \"%s\"",
    "Delete efforts": "删除工作记录",
    "Delete effort \"%s\"": "删除工作记录 \"%s\"",
    "Change task of effort": "更改工作记录的任务",
    "Change task of \"%s\" effort": "更改 \"%s\" 工作记录的任务",
    "Change effort start date and time": "更改工作记录开始日期和时间",
    "Change effort start date and time of \"%s\"": "更改 \"%s\" 工作记录的开始日期和时间",
    
    # Task commands
    "Drag and drop tasks": "拖放任务",
    "Delete tasks": "删除任务",
    "Delete task \"%s\"": "删除任务 \"%s\"",
    "New task": "新建任务",
    "New subtasks": "新建子任务",
    "New subtask of \"%s\"": "\"%s\" 的新子任务",
    "Mark tasks completed": "标记任务完成",
    "Mark \"%s\" completed": "标记 \"%s\" 完成",
    "Mark task active": "标记任务为活动",
    "Mark \"%s\" active": "标记 \"%s\" 为活动",
    "Mark task inactive": "标记任务为非活动",
    "Mark \"%s\" inactive": "标记 \"%s\" 为非活动",
    "Start tracking": "开始跟踪",
    "Start tracking \"%s\"": "开始跟踪 \"%s\"",
    "Stop tracking": "停止跟踪",
    "Stop tracking \"%s\"": "停止跟踪 \"%s\"",
    "Maximize priority": "最大化优先级",
    "Maximize priority of \"%s\"": "最大化 \"%s\" 的优先级",
    "Minimize priority": "最小化优先级",
    "Minimize priority of \"%s\"": "最小化 \"%s\" 的优先级",
    "Increase priority": "提高优先级",
    "Increase priority of \"%s\"": "提高 \"%s\" 的优先级",
    "Toggle category": "切换分类",
    "Toggle category of \"%s\"": "切换 \"%s\" 的分类",
    
    # Various
    "Check mark": "选中标记",
    "Check marks": "选中标记",
    "Clock": "时钟",
    "Alarm clock": "闹钟",
    "Stopwatch": "秒表",
    "Cogwheel": "齿轮",
    "Cogwheels": "齿轮",
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
        
        if line.startswith('msgid '):
            msgid = line[6:].strip('"')
            if i + 1 < len(lines) and lines[i + 1] == 'msgstr ""':
                if msgid in TRANSLATIONS:
                    result.append(f'msgstr "{TRANSLATIONS[msgid]}"')
                    count += 1
                    i += 1
                else:
                    result.append(lines[i + 1])
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
