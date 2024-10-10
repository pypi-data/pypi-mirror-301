#  Copyright 2017 Carlos Pascual-Izarra <cpascual@users.sourceforge.net>
#
#  This file is part of colorevo.
#
#  PeakEvo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PeakEvo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with colorevo. If not, see <http://www.gnu.org/licenses/>.


import cv2
import time
from .h5writer import H5Writer


class DummyWriter:
    """
    Dummy writer that does not write anything
    """

    def start(self, *args, **kwargs):
        pass

    def write_frame(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass


class AcqLoop:
    """
    Acquisition loop that captures images with opencv,
    saves them into an h5file file and makes them available
    as a shared numpy mem map
    """

    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.data = None
        self._acquiring = False
        self.t_offset = None
        self.period = None
        self.writer = DummyWriter()
        self.reset(None)

    def reset(self, outfile, max_fps=None):
        # stop writing
        self.writer.end()
        self.writer = DummyWriter()

        if max_fps is None:
            self.period = None
        else:
            self.period = 1.0 / max_fps

        # capture one frame to initialize the writer
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("problem capturing from source")

        # store the absolute start time
        self.t_offset = time.time()
        self.data = frame, 0
        if outfile is not None:
            self.writer = H5Writer(outfile, frame.shape, frame.dtype)
            self.writer.start()

    def run(self):
        self._acquiring = True
        while self._acquiring:
            t0 = time.time()
            _, frame = self.cap.read()
            t = time.time() - self.t_offset
            self.data = frame, t
            self.writer.write_frame(frame, t)
            # print('saved', t, self.writer)
            if self.period is not None:
                rest = self.period - (time.time() - t0)
                if rest >= 0:
                    time.sleep(rest)
                else:
                    print(
                        "Cannot reach {}fps. Achieved:{:.0f}fps".format(
                            1 / self.period, 1 / (self.period - rest)
                        )
                    )

    def stop(self):
        self._acquiring = False
        self.writer.end()


if __name__ == "__main__":
    import os
    import sys
    import tempfile
    import threading
    from PyQt6.QtCore import QTimer, QCoreApplication

    class Reader:
        def __init__(self):
            super(Reader, self).__init__()

            self.timer = QTimer()
            self.acq_loop = None
            self.timer.timeout.connect(self.process)
            self._last_processed = -1

        def start(self):
            # create the acq loop
            ofile = os.path.join(tempfile.gettempdir(), "kkcap.h5")
            self.acq_loop = AcqLoop(0, ofile)

            # create the acq thread and start it
            self.thread = threading.Thread(target=self.acq_loop.run, daemon=True)
            self.thread.start()
            self.timer.start(200)

        def process(self):
            try:
                fr, t = self.acq_loop.data
            except Exception:
                return
            if t <= self._last_processed:
                print("no new data. skipping")
                return
            self._last_processed = t
            print("processing... ", self._last_processed, fr.shape, fr.mean())

            if self._last_processed > 3:
                self.stop()

            time.sleep(0.5)

        def stop(self):
            print("STOPPING")
            self.acq_loop.stop()
            self.timer.stop()

    app = QCoreApplication(sys.argv)

    r = Reader()
    r.start()

    sys.exit(app.exec())
