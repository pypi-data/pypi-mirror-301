# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  adict )

from partis.schema import (
  is_mapping,
  is_sequence,
  EvaluatedContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolContext( EvaluatedContext,
  id = 'nwl' ):
  """Base evaluation context for NWL tools
  """

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    results,
    static ):

    super().__init__(
      module = results._schema.__module__ )

    self._p_results = results
    self._p_static = static

  #-----------------------------------------------------------------------------
  def locals( self, schema ):
    return {
      '_' : self._p_results,
      'static' : self._p_static }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class QueryContext( ToolContext,
  id = 'query' ):
  """Evaluation context for NWL tool query expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EnabledInputContext( ToolContext,
  id = 'inputs' ):
  """Evaluation context for NWL tool input expressions
  """
  #-----------------------------------------------------------------------------
  def __init__( self, *,
    results,
    static,
    parent = None,
    next_key = None ):

    super().__init__(
      results = results,
      static = static )

    if parent is None:
      parent = {
        'parent' : None,
        'value' : self._p_results.data }

      next_key = 'inputs'

    self._p_next_key = next_key
    self._p_parent = adict(parent)

  #-----------------------------------------------------------------------------
  def locals( self, schema ):
    return {
      '_' : adict({
        **self._p_results,
        'parent' : self._p_parent }),
      'static' : self._p_static }

  #-----------------------------------------------------------------------------
  def __call__( self, *,
    schema,
    parent,
    key ):

    value = self._p_parent.value[self._p_next_key]

    if not (
      (is_mapping(value) and key in value)
      or (is_sequence(value) and isinstance(key, int) and key < len(value) ) ):

      return self

    return type(self)(
      results = self._p_results,
      static = self._p_static,
      parent = {
        'parent' : self._p_parent,
        'value' : value },
      next_key = key )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OutputsContext( ToolContext,
  id = 'outputs' ):
  """Evaluation context for NWL tool output expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogContext( ToolContext,
  id = 'log' ):
  """Evaluation context for NWL tool logging expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CommandsContext( ToolContext,
  id = 'commands' ):
  """Evaluation context for NWL tool command expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CommandLogContext( CommandsContext,
  id = 'log' ):
  """Evaluation context for NWL tool command log expressions
  """

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    results,
    static,
    command ):

    super().__init__(
      results = results,
      static = static )

    self._p_command = command

  #-----------------------------------------------------------------------------
  def locals( self, schema ):

    return {
      '_' : adict({
        **self._p_results,
        'command' : self._p_command }),
      'static' : self._p_static }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ArgumentContext( CommandsContext,
  id = 'arg' ):
  """Evaluation context for NWL tool command argument expressions
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScriptContext( CommandsContext,
  id = 'script' ):
  """Evaluation context for NWL tool command scripts
  """
  pass
