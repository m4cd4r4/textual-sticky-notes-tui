#!/usr/bin/env bash
set -e

APP_NAME="stickynotes"

BIN_DIR="/usr/local/bin"
TARGET="$BIN_DIR/$APP_NAME"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do 
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" 
done
PROJECT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

check_root() {
  if [ "$EUID" -ne 0 ]; then
    echo "❌ Error: Installation to $BIN_DIR requires root privileges."
    echo "➡ Please run with sudo: sudo ./manage.sh $1"
    exit 1
  fi
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

install_self() {
  check_root "install" 
  
  echo "▶ Installing $APP_NAME globally to $BIN_DIR..."

  if [ ! -d "$BIN_DIR" ]; then
    mkdir -p "$BIN_DIR"
  fi

  if [ -e "$TARGET" ]; then
    if [ -L "$TARGET" ]; then
        rm "$TARGET"
    else
        echo "⚠ $TARGET already exists and is not a symlink."
        echo "   Please remove it manually."
        exit 1
    fi
  fi

  chmod +x "$PROJECT_DIR/$(basename "${BASH_SOURCE[0]}")"
  
  ln -s "$PROJECT_DIR/$(basename "${BASH_SOURCE[0]}")" "$TARGET"

  echo "✅ Installed to $TARGET"
  echo "➡ You can now run '$APP_NAME' from anywhere!"
}

uninstall_self() {
  check_root "uninstall" 

  echo "▶ Uninstalling $APP_NAME..."

  if [ ! -L "$TARGET" ] && [ ! -e "$TARGET" ]; then
    echo "❌ $APP_NAME is not installed"
    exit 1
  fi

  rm "$TARGET"
  echo "✅ Uninstalled"
}

run_app() {
  command_exists uv || {
    echo "❌ uv is not installed"
    echo "➡ Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
  }

  cd "$PROJECT_DIR"
  exec uv run src/main.py
}

case "$1" in
  install)
    install_self
    ;;
  uninstall)
    uninstall_self
    ;;
  *)
    run_app
    ;;
esac
