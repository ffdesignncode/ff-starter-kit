"""Контракты wrapper без установки ffmpeg, пакетов и загрузки моделей."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

SCRIPT = Path(__file__).parents[1] / 'skills/voice-notes/scripts/transcribe.py'
spec = importlib.util.spec_from_file_location('voice_transcribe', SCRIPT)
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class TranscribeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='voice-тест ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.audio = self.root / 'голос запись.ogg'
        self.audio.write_bytes(b'audio')
        self.wav_paths = []

    def convert(self, argv, **kwargs):
        self.assertIsInstance(argv, list)
        self.assertEqual(argv[argv.index('-i') + 1], str(self.audio))
        self.wav_paths.append(Path(argv[-1]))
        Path(argv[-1]).write_bytes(b'wav')
        return types.SimpleNamespace(returncode=0)

    def run_main(self, extra=(), converter=None, model_error=False, missing_dependency=False):
        class Model:
            def __init__(self, *args, **kwargs):
                if model_error:
                    raise ValueError('private details')
                self.args, self.kwargs = args, kwargs
            def transcribe(self, path, language):
                return iter([types.SimpleNamespace(text=' Привет, мир! ')]), None
        module = types.SimpleNamespace(WhisperModel=Model)
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', ['transcribe', str(self.audio), *extra]), \
             mock.patch.object(voice.shutil, 'which', return_value='/fake/ffmpeg'), \
             mock.patch.object(voice.subprocess, 'run', side_effect=converter or self.convert), \
             mock.patch.dict(sys.modules, {'faster_whisper': None if missing_dependency else module}), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = voice.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_success_unicode_and_utf8_output_cleanup(self):
        output = self.root / 'стенограмма текст.txt'
        code, stdout, _ = self.run_main(['-o', str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(stdout, 'Привет, мир!\n')
        self.assertEqual(output.read_bytes(), 'Привет, мир!\n'.encode())
        self.assertEqual(self.audio.read_bytes(), b'audio')
        self.assertTrue(self.wav_paths)
        self.assertTrue(all(not path.parent.exists() for path in self.wav_paths))

    def test_existing_output_and_input_preserved(self):
        output = self.root / 'existing.txt'
        output.write_text('keep')
        for target in (output, self.audio):
            with self.subTest(target=target):
                self.assertEqual(self.run_main(['-o', str(target)])[0], 1)
        self.assertEqual(output.read_text(), 'keep')
        self.assertEqual(self.audio.read_bytes(), b'audio')
        self.assertFalse(self.wav_paths)

    def test_missing_input(self):
        self.audio.unlink()
        self.assertEqual(self.run_main()[0], 1)
        self.assertFalse(self.wav_paths)

    def test_missing_ffmpeg(self):
        with mock.patch.object(sys, 'argv', ['transcribe', str(self.audio)]), \
             mock.patch.object(voice.shutil, 'which', return_value=None), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(voice.main(), 1)

    def test_missing_dependency_cleanup(self):
        self.assertEqual(self.run_main(missing_dependency=True)[0], 1)
        self.assertTrue(all(not path.parent.exists() for path in self.wav_paths))

    def test_model_failure_cleanup_and_private_error_hidden(self):
        code, stdout, stderr = self.run_main(model_error=True)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, '')
        self.assertNotIn('private details', stderr)
        self.assertTrue(all(not path.parent.exists() for path in self.wav_paths))

    def test_conversion_failure_cleanup(self):
        def failing(argv, **kwargs):
            self.convert(argv, **kwargs)
            return types.SimpleNamespace(returncode=1)
        self.assertEqual(self.run_main(converter=failing)[0], 1)
        self.assertTrue(all(not path.parent.exists() for path in self.wav_paths))

    def test_output_appearing_during_transcription_not_overwritten(self):
        output = self.root / 'race.txt'
        def racing(argv, **kwargs):
            output.write_text('keep')
            return self.convert(argv, **kwargs)
        self.assertEqual(self.run_main(['-o', str(output)], converter=racing)[0], 1)
        self.assertEqual(output.read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
