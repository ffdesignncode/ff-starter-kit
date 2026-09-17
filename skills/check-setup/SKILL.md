---
name: check-setup
description: Проверка окружения студента — версии git/brew/python3/ffmpeg/whisper-cpp/gh/claude, наличие хуков и модели whisper, права на файлы. Используй, когда просят «проверь моё окружение», «всё ли настроено» или после настройки по SETUP.md.
---

# check-setup — проверь моё окружение

Прогоняет диагностику и выдаёт отчёт таблицей. Ничего не чинит молча:
если что-то не так — честно помечает ❌ и предлагает шаг исправления.

## Что проверить

Выполни команды ниже (по одной, без `|| true`-магии под ковром — если команда
упала, это результат проверки):

```bash
uname -s                                  # Darwin = macOS
git --version
brew --version | head -1
python3 --version
ffmpeg -version | head -1
whisper-cli --help 2>&1 | head -1         # наличие whisper-cpp
gh --version | head -1
claude --version
ls -lh ~/.local/share/whisper-cpp/*.bin   # модель whisper на месте
ls -l ~/.claude/hooks/                    # 3 хука .sh, все исполняемые (rwx)
ls ~/.claude/output-styles/student.md
ls -d ~/.claude/skills/check-setup ~/.claude/skills/voice-notes
gh auth status                            # вход в GitHub выполнен
```

Проверка исполняемости хуков:

```bash
for f in ~/.claude/hooks/*.sh; do [ -x "$f" ] && echo "OK  $f" || echo "НЕТ +x  $f"; done
```

## Формат отчёта

Одна таблица, без вступления и вывода:

| Проверка | Статус | Значение / что делать |
|---|---|---|
| ОС — macOS | ✅/❌ | … |
| git | ✅/❌ | версия / `xcode-select --install` |
| Homebrew | ✅/❌ | версия / шаг 2 SETUP.md |
| python3 | ✅/❌ | версия / `brew install python@3` |
| ffmpeg | ✅/❌ | версия / `brew install ffmpeg` |
| whisper-cli | ✅/❌ | путь / `brew install whisper-cpp` |
| модель whisper | ✅/❌ | размер файла / шаг 5 SETUP.md |
| gh | ✅/❌ | версия / `brew install gh` |
| gh-авторизация | ✅/❌ | аккаунт / `gh auth login` (шаг 10) |
| Claude Code | ✅/❌ | версия / шаг 7 SETUP.md |
| хуки (3 шт, +x) | ✅/❌ | список / шаг 8 SETUP.md |
| output-style student | ✅/❌ | есть/нет / шаг 8 SETUP.md |
| скиллы (2 шт) | ✅/❌ | есть/нет / шаг 8 SETUP.md |

## Правила

- ❌ — это нормальный результат, не чини его без спроса. Предложи команду
  исправления и жди «давай».
- Не выдумывай: если вывод команды пуст или странный — покажи его как есть.
- Ссылаться на шаги `SETUP.md` стартового пакета.
