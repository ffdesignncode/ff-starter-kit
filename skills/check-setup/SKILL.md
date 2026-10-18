---
name: check-setup
description: Проверка окружения студента на macOS или Windows — VPN (страна и постоянный IP), версии git/python/ffmpeg/whisper/gh/claude/codex, наличие хуков, скиллов, Figma MCP и модели распознавания. Используй, когда просят «проверь моё окружение», «всё ли настроено» или после настройки по SETUP.md / SETUP_WINDOWS.md.
---

# check-setup — проверь моё окружение

Прогоняет диагностику и выдаёт отчёт таблицей. Ничего не чинит молча:
если что-то не так — честно помечает ❌ и предлагает шаг исправления.

## Шаг 1. Определи ОС

```bash
uname -s
```

- `Darwin` → **macOS**, работай по разделу «Проверки (macOS)».
- `MINGW*` / `MSYS*` / `CYGWIN*` → **Windows** (Git Bash), работай по разделу
  «Проверки (Windows)».
- Если `uname` нет (ты в PowerShell) — это Windows, подтверди `$PSVersionTable`
  и выполняй проверки Windows в PowerShell.

## Кто ты: Claude Code или Codex

- **Claude Code** — проверяй всё, кроме строк с пометкой «Codex».
- **Codex** — пропусти строки про `~/.claude` (хуки, output-style, скиллы
  Claude, `claude mcp list`) и проверь вместо них строки с пометкой «Codex».

## Проверки (macOS)

Выполни команды ниже (по одной, без `|| true`-магии под ковром — если команда
упала, это результат проверки):

```bash
curl -s ipinfo.io                         # VPN: country не RU, ip запомнить
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
claude mcp list 2>/dev/null | grep -i figma   # Figma MCP подключён (шаг 11 SETUP.md)
ls -d ~/.agents/skills/check-setup ~/.agents/skills/voice-notes   # Codex: скиллы
grep -A1 'mcp_servers.figma' ~/.codex/config.toml                  # Codex: Figma MCP
codex --version                           # Codex CLI (необязателен, если работают в приложении)
```

Проверка исполняемости хуков:

```bash
for f in ~/.claude/hooks/*.sh; do [ -x "$f" ] && echo "OK  $f" || echo "НЕТ +x  $f"; done
```

## Проверки (Windows)

В PowerShell (в Git Bash команды версий тоже работают):

```powershell
curl.exe -s ipinfo.io                     # VPN: country не RU, ip запомнить
git --version
bash --version | Select-Object -First 1   # bash из Git for Windows — нужен хукам
winget --version
python --version                          # на Windows команда python, не python3
ffmpeg -version | Select-Object -First 1
pip show faster-whisper                   # расшифровщик голоса (шаг 5 SETUP_WINDOWS.md)
gh --version | Select-Object -First 1
claude --version
Get-ChildItem $env:USERPROFILE\.claude\hooks          # 3 файла .sh
Get-ChildItem $env:USERPROFILE\.claude\output-styles  # student.md
Get-ChildItem $env:USERPROFILE\.claude\skills         # check-setup, voice-notes
gh auth status                            # вход в GitHub выполнен
claude mcp list | Select-String -Pattern figma   # Figma MCP подключён (шаг 11 SETUP_WINDOWS.md)
Get-ChildItem $env:USERPROFILE\.agents\skills       # Codex: check-setup, voice-notes
Select-String -Path $env:USERPROFILE\.codex\config.toml -Pattern "mcp_servers.figma"   # Codex: Figma MCP
codex --version                           # Codex CLI (необязателен, если работают в приложении)
```

Проверка, что хук реально запускается через bash (должен вывести JSON с текстом
«ANTI-FABRICATION CHECK»):

```bash
bash ~/.claude/hooks/anti_fabrication_check.sh
```

## Формат отчёта

Одна таблица, без вступления и вывода. Состав строк — по ОС студента.

macOS:

