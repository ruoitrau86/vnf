# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# this is the factory for visuals related to computation results


from luban.content import load, select, alert
import luban.content as lc



class Factory(object):

    def __init__(
        self, 
        computation=None, actor=None, director=None,
        on_all_results_retrieved = None
        ):
        self.computation = computation
        self.actor = actor
        self.director = director
        self.on_all_results_retrieved = on_all_results_retrieved
        return


    def create(self):
        #
        computation = self.computation
        actor = self.actor
        director = self.director
        on_all_results_retrieved = self.on_all_results_retrieved
        
        # utilities
        domaccess = director.retrieveDOMAccessor('computation')
        orm = domaccess.orm
        db = orm.db
    
        # 
        id = computation.id
        type = computation.getTableName()

        # the job
        job = computation.getJob(db)
        # always good to check the job
        from vnf.utils.job import check
        check(job, director)

        # the document to build
        doc = lc.document(Class='container', id='computation-results-container')

        # depending on retrieval status, we need to add some extra things to the document
        result_retrieval_status = computation.getResultRetrievalStatus(db)

        if result_retrieval_status is None:
            from vnf.utils.computation import start_results_retrieval
            start_results_retrieval(computation, director)
            result_retrieval_status = 'retrieving'

        refresh = select(element=doc).replaceBy(
            load(actor='loadvisual', visual='computation-results',
                 id=id, type=type,
                 on_all_results_retrieved = on_all_results_retrieved,
                 )
            )

        if result_retrieval_status == 'retrieving':
            p = doc.paragraph(text=['Still retrieving results...'])

            from vnf.utils.computation import get_results_retrieval_task
            task = get_results_retrieval_task(computation, db)
            if not task:
                raise RuntimeError, 'there should be an itask working at retrieving '+\
            'results for computation %s, but we found none' % computation.id

            pbar = lc.progressbar(
                id = 'itask-%s-pbar' % task.id,
                status = 'Retrieving results...',
                percentage = 0,
                skip = 1000,
                )
            pbar.onchecking = load(
                actor='itask',
                routine='checkProgress',
                id = task.id,
                )
            if on_all_results_retrieved:
                from vnf.content import safe_eval_action
                onfinished = safe_eval_action(on_all_results_retrieved)
            else:
                onfinished = refresh
            pbar.onfinished = onfinished
            pbar.oncanceled = refresh
            doc.add(pbar)

        elif result_retrieval_status.find('failed') != -1:
            p = doc.paragraph(text=['failed to retrieve results'])
            # the action to load this visual (type: string)
            refresh_action_in_str = 'select(id="computation-results-container").replaceBy(load(actor="loadvisual", visual="computation-results", id="%s", type="%s", on_all_results_retrieved = "%s"))' % (id, type, on_all_results_retrieved or '')
            # link to restart retrieval
            l = lc.link(
                label = 'restart results retrieval',
                onclick = [
                  load(actor='computation', routine='restartResultsRetrieval',
                       type = type, id = id,
                       posterior_action = refresh_action_in_str,
                       )
                  ],
                )
            doc.add(l)

        elif result_retrieval_status == 'retrieved':

            pass

        else:
            raise NotImplementedError, 'computation: %s, retrieval status: %s' % (
                type, result_retrieval_status)

        # display results 
        results = computation.results.dereference(db)
        for k, r in results:
    ##         alertdoc = doc.paragraph(
    ##             text=['loading computation result %s %s. please wait...' % (
    ##             r.getTableName(), r.id)]
    ##             )
            title = '%s %s: expand for details' % (r.__class__.__name__, r.id)
            doc1 = doc.document(
                id = 'resultdoc-%s' % r.id,
                Class='container', title=title, collapsable=True, collapsed=True)
            doc1.onexpand = [
                #select(element=alertdoc).hide(),
                select(element=doc1).replaceBy(
                load(actor='orm/%s' % r.getTableName(),
                     routine='createGraphicalView',
                     id = r.id)
                )
                ]
            continue

        return doc


# version
__id__ = "$Id$"

# End of file 
