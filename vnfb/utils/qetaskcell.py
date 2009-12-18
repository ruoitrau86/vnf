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

import luban.content as lc
from luban.content import load
from luban.content.Document import Document

from vnfb.utils.qegrid import QEGrid
from vnfb.utils.qeinput import QEInput

class QETaskCell:

    def __init__(self, director, type, simid, task):
        self._type  = type
        self._simid = simid
        self._task  = task
        self._director  = director


    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text=self._type, Class="text-bold")
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
            self._job(table)
            self._results(table)

            table.setColumnStyle(0, "qe-tasks-param")
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

        table.addRow(("Task:", link))


    def _input(self, table):
        # Suppose that self._task is not None
        qeinput = QEInput(self._director, self._simid, self._task.id, self._type)
        table.addRow(("Input:", qeinput.getLink()))


    def _output(self, table):
        table.addRow(("Output:", "None"))


    def _status(self, table):
        "Displays status of the simulation"
        link    = "Not Started"
        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            job  = jobs[0]
            link = job.status

        table.addRow(("Status:", link))


    def _job(self, table):
        "Displays id of the current job"
        self._job   = None
        link        = "None"
        jobs        = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            self._job  = jobs[0]
            link = lc.link(label=self._job.id,
                           onclick = load(actor     ='jobs/jobs-view',
                                          id        = self._job.id)
                            )

        table.addRow(("Job:", link))

        
    def _results(self, table):
        "STUB: Returns link to tar file for download. "
        celldoc     = lc.document(Class="display-inline")
        cell        = lc.document(id="results-link")   # Container for tar link
        celldoc.add(cell)

        tarlink     = self._tarlink()
        #link    = self._retrieveResults(director)

        # Change actor
        check    = lc.link(label="Check", id="qe-check-results",
                       onclick=load(actor       = "jobs/getresults",
                                    routine     = "retrieveStatus",
                                    id          = self._simid,
                                    taskid      = self._task.id)    # No jobid at this time
                      )

        cell.add(tarlink)
        celldoc.add(check)

        table.addRow(("Results: ", celldoc))

    def _tarlink(self):
        link    = lc.paragraph(text="None")
        return link


__date__ = "$Dec 12, 2009 3:21:13 PM$"


