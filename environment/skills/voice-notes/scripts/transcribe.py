#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Расшифровка аудио/видео в текст через faster-whisper (кроссплатформенно).

Зависимости: ffmpeg в PATH и faster-whisper в выбранном Python-окружении.
Подготовка — шаги 4–5 environment/windows/SETUP.md стартового пакета.

Примеры (Python из окружения voice-notes):
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
        "ffmpeg", "-nostdin", "-i", str(input_path),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y", wav_path,
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        # ffmpeg stderr может содержать имя/метаданные личного файла.
        raise RuntimeError("ffmpeg не смог прочитать или конвертировать файл.")


def transcribe(wav_path: str, model_name: str, language: str) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        raise RuntimeError(
            "не установлен faster-whisper в выбранном Python. "
            "Подготовьте отдельное окружение — шаг 5 инструкции Environment."
        ) from error

    print(
        "Загружаю модель (при первом запуске она скачается, это займёт время)...",
        file=sys.stderr,
    )
    try:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        print("Расшифровываю...", file=sys.stderr)
        segments, _info = model.transcribe(wav_path, language=language)
        return " ".join(seg.text.strip() for seg in segments).strip()
    except Exception as error:
        raise RuntimeError("не удалось загрузить модель или распознать аудио.") from error


def main() -> int:
    # Нативная Windows-консоль может использовать кодировку, отличную от UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Расшифровка аудио/видео в текст через faster-whisper."
    )
    parser.add_argument("input", help="путь к аудио/видео файлу (.ogg, .mp3, .m4a, .mp4, .wav и т.д.)")
    parser.add_argument("-o", "--output", help="сохранить текст в новый файл (UTF-8); существующий не заменяется")
    parser.add_argument("--model", default="small",
                        help="модель whisper: tiny, base, small, medium, large-v3 (по умолчанию small)")
    parser.add_argument("--language", default="ru", help="язык речи (по умолчанию ru)")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output) if args.output else None
    if not input_path.is_file():
        print("Ошибка: входной файл не найден или не является файлом.", file=sys.stderr)
        return 1
    if output_path and (
        output_path.resolve() == input_path or output_path.exists() or output_path.is_symlink()
    ):
        print("Ошибка: выходной файл уже существует или совпадает с входным; выберите новое имя.", file=sys.stderr)
        return 1
    if shutil.which("ffmpeg") is None:
        print(
            "Ошибка: ffmpeg не найден. Подготовьте его по шагу 4 Environment.\n"
            "На Windows после установки может понадобиться переоткрыть приложение.",
            file=sys.stderr,
        )
        return 1

    try:
        # Уникальный каталог; очищаются только созданные этим запуском файлы.
        with tempfile.TemporaryDirectory(prefix="ff-voice-") as temp_dir:
            wav_path = str(Path(temp_dir) / "input.wav")
            convert_to_wav(input_path, wav_path)
            text = transcribe(wav_path, args.model, args.language)
        if output_path:
            # Exclusive create защищает и от появления файла во время распознавания.
            with output_path.open("x", encoding="utf-8") as output_file:
                output_file.write(text + "\n")
        print(text)
    except RuntimeError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    except Exception:
        # Сторонние исключения могут содержать пути, URL и приватные метаданные.
        print("Ошибка: не удалось распознать или сохранить текст. Проверьте модель, зависимости и доступ к файлам.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
