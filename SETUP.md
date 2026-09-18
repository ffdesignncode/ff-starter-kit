# Настройка окружения студента — инструкция для Claude Code

> Это инструкция **для Claude Code**. Студент дал тебе папку `ff-starter-kit/`
> и сказал «настрой меня по SETUP.md». Выполняй по шагам, после каждого шага
> коротко отчитывайся (1–2 строки). Спрашивай студента только там, где помечено ⚠️.
>
> Железные правила на всю настройку:
> - **Не выдумывай.** Если команда не сработала — скажи честно и покажи вывод,
>   не придумывай «обходы» и не делай вид, что всё в порядке.
> - Студент — новичок, возможно не разработчик. Объясняй без жаргона, одно
>   действие за раз.
> - Целевая платформа этого файла — **macOS**. Если у студента Windows —
>   выполняй инструкцию `SETUP_WINDOWS.md` из этой же папки; этот файл — только
>   для macOS.

---

## 0. Предпосылки (проверить, не выдумывать)

Выполни и покажи студенту, чего не хватает:

```bash
uname -s                # должно быть Darwin (macOS)
claude --version        # Claude Code установлен (если нет — шаг 7)
git --version
which brew              # Homebrew
python3 --version
ffmpeg -version | head -1
which whisper-cli       # whisper-cpp (может ещё не стоять — нормально)
gh --version            # GitHub CLI (может ещё не стоять — нормально)
```

- Чего нет — ставим в шагах ниже. Не пропускай проверки «на глаз».
- Запомни вывод `uname -m` (arm64 или x86_64) — пригодится для путей Homebrew.

---

## 1. git

```bash
git --version
```

На macOS git обычно уже есть (при первом вызове система может предложить
установить Command Line Tools — ⚠️ студент подтверждает установку в диалоге).
Если git нет и диалога не было: `xcode-select --install`.

---

## 2. Homebrew (macOS)

```bash
which brew
```

Если нет — установи:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

⚠️ Установщик попросит пароль от компьютера — **пароль вводит студент лично**,
ты его не видишь и не запрашиваешь.

После установки добавь brew в PATH, если инсталлятор это сказал:

```bash
# на Apple Silicon (arm64):
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
# на Intel (x86_64) brew встаёт в /usr/local и обычно уже в PATH
```

Проверка: `brew --version`.

---

## 3. python3

```bash
python3 --version
```

Если нет или версия древняя — `brew install python@3`.

---

## 4. ffmpeg

```bash
brew install ffmpeg
ffmpeg -version | head -1
```

Нужен для конвертации голосовых сообщений перед расшифровкой.

---

## 5. whisper-cpp + модель распознавания речи

Это локальный расшифровщик голоса в текст: бесплатный, работает без интернета,
ничего никуда не отправляет.

```bash
brew install whisper-cpp
which whisper-cli
```

Скачай модель (храним в общем месте, не в проекте):

```bash
mkdir -p ~/.local/share/whisper-cpp
curl -L -o ~/.local/share/whisper-cpp/ggml-small.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
```

Модель `small` (~466 МБ) — хороший баланс скорости и качества для русского.
Если студент хочет качество выше и не боится ждать — можно `ggml-large-v3-turbo.bin`
(~1.6 ГБ) в ту же папку; тогда в скилле voice-notes поменять путь модели.

Проверка на реальном звуке: сгенерируй 3 секунды тишины и прогони — важно, что
команда отрабатывает без ошибок (текст будет пустым, это нормально):

```bash
ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 3 -y /tmp/whisper_test.wav
whisper-cli -m ~/.local/share/whisper-cpp/ggml-small.bin -l ru -f /tmp/whisper_test.wav
rm /tmp/whisper_test.wav
```

---

## 6. Диктовка: голос → текст (самый простой способ)

Платные приложения для диктовки не нужны. Схема:

1. ⚠️ Студент надиктовывает мысль **голосовым сообщением или видео-кружком в
   Telegram** (хоть самому себе в «Избранное») и скачивает файл на компьютер
   (в десктопном Telegram: правый клик → «Сохранить как…»).
2. Claude забирает файл и расшифровывает локально через whisper-cpp:
   ```bash
   ffmpeg -i voice.ogg -ar 16000 -ac 1 -c:a pcm_s16le -y /tmp/voice.wav
   whisper-cli -m ~/.local/share/whisper-cpp/ggml-small.bin -l ru -f /tmp/voice.wav
   ```
3. Расшифровка ложится в текстовый файл и используется как задание для Claude.

Весь этот процесс упакован в скилл `skills/voice-notes/SKILL.md` — скопируешь
его в шаге 8. Студенту достаточно сказать: «расшифруй голосовое <файл>».

---

## 7. Claude Code: установка и вход

```bash
claude --version
```

Если нет:

```bash
brew install --cask claude-code
```

⚠️ **Вход выполняет студент лично.** Запусти `claude`, дальше студент выбирает
вход с подпиской (Claude Pro/Max) — откроется браузер, он логинится в свой
аккаунт claude.com. Без подписки работать не будет; если подписки нет —
студент оформляет её сам, это его действие и его аккаунт.

---

## 8. Хуки, output-style, настройки, скиллы

Скопируй файлы пакета в `~/.claude/`:

```bash
KIT=~/Projects/ff-starter-kit   # поправь, если папка лежит elsewhere

mkdir -p ~/.claude/hooks ~/.claude/output-styles ~/.claude/skills
cp "$KIT"/hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
cp "$KIT"/output-styles/student.md ~/.claude/output-styles/
cp -R "$KIT"/skills/check-setup ~/.claude/skills/
cp -R "$KIT"/skills/voice-notes ~/.claude/skills/
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
`~/.claude/projects/<проект>/memory/`. Память студента сейчас пустая — это
нормально, чужую память копировать **нельзя** (там чужие факты).

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

⚠️ Спроси студента, как назвать рабочую папку, — `my-project` это заглушка.

---

## 10. GitHub CLI — ⚠️ логинится человек

Студент не обязан учить git: **все git-команды выполняешь ты** (clone/pull/push,
коммиты по просьбе «сохрани»). Единственное действие студента лично — один раз
войти в GitHub через браузер.

```bash
brew install gh
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

## 11. Финальный чек-лист (прогони в конце и покажи студенту)

```bash
echo "== версии =="
git --version
brew --version | head -1
python3 --version
ffmpeg -version | head -1
whisper-cli --help >/dev/null 2>&1 && echo "whisper-cli: OK" || echo "whisper-cli: НЕТ"
gh --version | head -1
claude --version

echo "== модель whisper =="
ls -lh ~/.local/share/whisper-cpp/*.bin

echo "== хуки и стили =="
ls -l ~/.claude/hooks/            # 3 .sh, все с +x
ls ~/.claude/output-styles/       # student.md
ls ~/.claude/skills/              # check-setup, voice-notes

echo "== settings.json =="
python3 -c "import json;d=json.load(open('$HOME/.claude/settings.json'));print('outputStyle:',d.get('outputStyle'));print('hooks:',list(d.get('hooks',{})))"

echo "== github =="
gh auth status
```

В новой сессии Claude: убедись, что виден инжект «🛑 ANTI-FABRICATION CHECK»
и работает output-style `student`.

Дополнительно прогони скилл `check-setup` — он выдаёт тот же отчёт таблицей.

Если что-то не сошлось — не говори «всё работает». Покажи студенту, что именно
не поднялось, и предложи обратиться к боту поддержки курса.
