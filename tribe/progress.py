# tribe.progress
# Provides a progress indicator and an elapsed time on the console.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jun 22 18:34:02 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: progress.py [43fd3e1] benjamin@bengfort.com $

"""
Provides a progress indicator and an elapsed time on the console.
"""

##########################################################################
## Imports
##########################################################################

import sys
import time
import threading

from tribe.utils import humanizedelta

##########################################################################
## Progress Inidicator
##########################################################################

class Progress(object):

    def __init__(self, stream=sys.stdout):
        self.count   = 0
        self.stream  = stream
        self.start   = time.time()
        self._clear  = 0
        self.pprint()

    @property
    def elapsed(self):
        """
        Returns the humanized version of the elapsed time.
        """
        return humanizedelta(seconds=time.time() - self.start)

    def update(self, flush=True):
        """
        Call on each iteration of the loop you're tracking.
        """
        self.count += 1
        if flush: self.pprint()

    def stop(self):
        """
        Call when you're finished tracking progress.
        """
        self.stream.write("\n")
        self.stream.flush()

    def pprint(self):
        """
        Writes the progress indication to the console.
        """
        if self.count > 0:
            status = "Parsed: {} emails".format(self.count)
        else:
            status = "initializing ..."

        # Clear the screen from the last message
        self.stream.write(" " * self._clear + "\r")

        # Compute the message and the clear length
        message = "Elapsed: {} | {}".format(self.elapsed, status)
        self._clear = len(message)

        # Write and flush to the stream
        self.stream.write(message + "\r")
        self.stream.flush()


class AsyncProgress(Progress):
    """
    Progress indicator where console is flushed at an interval rather than
    when update is called (e.g. synchronously). Useful for computationally
    heavy or time bound processing on each interation.
    """

    def __init__(self, stream=sys.stdout, interval=0.5):
        super(AsyncProgress, self).__init__(stream)
        self.interval = interval
        self.background()

    def background(self):
        """
        Sets a background timer thread that calls pprint() on an interval.
        """

        def background_update(progress):
            """
            Calls pprint and then resets the background timer.
            """
            progress.pprint()
            progress.background()

        self.timer = threading.Timer(self.interval, lambda: background_update(self))
        self.timer.start()

    def update(self):
        """
        Update now does not flush, the background timer does that.
        """
        super(AsyncProgress, self).update(flush=False)

    def stop(self):
        """
        Also cancels the timer.
        """
        if hasattr(self, 'timer'):
            self.timer.cancel()
        super(AsyncProgress, self).stop()

if __name__ == '__main__':

    p = AsyncProgress()
    for _ in range(100):
        time.sleep(.1)
        p.update()

    p.stop()
