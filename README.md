# Signal Viewer Application

## Description
The Signal Viewer is a desktop application developed using Python and Qt. It provides a multi-port, multi-channel signal viewer with the following key features:

- **Signal Browsing:** Users can open any signal file from their PC. The application includes sample signals from three different medical types (e.g., ECG, EMG, EEG) with both normal and abnormal examples.
- **Real-Time Signal Connection:** Users can connect to a website that emits real-time signals, read the emitted signal, and plot it.
- **Dual Graph Display:** The application features two main graphs with independent controls. Users can link or unlink the graphs for synchronized or independent operation.
- **Non-Rectangle Graph:** A unique non-rectangle graph is included to display suitable signals in cine mode.
- **Signal Manipulation:** Users can manipulate signals through UI elements to change color, add labels, control cine speed, zoom, pan, scroll, and more.
- **Signal Glue Feature:** The application allows users to cut and glue parts of signals from different graphs into a third graph with customizable interpolation parameters.
- **Exporting & Reporting:** Users can generate PDF reports with snapshots and statistical data (mean, std, duration, min, max) for the glued signals.

## Features
- Browse and open signal files from the PC.
- Connect to a real-time signal website.
- Independent and linked dual graph controls.
- Non-rectangle graph for cine mode signal display.
- Signal manipulation features (color change, zoom, pan, scroll, pause, play, rewind, etc.).
- Signal glue operation with customizable parameters.
- Export reports in PDF format with signal snapshots and data statistics.

## Demo Video



https://github.com/user-attachments/assets/0745c025-66e9-4b6f-8976-11581571f60b




## Technologies Used
- Python
- PyQt
- Pyqtgraoh (for plotting)
- PDF generation libraries (e.g., ReportLab or FPDF)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Mazenmarwan023/signal-viewer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd signal-viewer
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
## Contributors

- [Saif mohamed](https://github.com/seiftaha)
- [Mahmoud mohamed](https://github.com/mahmoudmo22)
- [Eman emad](https://github.com/alyaaa20)
- [Mazen marwan](https://github.com/Mazenmarwan023)

We appreciate everyone's contributions to this project!

## License

This project is open-source and available under the [MIT License](LICENSE).

---


