# Настройка окружения студента на Windows — инструкция для Claude Code и Codex

> **Если ты — Codex** (а не Claude Code): шаги 0–6, 9 и 10 выполняй как есть
> (в шаге 9 факты о студенте пиши в `docs\USER.md` проекта, а не в `memory/`,
> и копируй `AGENTS.md` вместо `CLAUDE.md`). **Вместо шагов 7, 8 и 11 выполни
> раздел 13 «Codex»**, а в финальном чек-листе — его проверки.

> Это инструкция **для Claude Code**. Студент дал тебе папку `ff-starter-kit/`
> и сказал «настрой меня по SETUP_WINDOWS.md». Выполняй по шагам, после каждого
> шага коротко отчитывайся (1–2 строки). Спрашивай студента только там, где
> помечено ⚠️.
>
> Железные правила на всю настройку:
> - **Не выдумывай.** Если команда не сработала — скажи честно и покажи вывод,
>   не придумывай «обходы» и не делай вид, что всё в порядке.
> - Студент — новичок, возможно не разработчик. Объясняй без жаргона, одно
>   действие за раз.
> - Целевая платформа этого файла — **Windows 10/11** (нативно, без WSL).
>   Если у студента macOS — выполняй `SETUP.md` из этой же папки.

Про пути: в инструкции два вида записи — это одни и те же места:

- **PowerShell**: `%USERPROFILE%\.claude\` (в командах PowerShell — `$env:USERPROFILE\.claude\`)
- **bash** (Git Bash, через него Claude Code выполняет команды на Windows): `~/.claude/`

Команды шагов — для **PowerShell**, если не сказано иное. Если ты выполняешь
команды через свой bash-инструмент, пути вида `~` и команды `cp`/`ls` тоже
работают — Git for Windows (шаг 1) даёт полноценный bash.

⚠️ Общая особенность Windows: **после установки почти любой программы через
winget нужно закрыть и заново открыть терминал**, чтобы обновился PATH. Если
свежепоставленная команда «не найдена» — сначала предложи студенту переоткрыть
PowerShell (или сам начни новую сессию оболочки), и только потом ищи другие
причины.

Если ты запущен в десктоп-приложении (Claude — вкладка Code, или Codex) и
переоткрыть терминал не можешь — подтяни свежий PATH прямо в команде:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
```

Не помогло — попроси студента полностью закрыть и заново открыть приложение,
потом продолжай с того же шага. Студент — новичок: ставь программы сам и не
отправляй его в PowerShell без крайней необходимости.

---

## 0. Предпосылки (проверить, не выдумывать)

Выполни в PowerShell и покажи студенту, чего не хватает:

```powershell
$PSVersionTable.PSVersion   # версия PowerShell (5.1 или 7.x — обе подойдут)
Get-Command git, bash, winget, python, ffmpeg, gh, claude -ErrorAction SilentlyContinue
```

`Get-Command` выведет найденные команды; чего нет в списке — того нет в системе,
ставим в шагах ниже. Не пропускай проверки «на глаз».

Проверь VPN (Claude и Codex из России не работают, а смена IP — риск блокировки
аккаунта):

```powershell
curl.exe -s ipinfo.io
```

- `"country"` должна быть **не `RU`**. Если `RU` — остановись и отправь студента
  к `VPN.md` (там два способа и проверка). Без VPN дальнейшие шаги с входом
  в аккаунты бессмысленны.
- Покажи студенту `"ip"` и попроси запомнить: при следующих проверках адрес
  должен быть тем же самым.

---

## 1. git (Git for Windows — он же даёт bash для хуков)

```powershell
git --version
```

Если нет — установи:

```powershell
winget install Git.Git --accept-package-agreements --accept-source-agreements
```

Важно: ставим именно **Git for Windows**, потому что вместе с ним приходит
`bash` (Git Bash) — он нужен для хуков Claude Code из шага 8, которые написаны
на bash. ⚠️ После установки переоткрой терминал.

Проверка — обе команды должны ответить версией:

```powershell
git --version
bash --version
```

Если `bash` не находится, хотя git встал — честно скажи студенту и проверь,
есть ли `C:\Program Files\Git\bin\bash.exe`. Не выдумывай.

---

## 2. winget (менеджер пакетов Windows)

