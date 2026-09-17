#!/usr/bin/env bash
# SessionStart hook (универсальный).
# Если в текущем проекте есть docs/SESSION_STATE.md — подгружает его
# в контекст сессии. Вне проекта с таким файлом молча ничего не делает.

set -u

CUR_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
SESSION_STATE="$CUR_DIR/docs/SESSION_STATE.md"

[ -f "$SESSION_STATE" ] || exit 0

cat <<HDR
## Загружено состояние проекта (docs/SESSION_STATE.md)

Авто-инъекция при старте сессии. Это сохранённое состояние работы — учитывай его.

$(cat "$SESSION_STATE")

---
Конец авто-инъекции. Если состояние устарело — уточни у пользователя и обнови файл.
HDR
