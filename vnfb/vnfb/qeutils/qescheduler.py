#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Temp solution for QE jobs submission. Hardcoded for the foxtrot cluster
# param: job (input -> temp solution)

# XXX: Make the wall time configurable
def schedule( sim, director, job ):
    # TODO: Change status of jobs depending on the scheduling steps
    # copy local job directory to server
    server          = director.clerk.getServers(id=job.serverid)    # not None
    settingslist    = director.clerk.getQESettings(where="simulationid='%s'" % sim.id)
    task            = director.clerk.getQETasks(id=job.taskid)  # not None
    settings        = settingslist[0]   # not None
    server_jobpath  = director.dds.abspath(job, server=server)

    # the scheduler
    scheduler = schedulerfactory( server )
    launch = lambda cmd: director.csaccessor.execute(
                                                    cmd,
                                                    server,
                                                    server_jobpath,
                                                    suppressException=True)
    scheduler = scheduler(launch, prefix = 'source ~/.vnf' )
    scheduler.setSimulationParams(job, settings, server, task)

    from pyre.units.time import hour
    walltime = 999*hour   # limit to one hour?
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath, walltime=walltime )

    # write id to the remote directory
    director.csaccessor.execute('echo "%s" > jobid' % id1, server, server_jobpath)

    return


def schedulerfactory( server ):
    'obtain scheduler factory'
    #right now, scheduler info is saved in db record of the server
    scheduler = server.scheduler
    if scheduler in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnfb.clusterscheduler import scheduler as factory
    try: scheduler = factory( scheduler )
    except: raise NotImplementedError, 'scheduler %r' % scheduler
    return scheduler


__date__ = "$Dec 7, 2009 8:45:49 AM$"


# ********************* DEAD CODE ********************* 

    # submit job through scheduler
    #walltime = job.walltime

    # update job db record
#    job.id_incomputingserver = id1
#    job.state = 'submitted'
#    import time
#    job.time_start = time.ctime()
#    director.clerk.updateRecordWithID(job)