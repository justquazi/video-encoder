# Video encoder using FFmpeg
# Quazi Heider
# March 06 2026
import os
import ffmpeg
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox
from PyQt6.QtCore import Qt
class ConverterUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Converter")
        self.resize(900,600)
        
        self.label1 = QLabel("Video Encoder")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label1.setStyleSheet("font-size: 50px; font-weight: bold")

        self.label2 = QLabel("No file(s) selected")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setStyleSheet("font-size: 18px; font-weight: bold")
        
        self.label3 = QLabel("Quazi Heider")
        self.label3.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label3.setStyleSheet("color: gray; font-size: 12px; font-weight: bold")
        
        self.label4 = QLabel("v 0.1.0")
        self.label4.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label4.setStyleSheet("color: gray; font-size: 12px; font-weight: bold")

        self.select_btn = QPushButton("Select Video")
        self.select_btn.setFixedSize(900, 70)
        self.convert_btn = QPushButton("Convert to MP4")
        self.convert_btn.setFixedSize(900, 70)

        layout = QVBoxLayout()
        layout.addStretch(1)          # space above title
        layout.addWidget(self.label1) # Video Encoder
        layout.addStretch(0)          # space between
        layout.addWidget(self.label3) # Name
        layout.addStretch(0)          # space between
        layout.addWidget(self.label4) # Version
        layout.addStretch(1)          # space below

        layout.addWidget(self.label2) # No file selected
        layout.addStretch(2)          # space below

        layout.addWidget(self.select_btn)
        layout.addWidget(self.convert_btn)

        self.setLayout(layout)

        self.select_btn.clicked.connect(self.select_video)
        self.convert_btn.clicked.connect(self.convert_video)

        self.input_file = None

    def select_video(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Video")
        if file:
            self.input_file = file
            self.label2.setText(file)
            self.label5 = QLabel("Select destination folder")

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select destination folder")
        if folder:
            self.output_folder = folder
    

    def convert_video(self):
        if not self.input_file:
            self.label2.setText("Select a file first")
            self.label2.setStyleSheet("color: red; font-size: 18px; font-weight: bold")
            return
        
        try:
            self.label2.setText("Converting...")
            import subprocess
            output = self.input_file + ".mp4"
            subprocess.run([
                "ffmpeg",
                 "-i", self.input_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                output
            ], check = True)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Conversion Error")
            msg.setText("Something went wrong during conversion.")
            msg.setInformativeText(str(e))
            msg.exec()

        self.label2.setText("Conversion completed successfully.")
        self.label2.setStyleSheet("color: green; font-size: 18px; font-weight: bold")


app = QApplication(sys.argv)
window = ConverterUI()
window.show()
app.exec()

