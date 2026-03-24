#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import filecmp
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / 'skills' / 'default'
REPORT_PATH = REPO_ROOT / 'docs' / 'skills-update-report.md'
LOCAL_SOURCE_ROOTS = [
    Path.home() / '.openclaw' / 'skills',
    Path('/Users/lichengyin/.codex/skills'),
]
AGENTMAIL_REPO = 'https://github.com/agentmail-to/agentmail-skills.git'
AGENTMAIL_SKILLS = {'agentmail', 'agentmail-cli', 'agentmail-mcp', 'agentmail-toolkit'}
IGNORE_NAMES = {'.DS_Store', 'GUIDE.md'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def snapshot_tree(root: Path) -> dict[str, str]:
    items: dict[str, str] = {}
    if not root.exists():
        return items
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if any(part in IGNORE_NAMES for part in path.parts):
            continue
        if path.is_dir():
            items[rel + '/'] = 'dir'
        elif path.is_file():
            items[rel] = sha256_file(path)
    return items


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def clone_agentmail_repo(tmp_root: Path) -> Path:
    repo_dir = tmp_root / 'agentmail-skills'
    subprocess.run(
        ['git', 'clone', '--depth', '1', AGENTMAIL_REPO, str(repo_dir)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return repo_dir


def find_source(skill_name: str, agentmail_repo: Path | None) -> tuple[str, Path | None]:
    if skill_name in AGENTMAIL_SKILLS:
        if agentmail_repo is None:
            return ('skill.sh/GitHub (unavailable)', None)
        candidate = agentmail_repo / skill_name
        return ('skill.sh / GitHub: agentmail-to/agentmail-skills', candidate if candidate.is_dir() else None)
    for root in LOCAL_SOURCE_ROOTS:
        candidate = root / skill_name
        if candidate.is_dir():
            return (str(root), candidate)
    return ('未找到可用上游源', None)


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f'Missing skills dir: {SKILLS_DIR}', file=sys.stderr)
        return 1

    report_rows: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix='openclaw-skill-refresh-') as tmp:
        tmp_root = Path(tmp)
        agentmail_repo = None
        try:
            agentmail_repo = clone_agentmail_repo(tmp_root)
        except Exception:
            agentmail_repo = None

        for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
            skill = skill_dir.name
            source_label, source_dir = find_source(skill, agentmail_repo)
            current_snapshot = snapshot_tree(skill_dir)
            before_hash = hashlib.sha256(repr(sorted(current_snapshot.items())).encode()).hexdigest()

            if source_dir is None:
                report_rows.append({
                    'skill': skill,
                    'status': '保留现状',
                    'source': source_label,
                    'detail': '未找到自动同步源，保留仓库现有版本',
                })
                continue

            source_snapshot = snapshot_tree(source_dir)
            source_hash = hashlib.sha256(repr(sorted(source_snapshot.items())).encode()).hexdigest()
            if before_hash == source_hash:
                report_rows.append({
                    'skill': skill,
                    'status': '已最新',
                    'source': source_label,
                    'detail': '与上游目录一致',
                })
                continue

            copy_tree(source_dir, skill_dir)
            report_rows.append({
                'skill': skill,
                'status': '已更新',
                'source': source_label,
                'detail': '已用上游目录覆盖本地默认包',
            })

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '# Skills 更新结果',
        '',
        f'- 生成时间: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'- 扫描目录: `{SKILLS_DIR}`',
        '- 同步优先级: `~/.openclaw/skills` -> `/Users/lichengyin/.codex/skills` -> `agentmail-to/agentmail-skills`',
        '',
        '| Skill | 结果 | 来源 | 说明 |',
        '|---|---|---|---|',
    ]
    for row in report_rows:
        lines.append(f"| {row['skill']} | {row['status']} | {row['source']} | {row['detail']} |")
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote {REPORT_PATH}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
