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

Team collaboration UI commands.
"""

import wx
from taskcoachlib.gui.uicommand import base_uicommand
from taskcoachlib.i18n import _


class ManageUsersUICommand(base_uicommand.UICommand):
    """管理用户命令。"""
    
    def __init__(self, settings=None, taskFile=None, **kwargs):
        self._settings = settings
        self._taskFile = taskFile
        super().__init__(
            menu_text=_("管理用户..."),
            help_text=_("管理团队成员和用户账户"),
            **kwargs
        )
    
    def do_command(self, event):
        from taskcoachlib.gui.dialog.user_dialogs import UserListDialog
        dialog = UserListDialog(wx.GetApp().GetTopWindow(), self._taskFile)
        dialog.ShowModal()
        dialog.Destroy()


class ManageTeamsUICommand(base_uicommand.UICommand):
    """管理团队命令。"""
    
    def __init__(self, settings=None, taskFile=None, **kwargs):
        self._settings = settings
        self._taskFile = taskFile
        super().__init__(
            menu_text=_("管理团队..."),
            help_text=_("管理组织内的团队"),
            **kwargs
        )
    
    def do_command(self, event):
        from taskcoachlib.gui.dialog.team_dialogs import TeamListDialog
        dialog = TeamListDialog(wx.GetApp().GetTopWindow(), self._taskFile)
        dialog.ShowModal()
        dialog.Destroy()


class ManageOrganizationsUICommand(base_uicommand.UICommand):
    """管理组织命令。"""
    
    def __init__(self, settings=None, taskFile=None, **kwargs):
        self._settings = settings
        self._taskFile = taskFile
        super().__init__(
            menu_text=_("管理组织..."),
            help_text=_("管理组织结构"),
            **kwargs
        )
    
    def do_command(self, event):
        from taskcoachlib.gui.dialog.organization_dialogs import OrganizationListDialog
        dialog = OrganizationListDialog(wx.GetApp().GetTopWindow(), self._taskFile)
        dialog.ShowModal()
        dialog.Destroy()


class AssignTaskUICommand(base_uicommand.UICommand):
    """分配任务命令。"""
    
    def __init__(self, settings=None, taskFile=None, viewer=None, **kwargs):
        self._settings = settings
        self._taskFile = taskFile
        self._viewer = viewer
        super().__init__(
            menu_text=_("分配任务..."),
            help_text=_("将任务分配给团队成员"),
            **kwargs
        )
    
    def enabled(self, event):
        if self._viewer is None:
            return False
        return bool(self._viewer.selectedItems())
    
    def do_command(self, event):
        tasks = self._viewer.selectedItems() if self._viewer else []
        if not tasks:
            wx.MessageBox(_("请先选择要分配的任务"), _("提示"), wx.OK | wx.ICON_INFORMATION)
            return
        
        from taskcoachlib.gui.dialog.assignment_dialogs import AssignTaskDialog
        dialog = AssignTaskDialog(
            wx.GetApp().GetTopWindow(), 
            self._taskFile, 
            tasks
        )
        if dialog.ShowModal() == wx.ID_OK:
            pass
        dialog.Destroy()


class ViewTeamTasksUICommand(base_uicommand.UICommand):
    """查看团队任务命令。"""
    
    def __init__(self, settings=None, taskFile=None, **kwargs):
        self._settings = settings
        self._taskFile = taskFile
        super().__init__(
            menu_text=_("团队任务视图"),
            help_text=_("查看所有团队成员的任务"),
            **kwargs
        )
    
    def do_command(self, event):
        wx.MessageBox(_("团队任务视图功能即将推出"), _("提示"), wx.OK | wx.ICON_INFORMATION)
