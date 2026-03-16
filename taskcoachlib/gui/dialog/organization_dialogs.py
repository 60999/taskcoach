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

Organization management dialogs.
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


class OrganizationListDialog(wx.Dialog):
    """组织列表对话框。"""
    
    def __init__(self, parent, taskFile, **kwargs):
        super().__init__(
            parent, 
            title=_("组织管理"),
            size=(600, 400),
            **kwargs
        )
        self.__taskFile = taskFile
        self.__create_gui()
    
    def __create_gui(self):
        """创建GUI界面。"""
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建列表
        self.__list = wx.ListCtrl(
            panel, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self.__list.InsertColumn(0, _("组织名称"), width=200)
        self.__list.InsertColumn(1, _("团队数"), width=100)
        self.__list.InsertColumn(2, _("描述"), width=250)
        
        # 按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__add_btn = wx.Button(panel, label=_("添加"))
        self.__edit_btn = wx.Button(panel, label=_("编辑"))
        self.__delete_btn = wx.Button(panel, label=_("删除"))
        self.__close_btn = wx.Button(panel, wx.ID_CLOSE, label=_("关闭"))
        
        button_sizer.Add(self.__add_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.__edit_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.__delete_btn, 0, wx.ALL, 5)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.__close_btn, 0, wx.ALL, 5)
        
        # 绑定事件
        self.__add_btn.Bind(wx.EVT_BUTTON, self.__on_add)
        self.__edit_btn.Bind(wx.EVT_BUTTON, self.__on_edit)
        self.__delete_btn.Bind(wx.EVT_BUTTON, self.__on_delete)
        self.__close_btn.Bind(wx.EVT_BUTTON, self.__on_close)
        
        sizer.Add(self.__list, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(sizer)
        self.__load_organizations()
    
    def __load_organizations(self):
        """加载组织列表。"""
        self.__list.DeleteAllItems()
        # TODO: 从taskFile加载组织数据
    
    def __on_add(self, event):
        """添加组织。"""
        dialog = OrganizationEditDialog(self, self.__taskFile)
        if dialog.ShowModal() == wx.ID_OK:
            self.__load_organizations()
        dialog.Destroy()
    
    def __on_edit(self, event):
        """编辑组织。"""
        idx = self.__list.GetFirstSelected()
        if idx == -1:
            wx.MessageBox(_("请先选择要编辑的组织"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        dialog = OrganizationEditDialog(self, self.__taskFile)
        if dialog.ShowModal() == wx.ID_OK:
            self.__load_organizations()
        dialog.Destroy()
    
    def __on_delete(self, event):
        """删除组织。"""
        idx = self.__list.GetFirstSelected()
        if idx == -1:
            wx.MessageBox(_("请先选择要删除的组织"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        if wx.MessageBox(_("确定要删除选中的组织吗？"), _("确认"), 
                        wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            # TODO: 删除组织
            self.__load_organizations()
    
    def __on_close(self, event):
        """关闭对话框。"""
        self.EndModal(wx.ID_CLOSE)


class OrganizationEditDialog(wx.Dialog):
    """组织编辑对话框。"""
    
    def __init__(self, parent, taskFile, organization=None, **kwargs):
        super().__init__(
            parent,
            title=_("编辑组织") if organization else _("添加组织"),
            size=(500, 350),
            **kwargs
        )
        self.__taskFile = taskFile
        self.__organization = organization
        self.__create_gui()
    
    def __create_gui(self):
        """创建GUI界面。"""
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 表单
        form_sizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        
        # 组织名称
        form_sizer.Add(wx.StaticText(panel, label=_("组织名称:")), 0, wx.ALIGN_CENTER_VERTICAL)
        self.__name_text = wx.TextCtrl(panel, size=(300, -1))
        form_sizer.Add(self.__name_text, 0, wx.EXPAND)
        
        # 描述
        form_sizer.Add(wx.StaticText(panel, label=_("描述:")), 0, wx.ALIGN_CENTER_VERTICAL)
        self.__desc_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 80))
        form_sizer.Add(self.__desc_text, 0, wx.EXPAND)
        
        # 按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__ok_btn = wx.Button(panel, wx.ID_OK, label=_("确定"))
        self.__cancel_btn = wx.Button(panel, wx.ID_CANCEL, label=_("取消"))
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.__ok_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.__cancel_btn, 0, wx.ALL, 5)
        
        sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(sizer)
        
        # 绑定事件
        self.__ok_btn.Bind(wx.EVT_BUTTON, self.__on_ok)
    
    def __on_ok(self, event):
        """确定按钮。"""
        name = self.__name_text.GetValue().strip()
        if not name:
            wx.MessageBox(_("请输入组织名称"), _("提示"), wx.OK | wx.ICON_WARNING)
            return
        
        # TODO: 保存组织
        self.EndModal(wx.ID_OK)
