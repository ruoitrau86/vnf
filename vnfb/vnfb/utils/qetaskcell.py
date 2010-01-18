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

import os
import luban.content as lc
from luban.content import load

from vnfb.utils.qeresults import QEResults
from vnfb.utils.qegrid import QEGrid
from vnfb.utils.qeinput import QEInput
from vnfb.utils.qetaskinfo import TaskInfo
from vnfb.utils.qeutils import latestJob

class QETaskCell:

    def __init__(self, director, type, colnum, simid, task):
        self._type      = type
        self._simid     = simid
        self._task      = task
        self._colnum    = colnum
        self._job       = None
        self._director  = director


    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text="Step %s: %s" % (self._colnum+1 , self._type), Class="text-bold")
        link    = lc.paragraph(text="")     # Task cannot be changed at this time
        #link    = lc.link(label="Change")  # Keep

        table   = QEGrid(lc.grid(Class="qe-grid"))
        table.addRow((type, link), (None, "qe-task-header-change"))

        return table.grid()


    def taskInfo(self):
        table   = QEGrid(lc.grid(Class="qe-tasks-info"))
        if self._task:
            self._taskId(table)
            self._input(table)
            self._output(table)
            self._status(table)
            self._jobId(table)
            self._results(table)

            table.setColumnStyle(0, "qe-tasks-param")
            table.setColumnStyle(1, "qe-tasks-value")

            table.setCellStyle(3, 1, "text-green")

            #table.addRow(("Jobs:", self._jobs()))  # Keep
        else:
            # May be it would be better to just replace content with task info?
            link    = lc.link(label="Create New Task",
                              onclick = load(actor      = 'material_simulations/espresso/task-create',
                                             routine    = 'createRecord',
                                             simid      = self._simid,
                                             tasktype   = self._type)
                             )

            table.addRow((link, ))
            #table.addRow(("or", ))                 # Keep
            #table.addRow(("Use Existing Task", ))  # Keep

        return table.grid()


    def action(self):
        "Displays simulation task action button: 'Run Task', 'Cancel'"
        link    = ""
        if self._task:
            link = lc.link(label="Run Task",
                           Class="qe-run-task",
                           onclick = load(actor     ='jobs/submit',    # 'jobs/checksubmit'
                                          routine   = 'submit',        # 'checkSubmit'
                                          id        = self._simid,
                                          taskid    = self._task.id)
                            )

        return link


    def _taskId(self, table):
        tid     = self._task.id
        link    = lc.link(label    = tid,
                           onclick  = load(actor    = 'material_simulations/espresso/task-view',
                                           id       = self._simid,
                                           taskid   = tid,
                                           type     = self._type)
                            )

        table.addRow(("Task:", link, ""))


    def _input(self, table):
        # Suppose that self._task is not None
        qeinput = QEInput(self._director, self._simid, self._task.id, self._type)
        table.addRow(("Input:", qeinput.getLink(), ""))


    def _output(self, table):
        action  = lc.link(label="Refresh",
                          Class     = "qe-task-action"
                          #onclick   = load()
                         )
        table.addRow(("Output:", "None", action))


    def _status(self, table):
        "Displays status of the simulation"
        link    = "Not Started"
        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            job  = latestJob(jobs)
            link = job.status

        table.addRow(("Status:", link, ""))


    def _jobId(self, table):
        "Displays id of the current job"
        link        = "None"
        action      = ""
        jobs        = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            self._job  = latestJob(jobs)
            link = lc.link(label=self._job.id,
                               onclick = load(actor     = 'jobs/jobs-view',
                                              id        = self._simid,
                                              taskid    = self._task.id,
                                              jobid     = self._job.id,
                                              type      = self._type)
                                )
            action = lc.link(label    = "All",
                              Class    = "qe-task-action",
                               onclick = load(actor     = 'jobs/jobs-view-all',
                                              id        = self._simid,
                                              taskid    = self._task.id,
                                              type      = self._type)
                                )

        table.addRow(("Job:", link, action))


#    def _latest(self, jobs):
#        "Retruns latest job based on timesubmitted column"
#        # jobs have at least one element
#        latest  = jobs[0]
#
#        for job in jobs:
#            if job.timesubmitted == "":
#                continue
#
#            if latest.timesubmitted == "":
#                latest = job
#
#            if float(job.timesubmitted) > float(latest.timesubmitted):
#                latest  = job
#
#        return latest

    def _results(self, table):
        "Returns link to tar file for download. "
        taskinfo    = TaskInfo(self._simid, self._task.id, self._type)
        results     = QEResults(self._director, self._job, taskinfo)
        container   = results.link()
        action      = results.action()
        
        table.addRow(("Results: ", container, action))


__date__ = "$Dec 12, 2009 3:21:13 PM$"


