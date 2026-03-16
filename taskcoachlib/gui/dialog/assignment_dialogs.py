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


def _(text):
    """延迟加载的翻译函数。"""
    try:
        from taskcoachlib.i18n import _ as translate
        return translate(text)
    except Exception:
        return text


class AssignTaskDialog(wx.Dialog):
    """任务分配对话框。"""
    
    def __init__(self, parent, taskFile, tasks, **kwargs):
        super().__init__(
            parent, 
            title=_("分配任务"),
            size=(500, 400),
            **kwargs
        )
        self.__taskFile = taskFile
        self.__tasks = tasks
        self.__create_gui()
    
    def __create_gui(self):
        """创建GUI界面。"""
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 任务信息
        task_count = len(self.__tasks)
        info_text = wx.StaticText(
            panel, 
            label=_("已选择 %d 个任务") % task_count
        )
        sizer.Add(info_text, 0, wx.ALL, 10)
        
        # 分配给
        assign_sizer = wx.BoxSizer(wx.HORIZONTAL)
        assign_sizer.Add(wx.StaticText(panel, label=_("分配给:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        
        self.__assignee_choice = wx.Choice(panel, choices=[_("选择团队成员...")])
        assign_sizer.Add(self.__assignee_choice, 1, wx.EXPAND)
        
        sizer.Add(assign_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # 备注
        note_sizer = wx.BoxSizer(wx.VERTICAL)
        note_sizer.Add(wx.StaticText(panel, label=_("备注:")), 0, wx.BOTTOM, 5)
        self.__note_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 100))
        note_sizer.Add(self.__note_text, 1, wx.EXPAND)
        
        sizer.Add(note_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        # 按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__ok_btn = wx.Button(panel, wx.ID_OK, label=_("确定"))
        self.__cancel_btn = wx.Button(panel, wx.ID_CANCEL, label=_("取消"))
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.__ok_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.__cancel_btn, 0, wx.ALL, 5)
        
        sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(sizer)
        
        # 绑定事件
        self.__ok_btn.Bind(wx.EVT_BUTTON, self.__on_ok)
    
    def __on_ok(self, event):
        """确定按钮。"""
        selection = self.__assignee_choice.GetSelection()
        if selection <= 0:
            wx.MessageBox(_("请选择要分配的团队成员"), _("提示"), wx.OK | wx.ICON_WARNING)
            return
        
        # TODO: 保存分配
        self.EndModal(wx.ID_OK)
    
    def get_assignee(self):
        """获取被分配者。"""
        selection = self.__assignee_choice.GetSelection()
        if selection > 0:
            return self.__assignee_choice.GetString(selection)
        return None
    
    def get_note(self):
        """获取备注。"""
        return self.__note_text.GetValue()
