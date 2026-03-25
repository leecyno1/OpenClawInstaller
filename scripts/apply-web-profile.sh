#!/bin/bash

set -euo pipefail

PROFILE_FILE="${1:-}"
CONFIG_DIR="${HOME}/.openclaw"
ENV_FILE="${CONFIG_DIR}/env"
PROFILE_DIR="${CONFIG_DIR}/profile"
PROFILE_JSON="${PROFILE_DIR}/web-config-profile.json"
LOADOUT_JSON="${PROFILE_DIR}/web-config-loadout.json"

if [ -z "$PROFILE_FILE" ] || [ ! -f "$PROFILE_FILE" ]; then
  echo "用法: bash scripts/apply-web-profile.sh <profile.json>" >&2
  exit 1
fi

mkdir -p "$PROFILE_DIR"
cp "$PROFILE_FILE" "$PROFILE_JSON"

python3 - "$PROFILE_FILE" "$LOADOUT_JSON" <<'PY'
import json, pathlib, sys
profile_path = pathlib.Path(sys.argv[1])
loadout_path = pathlib.Path(sys.argv[2])
data = json.loads(profile_path.read_text())
loadout = {
    "persona": data.get("persona", {}),
    "routing": data.get("routing", {}),
    "loadout": data.get("loadout", {}),
    "uiState": data.get("uiState", {}),
}
loadout_path.write_text(json.dumps(loadout, ensure_ascii=False, indent=2))
PY

extract_json() {
  local expr="$1"
  python3 - "$PROFILE_FILE" "$expr" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
expr = sys.argv[2].split('.')
cur = data
for part in expr:
    if not part:
        continue
    cur = cur.get(part, "")
if isinstance(cur, (list, dict)):
    print(json.dumps(cur, ensure_ascii=False))
else:
    print(cur if cur is not None else "")
PY
}

upsert_env_export() {
  local key="$1"
  local value="$2"
  mkdir -p "$(dirname "$ENV_FILE")"
  touch "$ENV_FILE"
  local tmp_file
  tmp_file="$(mktemp)"
  awk -v k="$key" -v v="$value" '
    BEGIN { done=0 }
    $0 ~ "^export " k "=" { print "export " k "=" v; done=1; next }
    { print }
    END { if (!done) print "export " k "=" v }
  ' "$ENV_FILE" > "$tmp_file" && mv "$tmp_file" "$ENV_FILE"
}

persona_id="$(extract_json 'persona.id')"
model_route="$(extract_json 'routing.modelRoute')"
token_rule="$(extract_json 'routing.tokenRule')"
skill_pack="$(extract_json 'routing.skillPack')"
security_json="$(extract_json 'routing.security')"
hotbar_json="$(extract_json 'loadout.hotbar')"
pinned_json="$(extract_json 'loadout.pinnedSkills')"
inventory_json="$(extract_json 'loadout.inventory')"
equipped_json="$(extract_json 'loadout.equipped')"

upsert_env_export "OPENCLAW_PERSONA_ROLE" "$persona_id"
upsert_env_export "OPENCLAW_RULE_PROFILE" "$token_rule"
upsert_env_export "OPENCLAW_WEB_SKILL_PACK" "$skill_pack"
upsert_env_export "OPENCLAW_WEB_MODEL_ROUTE" "$model_route"
upsert_env_export "OPENCLAW_WEB_SECURITY" "'$security_json'"
upsert_env_export "OPENCLAW_WEB_HOTBAR" "'$hotbar_json'"
upsert_env_export "OPENCLAW_WEB_PINNED_SKILLS" "'$pinned_json'"
upsert_env_export "OPENCLAW_WEB_INVENTORY" "'$inventory_json'"
upsert_env_export "OPENCLAW_WEB_EQUIPPED" "'$equipped_json'"

if command -v openclaw >/dev/null 2>&1; then
  openclaw config set "vendor.control.persona.role.id" "$persona_id" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.routing.mode" "$model_route" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.profile.skillPack" "$skill_pack" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.profile.security" "$security_json" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.profile.hotbar" "$hotbar_json" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.profile.pinnedSkills" "$pinned_json" >/dev/null 2>&1 || true
  openclaw config set "vendor.control.profile.equipped" "$equipped_json" >/dev/null 2>&1 || true
fi

echo "[INFO] Web 配置档案已写入: $PROFILE_JSON"
echo "[INFO] Web 构筑快照已写入: $LOADOUT_JSON"
echo "[INFO] 环境变量已同步到: $ENV_FILE"
