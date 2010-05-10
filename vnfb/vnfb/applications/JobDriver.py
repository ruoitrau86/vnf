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

# See also vnfb/applications/ITaskApp.py
# XXX Fix me!!!

#import time
#
from vnfb.dom.QEJob import QEJob
from vnfb.qeutils.qeutils import stamp, writeRecordFile, defaultInputName, readRecordFile
from vnfb.qeutils.qeconst import RUNSCRIPT, TYPE, NOPARALLEL
from vnfb.qeutils.qeutils import packname
from luban.applications.UIApp import UIApp as base

import pyre.idd
import pyre.inventory
import vnfb.components

"""
Jobs submission steps:
    - Creating job records          - 10%
    - Preparing configuration files - 20%
    - Preparing control files       - 40%
    - Copying files to cluster      - 60%
    - Submitting to queue           - 80%
    - Done                          - 100%

Important Note:
    - Depending on cluster "<" control character on command line might not be recognized
     (see _createRunScript() method) in this case try to use "-inp".
    - Dynmat task IS NOT a parallel program (no mpirun)
    - Both "<" and "-inp" work on foxtrot.danse.us
"""

class JobDriver(base):

    class Inventory(base.Inventory):
        id          = pyre.inventory.str('id', default='')      # Simulation Id
        taskid      = pyre.inventory.str('taskid', default='')
        subtype     = pyre.inventory.str('subtype', default='')
        
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session',])
        idd.meta['tip'] = "access to the token server"

        clerk = pyre.inventory.facility(name="clerk", factory=vnfb.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnfb.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'


    def main(self):
        "Main method"
        self.submitJob()


    def submitJob(self):
        """
        Submit simulation job
        The process of submission of simulation includes the following steps:
        1. Store configuration inputs to local disk storage
        2. Copy files to the computational cluster
        3. Submit Job
        """

        self._createJob()
        self._storeFiles()
        self._moveFiles()
        self._scheduleJob()
        self._updateStatus("submitted")


    def _createJob(self):
        "Create Job"
        self._sim   = self.clerk.getQESimulations(id = self.id)     # Should exist
        settings    = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)   # Should exist
        setting     = settings[0]
        params  = {"taskid":        self.taskid,
                   "serverid":      self._sim.serverid,
                   "status":        "Submitting",    # Fixed status
                   "timesubmitted": stamp(),
                   "creator":       self.sentry.username,
                   "numberprocessors":   setting.numproc, # -> take from QESettings
                   "description":   self.subtype
                   }

        self._job  = QEJob(self)
        self._job.createRecord(params)
        
        self._updateStatus("create-job")


    def _storeFiles(self):
        """TEMP SOLUTION: Stores files from configuration input strings """
        self._storeConfigurations()
        self._createRunScript()


    def _storeConfigurations(self):
        "Store Configuration files"
        inputs  = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
        dds     = self.dds

        if len(inputs) > 0:
            input   = inputs[0]     # Take the first input record

            fn          = defaultInputName(input.type)
            pfn         = packname(input.id, fn)        # E.g. 44XXJJG2pw.in
                        
            # Read text and store it in different location.
            # Not very efficient but will work for file of size < 1Mb

            text        = readRecordFile(dds, input, fn)            
            writeRecordFile(dds, self._job, pfn, text)   # -> qejobs directory
            dds.remember(self._job, pfn)     # Change object and filename?
            self._files.append(pfn)

        self._updateStatus("prepare-configs")


    def _createRunScript(self):
        server  = self.clerk.getServers(id = self._job.serverid)
        args    = self._commandArgs()
        
        # QE temp simulation directory is qesimulations/[simid] directory
        # E.g.: /home/dexity/espresso/qesimulations/3YEQ8PNV    -> no trailing slash
        qetempdir  = self.dds.abspath(self._sim, server=server)
        cmds    = [ "#!/bin/env bash",   # Suppose there is bash available
                    "export ESPRESSO_TMPDIR=%s/" % qetempdir,
                    " ".join(args)
        ]

        dds     = self.dds
        writeRecordFile(dds, self._job, RUNSCRIPT, "\n".join(cmds))    # -> qejobs directory
        dds.remember(self._job, RUNSCRIPT)  # Important step during which the .__dds_nodelist* files are created
        self._files.append(RUNSCRIPT)

        self._updateStatus("prepare-controls")


    def _commandArgs(self):
        "Returns list of command arguments (will be later on concatenated)"
        task        = self.clerk.getQETasks(id = self.taskid)
        settingslist = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)       # not None
        settings    = settingslist[0]
        inputs      = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
        input       = inputs[0]

        fn          = defaultInputName(input.type)
        inputFile   = packname(input.id, fn)        # E.g. 44XXJJG2pw.in
        outputFile  = inputFile + ".out"

        # No "mpirun" for single core simulations
        if input.type in NOPARALLEL:      
            args    = [ TYPE[task.type],
                        "<",
                        inputFile,
                        ">",
                        outputFile
                        ]
            return args

        # Example: mpirun --mca btl openib,sm,self pw.x -npool 8 -inp  PW > PW.out
        args   = [ settings.executable,
                    settings.params,
                    TYPE[task.type],
                    "-npool %s" % self._npool(settings, task.type),
                    "-inp",        # Options: "-inp" or "<"
                    inputFile,
                    ">",
                    outputFile
                    ]

        return args


    def _npool(self, settings, type):
        "Returns npool"
        # suppose settings is not None
        return settings.npool


    def _moveFiles(self):
        """
        Moves files from local server to the computational cluster.
        Files that need to be moved:
            - Configuration inputs
            - Simulation Settings
            - run.sh script (generate it first)
        Notes:
            - See also: submitjob.odb
        """
        dds     = self.dds
        server  = self.clerk.getServers(id = self._job.serverid)
        dds.make_available(self._job, server=server, files=self._files)

        # Create output directory (ESPRESSO_TEMPDIR) for QE
        dds.makedirs(self._sim, server=server)
        self._updateStatus("copy-files")
        

    def _test_makedirs(self):
        dds         = self.dds
        self._sim   = self.clerk.getQESimulations(id = self.id)
        server      = self.clerk.getServers(id = self._sim.serverid)
        dds.makedirs(self._sim, server=server)


    def _scheduleJob(self):
        "Schedule job"
        dds     = self.dds
        from vnfb.qeutils.qescheduler import schedule
        schedule(self._sim, self, self._job)
        self._updateStatus("enqueue")


    def _updateStatus(self, status):
        "Update job status"
        self._job.updateRecord({"status": status})


    def __init__(self):
        super(JobDriver, self).__init__( 'jobdriver')


    def _configure(self):
        super(JobDriver, self)._configure()
        self.id         = self.inventory.id
        self.taskid     = self.inventory.taskid
        self.subtype    = self.inventory.subtype

        self.idd        = self.inventory.idd
        self.clerk      = self.inventory.clerk
        self.dds        = self.inventory.dds
        self.csaccessor = self.inventory.csaccessor
        self.clerk.director     = self
        self.dds.director       = self
        


    def _init(self):
        super(JobDriver, self)._init()
        self._files = []

__date__ = "$Mar 3, 2010 11:04:10 PM$"


