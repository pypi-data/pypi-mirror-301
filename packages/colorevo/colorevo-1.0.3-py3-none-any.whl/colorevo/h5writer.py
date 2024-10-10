#  Copyright 2019 Carlos Pascual-Izarra <cpascual@users.sourceforge.net>
#
#  This file is part of colorevo.
#
#  colorevo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  colorevo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.


from datetime import datetime
import h5py


class H5Writer:
    """
    Saves frames and time to a hdf5 file file.
    Shamelessly adapted (simplified) from sardana.macroserver.recorders.h5storage
    (https://github.com/sardana-org/sardana )
    """

    def __init__(self, filename, frame_shape, frame_dtype):
        self.fd = fd = h5py.File(filename, mode="w")
        self._write_enabled = False

        fd.attrs["creator"] = f"colorevo's {self.__class__.__name__}"
        fd.attrs["HDF5_Version"] = h5py.version.hdf5_version
        fd.attrs["h5py_version"] = h5py.version.version

        self._frames = fd.create_dataset(
            "frames",
            dtype=frame_dtype,
            shape=([0] + list(frame_shape)),
            maxshape=([None] + list(frame_shape)),
            chunks=(1,) + tuple(frame_shape),
            compression="gzip",
        )

        self._times = fd.create_dataset(
            "times", dtype="float", shape=(0,), maxshape=(None,)
        )

        self._fr_count = 0

        fd.flush()

    def start(self):
        self.fd.attrs["start_time"] = datetime.now().isoformat()
        self._write_enabled = True

    def write_frame(self, frame, fr_time):
        if not self._write_enabled:
            return
        self._fr_count += 1
        self._frames.resize(self._fr_count, axis=0)
        self._times.resize(self._fr_count, axis=0)

        self._frames[self._fr_count - 1, ...] = frame
        self._times[self._fr_count - 1, ...] = fr_time

        self.fd.flush()

    def end(self):
        self.fd.attrs["end_time"] = datetime.now().isoformat()
        self._write_enabled = False
        self.fd.close()


if __name__ == "__main__":
    import os
    import tempfile
    import numpy
    import time

    sh = (4, 5)
    dt = "int8"

    fname = os.path.join(tempfile.gettempdir(), "kk.h5")
    w = H5Writer(fname, sh, dt)

    w.start()

    for i in range(9):
        f = numpy.random.randint(0, 100, sh)
        t = time.time()
        # print(f,t)
        w.write_frame(f, t)

    w.end()

    print(f"//////////// {fname} /////////////")

    def pp(name):
        e = f[name]
        print(e)
        print(f"{name}.attrs: {list(e.attrs)}")

    f = h5py.File(fname)
    print(f, list(f.attrs))
    f.visit(pp)
