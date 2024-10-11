import typing
import collections.abc
import typing_extensions
import bpy.types

class BakeNodeItemAddOperator(
    SocketItemAddOperator, BakeNodeOperator, bpy.types.Operator
):
    """Add a bake item to the bake node"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    default_socket_type: typing.Any
    id_data: typing.Any
    items_name: typing.Any
    node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class BakeNodeItemMoveOperator(
    SocketMoveItemOperator, BakeNodeOperator, bpy.types.Operator
):
    """Move a bake item up or down in the list"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    items_name: typing.Any
    node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class BakeNodeItemRemoveOperator(
    SocketItemRemoveOperator, BakeNodeOperator, bpy.types.Operator
):
    """Remove a bake item from the bake node"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    items_name: typing.Any
    node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class NodeOperator:
    @classmethod
    def get_node(cls, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class IndexSwitchItemAddOperator(bpy.types.Operator):
    """Add an item to the index switch"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class IndexSwitchItemRemoveOperator(bpy.types.Operator):
    """Remove an item from the index switch"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class MoveModifierToNodes(bpy.types.Operator):
    """Move inputs and outputs from in the modifier to a new node group"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class NewGeometryNodeGroupTool(bpy.types.Operator):
    """Create a new geometry node group for a tool"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class NewGeometryNodeTreeAssign(bpy.types.Operator):
    """Create a new geometry node group and assign it to the active modifier"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class NewGeometryNodesModifier(bpy.types.Operator):
    """Create a new modifier with a new geometry node group"""

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

    def execute(self, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class RepeatZoneItemAddOperator(
    SocketItemAddOperator, RepeatZoneOperator, bpy.types.Operator
):
    """Add a repeat item to the repeat zone"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    default_socket_type: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class RepeatZoneItemMoveOperator(
    SocketMoveItemOperator, RepeatZoneOperator, bpy.types.Operator
):
    """Move a repeat item up or down in the list"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class RepeatZoneItemRemoveOperator(
    SocketItemRemoveOperator, RepeatZoneOperator, bpy.types.Operator
):
    """Remove a repeat item from the repeat zone"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class ZoneOperator:
    @classmethod
    def get_node(cls, context):
        """

        :param context:
        """

    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class SimulationZoneItemAddOperator(
    SocketItemAddOperator, SimulationZoneOperator, bpy.types.Operator
):
    """Add a state item to the simulation zone"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    default_socket_type: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class SimulationZoneItemMoveOperator(
    SocketMoveItemOperator, SimulationZoneOperator, bpy.types.Operator
):
    """Move a simulation state item up or down in the list"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class SimulationZoneItemRemoveOperator(
    SocketItemRemoveOperator, SimulationZoneOperator, bpy.types.Operator
):
    """Remove a state item from the simulation zone"""

    active_index_name: typing.Any
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        :rtype: bpy.types.Struct
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        :rtype: typing.Any
        """

class SocketItemAddOperator:
    active_index_name: typing.Any
    default_socket_type: typing.Any
    items_name: typing.Any

    def execute(self, context):
        """

        :param context:
        """

class SocketItemRemoveOperator:
    active_index_name: typing.Any
    items_name: typing.Any

    def execute(self, context):
        """

        :param context:
        """

class SocketMoveItemOperator:
    active_index_name: typing.Any
    items_name: typing.Any

    def execute(self, context):
        """

        :param context:
        """

class BakeNodeOperator(NodeOperator):
    active_index_name: typing.Any
    items_name: typing.Any
    node_type: typing.Any

class RepeatZoneOperator(ZoneOperator):
    active_index_name: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

class SimulationZoneOperator(ZoneOperator):
    active_index_name: typing.Any
    input_node_type: typing.Any
    items_name: typing.Any
    output_node_type: typing.Any

def add_empty_geometry_node_group(name): ...
def edit_geometry_nodes_modifier_poll(context): ...
def geometry_modifier_poll(context): ...
def geometry_node_group_empty_modifier_new(name): ...
def geometry_node_group_empty_new(name): ...
def geometry_node_group_empty_tool_new(context): ...
def get_context_modifier(context): ...
def get_enabled_socket_with_name(sockets, name): ...
def get_socket_with_identifier(sockets, identifier): ...
def modifier_attribute_name_get(modifier, identifier): ...
def modifier_input_use_attribute(modifier, identifier): ...
def socket_idname_to_attribute_type(idname): ...
