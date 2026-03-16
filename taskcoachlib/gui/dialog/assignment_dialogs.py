# -*- coding: utf-8 -*-
"""
Task Coach - Your friendly task manager
Copyright (C) 2004-2024 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Task assignment dialogs.
"""

import wx
from taskcoachlib import widgets
from taskcoachlib.i18n import _
from taskcoachlib.domain.assignment import Assignment


def _(text):
    """延迟加载的翻译函数。"""
    try:
        from taskcoachlib.i18n import _ as translate
        return translate(text)
    except Exception:
        return text


class AssignTaskDialog(wx.Dialog):
    """
    任务分配对话框。
    
    用于将任务分配给团队成员。
    """
    
    def __init__(self, parent, taskFile, tasks, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            taskFile: 任务文件对象
            tasks: 要分配的任务列表
        """
        super().__init__(
            parent, 
            title=_("分配任务"),
            size=(500, 400),
            **kwargs
        )
        self._taskFile = taskFile
        self._tasks = tasks if hasattr(tasks, '__iter__') else [tasks]
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        
        self.SetMinSize((400, 300))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        task_count = len(self._tasks)
        self._info_text = wx.StaticText(
            self, 
            label=_("已选择 %d 个任务") % task_count
        )
        
        self._assignee_label = wx.StaticText(self, label=_("分配给:"))
        
        assignee_choices = [_("选择团队成员...")]
        for user in self._taskFile.users():
            if user.isActive():
                assignee_choices.append(user.displayName())
        self._assignee_choice = wx.Choice(self, choices=assignee_choices)
        self._assignee_choice.SetSelection(0)
        
        self._note_label = wx.StaticText(self, label=_("备注:"))
        self._note_text = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
        
        self._ok_btn = wx.Button(self, wx.ID_OK, label=_("确定"))
        self._cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("取消"))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        main_sizer.Add(self._info_text, 0, wx.ALL, 10)
        
        assign_sizer = wx.BoxSizer(wx.HORIZONTAL)
        assign_sizer.Add(self._assignee_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        assign_sizer.Add(self._assignee_choice, 1, wx.EXPAND)
        
        main_sizer.Add(assign_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        note_sizer = wx.BoxSizer(wx.VERTICAL)
        note_sizer.Add(self._note_label, 0, wx.BOTTOM, 5)
        note_sizer.Add(self._note_text, 1, wx.EXPAND)
        
        main_sizer.Add(note_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self._ok_btn, 0, wx.ALL, 5)
        button_sizer.Add(self._cancel_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def _bind_events(self):
        """绑定事件。"""
        self._ok_btn.Bind(wx.EVT_BUTTON, self._on_ok)
    
    def _on_ok(self, event):
        """确定按钮。"""
        selection = self._assignee_choice.GetSelection()
        if selection <= 0:
            wx.MessageBox(_("请选择要分配的团队成员"), _("提示"), wx.OK | wx.ICON_WARNING)
            return
        
        self.EndModal(wx.ID_OK)
    
    def get_assignee(self):
        """
        获取被分配者。
        
        Returns:
            用户对象或None
        """
        selection = self._assignee_choice.GetSelection()
        if selection > 0:
            users = [u for u in self._taskFile.users() if u.isActive()]
            if selection - 1 < len(users):
                return users[selection - 1]
        return None
    
    def get_note(self):
        """
        获取备注。
        
        Returns:
            备注文本
        """
        return self._note_text.GetValue()
