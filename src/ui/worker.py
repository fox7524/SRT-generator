from PyQt6.QtCore import QThread, pyqtSignal
from src.core.audio_extractor import extract_audio
from src.core.transcriber import transcribe_with_whisper, transcribe_with_mlx

class TranscriptionWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, video_path, engine, language):
        super().__init__()
        self.video_path = video_path
        self.engine = engine
        self.language = language

    def run(self):
        try:
            self.progress.emit("Videodan ses çıkarılıyor...")
            audio_path = extract_audio(self.video_path)
            
            self.progress.emit(f"Altyazı çıkarılıyor ({self.engine} - {self.language})... Bu işlem bilgisayarınızın hızına bağlı olarak vakit alabilir.")
            
            # Dil "Auto" ise None olarak geç
            lang_param = None if self.language == "Auto" else self.language
            
            if self.engine == "MLX Whisper":
                segments = transcribe_with_mlx(audio_path, lang_param)
            else:
                segments = transcribe_with_whisper(audio_path, lang_param)
                
            self.progress.emit("İşlem tamamlandı, dosyalar kaydediliyor...")
            self.finished.emit(segments)
        except Exception as e:
            self.error.emit(str(e))
