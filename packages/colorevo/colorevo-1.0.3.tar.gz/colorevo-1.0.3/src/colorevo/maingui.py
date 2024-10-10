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


import sys
import os
import re
import datetime
import logging
import threading
import numpy
import shutil
import click
import h5py
import json
from tempfile import gettempdir
from PyQt6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

from colorevo import __version__
from .configuration import BaseConfigurableClass
from .colors import bgr2hsv, bgr2rgb, hsv_generator
from .acq_cv2 import AcqLoop
from .h5writer import H5Writer

# Set logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Set interpretation of images as row-major (to avoid turned video)
pg.setConfigOptions(imageAxisOrder="row-major")


class ColorEvoMain(QtWidgets.QMainWindow, BaseConfigurableClass):
    itercolors = hsv_generator()
    _tmp_rec_file_name = os.path.join(gettempdir(), "colorevo_tmp_rec.h5")
    refresh_timer_period = 500  # ms
    workdir = os.path.join(os.path.dirname(__file__), os.path.pardir, "data")

    def __init__(self, parent=None, load_settings=True):
        super().__init__(parent=parent)
        self._qsettings = QtCore.QSettings()

        # initialize icon search path
        curdir = os.path.dirname(os.path.realpath(__file__))
        QtCore.QDir.addSearchPath("icons", os.path.join(curdir, "icons"))

        # timer for refreshing the plots in live operation
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.onRefresh)

        # initializations
        self.acq_loop = None
        self.acq_thread = None
        self._last_processed = -1
        self._h5file = None
        self._h5times = None

        self.imgPlot = pg.PlotWidget()
        self.evoPlot_h = pg.PlotWidget()
        self.evoPlot_s = pg.PlotWidget()
        self.evoPlot_v = pg.PlotWidget()
        self.toolBar = self.addToolBar("Toolbar")
        self.toolBar.setObjectName("mainTB")
        self.rois = []
        self.h_curves = []
        self.s_curves = []
        self.v_curves = []

        # allow dockwidgets to be placed anywhere
        self.setDockNestingEnabled(True)

        self._initImgPlot()
        self._initEvoPlots()
        self._initToolBar()
        self._initMenus()

        # register config properties
        self.registerConfigProperty(self.getCamera, self.setCamera, "camera")
        self.registerConfigProperty(self.getROIsConfig, self.restoreROIs, "ROIs")
        self.registerConfigProperty(self.fpsSB.value, self.fpsSB.setValue, "fps")
        self.registerConfigProperty(
            self._getTmpRecFile, self._setTmpRecFile, "tmp_rec_file"
        )

        # Load config settings
        if load_settings:
            self.loadSettings()

        # we are ready
        self.statusBar().showMessage("Started", 3000)

    def _initImgPlot(self):
        self.imgPlot.setAspectLocked(True)
        self.imgPlot.getPlotItem().getViewBox().invertY(True)

        # Add img itrm
        self.img = pg.ImageItem()
        self.imgPlot.addItem(self.img)

        # set up dockwidget
        dw = QtWidgets.QDockWidget("Image")
        dw.setObjectName("imageDW")
        dw.setWidget(self.imgPlot)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dw)
        self._imageDW = dw

    def _initEvoPlots(self):
        # configure plot
        self.evoPlot_h.setLabels(left=("hue",), bottom=("time (s)",))
        self.evoPlot_s.setLabels(left=("saturation",), bottom=("time (s)",))
        self.evoPlot_v.setLabels(left=("brightness",), bottom=("time (s)",))

        # add time selector (the time_selector_h acts as main and the other 2 as slaves)
        self.time_selector_h = pg.InfiniteLine(pos=0, angle=90, movable=True)
        self.time_selector_s = pg.InfiniteLine(pos=0, angle=90, movable=True)
        self.time_selector_v = pg.InfiniteLine(pos=0, angle=90, movable=True)
        self.time_selector_h.sigPositionChanged.connect(self.onMainTimeSelectorChanged)
        self.time_selector_s.sigPositionChanged.connect(self.onSlaveTimeSelectorChanged)
        self.time_selector_v.sigPositionChanged.connect(self.onSlaveTimeSelectorChanged)

        # set up dockwidgets
        dw = QtWidgets.QDockWidget("Hue Values")
        dw.setObjectName("huesDW")
        dw.setWidget(self.evoPlot_h)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dw)
        self._hueDW = dw

        dw = QtWidgets.QDockWidget("Saturation Values")
        dw.setObjectName("saturationDW")
        dw.setWidget(self.evoPlot_s)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dw)
        self._saturationDW = dw

        dw = QtWidgets.QDockWidget("Brightness Values")
        dw.setObjectName("brightnessDW")
        dw.setWidget(self.evoPlot_v)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dw)
        self._brightnessDW = dw

    def _initToolBar(self):
        # video file selector
        self.loadVideoAction = self.toolBar.addAction(
            QtGui.QIcon("icons:video-x-generic.svg"), "Open data source file"
        )
        self.loadVideoAction.setCheckable(True)
        self.loadVideoAction.toggled.connect(self.onLoadVideo)

        self.toolBar.addSeparator()
        # start/stop record button
        rec_icon = QtGui.QIcon()
        rec_icon.addPixmap(
            QtGui.QPixmap("icons:media-record.svg"),
            rec_icon.Mode.Normal,
            rec_icon.State.Off,
        )
        rec_icon.addPixmap(
            QtGui.QPixmap("icons:media-playback-stop.svg"),
            rec_icon.Mode.Normal,
            rec_icon.State.On,
        )
        self.recordAction = self.toolBar.addAction("Start/Stop recording")
        self.recordAction.setIcon(rec_icon)
        self.recordAction.setCheckable(True)
        self.recordAction.setChecked(False)
        self.recordAction.setEnabled(False)
        self.recordAction.toggled.connect(self.onRecordFromCameraActionToggled)

        # FPS spinbox
        self.fpsSB = sb = QtWidgets.QDoubleSpinBox()
        sb.setRange(0.1, 40)
        sb.setSuffix("fps")
        sb.setValue(24)
        sb.setSpecialValueText("stopped")
        sb.setToolTip("Maximum fps for file recording")
        self.toolBar.addWidget(sb)
        sb.valueChanged[float].connect(self.setAcqFps)

        self.toolBar.addSeparator()

        # Add rect ROI action
        self.addRectROIAction = self.toolBar.addAction(
            QtGui.QIcon("icons:draw-rectangle.svg"), "Add new rectangular ROI"
        )
        self.addRectROIAction.triggered.connect(self.addRectROI)

        # Add polyline ROI action
        self.addPolyLineROIAction = self.toolBar.addAction(
            QtGui.QIcon("icons:draw-polyline.svg"), "Add new polyline ROI"
        )
        self.addPolyLineROIAction.triggered.connect(self.addPolyLineROI)

        # Reset evoPlot action
        self.refreshEvoAction = self.toolBar.addAction(
            QtGui.QIcon("icons:view-refresh.svg"),
            "Recalculate color values (uncheck to abort)",
        )
        self.refreshEvoAction.setCheckable(True)
        self.refreshEvoAction.toggled.connect(self.refreshEvoPlot)

        # Clear all ROIs action
        self.removeAllRoisAction = self.toolBar.addAction(
            QtGui.QIcon("icons:edit-clear-history.svg"),
            "Remove all current ROIs",
        )
        self.removeAllRoisAction.triggered.connect(self.removeAllRois)

    def _initMenus(self):
        # File Menu
        file_menu = self.menuBar().addMenu("&File")

        # Save all ROIs action
        self.saveAllRoisAction = file_menu.addAction(
            QtGui.QIcon("icons:document-save-as-template.svg"),
            "Save current ROIs configuration to a file",
        )
        self.saveAllRoisAction.triggered.connect(self.onSaveAllRoisAction)

        # Restore ROIs action
        self.restoreRoisAction = file_menu.addAction(
            QtGui.QIcon("icons:document-new-from-template.svg"),
            "Restore ROI from a file",
        )
        self.restoreRoisAction.triggered.connect(self.onRestoreRoisAction)

        file_menu.addSeparator()

        # Other settings action
        self.setTmpRecDirAction = file_menu.addAction("Set temporary data file name...")
        self.setTmpRecDirAction.triggered.connect(self._setTmpRecFile)

        # Camera menu
        camera_menu = self.menuBar().addMenu("&Camera")
        self._cameraActions = QtGui.QActionGroup(self)

        camera_names = ["Disabled"]

        # add openCV cameras
        camera_names += [f"CV{id}" for id in range(8)]

        # create all camera actions
        for name in camera_names:
            a = self._cameraActions.addAction(name)
            a.setCheckable(True)

        # check the "Disabled" action by default
        self._cameraActions.actions()[0].setChecked(True)

        camera_menu.addActions(self._cameraActions.actions())

        self._cameraActions.triggered.connect(self.onCameraChanged)

        # View menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self._imageDW.toggleViewAction())
        view_menu.addAction(self._hueDW.toggleViewAction())
        view_menu.addAction(self._saturationDW.toggleViewAction())
        view_menu.addAction(self._brightnessDW.toggleViewAction())
        view_menu.addAction(self.toolBar.toggleViewAction())

    def onLoadVideo(self, checked):
        if not checked:
            return

        FRAMES_FLT = "Frames files (*.h5 *.hdf *hdf5)"
        VIDEOS_FLT = "Videos (*.avi *.mp4 *.mpeg *.mpg *.mov *.wmv)"
        OTHERS_FLT = "Other (*)"

        fname, flt = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory=self.workdir,
            filter=";;".join((FRAMES_FLT, VIDEOS_FLT, OTHERS_FLT)),
        )
        if not fname:
            logging.info("No data/video selected.")
            self.loadVideoAction.setChecked(False)
            return

        self.setCamera("Disabled")
        if self._h5file is not None:
            self._h5file.close()

        if flt == FRAMES_FLT:
            if self._h5file is not None:
                self._h5file.close()

            self.loadH5Frames(fname)

        elif flt in (VIDEOS_FLT, OTHERS_FLT):
            self.loadCVVideo(fname)

        # uncheck the loadVideo action
        self.loadVideoAction.setChecked(False)

    def loadH5Frames(self, fname):
        """Open h5 and load times and frames"""
        if self._h5file is not None:
            self._h5file.close()
        self._h5file = h5py.File(fname)
        self._h5times = self._h5file["times"][()]  # read it all to memory
        t0 = self._h5times[0]
        tf = self._h5times[-1]
        self.evoPlot_h.setXRange(t0, tf)
        self.evoPlot_s.setXRange(t0, tf)
        self.evoPlot_v.setXRange(t0, tf)
        # show time selectors (moving time_selector_h moves the other ones too)
        self.time_selector_h.setPos(t0)  # also updates the img (connected)
        self.time_selector_h.setBounds((t0, tf))
        self.time_selector_s.setBounds((t0, tf))
        self.time_selector_v.setBounds((t0, tf))
        self.evoPlot_h.addItem(self.time_selector_h)
        self.evoPlot_s.addItem(self.time_selector_s)
        self.evoPlot_v.addItem(self.time_selector_v)

    def loadCVVideo(self, fname):
        """
        Extract frames from a video file and write them in a h5file.
        Then open the h5file.
        """
        try:
            import cv2

            cap = cv2.VideoCapture(fname)
            if not cap.isOpened():
                raise IOError("CV capture failed to open file")
        except Exception as e:
            logging.error(f"Problem opening {fname}. Reason: {e}")
            return

        h5fname, flt = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption=f"Save frames from {os.path.basename(fname)}",
            directory=os.path.splitext(fname)[0] + ".h5",
            filter="HDF5 (*.h5)",
        )
        if not h5fname:
            return

        # capture one frame to initialize the writer
        ok, frame = cap.read()
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if not ok:
            logging.error(f"problem capturing from {fname}")

        app = QtWidgets.QApplication.instance()
        writer = H5Writer(h5fname, frame.shape, frame.dtype)
        writer.start()
        msg = "Extracting frames..."
        nframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while ok:
            if not self.loadVideoAction.isChecked():
                self.statusBar().showMessage(msg + "Aborted", 3000)
                break  # abort processing if refresh button is unchecked
            writer.write_frame(frame, t)
            ok, frame = cap.read()
            t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            i = cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.statusBar().showMessage(msg + f"({i}/{nframes})", 3000)
            app.processEvents()
        writer.end()

        # now simply open the h5file
        self.loadH5Frames(h5fname)

    def onCameraChanged(self):
        self.setCamera(self.getCamera())

    def getCamera(self):
        action = self._cameraActions.checkedAction()
        if action is None:
            return None
        return action.text()

    def setCamera(self, camera):
        # make sure the corresponding action is checked
        for c in self._cameraActions.actions():
            if c.text() == camera:
                if not c.isChecked():
                    c.setChecked(True)
                break
        else:
            # if we land here, it means camera is not known
            logging.warning(f"Unknown camera '{camera}'")
            return

        cv = re.fullmatch(r"CV([0-9]+)", camera)

        # stop recording
        self.recordAction.setChecked(False)

        # stop current AcqLoop
        if self.acq_loop is not None:
            self.acq_loop.stop()
            self.acq_thread.join()
            self.acq_loop.cap.release()
        self.recordAction.setEnabled(False)

        if camera == "Disabled":
            logging.info("Camera disabled")
            self.refresh_timer.stop()
            self.resetPlots()
            return
        elif cv:
            src = int(cv.groups()[0])
            try:
                self.acq_loop = AcqLoop(src)
            except Exception as e:
                logging.warning(f"Problem acquiring with {camera}: {e}")
                return
            self.recordAction.setEnabled(True)
        else:
            logging.warning(f'Unsupported source of video "{camera}"')
            return

        # remove time selectors
        self.evoPlot_h.removeItem(self.time_selector_h)
        self.evoPlot_s.removeItem(self.time_selector_s)
        self.evoPlot_v.removeItem(self.time_selector_v)

        # close and forget h5file if it was open
        if self._h5file is not None:
            self._h5file.close()
        self._h5file = None
        self._h5times = None

        # start acq loop (in new thread)
        self.acq_thread = threading.Thread(
            target=self.acq_loop.run, name="acq", daemon=True
        )
        self.acq_thread.start()

        # start refreshing the plots
        self.refresh_timer.start(self.refresh_timer_period)

    def onRecordFromCameraActionToggled(self, toggled):
        if toggled:
            # reset the acq loop with the tmp file
            self.acq_loop.reset(self._tmp_rec_file_name, self.fpsSB.value())
            self._last_processed = -1
            self.resetPlots()
        else:
            # reset the acq loop with the tmp file
            self.acq_loop.reset(None)
            self._last_processed = -1
            self.resetPlots()

            now = datetime.datetime.now()
            size = os.path.getsize(self._tmp_rec_file_name) // 1_048_576  # in Mb
            msg = f"{self._tmp_rec_file_name}: {size}Mb"
            self.statusBar().showMessage(msg)
            while True:  # loop until data is saved or discard is forced
                # offer to save data
                fname, flt = QtWidgets.QFileDialog.getSaveFileName(
                    parent=self,
                    caption=f"Save recorded data ({size}Mb)",
                    directory=os.path.join(
                        self.workdir, f"colorevo_{now:%Y%m%d-%H%M%S}.h5"
                    ),
                    filter="HDF5 (*.h5)",
                )
                if fname:
                    try:
                        shutil.move(self._tmp_rec_file_name, fname)
                        msg = f"{size}Mb saved in {fname}"
                        self.statusBar().showMessage(msg)
                        break
                    except Exception as e:
                        logging.warning("Problem saving data: %r", e)

                # Data wasn't saved. Ask for confirmation about discarding
                btn = QtWidgets.QMessageBox.warning(
                    self,
                    "Discard last data?",
                    (
                        "Are you sure that you want to discard the "
                        + f"{size}Mb of data just recorded?\n"
                    ),
                    buttons=(
                        QtWidgets.QMessageBox.StandardButton.Save
                        | QtWidgets.QMessageBox.StandardButton.Discard
                    ),
                )
                if btn == QtWidgets.QMessageBox.StandardButton.Discard:
                    msg = f"Data in {self._tmp_rec_file_name} *not* saved"
                    self.statusBar().showMessage(msg)
                    break

    def addROI(self, classname, state=None, color=None):
        """Afactory of slightly customized ROIs"""

        if color is None:
            color = self.getNewColor()
        pen = pg.mkPen(color=color)

        if classname == "RectROI":
            if state is None:
                state = {"pos": [10, 10], "size": [200, 200], "angle": 0}
            roi = pg.RectROI(pos=[10, 10], size=[200, 200], pen=pen, removable=True)
            roi.addRotateHandle([1, 0], [0.5, 0.5])
        elif classname == "PolyLineROI":
            roi = pg.PolyLineROI(
                positions=[[0, 0], [100, 0], [0, 100]],
                closed=True,
                pen=pen,
                removable=True,
            )
        else:
            raise ValueError("Unsupported classname ({classname})")

        # connect the remove signal
        roi.sigRemoveRequested.connect(self.onROIRemoveRequested)
        # add the roi to the plot
        self.imgPlot.addItem(roi)
        # restore state if given
        if state is not None:
            roi.setState(state)
        # make sure the ROI is drawn on top
        roi.setZValue(10 + len(self.rois))
        # add it to the current rois list
        self.rois.append(roi)
        # also create the associated evo curves
        self.addEvoCurves(roi.pen)

    def addRectROI(self):
        state = None
        for previous in reversed(self.rois):
            if isinstance(previous, pg.RectROI):
                state = previous.saveState()
                break
        self.addROI("RectROI", state=state)

    def addPolyLineROI(self):
        state = None
        for previous in reversed(self.rois):
            if isinstance(previous, pg.PolyLineROI):
                state = previous.saveState()
                break
        self.addROI("PolyLineROI", state=state)

    def getNewColor(self):
        """
        Return a new QColor ensuring that it is not already used by any roi
        """
        existing_colors = [r.pen.color().getRgb() for r in self.rois]
        color = QtGui.QColor.fromHsvF(*next(self.itercolors))
        while color.getRgb() in existing_colors:
            color = QtGui.QColor.fromHsvF(*next(self.itercolors))
        return color

    def onROIRemoveRequested(self):
        roi = self.sender()
        idx = self.rois.index(roi)
        self.removeROI(idx)

    def removeROI(self, idx=-1):
        roi = self.rois.pop(idx)
        self.imgPlot.removeItem(roi)
        h_curve = self.h_curves.pop(idx)
        self.evoPlot_h.removeItem(h_curve)
        s_curve = self.s_curves.pop(idx)
        self.evoPlot_s.removeItem(s_curve)
        v_curve = self.v_curves.pop(idx)
        self.evoPlot_v.removeItem(v_curve)

    def removeAllRois(self):
        """remove all existing rois"""
        for _ in range(len(self.rois)):
            self.removeROI(-1)
        # restart the color generator
        self.itercolors = hsv_generator()

    def getROIsConfig(self):
        ret = []
        for roi in self.rois:
            cname = roi.__class__.__name__
            state = roi.saveState()
            color = roi.pen.color().getRgb()
            ret.append((cname, state, color))
        return ret

    def onSaveAllRoisAction(self):
        cfg = self.getROIsConfig()

        fname, flt = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption=f"Save {len(cfg)} ROIs",
            directory=self.workdir,
            filter="ROI template (*.roi)",
        )
        if fname:
            # add extension if it was not set
            if not fname.endswith(".roi"):
                fname += ".roi"
            with open(fname, "w") as f:
                json.dump(cfg, f)

    def restoreROIs(self, config):
        """
        Restore the ROIs defined in config. Config can be generated by
        `getROIsConfig()`
        """
        self.removeAllRois()

        # create new rois from config
        for c in config:
            self.addROI(*c)

    def onRestoreRoisAction(self):
        fname, flt = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Load ROIs from file",
            directory=self.workdir,
            filter="ROI template (*.roi)",
        )
        if fname:
            with open(fname, "r") as f:
                self.restoreROIs(json.load(f))

    def addEvoCurves(self, pen):
        h_curve = pg.ScatterPlotItem(symbol="o", pen=pen, brush=pen.color(), size=7)
        s_curve = pg.ScatterPlotItem(symbol="o", pen=pen, brush=pen.color(), size=7)
        v_curve = pg.ScatterPlotItem(symbol="o", pen=pen, brush=pen.color(), size=7)
        self.evoPlot_h.addItem(h_curve)
        self.evoPlot_s.addItem(s_curve)
        self.evoPlot_v.addItem(v_curve)
        self.h_curves.append(h_curve)
        self.s_curves.append(s_curve)
        self.v_curves.append(v_curve)

    def onRefresh(self):
        # get last frame and time from the acq loop
        try:
            frame, t = self.acq_loop.data
        except Exception:
            return
        if t == self._last_processed:
            print(f"no new data since t={self._last_processed}. Skipping")
            return
        if frame is None:
            return
        self._last_processed = t
        # update the img and the plot
        self.img.setImage(bgr2rgb(frame))
        self.updateEvoPlot(frame, t)
        # report file size usage
        if self.recordAction.isChecked():
            size = os.path.getsize(self._tmp_rec_file_name) // 1_048_576  # in Mb
            msg = f"{self._tmp_rec_file_name}: {size}Mb"
            self.statusBar().showMessage(msg)

    def updateEvoPlot(self, frame, t):
        for roi, h_curve, s_curve, v_curve in zip(
            self.rois, self.h_curves, self.s_curves, self.v_curves
        ):
            selected = roi.getArrayRegion(frame, self.img)
            h, s, v = bgr2hsv(selected.astype(numpy.uint8)).mean(axis=(0, 1))
            h_curve.addPoints(x=(t,), y=(h,))
            s_curve.addPoints(x=(t,), y=(s,))
            v_curve.addPoints(x=(t,), y=(v,))

    def resetPlots(self):
        logging.info("Resetting plots")

        # black frame
        if self.img.image is not None:
            self.img.setImage(0 * self.img.image)

        # remove current color curves
        for h_curve in self.h_curves:
            self.evoPlot_h.removeItem(h_curve)
        self.h_curves = []
        for s_curve in self.s_curves:
            self.evoPlot_s.removeItem(s_curve)
        self.s_curves = []
        for v_curve in self.v_curves:
            self.evoPlot_v.removeItem(v_curve)
        self.v_curves = []

        # create new evo curves
        for roi in self.rois:
            self.addEvoCurves(roi.pen)

    def refreshEvoPlot(self, checked):
        if not checked:
            return

        self.resetPlots()

        if self._h5file is not None:
            self.onMainTimeSelectorChanged()  # re-show frame from cursor time

            msg = "Recalculating... "
            app = QtWidgets.QApplication.instance()

            frames = self._h5file["frames"]
            for i, (frame, t) in enumerate(zip(frames, self._h5times)):
                if not self.refreshEvoAction.isChecked():
                    self.statusBar().showMessage(msg + "Aborted", 3000)
                    break  # abort processing if refresh button is unchecked
                self.updateEvoPlot(frame, t)
                self.img.setImage(bgr2rgb(frame))
                self.statusBar().showMessage(
                    msg + f"({i+1}/{self._h5times.size}) frames", 3000
                )
                app.processEvents()

        # uncheck the button when finished
        self.refreshEvoAction.setChecked(False)

    def onMainTimeSelectorChanged(self):
        # find the index of the nearest frame to the selector
        xpos = self.time_selector_h.pos().x()
        with QtCore.QSignalBlocker(self.time_selector_s):
            self.time_selector_s.setPos(xpos)
        with QtCore.QSignalBlocker(self.time_selector_v):
            self.time_selector_v.setPos(xpos)
        adiff = numpy.abs(self._h5times - xpos)
        idx = numpy.argmin(adiff)
        # show frame at the found index
        frame = self._h5file["frames"][idx]
        self.img.setImage(bgr2rgb(frame))

    def onSlaveTimeSelectorChanged(self):
        self.time_selector_h.setPos(self.sender().pos().x())

    def setAcqFps(self, fps):
        if self.acq_loop is not None:
            self.acq_loop.period = 1 / fps

    @QtCore.pyqtSlot()
    def _setTmpRecFile(self, fname=None):
        """
        Sets the path and name of the file where the temporary data
        is recorded. If None given, a dialog is shown to prompt the user
        """
        if fname is None:
            fname, flt = QtWidgets.QFileDialog.getSaveFileName(
                parent=self,
                caption="File name for temporary data recording",
                directory=self._tmp_rec_file_name,
                filter="HDF5 (*.h5)",
            )
            if not fname:
                return
        self._tmp_rec_file_name = fname

    def _getTmpRecFile(self):
        return self._tmp_rec_file_name

    def saveSettings(self):
        """
        saves the application settings (so that they can be restored with
        :meth:`loadSettings`)
        """
        qsettings = QtCore.QSettings("colorevo", "colorevo")
        # main window geometry & state
        qsettings.setValue("geometry", self.saveGeometry())
        qsettings.setValue("state", self.saveState())
        # store the config dict
        qsettings.setValue("config", self.createQConfig())
        logging.info('Settings saved in "%s"', qsettings.fileName())

    def loadSettings(self):
        """
        restores the application settings previously saved with
        :meth:`saveSettings`.
        """
        qsettings = QtCore.QSettings("colorevo", "colorevo")

        # restore the app config
        try:
            self.applyQConfig(qsettings.value("config") or QtCore.QByteArray())
        except Exception as e:
            msg = (
                'Problem loading configuration from "%s".'
                + " Some settings may not be restored.\n Details: %r"
            )
            logging.warning(msg, qsettings.fileName(), e)
        self.restoreGeometry(qsettings.value("geometry") or QtCore.QByteArray())
        self.restoreState(qsettings.value("state") or QtCore.QByteArray())
        logging.info('Settings restored from "%s"', qsettings.fileName())

    def closeEvent(self, event):
        """
        Reimplemented from QMainWindow to clean and save settings on close
        """
        self.saveSettings()

        if self.acq_loop is not None:
            self.acq_loop.stop()
            self.acq_loop.cap.release()
        if self.acq_thread is not None:
            logging.info("Shutting down acquisition loop...")
            self.acq_thread.join()
        if self._h5file is not None:
            self._h5file.close()
        QtWidgets.QMainWindow.closeEvent(self, event)


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--keep-alive/--no-keep-alive",
    default=False,
    help="do not close GUI on exceptions",
)
@click.option("--reset", is_flag=True, help="reset configuration to default settings")
def main(keep_alive, reset):
    # Avoid closing GUI on exception if requested
    if keep_alive:
        import traceback

        def excepthook(etype, value, tb):
            traceback.print_exception(etype, value, tb)

        sys.excepthook = excepthook

    app = QtWidgets.QApplication(sys.argv)
    w = ColorEvoMain(load_settings=not reset)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
