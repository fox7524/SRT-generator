import ffmpeg
import os
import tempfile

def extract_audio(video_path: str) -> str:
    """
    Verilen video dosyasından sesi çıkarıp geçici bir wav dosyası olarak kaydeder.
    16kHz örnekleme hızı ve mono (1 kanal) formatında kaydeder.
    """
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "extracted_audio.wav")
    
    if os.path.exists(audio_path):
        try:
            os.remove(audio_path)
        except OSError:
            pass
            
    try:
        stream = ffmpeg.input(video_path)
        # acodec='pcm_s16le', ac=1 (mono), ar='16000' (16kHz)
        stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ac=1, ar='16000')
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
    except ffmpeg.Error as e:
        print("FFmpeg error:", e.stderr)
        raise RuntimeError("Ses çıkarma işlemi başarısız oldu. FFmpeg yüklü olduğundan emin olun.")
        
    return audio_path
