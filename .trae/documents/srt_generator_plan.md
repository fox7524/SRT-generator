# SRT Generator Uygulaması Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Kullanıcıların video dosyalarını yükleyerek (sürükle-bırak veya seçerek) Apple MLX veya Whisper motorlarıyla altyazı çıkarabilecekleri ve farklı formatlarda (SRT, TXT, RTF, XML) dışa aktarabilecekleri bir PyQt6 masaüstü uygulaması geliştirmek.

**Architecture:** 
- Arayüz (UI) katmanı `PyQt6` ile oluşturulacak. Ana pencere sürükle-bırak desteğine sahip olacak.
- Arka planda donmaları önlemek için transkripsiyon ve ses çıkarma işlemleri `QThread` (Worker thread) kullanılarak asenkron yürütülecek.
- Videodan ses çıkarma işlemi, dosya boyutundan bağımsız çalışabilmek için `ffmpeg` (veya `moviepy`/`pydub`) aracılığıyla geçici bir ses dosyası (WAV/MP3) oluşturularak yapılacak.
- Ses dosyası seçilen motora (Apple `mlx-whisper` veya standart `openai-whisper`/`faster-whisper`) iletilecek.
- Elde edilen segmentler (başlangıç, bitiş, metin) seçilen formatlara göre dönüştürülüp dışa aktarılacak.

**Tech Stack:** 
- Python 3.10+
- `PyQt6` (Arayüz)
- `mlx-whisper` (Apple Silicon optimizasyonlu model)
- `openai-whisper` veya `faster-whisper` (Standart model)
- `ffmpeg-python` (Ses çıkarma)
- Diğer standart kütüphaneler (`os`, `json`, `xml.etree.ElementTree` vb.)

---

### Görev 1: Proje Yapısının Kurulumu ve Bağımlılıkların Ayarlanması

**Files:**
- Create: `requirements.txt`
- Create: `README.md` (Güncelleme)

- [ ] **Adım 1: `requirements.txt` dosyasını oluştur**
Gerekli paketleri tanımla: PyQt6, mlx-whisper, openai-whisper, ffmpeg-python.
```txt
PyQt6>=6.5.0
mlx-whisper
openai-whisper
ffmpeg-python
```

- [ ] **Adım 2: Kurulum komutlarını içeren bir script veya açıklama ekle**
README dosyasına ffmpeg kurulumu (`brew install ffmpeg`) ve paket kurulumu (`pip install -r requirements.txt`) talimatlarını yaz.

### Görev 2: Arka Plan İşlemcisi (Worker Thread) ve Ses Çıkarma Modülünün Geliştirilmesi

**Files:**
- Create: `src/core/audio_extractor.py`
- Create: `src/core/transcriber.py`

- [ ] **Adım 1: Ses çıkarma fonksiyonunu yaz**
`audio_extractor.py` içinde, `ffmpeg-python` kullanarak verilen video dosyasından 16kHz WAV formatında ses çıkaran bir fonksiyon yaz.
```python
import ffmpeg
import os
import tempfile

def extract_audio(video_path: str) -> str:
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "extracted_audio.wav")
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ar='16000')
    ffmpeg.run(stream, overwrite_output=True, quiet=True)
    return audio_path
```

- [ ] **Adım 2: Transkripsiyon (Altyazı) arayüzünü oluştur**
`transcriber.py` içinde MLX ve Whisper motorlarını yönetecek yapıyı kur. Dil seçeneği (`None` ise otomatik algılama) desteklenmeli.

```python
import whisper
import mlx_whisper

def transcribe_with_whisper(audio_path: str, language: str = None):
    model = whisper.load_model("base")
    options = {}
    if language and language.lower() != "auto":
        options["language"] = language
    result = model.transcribe(audio_path, **options)
    return result["segments"]

def transcribe_with_mlx(audio_path: str, language: str = None):
    # MLX whisper kullanımı
    options = {"path_or_hf_repo": "mlx-community/whisper-base-mlx"}
    # Not: mlx_whisper API'si modele göre değişebilir, temel kullanım:
    result = mlx_whisper.transcribe(audio_path, **options)
    return result["segments"]
```

### Görev 3: Dışa Aktarma (Export) Fonksiyonlarının Yazılması

**Files:**
- Create: `src/core/exporter.py`

- [ ] **Adım 1: SRT ve TXT export fonksiyonlarını yaz**
```python
def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def export_srt(segments: list, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def export_txt(segments: list, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"{segment['text'].strip()}\n")
```

- [ ] **Adım 2: RTF ve XML export fonksiyonlarını ekle**
Basit bir RTF yapısı ve XML yapısı oluştur.

### Görev 4: PyQt6 Arayüzünün (UI) Geliştirilmesi

**Files:**
- Create: `src/ui/main_window.py`
- Create: `src/ui/worker.py`

- [ ] **Adım 1: Asenkron işlem için QThread sınıfını yaz (`worker.py`)**
Arayüzü dondurmamak için işlemleri burada çalıştır ve sinyallerle (`pyqtSignal`) ilerlemeyi UI'a aktar.
```python
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
            self.progress.emit("Ses çıkarılıyor...")
            audio_path = extract_audio(self.video_path)
            
            self.progress.emit(f"Altyazı çıkarılıyor ({self.engine})...")
            if self.engine == "MLX":
                segments = transcribe_with_mlx(audio_path, self.language)
            else:
                segments = transcribe_with_whisper(audio_path, self.language)
                
            self.finished.emit(segments)
        except Exception as e:
            self.error.emit(str(e))
```

- [ ] **Adım 2: Sürükle-Bırak destekli Ana Pencereyi oluştur**
Arayüz elemanları:
- Video yolu etiketi (Drag & Drop bölgesi)
- Motor seçimi ComboBox (MLX, Whisper)
- Dil seçimi ComboBox (Auto, English, Turkish vb.)
- Format seçimi (Checkboxes: SRT, TXT, RTF, XML)
- İlerleme etiketi / Progress Bar
- "Başlat" butonu

- [ ] **Adım 3: UI Sinyallerini bağla**
Dosya sürüklendiğinde yolu al, başlat butonuna basıldığında `TranscriptionWorker`'ı başlat, tamamlandığında `exporter.py` kullanarak dosyaları kaydet.

### Görev 5: Uygulamayı Birleştirme ve Başlatma

**Files:**
- Create: `main.py`

- [ ] **Adım 1: Uygulama giriş noktasını oluştur**
```python
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **Adım 2: Test Et**
Sistemin çalıştığını doğrulamak için örnek bir video ile uygulamayı başlat ve tüm formatlarda çıktı alabildiğini doğrula.
