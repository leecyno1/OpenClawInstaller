#!/usr/bin/env bash
set -euo pipefail

PORT="${CONFIG_UI_PORT:-18188}"
HOST="${CONFIG_UI_HOST:-0.0.0.0}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="$ROOT_DIR/web-config"
PID_FILE="/tmp/openclaw-config-ui-${PORT}.pid"
LOG_FILE="/tmp/openclaw-config-ui-${PORT}.log"

usage() {
  cat <<USAGE
Usage: $0 {start|stop|restart|status}
  CONFIG_UI_HOST=0.0.0.0 CONFIG_UI_PORT=18188 $0 start
USAGE
}

is_running() {
  local pid
  pid="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
  [[ -n "$pid" ]]
}

start_ui() {
  if [[ ! -d "$UI_DIR" ]]; then
    echo "[ERROR] UI directory not found: $UI_DIR"
    exit 1
  fi

  if is_running; then
    local existing_pid
    existing_pid="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
    if [[ -n "$existing_pid" ]]; then
      echo "$existing_pid" > "$PID_FILE"
    fi
    echo "[INFO] Config UI already running (PID: ${existing_pid:-unknown}, port: $PORT)"
    exit 0
  fi

  nohup python3 -m http.server "$PORT" --bind "$HOST" --directory "$UI_DIR" >"$LOG_FILE" 2>&1 < /dev/null &
  local pid
  pid="$!"

  local ok=0
  for _ in {1..20}; do
    if curl -fsS --max-time 1 "http://127.0.0.1:$PORT/" >/dev/null 2>&1; then
      ok=1
      break
    fi
    sleep 0.2
  done

  if [[ "$ok" -eq 1 ]]; then
    local listen_pid
    listen_pid="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
    echo "${listen_pid:-$pid}" > "$PID_FILE"
    echo "[OK] Config UI started: http://$HOST:$PORT (PID: ${listen_pid:-$pid})"
  else
    rm -f "$PID_FILE"
    echo "[ERROR] Failed to start Config UI. Check log: $LOG_FILE"
    exit 1
  fi
}

stop_ui() {
  if ! is_running; then
    echo "[INFO] Config UI is not running on port $PORT"
    rm -f "$PID_FILE"
    return 0
  fi

  local pid_by_file pid_by_port
  pid_by_file="$(cat "$PID_FILE" 2>/dev/null || true)"
  pid_by_port="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"

  if [[ -n "$pid_by_file" ]]; then
    kill "$pid_by_file" 2>/dev/null || true
  fi
  if [[ -n "$pid_by_port" ]] && [[ "$pid_by_port" != "$pid_by_file" ]]; then
    kill "$pid_by_port" 2>/dev/null || true
  fi

  sleep 1
  pid_by_port="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
  if [[ -n "$pid_by_port" ]]; then
    kill -9 "$pid_by_port" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
  echo "[OK] Config UI stopped (PID: ${pid_by_file:-$pid_by_port})"
}

status_ui() {
  if is_running; then
    local pid
    pid="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
    echo "[OK] Running: http://$HOST:$PORT (PID: $pid)"
  else
    echo "[INFO] Not running on port $PORT"
  fi
}

case "${1:-}" in
  start)
    start_ui
    ;;
  stop)
    stop_ui
    ;;
  restart)
    stop_ui || true
    start_ui
    ;;
  status)
    status_ui
    ;;
  *)
    usage
    exit 1
    ;;
esac
