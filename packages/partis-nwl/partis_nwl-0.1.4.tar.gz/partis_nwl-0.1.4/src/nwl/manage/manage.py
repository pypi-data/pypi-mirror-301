"""Submits a job pbs file using submit
"""

from subprocess import Popen, PIPE
import os
import sys
import re
import time
import ruamel.yaml as yaml
import logging
log = logging.getLogger(__name__)

from .db import (
  JobORM,
  JobDB )

MANAGERS = [
  "torque",
  "slurm" ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def h_to_hms( total_hours ):
  """Convert positive floating point hours to integer H,M,S
  """
  if total_hours <= 0.0:
    return 0, 0, 0

  # convert to an integer total number of seconds, rounding up
  total_secs = int( 0.5 + 3600.0 * total_hours )
  secs = total_secs % 60
  total_mins = total_secs // 60
  mins = total_mins % 60
  hrs = total_mins // 60

  return hrs, mins, secs

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class JobStatus:
  def __init__( self,
    job_id,
    job_name,
    run_root_dir,
    managed,
    submitted,
    started,
    stopped,
    failed ):

    self.job_id = str(job_id)
    self.job_name = str(job_name)
    self.run_root_dir = str(run_root_dir)
    self.managed = bool(managed)
    self.submitted = submitted
    self.started = started
    self.stopped = stopped
    self.failed = failed

    self._attrs = [
      'job_id',
      'job_name',
      'run_root_dir',
      'managed',
      'submitted',
      'started',
      'stopped',
      'failed' ]

    _kwargs = ", ".join([ f"{k} = {getattr(self, k)}" for k in self._attrs ])

    self._repr = f"JobStatus( {_kwargs} )"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return self._repr

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return repr( self )

  #-----------------------------------------------------------------------------
  def as_dict( self ):
    d = dict()

    for k in self._attrs:
      d[k] = getattr( self, k )

    return d

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class JobManager:
  job_manager = None

  #-----------------------------------------------------------------------------
  def __init__( self ):
    raise NotImplementedError("")

  #-----------------------------------------------------------------------------
  def _manager_script_template( self ):
    """Internal method to create a batch script template for the manager

    Returns
    -------
    template : str | callable
    """
    raise NotImplementedError("")

  #-----------------------------------------------------------------------------
  def _manager_submit( self,
    pbs_file,
    afterany = None,
    afterok = None ):
    """Internal method to submit batch script to the manager

    Parameters
    ----------
    pbs_file : str
      Path to batch script
    afterany : None | str | List[str]
      This job can begin execution after the specified jobs have terminated.
    afterok : None | str | List[str]
      This job can begin execution after the specified jobs have successfully
      executed (ran to completion with an exit code of zero). If the dependency(s)
      are not successful this job will be canceled.


    Returns
    -------
    job_id : str
      Id of submitted job
    """

    raise NotImplementedError("")

  #-----------------------------------------------------------------------------
  def _manager_status( self, job_id ):
    """Internal method to create a batch script template for the manager

    Parameters
    ----------
    job_id : str

    Returns
    -------
    managed : bool
      Returns true if the job is not complete (i.e. waiting, running, etc.),
      and is still being managed (i.e. not completed, cancelled, failed, etc. ).
      Managed means that the status of the given job is not final and could change.
    job_name : None | str
      Returns the name of the job as originally submitted if ``managed`` is True.
      This may be used to add tracking information for jobs that were
      submitted outside of this interface.
    run_root_dir : None | str
      Returns the run directory of the job as originally submitted if ``managed`` is True.
      This may be used to add tracking information for jobs that were
      submitted outside of this interface.
    """
    raise NotImplementedError("")

  #-----------------------------------------------------------------------------
  def _manager_cancel( self, job_id ):
    """Internal method to cancel job with manager
    """
    raise NotImplementedError("")

  #-----------------------------------------------------------------------------
  def submit( self,
    cmd_tmpl,
    job_name,
    job_email,
    job_queue,
    job_walltime,
    job_nodes,
    job_cpu_per_node,
    run_mpi_per_node,
    run_thread_per_mpi,
    run_root_dir,
    run_config_file = None,
    run_use_modules = None,
    run_load_modules = None,
    afterany = None,
    afterok = None ):
    """
    Parameters
    ----------
    cmd_tmpl : str | List[str]
      Template for command(s) to run. Available template arguments:
        run_mpi : the command to start a program with MPI with a total number
          of processes equal to ``job_nodes * run_mpi_per_node``
        run_thread_per_mpi : a number of threads specified for job
        run_config_file : a config file specified for job
    job_name : str
      Name of job
    job_email : str
      Email for user submitting job
    job_queue : str
      Queue/partition to submit job
    job_walltime : float
      Allocated walltime in hours
    job_nodes : int
      Number of compute nodes to request
    job_cpu_per_node : int
      Number of CPU cores to request per node. The total number of CPU cores
      will be equal to ``job_nodes * job_cpu_per_node``.
    run_mpi_per_node: int
      Number of MPI processes to start per node. Total number of processes will
      be equal to ``job_nodes * run_mpi_per_node``
    run_thread_per_mpi : int
      Number of threads suggested to be used by a program. This parameter does not
      affect resource allocated, but should be chosen to match. For example,
      a typical value might be ``job_cpu_per_node / run_mpi_per_node``, so that
      each process on a node has the same number of CPUs allocated as the number
      of threads it is told to use. However, it is free to the user to the user
      to choose this value to optimize resource utilization.
    run_root_dir : str
      Directory to create job script, output files, and to working directory when
      running script commands.
    run_config_file : None | str
      An optional path to a custom config file that is passed to the command.
    run_use_modules : None | str | List[str]
      Path(s) to directories to search for module files.
    run_load_modules : None | str | List[str]
      Module files to load before running commands.
    afterany : None | str | List[str]
      This job can begin execution after the specified jobs have terminated.
    afterok : None | str | List[str]
      This job can begin execution after the specified jobs have successfully
      executed (ran to completion with an exit code of zero). If the dependency(s)
      are not successful this job will be canceled.

    Returns
    -------
    job_id : str
      Resulting manager job id
    """


    cwd = os.getcwd()

    try:
      os.chdir( run_root_dir )

      # write the pbs file into the working directory using the given job name
      pbs_file = f"{job_name}.pbs"

      doc = format_pbs(
        manager_tmpl = self._manager_script_template(),
        cmd_tmpl = cmd_tmpl,
        job_name = job_name,
        job_email = job_email,
        job_queue = job_queue,
        job_walltime = job_walltime,
        job_nodes = job_nodes,
        job_cpu_per_node = job_cpu_per_node,
        run_use_modules = run_use_modules,
        run_load_modules = run_load_modules,
        run_root_dir = run_root_dir,
        run_config_file = run_config_file,
        run_mpi_per_node = run_mpi_per_node,
        run_thread_per_mpi = run_thread_per_mpi )

      with open( pbs_file, "w") as fp:
        fp.write( doc )

      _pbs_file = os.path.abspath( os.path.join( run_root_dir, pbs_file ) )
      log.info(f"created batch script: {_pbs_file}")

      job_id = self._manager_submit(
        pbs_file = pbs_file,
        afterany = afterany,
        afterok = afterok )

      stat_file = f"{job_name}.{job_id}.stat.yaml"
      res_file = f"{job_name}.{job_id}.res.yaml"

      with open( stat_file, "w" ) as fp:
        fp.write( yaml.round_trip_dump(
          dict(
            submitted = int(time.time()) ),
          default_flow_style = False,
          allow_unicode = True ) )

    finally:
      os.chdir( cwd )

    return job_id


  #-----------------------------------------------------------------------------
  def status( self, job_id ):
    """
    """

    job_id = str( job_id )

    # job information that will try to be recovered from the job_id
    run_root_dir = None
    job_name = None
    stat_file = None

    tracked = False
    managed = False
    submitted = None
    started = None
    stopped = None
    failed = False

    try:
      managed, _job_name, _run_root_dir = self._manager_status(
        job_id = job_id )

      if managed:
        assert _job_name is not None
        assert _run_root_dir is not None

        if job_name is None:
          job_name = _job_name

        if run_root_dir is None:
          run_root_dir = _run_root_dir

    except:
      pass


    if not ( tracked or managed ):
      raise ValueError(
        f"Job not found in tracking database or job manager: {job_id}" )

    # TODO: add tracking for jobs submitted outside of this interface?

    if stat_file is None and not ( run_root_dir is None or job_name is None ):
      # try to guess the name
      stat_file = os.path.join(
        run_root_dir,
        f"{job_name}.{job_id}.stat.yaml" )

    if stat_file is not None and os.path.exists( stat_file ):
      # should exist if the job started, but not if still waiting

      with open( stat_file, "r" ) as fp:
        stat = yaml.round_trip_load( fp.read() )

      submitted = stat.get( 'submitted', None )
      started = stat.get( 'started', None )
      stopped = stat.get( 'stopped', None )
      exitcode = stat.get( 'exitcode', None )

      # failed if exitcode is non-zero
      failed = failed or ( exitcode is not None and exitcode != 0 )

    # failed if the job never stopped and is no longer being managed
    failed = failed or ( not managed and not stopped )

    status = JobStatus(
      job_id = job_id,
      job_name = job_name,
      run_root_dir = run_root_dir,
      managed = managed,
      submitted = submitted,
      started = started,
      stopped = stopped,
      failed = failed )

    return status

  #-----------------------------------------------------------------------------
  def cancel( self, job_id ):
    return self._manager_cancel( job_id )

  #-----------------------------------------------------------------------------
  def command( self, args ):

    p = Popen( args, stdin=PIPE, stdout=PIPE, stderr=PIPE )
    out, err = p.communicate()
    rc = p.returncode

    if out is not None:
      out = out.decode('ascii').strip()
    else:
      out = ""

    if err is not None:
      err = err.decode('ascii').strip()
    else:
      err = ""

    out += err

    if rc != 0:
      msg = f"manager command failed: {args}\n{out}\n"
      raise ValueError( msg )

    return out

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Slurm( JobManager ):
  #-----------------------------------------------------------------------------
  def __init__( self ):
    self.command(["scontrol", "-h"])

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return "slurm"

  #-----------------------------------------------------------------------------
  def _manager_script_template( self ):
    return slurm_tmpl

  #-----------------------------------------------------------------------------
  def _manager_submit( self,
    pbs_file,
    afterany = None,
    afterok = None ):

    args = [ "sbatch", "--parsable", "--kill-on-invalid-dep=yes" ]

    if afterany is not None and len(afterany) > 0:
      if isinstance( afterany, list ):
        afterany = ":".join( afterany )

      args.append("--dependency=afterany:{:s}".format(afterany))

    if afterok is not None and len(afterok) > 0:
      if isinstance( afterok, list ):
        afterok = ":".join( afterok )

      args.append("--dependency=afterok:{:s}".format(afterok))

    args.append( pbs_file )

    out = self.command( args )

    job_id = out.split(":")[-1]

    return job_id

  #-----------------------------------------------------------------------------
  def _manager_status( self, job_id ):

    managed = False
    job_name = None
    run_root_dir = None

    args = [ "scontrol", "show", "job", "-dd", str(job_id) ]

    try:
      out = self.command( args )

    except:
      return False, None, None


    managed = True

    matches = list(re.finditer(r"((?P<key>\S+)\=(?P<value>\S+))", out ))

    _status = dict()

    for m in matches:
      value = m.group('value').strip()

      if value != "(null)":
        _status[ m.group('key') ] = value

    if "JobState" in _status:
      state = _status["JobState"]

      if state in ["CANCELLED", "CA", "COMPLETED", "C", "CD", "CG", "FAILED", "F", "NF" ]:
        # no longer being managed
        managed = False

      if "JobName" in _status:
        job_name = _status["JobName"]

      if "WorkDir" in _status:
        run_root_dir = _status["WorkDir"]

    return managed, job_name, run_root_dir

  #-----------------------------------------------------------------------------
  def _manager_cancel( self, job_id ):
    args = [ "scancel", str(job_id) ]

    self.command( args )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Torque( JobManager ):

  #-----------------------------------------------------------------------------
  def __init__( self ):
    self.command(["qstat"])

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return "torque"

  #-----------------------------------------------------------------------------
  def _manager_script_template( self ):
    return torque_tmpl

  #-----------------------------------------------------------------------------
  def _manager_submit( self,
    pbs_file,
    afterany = None,
    afterok = None ):


    args = [ "qsub", pbs_file ]
    add_attr = list()

    if afterany is not None and len(afterany) > 0:
      if isinstance( afterany, list ):
        afterany = ":".join( afterany )

      add_attr.append("depend=afterany:{:s}".format(afterany))

    if afterok is not None and len(afterok) > 0:
      if isinstance( afterok, list ):
        afterok = ":".join( afterok )

      add_attr.append("depend=afterok:{:s}".format(afterok))

    if len(add_attr) > 0:
      args.append("-W")
      args.extend( add_attr )

    out = self.command( args )

    job_id = out.split(":")[-1]

    return job_id

  #-----------------------------------------------------------------------------
  def _manager_status( self, job_id ):

    managed = False
    job_name = None
    run_root_dir = None

    args = [ "qstat", "-f", str(job_id) ]

    try:
      out = self.command( args )
      managed = True

    except:
      return False, None, None


    managed = True

    matches = list(re.finditer(r"((?P<key>\S+) \= (?P<value>\S+))", out ))

    _status = dict()

    for m in matches:
      value = m.group('value').strip()

      if value != "(null)":

        _status[ m.group('key') ] = value

    if "job_state" in _status:
      state = _status["job_state"]

      if state in [ "C", ]:
        # no longer being managed
        managed = False

    if "Job_Name" in _status:
      job_name = _status["Job_Name"].strip()

    #NOTE: the work directory is part of the variables list using a different
    # delimater format
    workdirs = list(re.finditer(r"PBS_O_WORKDIR\=(?P<value>[^\r\n\t\f\v \,]+)", out ))

    if len(workdirs) > 0:
      run_root_dir = workdirs[0].group('value').strip()

    return managed, job_name, run_root_dir

  #-----------------------------------------------------------------------------
  def _manager_cancel( self, job_id ):

    args = [ "qdel", str(job_id) ]

    out = self.command( args )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def default_job_manager():

    errors = list()

    try:
      return Slurm()

    except Exception as e:
      msg = f"slurm: {e}"
      # log.info( msg )
      errors.append( msg )

    try:
      return Torque()

    except Exception as e:
      msg = f"torque: {e}"
      # log.info( msg )
      errors.append( msg )

    msg = f"Could not determin job manager: {errors}"

    raise ValueError( msg )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
run_log_tmpl = "{run_cmd} > \"${{RUN_LOG_FILE}}\" 2>&1"
run_log_append_tmpl = "{run_cmd} >> \"${{RUN_LOG_FILE}}\" 2>&1"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mpi_cmd_tmpl = "mpirun -machinefile ${{RUN_NODEFILE}}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
module_use_tmpl = "module use {use_modules:s}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
module_load_tmpl = "module load {load_modules:s}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cmd_check_tmpl = """
if [[ $CMD_EXIT_CODE -eq 0 ]];
then
# reset exit code for next command
echo "  - {run_cmd_sans}" >> "${{RUN_STAT_FILE}}"
CMD_EXIT_CODE=0
{{ {run_cmd}; }} || CMD_EXIT_CODE=$?
fi
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
torque_tmpl = """
######################################+########################################
#                   PBS options header for submit script                        #
######################################+########################################

# A comprehensive guide to PBS job submissions can be found at:
# http://docs.adaptivecomputing.com/torque/4-0-2/help.htmm

# PBS option : job identifier : name
#PBS -N {job_name:s}

# PBS option : admin : queue
#PBS -q {job_queue:s}

# PBS option : streams : join standard output and error
#PBS -j oe

# PBS option : streams : keep streams
#PBS -k oe

# PBS option : mail : mailing conditions
#PBS -m n

# PBS option : mail : emails
# NOTE: external email addresses (e.g. user@nanohmic.com) are permitted
#PBS -M {job_email:s}

# PBS option : resource : nodes - no. of nodes, ppn - no. of threads per node
# NOTE: No. of threads per MPI process are specified in batch script below
#PBS -l nodes={job_nodes:d}:ppn={job_cpu_per_node:d}

# PBS option : resource : walltime (HH:MM:SS)
#PBS -l walltime={job_walltime_hrs:d}:{job_walltime_mins:d}:{job_walltime_secs:d}

# PBS option : environment : shell path
#PBS -S /bin/bash
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
slurm_tmpl = """
######################################+########################################
#                   SBATCH options header for sbatch script                   #
######################################+########################################
# A comprehensive guide to SBATCH job submissions can be found at:

# SBATCH option : job identifier : name
#SBATCH --job-name={job_name:s}

# SBATCH option : admin : queue
#SBATCH --partition={job_queue:s}

# NOTE: external email addresses (e.g. user@nanohmic.com) are permitted
#SBATCH --mail-user={job_email:s}

# SBATCH option : resource : nodes - no. of nodes, ppn - no. of threads per node
# NOTE: No. of threads per MPI process are specified in batch script below
#SBATCH --nodes={job_nodes:d}
#SBATCH --cpus-per-task={job_cpu_per_node:d}

# SBATCH option : resource : walltime (HH:MM:SS)
#SBATCH --time={job_walltime_hrs:d}:{job_walltime_mins:d}:{job_walltime_secs:d}

#SBATCH --export=NONE

# interoperable evironment variables with PBS
export PBS_JOBID="${{SLURM_JOB_ID}}"
export PBS_JOBNAME="${{SLURM_JOB_NAME}}"
export PBS_O_QUEUE="${{SLURM_JOB_PARTITION}}"
export PBS_NUM_NODES="${{SLURM_JOB_NUM_NODES}}"
export PBS_NUM_PPN="${{SLURM_CPUS_ON_NODE}}"
export PBS_NP="${{SLURM_NTASKS}}"
export PBS_O_WORKDIR="${{SLURM_SUBMIT_DIR}}"
export PBS_O_NODENUM="${{SLURM_NODEID}}"
export PBS_O_HOST="${{SLURM_SUBMIT_HOST}}"
export PBS_NODEFILE="${{PBS_O_WORKDIR}}/.nodefile_${{SLURM_JOBID}}"
echo "${{SLURM_JOB_NODELIST}}">"${{PBS_NODEFILE}}"
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
local_tmpl = """
######################################+########################################
#                       Emmulates environment PBS variabls                    #
######################################+########################################

# interoperable evironment variables with PBS
export PBS_JOBID='{job_id}'
export PBS_JOBNAME='{job_name}'
export PBS_O_QUEUE='{job_queue}'
export PBS_NUM_NODES='{job_nodes:d}'
export PBS_NUM_PPN='{job_cpu_per_node:d}'
export PBS_NP='1'
export PBS_O_WORKDIR='{run_root_dir:s}'
export PBS_O_NODENUM='0'
export PBS_O_HOST='{hostname:d}'
export PBS_NODEFILE="${{PBS_O_WORKDIR}}/.nodefile"
echo '{hostname:d}'>"${{PBS_NODEFILE}}"
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# template PBS job file
script_tmpl = """#!/bin/bash
######################################+########################################
#                                                                             #
# Script for submitting runs Nanohmics' Hyperion cluster                      #
#                                                                             #
# This script can be modified to run on other clusters by updating cluster    #
# specific PBS flags, module names, and executable paths.                     #
#                                                                             #
######################################+########################################

{job_options:s}

######################################+########################################
#                                BATCH script                                 #
######################################+########################################

set -ef -o pipefail

# ensure init modules
. "${{MODULESHOME}}/init/bash"

# ------------------------- SET RUN PARAMETERS ------------------------- #
# MPI processes per node
RUN_NUM_MPPN='{run_mpi_per_node:d}'
RUN_ROOT='{run_root_dir:s}'
RUN_CONFIG='{run_config_file:s}'
RUN_LOG_FILE="{job_name:s}.${{PBS_JOBID}}.log"
RUN_STAT_FILE="{job_name:s}.${{PBS_JOBID}}.stat.yaml"
RUN_RES_FILE="{job_name:s}.${{PBS_JOBID}}.res.yaml"

# Parameter : path to modified pbs nodefile
RUN_NODEFILE="${{RUN_ROOT}}/{job_name:s}.${{PBS_JOBID}}.nodefile"

# Action : write modified nodefile, replicate each node for each MPI process on the node
sort ${{PBS_NODEFILE}} | uniq |
    awk "{{for(i=0;i<${{RUN_NUM_MPPN}};i++)print}}" > ${{RUN_NODEFILE}}

# -------------------------- PRINT PBS PARAMETERS --------------------------- #

printf '%s\\n' '# PBS Parameter Summary --------------------------------------#'
printf 'PBS_ENVIRONMENT      : %s\\n' "$PBS_ENVIRONMENT"
printf 'PBS_O_HOST           : %s\\n' "$PBS_O_HOST"
printf 'PBS_O_WORKDIR        : %s\\n' "$PBS_O_WORKDIR"
printf 'PBS_O_NODENUM        : %s\\n' "$PBS_O_NODENUM"
printf 'PBS_O_QUEUE          : %s\\n' "$PBS_O_QUEUE"
printf 'PBS_JOBNAME          : %s\\n' "$PBS_JOBNAME"
printf 'PBS_JOBID            : %s\\n' "$PBS_JOBID"
printf 'PBS_NUM_NODES        : %s\\n' "$PBS_NUM_NODES"
printf 'PBS_NUM_PPN          : %s\\n' "$PBS_NUM_PPN"
printf 'PBS_NODEFILE         : %s\\n' "$PBS_NODEFILE"
printf '%s\\n' '# Run Parameter Summary --------------------------------------#'
printf 'RUN_NUM_MPPN         : %s\\n' "$RUN_NUM_MPPN"
printf 'RUN_NODEFILE         : %s\\n' "$RUN_NODEFILE"
printf 'RUN_ROOT             : %s\\n' "$RUN_ROOT"
printf 'RUN_CONFIG           : %s\\n' "$RUN_CONFIG"
printf 'RUN_LOG_FILE         : %s\\n' "$RUN_LOG_FILE"
printf 'RUN_STAT_FILE        : %s\\n' "$RUN_STAT_FILE"
printf 'RUN_RES_FILE         : %s\\n' "$RUN_RES_FILE"
printf '%s\\n' '# ------------------------------------------------------------#'

printf '%s\\n\\n' '# User -------------------------------------------------------#'
id

printf '%s\\n\\n' '# Modules ----------------------------------------------------#'

# clean the user's module environment
module purge

# load the modules environment
{run_use_modules:s}

module avail

{run_load_modules:s}

module list

printf '%s\\n\\n' '# Environment ------------------------------------------------#'
env

# --------------------------- RUN MPI EXECUTABLE ---------------------------- #

# set current path to be the run root directory
cd "${{RUN_ROOT}}"

echo $PWD

printf '%s\\n\\n' '# Commands ----------------------------------------------------#'
echo "started: "$(date +"%s") >> "${{RUN_STAT_FILE}}"
echo "commands:" >> "${{RUN_STAT_FILE}}"

# primary run command
CMD_EXIT_CODE=0

{run_cmd}

echo "stopped: "$(date +"%s") >> "${{RUN_STAT_FILE}}"
echo "exitcode: ${{CMD_EXIT_CODE}}" >> "${{RUN_STAT_FILE}}"

"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def format_tmpl( tmpl, **kwargs ):
  if isinstance( tmpl, str ):
    return tmpl.format( **kwargs )

  if callable( tmpl ):
    return tmpl( **kwargs )

  raise ValueError(f"`tmpl` must be format string or callable: {tmpl}")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def format_pbs(
  manager_tmpl,
  cmd_tmpl,
  job_name,
  job_email,
  job_queue,
  job_walltime,
  job_nodes,
  job_cpu_per_node,
  run_mpi_per_node,
  run_thread_per_mpi,
  run_root_dir,
  run_config_file = None,
  run_use_modules = None,
  run_load_modules = None ):

  run_mpi_total = run_mpi_per_node * job_nodes

  walltime_hrs, walltime_mins, walltime_secs = h_to_hms( job_walltime )

  job_options = format_tmpl(
    tmpl = manager_tmpl,
    job_name = job_name,
    job_email = job_email,
    job_queue = job_queue,
    job_walltime_hrs = walltime_hrs,
    job_walltime_mins = walltime_mins,
    job_walltime_secs = walltime_secs,
    job_nodes = job_nodes,
    job_cpu_per_node = job_cpu_per_node )

  if run_use_modules is not None:
    if not isinstance( run_use_modules, list ):
      run_use_modules = [ run_use_modules, ]

    run_use_modules = "\n".join([
      format_tmpl(
        tmpl = module_use_tmpl,
        use_modules = m )
      for m in run_use_modules ])

  else:
    run_use_modules = ""

  if run_load_modules is not None:
    if not isinstance( run_load_modules, list ):
      run_load_modules = [ run_load_modules, ]

    run_load_modules = format_tmpl(
      tmpl = module_load_tmpl,
      load_modules = " ".join( run_load_modules ) )

  else:
    run_load_modules = ""

  if run_config_file is None:
    run_config_file = "<no file>"


  if not isinstance( cmd_tmpl, list ):
    cmd_tmpl = [ cmd_tmpl, ]

  if run_mpi_total > 1:
    run_mpi = format_tmpl(
      tmpl = mpi_cmd_tmpl,
      run_mpi_total = run_mpi_total )

  else:
    run_mpi = ""

  commands = list()

  for i, cmd in enumerate( cmd_tmpl ):

    # format base command
    cmd = format_tmpl(
      tmpl = cmd,
      run_mpi = run_mpi,
      run_thread_per_mpi = run_thread_per_mpi,
      run_config_file = run_config_file )

    # add logging
    if i == 0:
      cmd = format_tmpl(
        tmpl = run_log_tmpl,
        run_cmd = cmd )

    else:
      cmd = format_tmpl(
        tmpl = run_log_append_tmpl,
        run_cmd = cmd )

    # sanitize command string
    cmd_sans = cmd.replace('"', '\\"')

    # add checking for return status
    cmd = format_tmpl(
      tmpl = cmd_check_tmpl,
      run_cmd = cmd,
      run_cmd_sans = cmd_sans )

    commands.append( cmd )

  run_cmd = "\n\n".join( commands )

  return format_tmpl(
    tmpl = script_tmpl,
    job_name = job_name,
    run_cmd = run_cmd,
    job_options = job_options,
    run_use_modules = run_use_modules,
    run_load_modules = run_load_modules,
    run_root_dir = run_root_dir,
    run_config_file = run_config_file,
    run_mpi_per_node = run_mpi_per_node,
    run_mpi_total = run_mpi_total )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_last_job_file( path, pattern ):
  files = list()
  rec = re.compile( pattern )

  for file in os.listdir( path ):
    match = rec.fullmatch(file)

    if match is not None:
      files.append( file )

  if len(files) == 0:
    return None

  files = sorted( files )

  return os.path.join( str(path), files[-1] )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

JobManager.job_manager = default_job_manager()