```powershell
winget --version
```

winget — это стандартный установщик программ Microsoft, дальше всё ставим
через него. Если команда не найдена (бывает на старых Windows 10):

⚠️ **Студент ставит лично**: открыть **Microsoft Store**, найти приложение
**«Установщик приложения»** (App Installer) от Microsoft и нажать «Получить».
Это бесплатно и официально. После установки — переоткрыть PowerShell.

Если Microsoft Store на машине нет или не открывается — не выдумывай обходы:
скажи студенту честно и предложи обратиться к боту поддержки курса.

---

## 3. python

```powershell
python --version
```

На Windows команда называется `python` (не `python3`).

Если нет или версия ниже 3.10 — установи:

```powershell
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
```

⚠️ После установки переоткрой терминал и повтори `python --version`.

Известный подвох Windows: если `python` открывает Microsoft Store вместо запуска —
это системный «псевдоним-заглушка». ⚠️ Студент лично: Параметры → Приложения →
Дополнительные параметры приложений → «Псевдонимы выполнения приложений» →
отключить переключатели у `python.exe` / `python3.exe`. Если не сработало —
скажи честно и попроси помощь курса.

---

## 4. ffmpeg

```powershell
winget install Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
```

Если пакет не нашёлся — альтернатива: `winget install ffmpeg`
(резолвится в тот же Gyan.FFmpeg). Если и это не сработало — покажи вывод
студенту как есть, не выдумывай другой источник.

⚠️ После установки переоткрой терминал, затем проверка:

```powershell
ffmpeg -version | Select-Object -First 1
```

ffmpeg нужен для конвертации голосовых сообщений перед расшифровкой.

---

## 5. faster-whisper + скрипт расшифровки

Локальный расшифровщик голоса в текст: бесплатный, работает без интернета
(после скачивания модели), ничего никуда не отправляет. На Windows вместо
whisper-cpp используем **faster-whisper** — тот же движок распознавания,
ставится одной командой:

```powershell
pip install faster-whisper
```

Если `pip` не находится — `python -m pip install faster-whisper`.

Расшифровку выполняет скрипт пакета `scripts/transcribe.py` — он сам
конвертирует файл через ffmpeg и прогоняет модель. Проверка (выполняй из
папки пакета):

```powershell
python scripts\transcribe.py --help
```

Должна вывестись справка по аргументам.

Модель `small` (~466 МБ) скачается автоматически при **первой реальной
расшифровке**. Прогони проверку на реальном звуке — сгенерируй 3 секунды
тишины; важно, что всё отрабатывает без ошибок (текст будет пустым, это
нормально, а модель заодно скачается):

```powershell
ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 3 -y whisper_test.wav
python scripts\transcribe.py whisper_test.wav
del whisper_test.wav
```

Если студент хочет качество выше и не боится ждать — можно использовать
модель `medium` или `large-v3` (флаг `--model` у скрипта); скачаются при
первом запуске так же автоматически.

---

## 6. Диктовка: голос → текст (самый простой способ)

Платные приложения для диктовки не нужны. Схема:

1. ⚠️ Студент надиктовывает мысль **голосовым сообщением или видео-кружком в
   Telegram** (хоть самому себе в «Избранное») и скачивает файл на компьютер
   (в десктопном Telegram: правый клик → «Сохранить как…»).
2. Claude забирает файл и расшифровывает локально скриптом пакета:
   ```powershell
   python <папка пакета>\scripts\transcribe.py voice.ogg
   ```
   (в bash: `python ~/Projects/ff-starter-kit/scripts/transcribe.py voice.ogg`)
3. Расшифровка ложится в текстовый файл (флаг `-o текст.txt`) и используется
   как задание для Claude.

Весь этот процесс упакован в скилл `skills/voice-notes/SKILL.md` — скопируешь
его в шаге 8. Студенту достаточно сказать: «расшифруй голосовое <файл>».

---

## 7. Claude Code: установка и вход

Если ты запущен в десктоп-приложении Claude (вкладка Code), Claude Code уже
работает и вход уже выполнен. Отдельная версия для PowerShell (CLI) не обязательна:
пропусти этот шаг, а в чек-листе отметь «работает в приложении». Хуки, скиллы
и настройки из шага 8 действуют и в приложении.

