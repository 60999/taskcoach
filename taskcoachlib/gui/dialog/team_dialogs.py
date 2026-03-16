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

Team management dialogs.
"""

import wx
from taskcoachlib import widgets
from taskcoachlib.i18n import _
from taskcoachlib.domain.organization import Team


def _(text):
    """延迟加载的翻译函数。"""
    try:
        from taskcoachlib.i18n import _ as translate
        return translate(text)
    except Exception:
        return text


class TeamListDialog(wx.Dialog):
    """
    团队列表对话框。
    
    用于管理团队列表，支持添加、编辑、删除团队。
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
            title=_("团队管理"),
            size=(600, 400),
            **kwargs
        )
        self._taskFile = taskFile
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_teams()
        
        self.SetMinSize((500, 300))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self._list.InsertColumn(0, _("团队名称"), width=200)
        self._list.InsertColumn(1, _("成员数"), width=100)
        self._list.InsertColumn(2, _("所属组织"), width=200)
        
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
    
    def _load_teams(self):
        """加载团队列表。"""
        self._list.DeleteAllItems()
        for team in self._taskFile.teams():
            idx = self._list.InsertItem(self._list.GetItemCount(), team.subject() or '')
            self._list.SetItem(idx, 1, str(team.memberCount()))
            org = team.organization()
            org_name = org.subject() if org else _("无")
            self._list.SetItem(idx, 2, org_name)
            self._list.SetItemData(idx, id(team))
    
    def _get_selected_team(self):
        """获取选中的团队。"""
        idx = self._list.GetFirstSelected()
        if idx == -1:
            return None
        
        team_data = self._list.GetItemData(idx)
        for team in self._taskFile.teams():
            if id(team) == team_data:
                return team
        return None
    
    def _on_add(self, event):
        """添加团队。"""
        dialog = TeamEditDialog(self, self._taskFile)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getTeamData()
            team = Team(subject=data['subject'])
            if data.get('organization'):
                team.setOrganization(data['organization'])
            self._taskFile.teams().append(team)
            self._load_teams()
        dialog.Destroy()
    
    def _on_edit(self, event):
        """编辑团队。"""
        team = self._get_selected_team()
        if team is None:
            wx.MessageBox(_("请先选择要编辑的团队"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        dialog = TeamEditDialog(self, self._taskFile, team=team)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getTeamData()
            team.setSubject(data['subject'])
            if data.get('organization'):
                team.setOrganization(data['organization'])
            self._load_teams()
        dialog.Destroy()
    
    def _on_delete(self, event):
        """删除团队。"""
        team = self._get_selected_team()
        if team is None:
            wx.MessageBox(_("请先选择要删除的团队"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        if wx.MessageBox(
            _("确定要删除团队 '%s' 吗？") % team.subject(), 
            _("确认删除"), 
            wx.YES_NO | wx.ICON_QUESTION
        ) == wx.YES:
            self._taskFile.teams().remove(team)
            self._load_teams()
    
    def _on_close(self, event):
        """关闭对话框。"""
        self.EndModal(wx.ID_CLOSE)


class TeamEditDialog(wx.Dialog):
    """
    团队编辑对话框。
    
    用于创建和编辑团队信息。
    """
    
    def __init__(self, parent, taskFile, team=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            taskFile: 任务文件对象
            team: 团队对象（编辑模式）
        """
        self._taskFile = taskFile
        self._team = team
        self._is_new = team is None
        
        super().__init__(
            parent,
            title=_("编辑团队") if team else _("添加团队"),
            size=(500, 350),
            **kwargs
        )
        
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_team_data()
        
        self.SetMinSize((400, 200))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._name_label = wx.StaticText(self, label=_("团队名称:"))
        self._name_text = wx.TextCtrl(self, size=(300, -1))
        
        self._org_label = wx.StaticText(self, label=_("所属组织:"))
        org_names = [_("无")] + [org.subject() for org in self._taskFile.organizations()]
        self._org_choice = wx.Choice(self, choices=org_names)
        self._org_choice.SetSelection(0)
        
        self._ok_btn = wx.Button(self, wx.ID_OK, label=_("确定"))
        self._cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("取消"))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._name_text, 0, wx.EXPAND)
        
        form_sizer.Add(self._org_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._org_choice, 0, wx.EXPAND)
        
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
    
    def _load_team_data(self):
        """加载团队数据。"""
        if self._team is not None:
            self._name_text.SetValue(self._team.subject() or '')
            org = self._team.organization()
            if org:
                for i, o in enumerate(self._taskFile.organizations()):
                    if o == org:
                        self._org_choice.SetSelection(i + 1)
                        break
    
    def _on_ok(self, event):
        """确定按钮。"""
        name = self._name_text.GetValue().strip()
        if not name:
            wx.MessageBox(_("请输入团队名称"), _("提示"), wx.OK | wx.ICON_WARNING)
            return
        
        self.EndModal(wx.ID_OK)
    
    def getTeamData(self):
        """
        获取团队数据。
        
        Returns:
            团队数据字典
        """
        org_idx = self._org_choice.GetSelection()
        organization = None
        if org_idx > 0:
            orgs = list(self._taskFile.organizations())
            if org_idx - 1 < len(orgs):
                organization = orgs[org_idx - 1]
        
        return {
            'subject': self._name_text.GetValue().strip(),
            'organization': organization,
        }
