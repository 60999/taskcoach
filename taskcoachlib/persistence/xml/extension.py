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

XML persistence extension for kanban, tag and workflow entities.
"""

from xml.etree import ElementTree as ET
from taskcoachlib.domain import date


class KanbanXMLWriter:
    """看板XML写入器。"""
    
    @staticmethod
    def write_boards(root, boards):
        """写入看板节点。"""
        boards_node = ET.SubElement(root, "boards")
        for board in boards:
            KanbanXMLWriter.write_board(boards_node, board)
        return boards_node
    
    @staticmethod
    def write_board(parent_node, board):
        """写入单个看板节点。"""
        attrs = dict(
            id=board.id(),
            name=board.subject() or board.description(),
        )
        if board.description():
            attrs["description"] = board.description()
        if board.ownerId():
            attrs["owner_id"] = board.ownerId()
        if board.organizationId():
            attrs["organization_id"] = board.organizationId()
        
        node = ET.SubElement(parent_node, "board", attrs)
        
        columns_node = ET.SubElement(node, "columns")
        for column in board.columns():
            KanbanXMLWriter.write_column(columns_node, column)
        
        swimlanes_node = ET.SubElement(node, "swimlanes")
        for swimlane in board.swimlanes():
            KanbanXMLWriter.write_swimlane(swimlanes_node, swimlane)
        
        return node
    
    @staticmethod
    def write_column(parent_node, column):
        """写入看板列节点。"""
        attrs = dict(
            id=column.id(),
            name=column.subject(),
            position=str(column.position()),
        )
        if column.color():
            attrs["color"] = column.color()
        if column.wipLimit() is not None:
            attrs["wip_limit"] = str(column.wipLimit())
        if column.taskStatus():
            attrs["task_status"] = column.taskStatus()
        
        return ET.SubElement(parent_node, "column", attrs)
    
    @staticmethod
    def write_swimlane(parent_node, swimlane):
        """写入泳道节点。"""
        attrs = dict(
            id=swimlane.id(),
            name=swimlane.subject(),
            position=str(swimlane.position()),
        )
        return ET.SubElement(parent_node, "swimlane", attrs)


class TagXMLWriter:
    """标签XML写入器。"""
    
    @staticmethod
    def write_tags(root, tags):
        """写入标签节点。"""
        tags_node = ET.SubElement(root, "tags")
        for tag in tags:
            TagXMLWriter.write_tag(tags_node, tag)
        return tags_node
    
    @staticmethod
    def write_tag(parent_node, tag):
        """写入单个标签节点。"""
        attrs = dict(
            id=tag.id(),
            name=tag.subject(),
        )
        if tag.color():
            attrs["color"] = tag.color()
        if tag.description():
            attrs["description"] = tag.description()
        if tag.organizationId():
            attrs["organization_id"] = tag.organizationId()
        
        return ET.SubElement(parent_node, "tag", attrs)


class WorkflowXMLWriter:
    """工作流XML写入器。"""
    
    @staticmethod
    def write_workflows(root, workflows):
        """写入工作流节点。"""
        workflows_node = ET.SubElement(root, "workflows")
        for workflow in workflows:
            WorkflowXMLWriter.write_workflow(workflows_node, workflow)
        return workflows_node
    
    @staticmethod
    def write_workflow(parent_node, workflow):
        """写入单个工作流节点。"""
        attrs = dict(
            id=workflow.id(),
            name=workflow.subject() or workflow.description(),
        )
        if workflow.description():
            attrs["description"] = workflow.description()
        if workflow.initialStateId():
            attrs["initial_state_id"] = workflow.initialStateId()
        if workflow.organizationId():
            attrs["organization_id"] = workflow.organizationId()
        
        node = ET.SubElement(parent_node, "workflow", attrs)
        
        states_node = ET.SubElement(node, "states")
        for state in workflow.states():
            WorkflowXMLWriter.write_state(states_node, state)
        
        transitions_node = ET.SubElement(node, "transitions")
        for transition in workflow.transitions():
            WorkflowXMLWriter.write_transition(transitions_node, transition)
        
        return node
    
    @staticmethod
    def write_state(parent_node, state):
        """写入状态节点。"""
        attrs = dict(
            id=state.id(),
            name=state.subject(),
        )
        if state.color():
            attrs["color"] = state.color()
        if state.isInitial():
            attrs["is_initial"] = "True"
        if state.isFinal():
            attrs["is_final"] = "True"
        
        return ET.SubElement(parent_node, "state", attrs)
    
    @staticmethod
    def write_transition(parent_node, transition):
        """写入转换节点。"""
        attrs = dict(
            id=transition.id(),
            name=transition.subject(),
            from_state_id=transition.fromStateId(),
            to_state_id=transition.toStateId(),
        )
        
        node = ET.SubElement(parent_node, "transition", attrs)
        
        for rule in transition.rules():
            WorkflowXMLWriter.write_rule(node, rule)
        
        return node
    
    @staticmethod
    def write_rule(parent_node, rule):
        """写入规则节点。"""
        attrs = dict(
            id=rule.id(),
            rule_type=rule.ruleType(),
        )
        if rule.condition():
            attrs["condition"] = rule.condition()
        if rule.action():
            attrs["action"] = rule.action()
        
        return ET.SubElement(parent_node, "rule", attrs)


class XMLPersistenceExtension:
    """XML持久化扩展管理器。"""
    
    def __init__(self):
        self._boards = []
        self._tags = []
        self._workflows = []
    
    def set_boards(self, boards):
        """设置看板列表。"""
        self._boards = boards
    
    def set_tags(self, tags):
        """设置标签列表。"""
        self._tags = tags
    
    def set_workflows(self, workflows):
        """设置工作流列表。"""
        self._workflows = workflows
    
    def write_to_root(self, root):
        """将所有扩展数据写入XML根节点。"""
        if self._boards:
            KanbanXMLWriter.write_boards(root, self._boards)
        if self._tags:
            TagXMLWriter.write_tags(root, self._tags)
        if self._workflows:
            WorkflowXMLWriter.write_workflows(root, self._workflows)
    
    @staticmethod
    def read_from_root(root, version):
        """从XML根节点读取扩展数据。"""
        extension = XMLPersistenceExtension()
        
        extension._boards = XMLPersistenceExtension._parse_boards(root, version)
        extension._tags = XMLPersistenceExtension._parse_tags(root, version)
        extension._workflows = XMLPersistenceExtension._parse_workflows(root, version)
        
        return extension
    
    @staticmethod
    def _parse_boards(root, version):
        """解析看板节点。"""
        boards = []
        boards_node = root.find("boards")
        if boards_node is None:
            return boards
        
        for board_node in boards_node.findall("board"):
            from taskcoachlib.domain.kanban import Board, BoardColumn, Swimlane
            
            board = Board(
                id=board_node.attrib.get("id", ""),
                subject=board_node.attrib.get("name", ""),
                description=board_node.attrib.get("description", ""),
                owner_id=board_node.attrib.get("owner_id", ""),
                organization_id=board_node.attrib.get("organization_id", ""),
            )
            
            columns_node = board_node.find("columns")
            if columns_node is not None:
                for column_node in columns_node.findall("column"):
                    column = BoardColumn(
                        id=column_node.attrib.get("id", ""),
                        subject=column_node.attrib.get("name", ""),
                        position=int(column_node.attrib.get("position", "0")),
                        color=column_node.attrib.get("color", "#E8E8E8"),
                        wip_limit=int(column_node.attrib.get("wip_limit", "0")) or None,
                        task_status=column_node.attrib.get("task_status"),
                    )
                    board.addColumn(column)
            
            swimlanes_node = board_node.find("swimlanes")
            if swimlanes_node is not None:
                for swimlane_node in swimlanes_node.findall("swimlane"):
                    swimlane = Swimlane(
                        id=swimlane_node.attrib.get("id", ""),
                        subject=swimlane_node.attrib.get("name", ""),
                        position=int(swimlane_node.attrib.get("position", "0")),
                    )
                    board.addSwimlane(swimlane)
            
            boards.append(board)
        
        return boards
    
    @staticmethod
    def _parse_tags(root, version):
        """解析标签节点。"""
        tags = []
        tags_node = root.find("tags")
        if tags_node is None:
            return tags
        
        for tag_node in tags_node.findall("tag"):
            from taskcoachlib.domain.tag import Tag
            
            tag = Tag(
                id=tag_node.attrib.get("id", ""),
                subject=tag_node.attrib.get("name", ""),
                description=tag_node.attrib.get("description", ""),
                color=tag_node.attrib.get("color", "#3498db"),
                organization_id=tag_node.attrib.get("organization_id", ""),
            )
            tags.append(tag)
        
        return tags
    
    @staticmethod
    def _parse_workflows(root, version):
        """解析工作流节点。"""
        workflows = []
        workflows_node = root.find("workflows")
        if workflows_node is None:
            return workflows
        
        for workflow_node in workflows_node.findall("workflow"):
            from taskcoachlib.domain.workflow import Workflow, State, Transition, TransitionRule
            
            workflow = Workflow(
                id=workflow_node.attrib.get("id", ""),
                subject=workflow_node.attrib.get("name", ""),
                description=workflow_node.attrib.get("description", ""),
                initial_state_id=workflow_node.attrib.get("initial_state_id"),
                organization_id=workflow_node.attrib.get("organization_id", ""),
            )
            
            states_node = workflow_node.find("states")
            if states_node is not None:
                for state_node in states_node.findall("state"):
                    state = State(
                        id=state_node.attrib.get("id", ""),
                        subject=state_node.attrib.get("name", ""),
                        color=state_node.attrib.get("color", "#808080"),
                        is_initial=state_node.attrib.get("is_initial", "False") == "True",
                        is_final=state_node.attrib.get("is_final", "False") == "True",
                    )
                    workflow.addState(state)
            
            transitions_node = workflow_node.find("transitions")
            if transitions_node is not None:
                for transition_node in transitions_node.findall("transition"):
                    transition = Transition(
                        id=transition_node.attrib.get("id", ""),
                        subject=transition_node.attrib.get("name", ""),
                        from_state_id=transition_node.attrib.get("from_state_id", ""),
                        to_state_id=transition_node.attrib.get("to_state_id", ""),
                    )
                    
                    for rule_node in transition_node.findall("rule"):
                        rule = TransitionRule(
                            id=rule_node.attrib.get("id", ""),
                            rule_type=rule_node.attrib.get("rule_type", "condition"),
                            condition=rule_node.attrib.get("condition", ""),
                            action=rule_node.attrib.get("action", ""),
                        )
                        transition.addRule(rule)
                    
                    workflow.addTransition(transition)
            
            workflows.append(workflow)
        
        return workflows
    
    def get_boards(self):
        """获取看板列表。"""
        return self._boards
    
    def get_tags(self):
        """获取标签列表。"""
        return self._tags
    
    def get_workflows(self):
        """获取工作流列表。"""
        return self._workflows
