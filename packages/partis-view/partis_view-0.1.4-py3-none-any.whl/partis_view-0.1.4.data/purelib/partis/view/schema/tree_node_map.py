#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from partis.schema import (
  is_valued,
  is_evaluated,
  is_schema,
  Schema,
  SchemaStruct,
  EvaluatedMeta,
  PassPrim,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  SchemaStruct )

from partis.schema.hint import (
  Hint,
  HintLoc,
  HintList )

from partis.schema.color import (
  Color )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from .type_combo_w import TypeComboWidget

from .tree_edit_w import (
  TreeEditNode,
  TreeEditWidget )

from .evaluated_w import (
  EvaluatedTreeEditNode )

from .optional_w import (
  OptionalTreeEditNode )

from .bool_w import (
  BoolTreeEditNode )

from .int_w import (
  IntTreeEditNode )

from .float_w import (
  FloatTreeEditNode )

from .str_w import (
  StrTreeEditNode )

from .color_w import (
  ColorTreeEditNode )

from .list_w import (
  ListTreeEditNode )

from .map_w import (
  MapTreeEditNode )

from .struct_w import (
  StructTreeEditNode )

from .union_w import (
  UnionTreeEditNode )

from .pass_w import (
  PassTreeEditNode )

from .hint_w import (
  HintListNode,
  HintLocNode,
  HintNode )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
tree_schema_map = {
  HintLoc.schema : HintLocNode,
  Hint.schema : HintNode,
  HintList : HintListNode,
  PassPrim : PassTreeEditNode,
  BoolPrim : BoolTreeEditNode,
  IntPrim : IntTreeEditNode,
  FloatPrim : FloatTreeEditNode,
  Color : ColorTreeEditNode,
  StrPrim : StrTreeEditNode,
  SeqPrim : ListTreeEditNode,
  MapPrim : MapTreeEditNode,
  UnionPrim : UnionTreeEditNode,
  SchemaStruct : StructTreeEditNode }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeEditNodeMap:
  """Maps schema to TreeEditNode

  Parameters
  ----------
  node_map : dict[ Schema, :class:`partis.view.schema.tree_node_w.TreeEditNode` ]
    Specialized mapping of schemas to tree nodes

  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    node_map = None ):

    if node_map is None:
      node_map = dict()

    for k, v in node_map.items():
      if not is_schema(k):
        raise ValueError(
          f'Key must be a Schema: {type(k)}' )

      if not issubclass( v, TreeEditNode ):
        raise ValueError(
          f"Value must be subclass of TreeEditNode: {v}" )


    self._p_node_map = {
      **node_map,
      **tree_schema_map }

  #-----------------------------------------------------------------------------
  @property
  def node_map(self):
    return self._p_node_map

  #-----------------------------------------------------------------------------
  def __call__( self, schema, state = None ):
    # ensure the lookup is not done on a proxy
    schema = schema.schema

    if state is None:
      # use init value to determine if the state will start out as an expression
      state = schema.decode(
        val = schema.init_val )

    if not is_valued( state ) and is_evaluated( state._src ):
      return EvaluatedTreeEditNode

    for k, v in self.node_map.items():

      if isinstance( k, Schema ) and issubclass( schema, k ):
        # check for sub classes
        return v

      elif issubclass( type(schema), k ):
        # check for class types instead
        return v

    raise NotImplementedError(
      f"Tree widget not defined for schema: {schema} ({type(schema)})")
