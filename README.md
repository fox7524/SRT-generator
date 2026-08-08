# SRT Generator

Apple MLX ve Whisper motorlarını kullanarak, videolardan otomatik olarak altyazı çıkaran ve çeşitli formatlarda (SRT, TXT, RTF, XML) kaydedebilen macOS/Masaüstü uygulaması.

## Özellikler
- **Apple MLX Whisper Desteği**: M serisi Apple Silicon (M1/M2/M3 vb.) işlemcilerde maksimum performans.
- **OpenAI Whisper Desteği**: Evrensel standart model desteği.
- **Sürükle & Bırak Arayüzü**: Kullanımı kolay PyQt6 arayüzü.
- **Dil Seçimi**: Otomatik algılama veya manuel dil seçimi.
- **Geniş Dışa Aktarım Desteği**: Altyazıları SRT, Düz Metin (TXT), RTF ve XML formatında dışa aktarma.
- **Video Boyutu Bağımsız**: Video dosyalarından geçici olarak sesi çıkararak çalıştığı için çok büyük dosyalarda bile düşük bellek tüketimi sağlar.

## Kurulum

### 1. Sistem Bağımlılıkları
Uygulamanın videolardan ses çıkarabilmesi için sisteminizde `ffmpeg` yüklü olmalıdır. macOS üzerinde Homebrew ile kurabilirsiniz:
```bash
brew install ffmpeg
```

### 2. Python Bağımlılıkları
Sanal ortam oluşturulması önerilir:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Kullanım

Uygulamayı başlatmak için:
```bash
python main.py
```

1. Açılan pencerede **Video Yükle** alanına dosyanızı sürükleyin veya tıklayarak seçin.
2. Motoru (MLX veya Whisper) ve Dili seçin.
3. Çıktı formatlarını seçin.
4. **Altyazı Çıkar** butonuna basın. İşlem bitince dosyalarınız oluşturulacaktır.
