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
from taskcoachlib.domain.organization import Organization


def _(text):
    """延迟加载的翻译函数。"""
    try:
        from taskcoachlib.i18n import _ as translate
        return translate(text)
    except Exception:
        return text


class OrganizationListDialog(wx.Dialog):
    """
    组织列表对话框。
    
    用于管理组织列表，支持添加、编辑、删除组织。
    """
    
    def __init__(self, parent, taskFile, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            taskFile: 任务文件对象
        """
        super().__init__(
            parent, 
            title=_("组织管理"),
            size=(600, 400),
            **kwargs
        )
        self._taskFile = taskFile
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_organizations()
        
        self.SetMinSize((500, 300))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self._list.InsertColumn(0, _("组织名称"), width=200)
        self._list.InsertColumn(1, _("团队数"), width=100)
        self._list.InsertColumn(2, _("成员数"), width=100)
        self._list.InsertColumn(3, _("描述"), width=150)
        
        self._add_btn = wx.Button(self, label=_("添加"))
        self._edit_btn = wx.Button(self, label=_("编辑"))
        self._delete_btn = wx.Button(self, label=_("删除"))
        self._close_btn = wx.Button(self, wx.ID_CLOSE, label=_("关闭"))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self._add_btn, 0, wx.ALL, 5)
        button_sizer.Add(self._edit_btn, 0, wx.ALL, 5)
        button_sizer.Add(self._delete_btn, 0, wx.ALL, 5)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self._close_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(self._list, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def _bind_events(self):
        """绑定事件。"""
        self._add_btn.Bind(wx.EVT_BUTTON, self._on_add)
        self._edit_btn.Bind(wx.EVT_BUTTON, self._on_edit)
        self._delete_btn.Bind(wx.EVT_BUTTON, self._on_delete)
        self._close_btn.Bind(wx.EVT_BUTTON, self._on_close)
        self._list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_edit)
    
    def _load_organizations(self):
        """加载组织列表。"""
        self._list.DeleteAllItems()
        for org in self._taskFile.organizations():
            idx = self._list.InsertItem(self._list.GetItemCount(), org.subject() or '')
            self._list.SetItem(idx, 1, str(len(org.teams())))
            self._list.SetItem(idx, 2, str(org.memberCount()))
            description = org.settings().get('description', '') if org.settings() else ''
            self._list.SetItem(idx, 3, description[:50] if description else '')
            self._list.SetItemData(idx, id(org))
    
    def _get_selected_organization(self):
        """获取选中的组织。"""
        idx = self._list.GetFirstSelected()
        if idx == -1:
            return None
        
        org_data = self._list.GetItemData(idx)
        for org in self._taskFile.organizations():
            if id(org) == org_data:
                return org
        return None
    
    def _on_add(self, event):
        """添加组织。"""
        dialog = OrganizationEditDialog(self, self._taskFile)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getOrganizationData()
            org = Organization(subject=data['subject'])
            if data.get('description'):
                org.setSetting('description', data['description'])
            self._taskFile.organizations().append(org)
            self._load_organizations()
        dialog.Destroy()
    
    def _on_edit(self, event):
        """编辑组织。"""
        org = self._get_selected_organization()
        if org is None:
            wx.MessageBox(_("请先选择要编辑的组织"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        dialog = OrganizationEditDialog(self, self._taskFile, organization=org)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getOrganizationData()
            org.setSubject(data['subject'])
            if data.get('description'):
                org.setSetting('description', data['description'])
            self._load_organizations()
        dialog.Destroy()
    
    def _on_delete(self, event):
        """删除组织。"""
        org = self._get_selected_organization()
        if org is None:
            wx.MessageBox(_("请先选择要删除的组织"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        if wx.MessageBox(
            _("确定要删除组织 '%s' 吗？\n这将同时删除该组织下的所有团队。") % org.subject(), 
            _("确认删除"), 
            wx.YES_NO | wx.ICON_QUESTION
        ) == wx.YES:
            self._taskFile.organizations().remove(org)
            self._load_organizations()
    
    def _on_close(self, event):
        """关闭对话框。"""
        self.EndModal(wx.ID_CLOSE)


class OrganizationEditDialog(wx.Dialog):
    """
    组织编辑对话框。
    
    用于创建和编辑组织信息。
    """
    
    def __init__(self, parent, taskFile, organization=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            taskFile: 任务文件对象
            organization: 组织对象（编辑模式）
        """
        self._taskFile = taskFile
        self._organization = organization
        self._is_new = organization is None
        
        super().__init__(
            parent,
            title=_("编辑组织") if organization else _("添加组织"),
            size=(500, 350),
            **kwargs
        )
        
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_organization_data()
        
        self.SetMinSize((400, 250))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._name_label = wx.StaticText(self, label=_("组织名称:"))
        self._name_text = wx.TextCtrl(self, size=(300, -1))
        
        self._desc_label = wx.StaticText(self, label=_("描述:"))
        self._desc_text = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(300, 80))
        
        self._ok_btn = wx.Button(self, wx.ID_OK, label=_("确定"))
        self._cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("取消"))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._name_text, 0, wx.EXPAND)
        
        form_sizer.Add(self._desc_label, 0, wx.ALIGN_TOP)
        form_sizer.Add(self._desc_text, 0, wx.EXPAND)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self._ok_btn, 0, wx.ALL, 5)
        button_sizer.Add(self._cancel_btn, 0, wx.ALL, 5)
        
        main_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def _bind_events(self):
        """绑定事件。"""
        self._ok_btn.Bind(wx.EVT_BUTTON, self._on_ok)
    
    def _load_organization_data(self):
        """加载组织数据。"""
        if self._organization is not None:
            self._name_text.SetValue(self._organization.subject() or '')
            description = self._organization.settings().get('description', '') if self._organization.settings() else ''
            self._desc_text.SetValue(description)
    
    def _on_ok(self, event):
        """确定按钮。"""
        name = self._name_text.GetValue().strip()
        if not name:
            wx.MessageBox(_("请输入组织名称"), _("提示"), wx.OK | wx.ICON_WARNING)
            return
        
        self.EndModal(wx.ID_OK)
    
    def getOrganizationData(self):
        """
        获取组织数据。
        
        Returns:
            组织数据字典
        """
        return {
            'subject': self._name_text.GetValue().strip(),
            'description': self._desc_text.GetValue().strip(),
        }
