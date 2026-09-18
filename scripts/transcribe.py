#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Расшифровка аудио/видео в текст через faster-whisper (кроссплатформенно).

Работает на macOS, Windows и Linux. Зависимости: ffmpeg и faster-whisper
(шаги 4–5 в SETUP.md для macOS или SETUP_WINDOWS.md для Windows).

Примеры:
    python scripts/transcribe.py voice.ogg
    python scripts/transcribe.py voice.ogg -o text.txt
    python scripts/transcribe.py video.mp4 --model small --language ru
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def convert_to_wav(input_path: Path, wav_path: str) -> None:
    """Конвертирует входной файл в wav 16 кГц моно (формат, который ждёт whisper)."""
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        "-y",
        wav_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        tail = (result.stderr or "").strip().splitlines()[-5:]
        print("Ошибка: ffmpeg не смог прочитать файл. Вывод ffmpeg:", file=sys.stderr)
        for line in tail:
            print(f"  {line}", file=sys.stderr)
        sys.exit(1)


def transcribe(wav_path: str, model_name: str, language: str) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(
            "Ошибка: не установлен faster-whisper.\n"
            "Установите: pip install faster-whisper\n"
            "(если pip не виден: python -m pip install faster-whisper)\n"
            "Подробности — шаг 5 в SETUP.md (macOS) или SETUP_WINDOWS.md (Windows).",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"Загружаю модель '{model_name}' (при первом запуске она скачается, "
        "это займёт время)...",
        file=sys.stderr,
    )
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    print("Расшифровываю...", file=sys.stderr)
    segments, _info = model.transcribe(wav_path, language=language)
    return " ".join(seg.text.strip() for seg in segments).strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Расшифровка аудио/видео в текст через faster-whisper."
    )
    parser.add_argument("input", help="путь к аудио/видео файлу (.ogg, .mp3, .m4a, .mp4, .wav и т.д.)")
    parser.add_argument("-o", "--output", help="сохранить текст в файл (UTF-8)")
    parser.add_argument("--model", default="small",
                        help="модель whisper: tiny, base, small, medium, large-v3 (по умолчанию small)")
    parser.add_argument("--language", default="ru",
                        help="язык речи (по умолчанию ru)")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print(
            "Ошибка: ffmpeg не найден.\n"
            "Установите ffmpeg — шаг 4 в SETUP.md (macOS) или SETUP_WINDOWS.md (Windows).\n"
            "На Windows после установки может понадобиться переоткрыть терминал.",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Ошибка: файл не найден: {input_path}", file=sys.stderr)
        sys.exit(1)

    wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav_path = wav_file.name
    wav_file.close()  # закрываем сразу: на Windows ffmpeg не пишет в открытый файл

    try:
        convert_to_wav(input_path, wav_path)
        text = transcribe(wav_path, args.model, args.language)
    finally:
        Path(wav_path).unlink(missing_ok=True)

    print(text)

    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"Текст сохранён в {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
