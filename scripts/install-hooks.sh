#!/bin/sh
set -e

repo_root=$(git rev-parse --show-toplevel)
mkdir -p "$repo_root/.git/hooks"
cp "$repo_root/scripts/git-hooks/pre-commit" "$repo_root/.git/hooks/pre-commit"
chmod +x "$repo_root/.git/hooks/pre-commit"

echo "Installed pre-commit hook."
