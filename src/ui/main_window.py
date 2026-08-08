import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, 
    QCheckBox, QPushButton, QProgressBar, QMessageBox, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from src.ui.worker import TranscriptionWorker
from src.core.exporter import export_srt, export_txt, export_rtf, export_xml

class DragDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Videonuzu buraya sürükleyin\nveya seçmek için tıklayın")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 50px;
                background-color: #f9f9f9;
                color: #555;
                font-size: 16px;
            }
            QLabel:hover {
                background-color: #e9e9e9;
                border-color: #888;
            }
        """)
        self.setAcceptDrops(True)
        self.video_path = None
        self.main_window = parent

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.set_video_path(file_path)

    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Video Seç", "", "Video Dosyaları (*.mp4 *.mkv *.avi *.mov *.flv)")
        if file_path:
            self.set_video_path(file_path)

    def set_video_path(self, file_path):
        self.video_path = file_path
        filename = os.path.basename(file_path)
        self.setText(f"Seçilen Video:\n{filename}")
        if self.main_window:
            self.main_window.start_btn.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Generator - AI Altyazı Çıkarıcı")
        self.setMinimumSize(500, 400)
        self.worker = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Sürükle-Bırak Alanı
        self.drop_label = DragDropLabel(self)
        layout.addWidget(self.drop_label)

        # Ayarlar Alanı
        settings_layout = QHBoxLayout()
        
        # Motor Seçimi
        engine_layout = QVBoxLayout()
        engine_layout.addWidget(QLabel("AI Motoru:"))
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["MLX Whisper", "OpenAI Whisper"])
        engine_layout.addWidget(self.engine_combo)
        settings_layout.addLayout(engine_layout)

        # Dil Seçimi
        lang_layout = QVBoxLayout()
        lang_layout.addWidget(QLabel("Dil:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Auto", "tr", "en", "de", "fr", "es", "it", "ru"])
        lang_layout.addWidget(self.lang_combo)
        settings_layout.addLayout(lang_layout)

        layout.addLayout(settings_layout)

        # Format Seçimi
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Çıktı Formatları:"))
        self.cb_srt = QCheckBox("SRT")
        self.cb_srt.setChecked(True)
        self.cb_txt = QCheckBox("TXT")
        self.cb_rtf = QCheckBox("RTF")
        self.cb_xml = QCheckBox("XML")
        
        format_layout.addWidget(self.cb_srt)
        format_layout.addWidget(self.cb_txt)
        format_layout.addWidget(self.cb_rtf)
        format_layout.addWidget(self.cb_xml)
        format_layout.addStretch()
        layout.addLayout(format_layout)

        # Durum ve İlerleme
        self.status_label = QLabel("Hazır.")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Başlat Butonu
        self.start_btn = QPushButton("Altyazı Çıkar")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_transcription)
        self.start_btn.setMinimumHeight(40)
        layout.addWidget(self.start_btn)

    def start_transcription(self):
        if not self.drop_label.video_path:
            return

        engine = self.engine_combo.currentText()
        lang = self.lang_combo.currentText()

        self.start_btn.setEnabled(False)
        self.progress_bar.show()
        self.status_label.setText("İşlem başlatılıyor...")

        self.worker = TranscriptionWorker(self.drop_label.video_path, engine, lang)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_finished(self, segments):
        self.progress_bar.hide()
        self.status_label.setText("İşlem başarılı! Dosyalar kaydediliyor...")
        
        video_path = self.drop_label.video_path
        base_name = os.path.splitext(video_path)[0]
        
        try:
            if self.cb_srt.isChecked():
                export_srt(segments, f"{base_name}.srt")
            if self.cb_txt.isChecked():
                export_txt(segments, f"{base_name}.txt")
            if self.cb_rtf.isChecked():
                export_rtf(segments, f"{base_name}.rtf")
            if self.cb_xml.isChecked():
                export_xml(segments, f"{base_name}.xml")
                
            QMessageBox.information(self, "Başarılı", f"Altyazılar başarıyla çıkarıldı ve video klasörüne kaydedildi.\n\nVideo: {video_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilirken hata oluştu: {str(e)}")
            
        self.status_label.setText("Hazır.")
        self.start_btn.setEnabled(True)

    def on_error(self, error_msg):
        self.progress_bar.hide()
        self.status_label.setText("Hata oluştu.")
        self.start_btn.setEnabled(True)
        QMessageBox.critical(self, "Hata", f"İşlem sırasında bir hata oluştu:\n{error_msg}")
