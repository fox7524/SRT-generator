# SRT Generator - AI Altyazı Çıkarıcı 🎬🤖

![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-PyQt6-green.svg)

Apple MLX ve OpenAI Whisper motorlarını kullanarak, video dosyalarından tamamen otomatik ve yerel (çevrimdışı) olarak yüksek doğrulukta altyazı çıkaran modern bir macOS/Masaüstü uygulamasıdır. Videonun boyutu ne olursa olsun, arka planda sadece ses dosyasını işleyerek bellek tasarrufu sağlar.

---

## 🌟 Öne Çıkan Özellikler

- **⚡ Apple MLX Optimizasyonu**: M serisi Apple Silicon (M1/M2/M3 vb.) işlemcilerde donanımsal hızlandırma sayesinde inanılmaz hızlı çeviri süreleri.
- **🌍 OpenAI Whisper Desteği**: Standart mimariler ve esneklik için evrensel model desteği.
- **🎯 Kolay Kullanım**: Sürükle ve bırak destekli, kullanıcı dostu modern PyQt6 arayüzü.
- **🗣️ Çoklu Dil Desteği**: İster otomatik dil algılamayı kullanın, isterseniz videonun dilini (Türkçe, İngilizce, Almanca vb.) manuel olarak seçin.
- **💾 Geniş Çıktı Yelpazesi**: Altyazıları **SRT**, **TXT** (Düz Metin), **RTF** ve **XML** formatlarında aynı anda dışa aktarabilirsiniz.
- **🚀 Boyut Bağımsızlık**: Sistem belleğini yormamak için videolardan anlık 16kHz WAV ses çıkarıp işler. GB'larca büyüklükteki videoları bile sorunsuz okur.

---

## 🛠️ Kurulum Rehberi

Uygulamayı kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Sistem Bağımlılıkları (FFmpeg)
Videodan ses çıkarma işlemleri için `ffmpeg` gereklidir. macOS üzerinde Homebrew kullanarak tek tıkla kurabilirsiniz:
```bash
brew install ffmpeg
```

### 2. Python Ortamı ve Paketler
Uygulama Python 3.10 ve üzeri bir sürüm gerektirir. Temiz bir kurulum için sanal ortam (virtual environment) kullanmanız önerilir:

```bash
# Proje dizinine gidin
cd SRT-generator

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktif edin (macOS/Linux)
source venv/bin/activate

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

---

## 🖥️ Nasıl Kullanılır?

Tüm kurulumlar tamamlandıktan sonra uygulamayı başlatmak çok basittir:

```bash
python main.py
```

1. Açılan arayüzde yer alan **"Videonuzu buraya sürükleyin"** alanına video dosyanızı (mp4, mkv, avi vb.) sürükleyip bırakın.
2. İşlem için **AI Motorunu** seçin (Apple Silicon Mac'iniz varsa kesinlikle `MLX Whisper` önerilir).
3. Videonun **dilini** seçin (Emin değilseniz `Auto` bırakın).
4. İhtiyacınız olan **Çıktı Formatlarını** işaretleyin.
5. **Altyazı Çıkar** butonuna basın ve arkanıza yaslanın. 
6. İşlem tamamlandığında, altyazı dosyalarınız videonuzla aynı klasöre otomatik olarak kaydedilecektir.

---

## ⚖️ Lisans ve Kullanım Hakları (CC BY-NC 4.0)

Bu proje **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** lisansı ile lisanslanmıştır.

**Bunun Anlamı Nedir?**
- ✅ **Kullanabilirsiniz**: Bu projeyi kişisel amaçlarınız için kullanabilir, kopyalayabilir ve bilgisayarınızda çalıştırabilirsiniz.
- ✅ **Değiştirebilirsiniz**: Kodu kendi ihtiyaçlarınıza göre düzenleyebilirsiniz.
- ✅ **Paylaşabilirsiniz**: Projeyi veya kendi düzenlediğiniz halini başkalarıyla paylaşabilirsiniz.

**ŞARTLAR:**
1. ℹ️ **Atıf (Attribution)**: Bu kodu kullanırken, paylaşırken veya değiştirirken orijinal yazara (bana) atıfta bulunmalı/kredi vermelisiniz.
2. 🚫 **Ticari Kullanım Yasaktır (NonCommercial)**: Bu kod, bu uygulama veya bu uygulamadan üretilen değiştirilmiş versiyonlar **TİCARİ BİR AMAÇLA, PARA KAZANMAK İÇİN KULLANILAMAZ VEYA SATILAMAZ**. Uygulamanın ticari hakları tamamen yazara aittir.

Lisansın tam metni için projedeki [LICENSE](./LICENSE) dosyasına göz atabilirsiniz.