| Проверка | Статус | Значение / что делать |
|---|---|---|
| ОС — macOS | ✅/❌ | … |
| VPN | ✅/❌ | страна и IP / `VPN.md` |
| git | ✅/❌ | версия / `xcode-select --install` |
| Homebrew | ✅/❌ | версия / шаг 2 SETUP.md |
| python3 | ✅/❌ | версия (≥ 3.9 достаточно, системный /usr/bin/python3 тоже считается) / `brew install python@3` |
| ffmpeg | ✅/❌ | версия / `brew install ffmpeg` |
| whisper-cli | ✅/❌ | путь / `brew install whisper-cpp` |
| модель whisper | ✅/❌ | размер файла / шаг 5 SETUP.md |
| gh | ✅/❌ | версия / `brew install gh` |
| gh-авторизация | ✅/❌ | аккаунт / `gh auth login` (шаг 10) |
| Figma MCP | ✅/❌ | connected / шаг 11 SETUP.md |
| Claude Code | ✅/❌ | версия / шаг 7 SETUP.md |
| хуки (3 шт, +x) | ✅/❌ | список / шаг 8 SETUP.md |
| output-style student | ✅/❌ | есть/нет / шаг 8 SETUP.md |
| скиллы (2 шт) | ✅/❌ | есть/нет / шаг 8 SETUP.md |
| Codex: скиллы | ✅/❌ | есть/нет / раздел 13.2 SETUP.md |
| Codex: Figma MCP | ✅/❌ | есть в config.toml / раздел 13.4 SETUP.md |

Windows:

| Проверка | Статус | Значение / что делать |
|---|---|---|
| ОС — Windows | ✅/❌ | … |
| VPN | ✅/❌ | страна и IP / `VPN.md` |
| git | ✅/❌ | версия / `winget install Git.Git` (шаг 1 SETUP_WINDOWS.md) |
| bash (Git Bash) | ✅/❌ | версия / переустановить Git for Windows, шаг 1 |
| winget | ✅/❌ | версия / шаг 2 SETUP_WINDOWS.md |
| python | ✅/❌ | версия / `winget install Python.Python.3.12` (шаг 3) |
| ffmpeg | ✅/❌ | версия / `winget install Gyan.FFmpeg` (шаг 4) |
| faster-whisper | ✅/❌ | версия / `pip install faster-whisper` (шаг 5) |
| gh | ✅/❌ | версия / `winget install GitHub.cli` (шаг 10) |
| gh-авторизация | ✅/❌ | аккаунт / `gh auth login` (шаг 10) |
| Figma MCP | ✅/❌ | connected / шаг 11 SETUP_WINDOWS.md |
| Claude Code | ✅/❌ | версия / шаг 7 SETUP_WINDOWS.md |
| хуки (3 шт) | ✅/❌ | список / шаг 8 SETUP_WINDOWS.md |
| хук запускается через bash | ✅/❌ | JSON на выводе / шаг 8 SETUP_WINDOWS.md |
| output-style student | ✅/❌ | есть/нет / шаг 8 SETUP_WINDOWS.md |
| скиллы (2 шт) | ✅/❌ | есть/нет / шаг 8 SETUP_WINDOWS.md |
| Codex: скиллы | ✅/❌ | есть/нет / раздел 13.2 SETUP_WINDOWS.md |
| Codex: Figma MCP | ✅/❌ | есть в config.toml / раздел 13.4 SETUP_WINDOWS.md |

## Правила

- Строки Claude или Codex, которые к студенту не относятся, в таблицу не включай.
- VPN со страной `RU` — главный ❌: без VPN Claude и Codex не работают,
  отправь студента к `VPN.md`.
- ❌ — это нормальный результат, не чини его без спроса. Предложи команду
  исправления и жди «давай».
- Не выдумывай: если вывод команды пуст или странный — покажи его как есть.
- Ссылаться на шаги `SETUP.md` (macOS) или `SETUP_WINDOWS.md` (Windows)
  стартового пакета.
- На Windows помни про подвох: свежеустановленная программа «не найдена» →
  сначала предложи переоткрыть терминал (обновится PATH), потом ищи причины.
