def transcribe_with_whisper(audio_path: str, language: str = None):
    try:
        import whisper
    except ImportError:
        raise ImportError("openai-whisper kütüphanesi bulunamadı.")
        
    model = whisper.load_model("base")
    options = {}
    if language and language.lower() != "auto":
        options["language"] = language
        
    result = model.transcribe(audio_path, **options)
    return result["segments"]

def transcribe_with_mlx(audio_path: str, language: str = None):
    try:
        import mlx_whisper
    except ImportError:
        raise ImportError("mlx-whisper kütüphanesi bulunamadı. Apple Silicon üzerinde olduğunuzdan emin olun.")
        
    # MLX whisper base modeli
    options = {
        "path_or_hf_repo": "mlx-community/whisper-base-mlx"
    }
    
    if language and language.lower() != "auto":
        # mlx_whisper genellikle dil belirlemeyi destekler, kwargs olarak verilebilir
        options["language"] = language
        
    result = mlx_whisper.transcribe(audio_path, **options)
    return result["segments"]