```powershell
claude --version
```

Если нет — официальный установщик Windows:

```powershell
irm https://claude.ai/install.ps1 | iex
```

⚠️ После установки переоткрой терминал и повтори `claude --version`.

Если установщик не сработал — fallback через npm (скажи студенту, что ставим
запасным способом):

```powershell
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
# переоткрыть терминал, затем:
npm install -g @anthropic-ai/claude-code
```

⚠️ **Вход выполняет студент лично.** Запусти `claude`, дальше студент выбирает
вход с подпиской (Claude Pro/Max) — откроется браузер, он логинится в свой
аккаунт claude.com. Без подписки работать не будет; если подписки нет —
студент оформляет её сам, это его действие и его аккаунт.

---

## 8. Хуки, output-style, настройки, скиллы

**Зачем этот шаг (частый вопрос студента «надо ли обвязку?»): надо.**
Файлы в папке пакета — это шаблоны. Они начинают работать только после
копирования в `~/.claude/`: Claude Code читает хуки, стили и настройки именно
оттуда, а не из папки пакета. Без этого шага хуки и стиль не активируются.
Копирование делаешь ты (Claude), студенту вручную ничего копировать не нужно.

Целевая папка — `%USERPROFILE%\.claude\` (PowerShell: `$env:USERPROFILE\.claude\`,
bash: `~/.claude/`).

Копирование удобнее сделать через bash (Git Bash из шага 1):

```bash
KIT=~/Projects/ff-starter-kit   # поправь, если папка лежит в другом месте

