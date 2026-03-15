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

Kanban viewer for TaskCoach.
"""

import wx
import wx.lib.scrolledpanel as scrolled
from taskcoachlib import patterns, command
from taskcoachlib.i18n import _
from taskcoachlib.gui import uicommand
from . import base


class KanbanCard(wx.Panel):
    """看板卡片组件。"""
    
    def __init__(self, parent, task, column, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self._task = task
        self._column = column
        self._settings = settings
        self._selected = False
        self._init_ui()
        self._bind_events()
    
    def _init_ui(self):
        """初始化UI。"""
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetMinSize((180, 80))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self._title_label = wx.StaticText(self, label=self._task.subject() if self._task else "")
        self._title_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(self._title_label, 0, wx.ALL, 5)
        
        self._description_label = wx.StaticText(self, label="")
        if self._task and self._task.description():
            desc = self._task.description()
            if len(desc) > 50:
                desc = desc[:50] + "..."
            self._description_label.SetLabel(desc)
        sizer.Add(self._description_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        self.SetSizer(sizer)
    
    def _bind_events(self):
        """绑定事件。"""
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
    
    def _on_paint(self, event):
        """绘制事件处理。"""
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()
        
        if self._selected:
            dc.SetPen(wx.Pen(wx.Colour(66, 133, 244), 2))
        else:
            dc.SetPen(wx.Pen(wx.Colour(200, 200, 200), 1))
        
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height, 5)
        
        event.Skip()
    
    def _on_left_down(self, event):
        """鼠标左键按下事件。"""
        self._selected = True
        self.Refresh()
        event.Skip()
    
    def _on_left_up(self, event):
        """鼠标左键释放事件。"""
        event.Skip()
    
    def get_task(self):
        """获取关联的任务。"""
        return self._task
    
    def set_selected(self, selected):
        """设置选中状态。"""
        self._selected = selected
        self.Refresh()


class KanbanColumn(wx.Panel):
    """看板列组件。"""
    
    def __init__(self, parent, column, board, task_list, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self._column = column
        self._board = board
        self._task_list = task_list
        self._settings = settings
        self._cards = []
        self._init_ui()
        self._bind_events()
    
    def _init_ui(self):
        """初始化UI。"""
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.SetMinSize((200, 400))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        header_panel = wx.Panel(self)
        header_panel.SetBackgroundColour(self._get_header_color())
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self._title_label = wx.StaticText(header_panel, label=self._column.subject())
        self._title_label.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self._title_label.SetForegroundColour(wx.Colour(50, 50, 50))
        header_sizer.Add(self._title_label, 1, wx.ALL, 8)
        
        self._count_label = wx.StaticText(header_panel, label="0")
        self._count_label.SetForegroundColour(wx.Colour(100, 100, 100))
        header_sizer.Add(self._count_label, 0, wx.ALL, 8)
        
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND)
        
        self._cards_panel = scrolled.ScrolledPanel(self, style=wx.VSCROLL)
        self._cards_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        self._cards_sizer = wx.BoxSizer(wx.VERTICAL)
        self._cards_panel.SetSizer(self._cards_sizer)
        self._cards_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        
        main_sizer.Add(self._cards_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def _get_header_color(self):
        """获取头部颜色。"""
        color = self._column.color()
        if color:
            try:
                return wx.Colour(color)
            except:
                pass
        return wx.Colour(220, 220, 220)
    
    def _bind_events(self):
        """绑定事件。"""
        pass
    
    def add_card(self, task):
        """添加卡片。"""
        card = KanbanCard(self._cards_panel, task, self._column, self._settings)
        self._cards.append(card)
        self._cards_sizer.Add(card, 0, wx.ALL | wx.EXPAND, 3)
        self._update_count()
        self.Layout()
    
    def remove_card(self, task):
        """移除卡片。"""
        for card in self._cards[:]:
            if card.get_task() == task:
                self._cards.remove(card)
                card.Destroy()
        self._update_count()
        self.Layout()
    
    def clear_cards(self):
        """清空所有卡片。"""
        for card in self._cards:
            card.Destroy()
        self._cards = []
        self._update_count()
        self.Layout()
    
    def _update_count(self):
        """更新计数。"""
        self._count_label.SetLabel(str(len(self._cards)))
    
    def get_column(self):
        """获取列实体。"""
        return self._column
    
    def get_card_count(self):
        """获取卡片数量。"""
        return len(self._cards)


class KanbanBoard(wx.Panel):
    """看板组件。"""
    
    def __init__(self, parent, board, task_list, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self._board = board
        self._task_list = task_list
        self._settings = settings
        self._columns = []
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI。"""
        self.SetBackgroundColour(wx.Colour(230, 230, 230))
        
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        for column in self._board.columns():
            kanban_column = KanbanColumn(self, column, self._board, self._task_list, self._settings)
            self._columns.append(kanban_column)
            main_sizer.Add(kanban_column, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
    
    def refresh_tasks(self, tasks):
        """刷新任务显示。"""
        for column in self._columns:
            column.clear_cards()
        
        for task in tasks:
            column = self._find_column_for_task(task)
            if column:
                column.add_card(task)
    
    def _find_column_for_task(self, task):
        """根据任务状态查找对应的列。"""
        for column in self._columns:
            col_entity = column.get_column()
            if col_entity.taskStatus() == task.getStatus():
                return column
        
        if self._columns:
            return self._columns[0]
        return None
    
    def get_board(self):
        """获取看板实体。"""
        return self._board


class KanbanViewer(base.Viewer):
    """看板视图。"""
    
    defaultTitle = _("Kanban board")
    defaultBitmap = "kanban"
    
    def __init__(self, parent, taskFile, settings, *args, **kwargs):
        self._board = None
        super().__init__(parent, taskFile, settings, *args, **kwargs)
    
    def createWidget(self):
        """创建控件。"""
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(230, 230, 230))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self._board_selector = wx.Choice(panel)
        self._board_selector.Bind(wx.EVT_CHOICE, self._on_board_selected)
        sizer.Add(self._board_selector, 0, wx.ALL | wx.EXPAND, 5)
        
        self._board_panel = wx.Panel(panel)
        self._board_panel.SetBackgroundColour(wx.Colour(230, 230, 230))
        self._board_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._board_panel.SetSizer(self._board_sizer)
        
        sizer.Add(self._board_panel, 1, wx.EXPAND)
        
        panel.SetSizer(sizer)
        
        self._load_boards()
        
        return panel
    
    def _load_boards(self):
        """加载看板列表。"""
        self._board_selector.Clear()
        
        if hasattr(self.taskFile, 'boards') and self.taskFile.boards():
            for board in self.taskFile.boards():
                self._board_selector.Append(board.subject(), board)
            self._board_selector.SetSelection(0)
            self._display_board(self.taskFile.boards()[0])
        else:
            self._create_default_board()
    
    def _create_default_board(self):
        """创建默认看板。"""
        from taskcoachlib.domain.kanban import Board, BoardColumn
        
        board = Board(subject=_("Default board"))
        
        columns = [
            BoardColumn(subject=_("To do"), position=0, color="#E8E8E8", task_status=0),
            BoardColumn(subject=_("In progress"), position=1, color="#FFE4B5", task_status=1),
            BoardColumn(subject=_("Completed"), position=2, color="#90EE90", task_status=2),
        ]
        
        for column in columns:
            board.addColumn(column)
        
        self._board_selector.Append(board.subject(), board)
        self._board_selector.SetSelection(0)
        self._display_board(board)
    
    def _display_board(self, board):
        """显示看板。"""
        self._board_panel.Freeze()
        
        for child in self._board_panel.GetChildren():
            child.Destroy()
        
        self._board = KanbanBoard(self._board_panel, board, self.presentation(), self.settings)
        self._board_sizer.Add(self._board, 1, wx.EXPAND)
        
        self._board_panel.Thaw()
        self._board_panel.Layout()
        
        self.refresh()
    
    def _on_board_selected(self, event):
        """看板选择事件。"""
        selection = self._board_selector.GetSelection()
        if selection != wx.NOT_FOUND:
            board = self._board_selector.GetClientData(selection)
            self._display_board(board)
    
    def domainObjectsToView(self):
        """返回要显示的域对象。"""
        return self.taskFile.tasks()
    
    def createFilter(self, presentation):
        """创建过滤器。"""
        return presentation
    
    def create_sorter(self, presentation):
        """创建排序器。"""
        return presentation
    
    def refresh(self):
        """刷新视图。"""
        super().refresh()
        if self._board:
            self._board.refresh_tasks(self.presentation())
    
    def curselection(self):
        """返回当前选择。"""
        return []
    
    def curselectionIsInstanceOf(self, class_):
        """检查当前选择是否为指定类的实例。"""
        return False
    
    def select(self, *args, **kwargs):
        """选择项目。"""
        pass
    
    def selectall(self):
        """全选。"""
        pass
    
    def clear_selection(self):
        """清除选择。"""
        pass
    
    def copyItemsToClipboard(self):
        """复制项目到剪贴板。"""
        pass
    
    def cutItemsToClipboard(self):
        """剪切项目到剪贴板。"""
        pass
    
    def pasteItemsFromClipboard(self):
        """从剪贴板粘贴项目。"""
        pass
