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
        
        self.label1 = QLabel("MOD to MP4 Video Encoder")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        self.label5 = QLabel("No destination selected")
        self.label5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label5.setStyleSheet("font-size: 18px; font-weight: bold")

        self.select_btn = QPushButton("Select Videos")
        self.select_btn.setFixedSize(900, 70)
        self.dest_btn = QPushButton("Select Destination Folder")
        self.dest_btn.setFixedSize(900,70)
        self.convert_btn = QPushButton("Convert to MP4")
        self.convert_btn.setFixedSize(900, 70)
        self.convert_btn.setEnabled(False)

        layout = QVBoxLayout()
        layout.addStretch(1)          # space above title
        layout.addWidget(self.label1) # Video Encoder
        layout.addStretch(0)          # space between
        layout.addWidget(self.label3) # Name
        layout.addStretch(0)          # space between
        layout.addWidget(self.label4) # Version
        layout.addStretch(1)          # space below

        layout.addWidget(self.label2) # No file selected
        layout.addStretch(0)          # space below
        layout.addWidget(self.label5)
        layout.addStretch(1)

        layout.addWidget(self.select_btn)
        layout.addWidget(self.dest_btn)
        layout.addWidget(self.convert_btn)


        self.setLayout(layout)

        self.select_btn.clicked.connect(self.select_video)
        self.dest_btn.clicked.connect(self.select_destination)
        self.convert_btn.clicked.connect(self.convert_video)

        self.input_files = None

    def select_video(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Videos")
        if files:
            self.input_files = files
            filenames = [os.path.basename(file) for file in files]
            label_text = ""
            if len(filenames) > 5:
                n = len(filenames)
                label_text = str(n) + " files selected"
            else: 
                for filename in filenames:
                    label_text = label_text + filename + ', '
    
            self.label2.setText(label_text)
            self.label2.setStyleSheet("font-size: 18px; font-weight: bold")
           

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select destination folder")
        if folder:
            self.output_folder = folder
            label_5_text = "Save to: " + os.path.basename(folder) 
            self.label5.setText(label_5_text)
            self.convert_btn.setEnabled(True)

    def convert_video(self):
        if not self.input_files:
            self.label2.setText("Select a file first")
            self.label2.setStyleSheet("color: red; font-size: 18px; font-weight: bold")
            return
        
        try:
            
            import subprocess
            for file in self.input_files:
                output_filename = os.path.basename(file[:-4]) + ".mp4"
                output = os.path.join(self.output_folder, output_filename)
                subprocess.run(["ffmpeg", "-i", file, "-c:v", "libx264", "-c:a", "aac", output], check = True)
                self.label2.setText("Converting " + output_filename[:-4])
                self.label2.setStyleSheet("color: yellow; font-size: 18px; font-weight: bold")
                QApplication.processEvents()

            self.label2.setText("Conversion completed successfully.")
            self.label2.setStyleSheet("color: green; font-size: 18px; font-weight: bold")
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Conversion Error")
            msg.setText("Something went wrong during conversion.")
            msg.setInformativeText(str(e))
            msg.exec()
            self.label2.setText("Conversion unsuccessful.")
            self.label2.setStyleSheet("color: red; font-size: 18px; font-weight: bold")

        


app = QApplication(sys.argv)
window = ConverterUI()
window.show()
app.exec()