mkdir -p ~/.claude/hooks ~/.claude/output-styles ~/.claude/skills
cp "$KIT"/hooks/*.sh ~/.claude/hooks/
cp "$KIT"/output-styles/student.md ~/.claude/output-styles/
cp -R "$KIT"/skills/check-setup ~/.claude/skills/
cp -R "$KIT"/skills/voice-notes ~/.claude/skills/
```

То же самое в PowerShell, если bash под рукой нет:

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.claude\hooks, $env:USERPROFILE\.claude\output-styles, $env:USERPROFILE\.claude\skills
Copy-Item "$KIT\hooks\*.sh" $env:USERPROFILE\.claude\hooks\
Copy-Item "$KIT\output-styles\student.md" $env:USERPROFILE\.claude\output-styles\
Copy-Item -Recurse "$KIT\skills\check-setup", "$KIT\skills\voice-notes" $env:USERPROFILE\.claude\skills\
```

Хуки `.sh` остаются bash-скриптами — на Windows их выполняет bash из Git for
Windows (шаг 1), в `settings.snippet.json` вызов уже записан как
`bash "$HOME/.claude/hooks/<имя>.sh"`, это работает и на macOS, и на Windows.

Проверка, что хук реально запускается (должен вывести JSON с текстом
«ANTI-FABRICATION CHECK»):

```bash
bash ~/.claude/hooks/anti_fabrication_check.sh
```

Слей `settings.snippet.json` в `~/.claude/settings.json`:

- Если `settings.json` ещё нет — просто скопируй сниппет целиком (поле
  `_comment` удали).
- Если файл есть — аккуратно добавь ключи `outputStyle` и `hooks`,
  **не снося** существующие настройки. Покажи студенту итоговый файл.

Что даёт каждый хук:

- **anti_fabrication_check.sh** — перед каждым ответом напоминает: не выдумывать,
  открыть источник, признавать незнание.
- **session_start.sh** — в начале сессии подгружает `docs/SESSION_STATE.md`
  текущего проекта (если файл есть).
- **pre_compact.sh** — перед сжатием контекста напоминает обновить
  `docs/SESSION_STATE.md`, чтобы память не терялась.

---

## 9. Стартовая файловая память — ⚠️ разговор со студентом

Claude Code умеет хранить факты между сессиями в
`%USERPROFILE%\.claude\projects\<проект>\memory\`. Память студента сейчас
пустая — это нормально, чужую память копировать **нельзя** (там чужие факты).

⚠️ **Спроси студента** (коротко, одним сообщением, нумерованным списком):

1. Как тебя зовут и как к тебе обращаться?
2. Чем занимаешься / чему учишься?
3. Какая цель на ближайшие месяцы — что хочешь делать с Claude Code?
4. Ты разработчик или нет?
5. Какие правила общения тебе важны? (предложи дефолт: короткие ответы,
   без воды, не выдумывать, одно действие за раз)

Ответы запиши в память (например `memory/user_profile.md` + индекс `MEMORY.md`).
Дальше память будет пополняться сама по ходу работы — это и есть «становиться
умнее».

Также скопируй шаблоны в будущую рабочую папку студента (или сразу создай её):

```bash
mkdir -p ~/Projects/my-project/docs
cp "$KIT"/CLAUDE.md ~/Projects/my-project/
cp "$KIT"/ARCHITECTURE.md ~/Projects/my-project/
cp "$KIT"/docs/SESSION_STATE.md ~/Projects/my-project/docs/
```

(в PowerShell папка будет `$env:USERPROFILE\Projects\my-project` — то же место).

⚠️ Спроси студента, как назвать рабочую папку, — `my-project` это заглушка.

---

## 10. GitHub CLI — ⚠️ логинится человек

Студент не обязан учить git: **все git-команды выполняешь ты** (clone/pull/push,
коммиты по просьбе «сохрани»). Единственное действие студента лично — один раз
войти в GitHub через браузер.

```powershell
winget install GitHub.cli --accept-package-agreements --accept-source-agreements
```

⚠️ Переоткрой терминал, затем:

```powershell
gh auth login
```

⚠️ Подскажи студенту выбор по шагам:

1. `GitHub.com` → 2. `HTTPS` → 3. на вопрос про вход через браузер — **Yes** →
4. gh покажет код вида `XXXX-XXXX` — студент копирует его, жмёт Enter →
5. в открывшемся браузере студент входит в **свой** GitHub-аккаунт,
   вставляет код, жмёт Authorize.

Проверка: `gh auth status`.

Если вход не идёт — **не выдумывай обходы с паролями и токенами**. Скажи
студенту, что нужен вход в GitHub, и предложи обратиться за помощью к курсу.

---

## 11. Figma — подключение MCP-сервера

Частый вопрос: «Фигму подключаем через connectors или скиллом?» — **через
connectors (MCP)**, отдельного скилла нет. Но сначала MCP-сервер надо включить
в самой Figma.

Требования:

- **Десктопное приложение Figma** (не браузер) — MCP-сервер живёт только в нём.
- Аккаунт Figma с **Dev или Full seat** на платном тарифе
  (Professional/Organization/Enterprise). На бесплатном тарифе сервера нет.

Шаг 1 — ⚠️ **делает студент вручную** в десктопной Figma:

1. Открыть любой файл в десктопном приложении Figma.
2. Переключиться на вкладку **Dev** (Dev Mode).
3. Включить **MCP server** (Enable Dev Mode MCP Server).

Шаг 2 — подключи connector в Claude Code (делаешь ты, команда одна и та же,
что на macOS):

```powershell
claude mcp add --transport http figma http://127.0.0.1:3845/mcp
```

Проверка:

```powershell
claude mcp list
```

В списке должен быть `figma` со статусом подключения. Внутри сессии Claude Code
то же самое показывает команда `/mcp`.

⚠️ Подвох: сервер работает, только пока открыто десктопное приложение Figma с
включённым MCP. Если `figma` не подключается — сначала проверь, что Figma
запущена и в ней открыт файл с включённым сервером во вкладке Dev.

---

## 12. Финальный чек-лист (прогони в конце и покажи студенту)

```powershell
echo "== версии =="
git --version
bash --version | Select-Object -First 1
winget --version
python --version
ffmpeg -version | Select-Object -First 1
pip show faster-whisper
gh --version | Select-Object -First 1
claude --version

echo "== обвязка =="
Get-ChildItem $env:USERPROFILE\.claude\hooks          # 3 файла .sh
Get-ChildItem $env:USERPROFILE\.claude\output-styles  # student.md
Get-ChildItem $env:USERPROFILE\.claude\skills         # check-setup, voice-notes

echo "== settings.json =="
Get-Content $env:USERPROFILE\.claude\settings.json

echo "== github =="
gh auth status

echo "== figma MCP =="
claude mcp list | Select-String -Pattern figma
```

Отдельно проверь, что хук запускается через bash (должен вывести JSON):

```bash
bash ~/.claude/hooks/anti_fabrication_check.sh
```

И что расшифровка работает (модель `small` при этом скачается, если ещё не
скачана — это нормально, ~466 МБ один раз):

```powershell
cd <папка пакета>
ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 3 -y whisper_test.wav
python scripts\transcribe.py whisper_test.wav
del whisper_test.wav
```

В новой сессии Claude: убедись, что виден инжект «🛑 ANTI-FABRICATION CHECK»
и работает output-style `student`.

Дополнительно прогони скилл `check-setup` — он выдаёт тот же отчёт таблицей.

Если что-то не сошлось — не говори «всё работает». Покажи студенту, что именно
не поднялось, и предложи обратиться к боту поддержки курса.

---

## 13. Codex (только если ты — Codex, а не Claude Code)

Codex — ИИ-агент от OpenAI. Он работает в **приложении ChatGPT для компьютера**
(режим Codex) и в терминале (Codex CLI). Приложение и CLI делят одну настройку
`%USERPROFILE%\.codex\config.toml` и одни и те же скиллы, поэтому окружение
одинаковое. Нужна подписка ChatGPT (Plus или выше) — оформляет студент сам.

### 13.1. Приложение и вход — ⚠️ делает студент

Приложение студент скачивает сам: https://chatgpt.com/download → вход в свой
аккаунт ChatGPT → режим **Codex** → открыть папку `ff-starter-kit`. Раз ты это
читаешь — этот шаг уже сделан.

CLI (по желанию студента, для работы в терминале), в новом окне PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Переоткрой PowerShell, первый запуск `codex` → **Sign in with ChatGPT** —
входит студент лично.

### 13.2. Скиллы

Codex читает скиллы из `%USERPROFILE%\.agents\skills\` (формат `SKILL.md` тот
же, что у Claude Code):

```powershell
$KIT = "$env:USERPROFILE\Projects\ff-starter-kit"   # поправь, если папка лежит в другом месте

New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
Copy-Item -Recurse -Force "$KIT\skills\check-setup" "$env:USERPROFILE\.agents\skills\"
Copy-Item -Recurse -Force "$KIT\skills\voice-notes" "$env:USERPROFILE\.agents\skills\"
Get-ChildItem "$env:USERPROFILE\.agents\skills"
```

Хуков, как у Claude Code (напоминания про анти-фабрикацию и память), в этой
настройке нет — правила работы целиком лежат в `AGENTS.md`, честно скажи об
этом студенту.

### 13.3. Правила и память проекта

В шаге 9 вместо `CLAUDE.md` скопируй в рабочую папку студента `AGENTS.md`,
а ответы студента о себе запиши в `docs\USER.md`:

```powershell
Copy-Item "$KIT\AGENTS.md" "$env:USERPROFILE\Projects\my-project\"
```

### 13.4. Figma (MCP)

Сначала ⚠️ студент вручную включает MCP-сервер в десктопной Figma — так же,
как в шаге 11 (Dev Mode → Enable desktop MCP server; нужен платный тариф
с Dev/Full seat).

Затем добавь сервер в общую настройку Codex — допиши в
`%USERPROFILE%\.codex\config.toml` (создай файл, если его нет; существующие
настройки не трогай):

```toml
[mcp_servers.figma]
url = "http://127.0.0.1:3845/mcp"
```

То же самое можно сделать командой CLI `codex mcp add figma --url http://127.0.0.1:3845/mcp`
или в приложении: Settings → MCP servers → Add server → Streamable HTTP.
После изменения настройки приложение нужно перезапустить (Restart).

Проверка (если стоит CLI):

```powershell
codex mcp list
```

### 13.5. Чек-лист Codex

```powershell
curl.exe -s ipinfo.io | Select-String country          # не RU
Get-ChildItem "$env:USERPROFILE\.agents\skills"           # check-setup, voice-notes
Select-String -Path "$env:USERPROFILE\.codex\config.toml" -Pattern "mcp_servers.figma" -Context 0,1
Test-Path "$env:USERPROFILE\Projects\my-project\AGENTS.md"
codex --version   # если CLI не ставили — ошибка «не найдено» нормальна
```

Плюс версии из шага 12 (git, winget, python, ffmpeg, faster-whisper, gh).
