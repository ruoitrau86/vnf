.. _vnfdeveloperguidemonitoring:

Monitoring
==========


VNF is a complex system that needs constant monitoring of system
health and system status. This is done by periodically running
scripts, each of which working on one aspect of the system.

Several scripts exist in $EXPORT_ROOT/vnf/bin to do this job:

* cron-monitors.sh: script that periodically calls script
  "run-monitors.sh"
* run-monitors.sh: script that runs monitor scripts

The cron-monitors.sh calls "timer.py" to periodically run a
script (s). (This could be replaced by a cron job.)

The runmonitors.sh script has the following main content::

 ./launch-detached.py -cmd='./updatejobstatus.py' -home=$WORKDIR
 ./launch-detached.py -cmd='./checkservers.py' -home=$WORKDIR
 ...

Each line looks like this::

 ./launch-detached.py -cmd=<cmd> -home=$WORKDIR

The launch-detached.py script is responsible to launch the command
<cmd> to a separate process so that the running of the command does
not block the script. Each command <cmd> is a regular command that
does something. For example, command "checkservers.py" check the 
computing servers to see if they are working correctly.

.. note::
   cron-monitors.sh will be automatically started when a vnf installation
   is started by ::
   
    $ start-luban-project.py /path/to/vnf/export

   So usually you don't need to start it manually.


Computing servers
-----------------

checkservers.py
"""""""""""""""

Check computing servers that are currently online.
If a computing server is not accessible, take it down.
An email will be sent to vnf developer m ailing list 

To run it::

 $ cd $EXPORT_ROOT/vnf/bin
 $ ./checkservers.py

This command has the following options:

* --check-softwares: check whether the software installation on the server is behaving correctly


activateserver.py
"""""""""""""""""
After a server is taking down automatically by the system monitor, 
and you have finished 

Activate a computing server.

To run it::

 $ cd $EXPORT_ROOT/vnf/bin
 $ ./activateserver.py -id=<server id>



Monitoring of web servers
-------------------------

Additional monitoring can be achieved by periodically poking and running work-flows
on the vnf release sites.
This actually depends on the deployment. 
Currently there are cron jobs being run to check whether some vnf release sites
are alive, and run some simple work flows on them. 
These cron jobs are now running on a linux virtual machine that is also
a buildbot slave for vnf.

