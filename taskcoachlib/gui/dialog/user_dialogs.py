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

User management dialogs for team collaboration.
"""

import wx
from taskcoachlib import widgets
from taskcoachlib.domain.user.auth import PasswordHasher, validate_password_strength
from taskcoachlib.domain.user import User


def _(text):
    """延迟加载的翻译函数，避免在模块加载时调用wx.StandardPaths。"""
    try:
        from taskcoachlib.i18n import _ as translate
        return translate(text)
    except Exception:
        return text


class UserListDialog(wx.Dialog):
    """
    用户列表对话框。
    
    用于管理用户列表，支持添加、编辑、删除用户。
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
            title=_("用户管理"),
            size=(600, 400),
            **kwargs
        )
        self._taskFile = taskFile
        self._password_hasher = PasswordHasher()
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_users()
        
        self.SetMinSize((500, 300))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self._list.InsertColumn(0, _("用户名"), width=150)
        self._list.InsertColumn(1, _("邮箱"), width=200)
        self._list.InsertColumn(2, _("显示名称"), width=150)
        self._list.InsertColumn(3, _("状态"), width=80)
        
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
    
    def _load_users(self):
        """加载用户列表。"""
        self._list.DeleteAllItems()
        for user in self._taskFile.users():
            idx = self._list.InsertItem(self._list.GetItemCount(), user.username() or '')
            self._list.SetItem(idx, 1, user.email() or '')
            self._list.SetItem(idx, 2, user.displayName() or '')
            status = _("活跃") if user.isActive() else _("禁用")
            self._list.SetItem(idx, 3, status)
            self._list.SetItemData(idx, id(user))
    
    def _get_selected_user(self):
        """获取选中的用户。"""
        idx = self._list.GetFirstSelected()
        if idx == -1:
            return None
        
        user_data = self._list.GetItemData(idx)
        for user in self._taskFile.users():
            if id(user) == user_data:
                return user
        return None
    
    def _on_add(self, event):
        """添加用户。"""
        dialog = UserDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getUserData()
            user = User(
                username=data['username'],
                email=data['email'],
                display_name=data['display_name'],
                is_active=data['is_active'],
                is_superuser=data['is_superuser'],
            )
            if data.get('password_hash'):
                user.setPasswordHash(data['password_hash'])
            self._taskFile.users().append(user)
            self._load_users()
        dialog.Destroy()
    
    def _on_edit(self, event):
        """编辑用户。"""
        user = self._get_selected_user()
        if user is None:
            wx.MessageBox(_("请先选择要编辑的用户"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        dialog = UserDialog(self, user=user)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.getUserData()
            user.setUsername(data['username'])
            user.setEmail(data['email'])
            user.setDisplayName(data['display_name'])
            user.setIsActive(data['is_active'])
            user.setIsSuperuser(data['is_superuser'])
            if data.get('password_hash'):
                user.setPasswordHash(data['password_hash'])
            self._load_users()
        dialog.Destroy()
    
    def _on_delete(self, event):
        """删除用户。"""
        user = self._get_selected_user()
        if user is None:
            wx.MessageBox(_("请先选择要删除的用户"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        if wx.MessageBox(
            _("确定要删除用户 '%s' 吗？") % user.username(), 
            _("确认删除"), 
            wx.YES_NO | wx.ICON_QUESTION
        ) == wx.YES:
            self._taskFile.users().remove(user)
            self._load_users()
    
    def _on_close(self, event):
        """关闭对话框。"""
        self.EndModal(wx.ID_CLOSE)


class UserDialog(wx.Dialog):
    """
    用户编辑对话框。
    
    用于创建和编辑用户信息。
    """
    
    def __init__(self, parent, user=None, title=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            user: 用户对象（编辑模式）
            title: 对话框标题
        """
        self._user = user
        self._password_hasher = PasswordHasher()
        self._is_new_user = user is None
        
        if title is None:
            title = _('New User') if self._is_new_user else _('Edit User')
        
        super().__init__(parent, title=title, **kwargs)
        
        self._create_controls()
        self._layout_controls()
        self._bind_events()
        self._load_user_data()
        
        self.SetMinSize((400, 350))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._username_label = wx.StaticText(self, label=_('Username:'))
        self._username_ctrl = wx.TextCtrl(self, size=(200, -1))
        
        self._email_label = wx.StaticText(self, label=_('Email:'))
        self._email_ctrl = wx.TextCtrl(self, size=(200, -1))
        
        self._display_name_label = wx.StaticText(self, label=_('Display Name:'))
        self._display_name_ctrl = wx.TextCtrl(self, size=(200, -1))
        
        self._password_label = wx.StaticText(self, label=_('Password:'))
        self._password_ctrl = wx.TextCtrl(self, size=(200, -1), style=wx.TE_PASSWORD)
        
        self._confirm_password_label = wx.StaticText(self, label=_('Confirm Password:'))
        self._confirm_password_ctrl = wx.TextCtrl(self, size=(200, -1), style=wx.TE_PASSWORD)
        
        self._is_active_checkbox = wx.CheckBox(self, label=_('Active'))
        self._is_active_checkbox.SetValue(True)
        
        self._is_superuser_checkbox = wx.CheckBox(self, label=_('Superuser'))
        self._is_superuser_checkbox.SetValue(False)
        
        self._error_label = wx.StaticText(self)
        self._error_label.SetForegroundColour(wx.RED)
        
        self._ok_button = wx.Button(self, wx.ID_OK, _('OK'))
        self._cancel_button = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=8, hgap=8)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._username_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._username_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._email_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._email_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._display_name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._display_name_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._password_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._password_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._confirm_password_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._confirm_password_ctrl, 1, wx.EXPAND)
        
        form_sizer.AddSpacer(1)
        form_sizer.Add(self._is_active_checkbox, 0, wx.ALIGN_CENTER_VERTICAL)
        
        form_sizer.AddSpacer(1)
        form_sizer.Add(self._is_superuser_checkbox, 0, wx.ALIGN_CENTER_VERTICAL)
        
        main_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self._error_label, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def _bind_events(self):
        """绑定事件。"""
        self._ok_button.Bind(wx.EVT_BUTTON, self._on_ok)
        self._password_ctrl.Bind(wx.EVT_TEXT, self._on_password_change)
    
    def _load_user_data(self):
        """加载用户数据。"""
        if self._user is not None:
            self._username_ctrl.SetValue(self._user.username() or '')
            self._email_ctrl.SetValue(self._user.email() or '')
            self._display_name_ctrl.SetValue(self._user.displayName() or '')
            self._is_active_checkbox.SetValue(self._user.isActive())
            self._is_superuser_checkbox.SetValue(self._user.isSuperuser())
            
            self._password_label.SetLabel(_('New Password:'))
            self._confirm_password_label.SetLabel(_('Confirm New Password:'))
    
    def _on_password_change(self, event):
        """密码变更事件处理。"""
        password = self._password_ctrl.GetValue()
        if password:
            valid, errors = validate_password_strength(password)
            if not valid:
                self._error_label.SetLabel('; '.join(errors))
            else:
                self._error_label.SetLabel('')
        else:
            self._error_label.SetLabel('')
        event.Skip()
    
    def _on_ok(self, event):
        """确定按钮事件处理。"""
        if not self._validate():
            return
        
        event.Skip()
    
    def _validate(self):
        """验证输入。"""
        username = self._username_ctrl.GetValue().strip()
        if not username:
            self._error_label.SetLabel(_('Username is required.'))
            return False
        
        email = self._email_ctrl.GetValue().strip()
        if email and '@' not in email:
            self._error_label.SetLabel(_('Invalid email format.'))
            return False
        
        password = self._password_ctrl.GetValue()
        confirm_password = self._confirm_password_ctrl.GetValue()
        
        if self._is_new_user:
            if not password:
                self._error_label.SetLabel(_('Password is required for new user.'))
                return False
            
            valid, errors = validate_password_strength(password)
            if not valid:
                self._error_label.SetLabel('; '.join(errors))
                return False
        
        if password or confirm_password:
            if password != confirm_password:
                self._error_label.SetLabel(_('Passwords do not match.'))
                return False
            
            valid, errors = validate_password_strength(password)
            if not valid:
                self._error_label.SetLabel('; '.join(errors))
                return False
        
        return True
    
    def getUserData(self):
        """
        获取用户数据。
        
        Returns:
            用户数据字典
        """
        data = {
            'username': self._username_ctrl.GetValue().strip(),
            'email': self._email_ctrl.GetValue().strip(),
            'display_name': self._display_name_ctrl.GetValue().strip(),
            'is_active': self._is_active_checkbox.IsChecked(),
            'is_superuser': self._is_superuser_checkbox.IsChecked(),
        }
        
        password = self._password_ctrl.GetValue()
        if password:
            data['password_hash'] = self._password_hasher.hash(password)
        
        return data


class OrganizationDialog(wx.Dialog):
    """
    组织编辑对话框。
    
    用于创建和编辑组织信息。
    """
    
    def __init__(self, parent, organization=None, title=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            organization: 组织对象（编辑模式）
            title: 对话框标题
        """
        self._organization = organization
        self._is_new = organization is None
        
        if title is None:
            title = _('New Organization') if self._is_new else _('Edit Organization')
        
        super().__init__(parent, title=title, **kwargs)
        
        self._create_controls()
        self._layout_controls()
        self._load_organization_data()
        
        self.SetMinSize((400, 250))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._name_label = wx.StaticText(self, label=_('Name:'))
        self._name_ctrl = wx.TextCtrl(self, size=(250, -1))
        
        self._description_label = wx.StaticText(self, label=_('Description:'))
        self._description_ctrl = wx.TextCtrl(self, size=(250, 60), style=wx.TE_MULTILINE)
        
        self._ok_button = wx.Button(self, wx.ID_OK, _('OK'))
        self._cancel_button = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=8, hgap=8)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP, 5)
        form_sizer.Add(self._name_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._description_label, 0, wx.ALIGN_TOP | wx.TOP, 5)
        form_sizer.Add(self._description_ctrl, 1, wx.EXPAND)
        
        main_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def _load_organization_data(self):
        """加载组织数据。"""
        if self._organization is not None:
            self._name_ctrl.SetValue(self._organization.subject() or '')
    
    def getOrganizationData(self):
        """
        获取组织数据。
        
        Returns:
            组织数据字典
        """
        return {
            'subject': self._name_ctrl.GetValue().strip(),
            'description': self._description_ctrl.GetValue().strip(),
        }


class TeamDialog(wx.Dialog):
    """
    团队编辑对话框。
    
    用于创建和编辑团队信息。
    """
    
    def __init__(self, parent, team=None, organization=None, title=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            team: 团队对象（编辑模式）
            organization: 所属组织
            title: 对话框标题
        """
        self._team = team
        self._organization = organization
        self._is_new = team is None
        
        if title is None:
            title = _('New Team') if self._is_new else _('Edit Team')
        
        super().__init__(parent, title=title, **kwargs)
        
        self._create_controls()
        self._layout_controls()
        self._load_team_data()
        
        self.SetMinSize((400, 200))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._name_label = wx.StaticText(self, label=_('Name:'))
        self._name_ctrl = wx.TextCtrl(self, size=(250, -1))
        
        self._ok_button = wx.Button(self, wx.ID_OK, _('OK'))
        self._cancel_button = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=8, hgap=8)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._name_ctrl, 1, wx.EXPAND)
        
        main_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def _load_team_data(self):
        """加载团队数据。"""
        if self._team is not None:
            self._name_ctrl.SetValue(self._team.subject() or '')
    
    def getTeamData(self):
        """
        获取团队数据。
        
        Returns:
            团队数据字典
        """
        return {
            'subject': self._name_ctrl.GetValue().strip(),
            'organization': self._organization,
        }


class InviteUserDialog(wx.Dialog):
    """
    邀请用户对话框。
    
    用于邀请用户加入组织或团队。
    """
    
    def __init__(self, parent, organization=None, team=None, title=None, **kwargs):
        """
        初始化对话框。
        
        Args:
            parent: 父窗口
            organization: 组织对象
            team: 团队对象（可选）
            title: 对话框标题
        """
        self._organization = organization
        self._team = team
        
        if title is None:
            title = _('Invite User')
        
        super().__init__(parent, title=title, **kwargs)
        
        self._create_controls()
        self._layout_controls()
        
        self.SetMinSize((400, 200))
        self.Fit()
    
    def _create_controls(self):
        """创建控件。"""
        self._email_label = wx.StaticText(self, label=_('Email:'))
        self._email_ctrl = wx.TextCtrl(self, size=(250, -1))
        
        self._role_label = wx.StaticText(self, label=_('Role:'))
        self._role_choice = wx.Choice(self, choices=[_('Admin'), _('Member'), _('Guest')])
        self._role_choice.SetSelection(1)
        
        self._ok_button = wx.Button(self, wx.ID_OK, _('Send Invite'))
        self._cancel_button = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
    
    def _layout_controls(self):
        """布局控件。"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, vgap=8, hgap=8)
        form_sizer.AddGrowableCol(1, 1)
        
        form_sizer.Add(self._email_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._email_ctrl, 1, wx.EXPAND)
        
        form_sizer.Add(self._role_label, 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self._role_choice, 1, wx.EXPAND)
        
        main_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def getInviteData(self):
        """
        获取邀请数据。
        
        Returns:
            邀请数据字典
        """
        role_map = {0: 'admin', 1: 'member', 2: 'guest'}
        return {
            'email': self._email_ctrl.GetValue().strip(),
            'role': role_map[self._role_choice.GetSelection()],
            'organization': self._organization,
            'team': self._team,
        }
