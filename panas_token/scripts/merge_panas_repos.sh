#!/usr/bin/env bash
set -euo pipefail

# Merge PANAS-TOKEN and panas-token.M into panas_multichain via git subtree
# - Preserves history by default (set SQUASH=1 to squash)
# - Detects default branch of source repos automatically

PANAS_MULTICHAIN_URL=${PANAS_MULTICHAIN_URL:-"https://github.com/panacea-icono/panas_multichain.git"}
PANAS_TOKEN_URL=${PANAS_TOKEN_URL:-"https://github.com/panacea-icono/PANAS-TOKEN.git"}
PANAS_TOKEN_M_URL=${PANAS_TOKEN_M_URL:-"https://github.com/panacea-icono/panas-token.M.git"}

DEST_DIR=${DEST_DIR:-"panas_multichain"}
DEST_BRANCH=${DEST_BRANCH:-"merge/panas-tokens"}
PREFIX_A=${PREFIX_A:-"integrations/PANAS-TOKEN"}
PREFIX_B=${PREFIX_B:-"integrations/panas-token.M"}
# Optional: newline-separated list of extra repo URLs to integrate
EXTRA_LIST_FILE=${EXTRA_LIST_FILE:-""}
EXTRA_REPOS=${EXTRA_REPOS:-""}

# Optional Git config (for commits created by subtree)
GIT_USER_NAME=${GIT_USER_NAME:-"panas-integrator-bot"}
GIT_USER_EMAIL=${GIT_USER_EMAIL:-"devnull+panas@panacea.local"}

# Optional auto-push
AUTO_PUSH=${AUTO_PUSH:-0}
SQUASH=${SQUASH:-0}

info() { echo "[merge] $*"; }

detect_default_branch() {
  local url="$1"
  git ls-remote --symref "$url" HEAD 2>/dev/null | awk '/^ref:/ {print $2}' | sed 's#refs/heads/##'
}

subtree_add() {
  local prefix="$1" url="$2" branch="$3"
  if [[ "$SQUASH" == "1" ]]; then
    git subtree add --prefix="$prefix" "$url" "$branch" --squash
  else
    git subtree add --prefix="$prefix" "$url" "$branch"
  fi
}

main() {
  if [[ ! -d "$DEST_DIR/.git" ]]; then
    info "Cloning panas_multichain into $DEST_DIR"
    git clone "$PANAS_MULTICHAIN_URL" "$DEST_DIR"
  else
    info "Using existing $DEST_DIR"
  fi

  cd "$DEST_DIR"
  # Try to fetch; ignore failures (e.g., offline) and proceed with local init if needed
  git fetch --all --tags || true

  info "Creating branch $DEST_BRANCH"
  git checkout -B "$DEST_BRANCH"

  # If repository has no commits yet, create an initial commit so subtree can proceed
  if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    info "Initializing empty repository with initial commit"
    echo "# PANAS Multichain (monorepo)" > README.md
    git add README.md
    git commit -m "chore: init monorepo"
  fi

  # Ensure git identity is set (for subtree commits)
  git config user.name "$GIT_USER_NAME"
  git config user.email "$GIT_USER_EMAIL"

  local a_branch b_branch
  a_branch=$(detect_default_branch "$PANAS_TOKEN_URL"); b_branch=${a_branch:-main}
  info "PANAS-TOKEN default branch: $b_branch"
  subtree_add "$PREFIX_A" "$PANAS_TOKEN_URL" "$b_branch"

  b_branch=$(detect_default_branch "$PANAS_TOKEN_M_URL"); b_branch=${b_branch:-main}
  info "panas-token.M default branch: $b_branch"
  subtree_add "$PREFIX_B" "$PANAS_TOKEN_M_URL" "$b_branch"

  # Handle extra repositories if provided
  if [[ -n "$EXTRA_LIST_FILE" && -f "$EXTRA_LIST_FILE" ]]; then
    mapfile -t EXTRA <"$EXTRA_LIST_FILE"
  else
    # split EXTRA_REPOS by whitespace/newlines
    read -r -a EXTRA <<< "$EXTRA_REPOS"
  fi

  for url in "${EXTRA[@]:-}"; do
    [[ -z "$url" ]] && continue
    # derive prefix from repo name
    name=$(basename -s .git "$url")
    pref="integrations/$name"
    br=$(detect_default_branch "$url"); br=${br:-main}
    info "Adding extra repo $url at $pref (branch $br)"
    subtree_add "$pref" "$url" "$br"
  done

  info "Done. Review changes, then push:" 
  echo "\n  cd $DEST_DIR && git push -u origin $DEST_BRANCH\n"

  if [[ "$AUTO_PUSH" == "1" ]]; then
    info "Auto pushing $DEST_BRANCH to origin"
    git push -u origin "$DEST_BRANCH"
  fi
}

main "$@"
