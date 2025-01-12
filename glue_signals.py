import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,QLabel,
                             QHBoxLayout,QGridLayout,QPushButton,QLineEdit,QSlider, 
                             QComboBox,QCheckBox,QColorDialog,QFileDialog,QStackedWidget,QMessageBox)
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QIcon
import numpy as np
import pyqtgraph as pg
from scipy.interpolate import interp1d




class GlueSignalsWindow(QMainWindow):
    def __init__(self, signal1, signal2, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Glue Signal Portions")
        self.setGeometry(100, 100, 800, 600)

        self.signal1 = signal1
        self.signal2 = signal2

        # Main layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        # Graph for Signal 1
        self.plot1 = pg.PlotWidget(title="Signal 1 Portion")
        self.plot1.plot(self.signal1)
        main_layout.addWidget(self.plot1)

        # Region for selection on Signal 1
        self.region1 = pg.LinearRegionItem()
        self.plot1.addItem(self.region1)

        # Graph for Signal 2
        self.plot2 = pg.PlotWidget(title="Signal 2 Portion")
        self.plot2.plot(self.signal2)
        main_layout.addWidget(self.plot2)

        # Region for selection on Signal 2
        self.region2 = pg.LinearRegionItem()
        self.plot2.addItem(self.region2)

        # Controls for gap and interpolation
        control_layout = QGridLayout()

        # Gap slider layout
        gap_layout = QVBoxLayout()
        gap_layout.addWidget(QLabel("Gap Size:"))
        self.gap_slider = QSlider(Qt.Horizontal)
        self.gap_slider.setMinimum(0)
        self.gap_slider.setMaximum(1000)
        self.gap_slider.setValue(0)
        self.gap_slider.setMaximumWidth(400)
        self.gap_slider.valueChanged.connect(self.perform_glue)
        gap_layout.addWidget(self.gap_slider)
        
        # Gap value label
        self.gap_value_label = QLabel("0")
        gap_layout.addWidget(self.gap_value_label)
        self.gap_slider.valueChanged.connect(lambda v: self.gap_value_label.setText(str(v)))
        
        control_layout.addLayout(gap_layout,0,0)

        # Interpolation order selector
        interp_layout = QVBoxLayout()
        interp_layout.addWidget(QLabel("Interpolation Order:"))
        self.interpolation_selector = QComboBox()
        self.interpolation_selector.addItems(["Linear (1)", "Quadratic (2)", "Cubic (3)"])
        self.interpolation_selector.currentIndexChanged.connect(self.perform_glue)
        interp_layout.addWidget(self.interpolation_selector)
        control_layout.addLayout(interp_layout,0,1)

        main_layout.addLayout(control_layout)
        self.setCentralWidget(main_widget)

    def set_gap(self, gap_value):
        # Update gap input without triggering a loop
        self.gap_slider.setValue(gap_value)
        self.perform_glue()

    def perform_glue(self):
        # Extract selected portions from both signals
        start1, end1 = self.region1.getRegion()
        start2, end2 = self.region2.getRegion()

        # Get the gap value from slider
        gap = self.gap_slider.value()

        # Get interpolation order from selector (adding 1 because index starts at 0)
        interpolation_order = self.interpolation_selector.currentIndex() + 1
    
        # Slice the signals based on selected regions
        signal1_portion = self.signal1[int(start1):int(end1)]
        signal2_portion = self.signal2[int(start2):int(end2)]

        if len(signal1_portion) == 0 or len(signal2_portion) == 0:
            return

        # Get reference points for interpolation
        n_points = min(5, len(signal1_portion), len(signal2_portion))
        reference_points1 = signal1_portion[-n_points:]
        reference_points2 = signal2_portion[:n_points]

        # Handle small or zero gap cases
        if gap <= 2:
            # Create a minimum connection point between signals
            connection_point = (signal1_portion[-1] + signal2_portion[0]) / 2
            if gap == 0:
                gap_signal = np.array([])
                # Adjust the last and first points to ensure smooth connection
                signal1_portion = np.concatenate([signal1_portion[:-1], [connection_point]])
                signal2_portion = np.concatenate([[connection_point], signal2_portion[1:]])
            else:
                # For gaps of 1-2 points, create minimal smooth connection
                gap_signal = np.array([connection_point] * gap)
        else:
            # Normal interpolation for larger gaps
            # Create x values for reference points and gap
            x_ref1 = np.arange(n_points)
            x_ref2 = np.arange(n_points) + n_points + gap
            x_gap = np.linspace(n_points, n_points + gap, gap)
            
            # Combine reference points for interpolation
            x_combined = np.concatenate([x_ref1, x_ref2])
            y_combined = np.concatenate([reference_points1, reference_points2])

            # Create interpolated gap based on order
            interpolation_kinds = {1: 'linear', 2: 'quadratic', 3: 'cubic'}
            kind = interpolation_kinds.get(interpolation_order, 'linear')
            
            # Create interpolator using reference points
            interpolator = interp1d(x_combined, y_combined, kind=kind, fill_value='extrapolate')
            
            # Generate gap signal
            gap_signal = interpolator(x_gap)

        # Glue the signals together
        glued_signal = np.concatenate([signal1_portion, gap_signal, signal2_portion])

        # Display the result
        self.parent().plot_glued_signal_with_colors(signal1_portion, gap_signal, signal2_portion, glued_signal)
        self.parent().canvas3.repaint()




























    def interpolate_gap(self, gap_signal, order):
        """Smooth the gap using robust interpolation."""
        # Generate x-axis indices for the gap signal
        x = np.linspace(0, len(gap_signal) - 1, len(gap_signal))
        
        # Check if the gap signal length is sufficient
        if len(x) < 2:
            print("Not enough points for interpolation.")
            return gap_signal

        # Select interpolation kind based on order
        interpolation_kinds = {1: 'linear', 2: 'quadratic', 3: 'cubic'}
        kind = interpolation_kinds.get(order, 'linear')  # Default to linear if order is unsupported

        # Create the interpolator
        interpolator = interp1d(x, gap_signal, kind=kind, fill_value="extrapolate")
        print(kind)
        
        # Apply interpolation
        return interpolator(x)
