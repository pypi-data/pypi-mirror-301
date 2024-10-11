import os
import sys
import numpy as np
import argparse
from argparse import RawTextHelpFormatter

import logging
log = logging.getLogger(__name__)

from .manage import (
  JobManager )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def total_walltime( job, exclude = None ):
  if exclude is None:
    exclude = list()

  total_n = 1
  total_w = job.walltime

  jobs = job.afterok + job.afterany

  exclude.extend( jobs )

  for j in jobs:
    if isinstance( j, Job ):
      n, w = total_walltime( j, exclude = exclude )

      total_n += n
      total_w += w


  return total_n, total_w

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Job:
  """
  Parameters
  ----------
  name : str
    Name of job
  path : str
    Path to job run directory
  run_cmd : str
    Template string for command to run. Available template variables are:
    `run_config_file`, `run_thread_per_mpi`.
  config_file : None | str
    Config file passed to command template string as `run_config_file`
  walltime : None | float
    Number of hours set as maximum job walltime (default: 1)
  nodes : None | int
    Number of compute nodes to request
  cpu_per_node : None | int
    Number of processors to request per node
  mpi_per_node : None | int
    Number of MPI processes to start per node
  thread_per_mpi : None | int
    Number of threads per MPI process, passed to command template as `run_thread_per_mpi`
  queue : None | str
    Job queue to submit to.
  use_modules : None | List[str]
    List of directories to use for searching module files
  load_modules : None | List[str]
    List of modules to load
  afterok : None | str | List[str | Job]
    Submit this job only after given job(s) complete without error
  afterany : None | str | List[str | Job]
    Submit this job only after given job(s) exit (with or without error)
  """

  default_email = None
  default_queue = None

  #-----------------------------------------------------------------------------
  def __init__( self,
    name,
    path = None,
    run_cmd = None,
    config_file = None,
    walltime = None,
    nodes = None,
    cpu_per_node = None,
    mpi_per_node = None,
    thread_per_mpi = None,
    queue = None,
    use_modules = None,
    load_modules = None,
    afterok = None,
    afterany = None,
    email = None ):

    if path is None:
      path = os.getcwd()

    path = os.path.abspath( path )

    if run_cmd is None:
      run_cmd = ""

    if walltime is None:
      walltime = 1.0

    if nodes is None:
      nodes = 1

    if cpu_per_node is None:
      cpu_per_node = 1

    if mpi_per_node is None:
      mpi_per_node = 1

    if thread_per_mpi is None:
      thread_per_mpi = cpu_per_node // mpi_per_node


    if afterok is None:
      afterok = list()

    else:
      if not isinstance( afterok, list ):
        afterok = [ afterok, ]

    if afterany is None:
      afterany = list()

    else:
      if not isinstance( afterany, list ):
        afterany = [ afterany, ]


    self._name = name
    self._path = path
    self._config_file = config_file
    self._run_cmd = run_cmd
    self._use_modules = use_modules
    self._load_modules = load_modules
    self._walltime = walltime
    self._nodes = nodes
    self._cpu_per_node = cpu_per_node
    self._mpi_per_node = mpi_per_node
    self._thread_per_mpi = thread_per_mpi
    self._queue = queue
    self._afterok = afterok
    self._afterany = afterany
    self._email = email
    self._job_id = None

  #-----------------------------------------------------------------------------
  def __str__( self ):
    opts = ", ".join([
      f"nodes {self.nodes}",
      f"ppn {self.cpu_per_node}",
      f"mpn {self.mpi_per_node}",
      f"tpm {self.thread_per_mpi}" ])

    return f"job '{self.name}' ({opts}) \"{self.path}\""

  #-----------------------------------------------------------------------------
  @property
  def name( self ):
    return self._name

  #-----------------------------------------------------------------------------
  @property
  def path( self ):
    return self._path

  #-----------------------------------------------------------------------------
  @property
  def config_file( self ):
    return self._config_file

  #-----------------------------------------------------------------------------
  @property
  def run_cmd( self ):
    return self._run_cmd

  #-----------------------------------------------------------------------------
  @property
  def walltime( self ):
    return self._walltime

  #-----------------------------------------------------------------------------
  @property
  def nodes( self ):
    return self._nodes

  #-----------------------------------------------------------------------------
  @property
  def cpu_per_node( self ):
    return self._cpu_per_node

  #-----------------------------------------------------------------------------
  @property
  def mpi_per_node( self ):
    return self._mpi_per_node

  #-----------------------------------------------------------------------------
  @property
  def thread_per_mpi( self ):
    return self._thread_per_mpi

  #-----------------------------------------------------------------------------
  @property
  def use_modules( self ):
    return self._use_modules

  #-----------------------------------------------------------------------------
  @property
  def load_modules( self ):
    return self._load_modules

  #-----------------------------------------------------------------------------
  @property
  def afterok( self ):
    return self._afterok

  #-----------------------------------------------------------------------------
  @property
  def afterany( self ):
    return self._afterany

  #-----------------------------------------------------------------------------
  @property
  def job_id( self ):
    return self._job_id

  #-----------------------------------------------------------------------------
  @property
  def email( self ):
    return self._email

  #-----------------------------------------------------------------------------
  @classmethod
  def set_default_email( cls, email ):
    cls.default_email = email

  #-----------------------------------------------------------------------------
  @property
  def queue( self ):
    return self._queue

  #-----------------------------------------------------------------------------
  @classmethod
  def set_default_queue( cls, queue ):
    cls.default_queue = queue

  #-----------------------------------------------------------------------------
  @property
  def status( self ):
    if self.job_id is None:
      raise ValueError(f"job not submitted: {self}")

    res = JobManager.job_manager.status(
      job_id = self.job_id )

    return res

  #-----------------------------------------------------------------------------
  def cancel( self ):

    if self.job_id is None:
      raise ValueError(f"job not submitted: {self}")

    res = JobManager.job_manager.cancel(
      job_id = self.job_id )

    return res

  #-----------------------------------------------------------------------------
  def submit( self,
    email = None,
    queue = None ):
    """
    Parameters
    ----------
    email : str
      User email
    queue : str
      Queue to submit to
    """

    if self.job_id is not None:
      raise ValueError(f"job already submitted: {self}")

    if email is not None:
      self._email = email

    if self.email is None:
      if self.default_email is None:
        raise ValueError("No email given for job, or submit, and no email set by `set_default_email`" )

      self._email = self.default_email

    if queue is not None:
      self._queue = queue

    if self.queue is None:
      if self.default_queue is None:
        raise ValueError("No queue given for job, or submit, and no queue set by `set_default_queue`" )

      self._queue = self.default_queue

    if self.run_cmd is None:
      return None

    afterok = list()
    afterany = list()

    for job in self.afterok:
      if isinstance( job, Job ):
        if job.job_id is None:
          job.submit(
            email = self.email,
            queue = self.queue )

        job_id = job.job_id

      else:
        job_id = str(job)

      afterok.append( job_id )

    for job in self.afterany:
      if isinstance( job, Job ):
        if job.job_id is None:
          job.submit(
            email = self.email,
            queue = self.queue )

        job_id = job.job_id

      else:
        job_id = str(job)

      afterany.append( job_id )

    self._job_id = JobManager.job_manager.submit(
      afterok = afterok,
      afterany = afterany,
      cmd_tmpl = self.run_cmd,
      job_name = self.name,
      job_email = self.email,
      job_queue = self.queue,
      job_walltime = self.walltime,
      job_nodes = self.nodes,
      job_cpu_per_node = self.cpu_per_node,
      run_mpi_per_node = self.mpi_per_node,
      run_thread_per_mpi = self.thread_per_mpi,
      run_use_modules = self.use_modules,
      run_load_modules = self.load_modules,
      run_root_dir = self.path,
      run_config_file = self.config_file )

  #-----------------------------------------------------------------------------
  @classmethod
  def parse_args( cls ):
    parser = argparse.ArgumentParser(
      description = "Job arguments",
      formatter_class = RawTextHelpFormatter )


    parser.add_argument( "--walltime",
      type = float,
      default = None,
      help = "walltime in hours." )

    parser.add_argument( "--nodes",
      type = int,
      default = None,
      help = "number of nodes." )

    parser.add_argument( "--ppn",
      type = int,
      default = None,
      help = "number processors per node" )

    parser.add_argument( "--mpn",
      type = int,
      default = None,
      help = "number of mpi processes per node." )

    parser.add_argument( "--tpm",
      type = int,
      default = None,
      help = "number of threads per mpi process." )

    parser.add_argument( "-q", "--queue",
      type = str,
      required = True,
      help = "queue to submit job." )

    parser.add_argument( "-m", "--email",
      type = str,
      required = True,
      help = "email of user submitting job" )

    parser.add_argument( "-r", "--root",
      type = str,
      default = None,
      help = "root directory to run job" )

    parser.add_argument( "-u", "--use_modules",
      type = str,
      default = None,
      nargs = '+',
      help = "use module files" )

    parser.add_argument( "-l", "--load_modules",
      type = str,
      default = None,
      nargs = '+',
      help = "load modules" )

    args = parser.parse_args( )

    job_kwargs = dict(
      walltime = args.walltime,
      nodes = args.nodes,
      cpu_per_node = args.ppn,
      mpi_per_node = args.mpn,
      thread_per_mpi = args.tpm,
      queue = args.queue,
      root = args.root,
      use_modules = args.use_modules,
      load_modules = args.load_modules,
      email = args.email )

    return job_kwargs
