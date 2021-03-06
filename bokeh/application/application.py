'''

'''
from __future__ import absolute_import

import logging
log = logging.getLogger(__name__)

from ..document import Document

class Application(object):
    ''' An Application is a factory for Document instances.

    '''

    def __init__(self, *handlers):
        self._handlers = list(handlers)

    # TODO (havocp) should this potentially create multiple documents?
    # or does multiple docs mean multiple Application?
    def create_document(self):
        ''' Loads a new document using the Application's handlers to fill it in. '''
        doc = Document()
        for h in self._handlers:
            # TODO (havocp) we need to check the 'failed' flag on each handler
            # and build a composite error display.
            h.modify_document(doc)
            if h.failed:
                log.error("Error running application handler %r: %s %s ", h, h.error, h.error_detail)

        # A future server setting could make it configurable whether to do this,
        # since it has some performance impact probably. Let's see if we need to.
        doc.validate()

        return doc

    def add(self, handler):
        ''' Add a handler to the pipeline used to initialize new documents.

        Args:
            handler (Handler) : a handler to process this Application

        '''
        self._handlers.append(handler)

    @property
    def handlers(self):
        return tuple(self._handlers)
