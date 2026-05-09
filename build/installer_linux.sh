#!/bin/bash
set -e

VARIANT="VARIANT_PLACEHOLDER"
VERSION="VERSION_PLACEHOLDER"
REAL_USER=${SUDO_USER:-$USER}
REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)

echo "Installing Duck AI v$VERSION..."

mkdir -p "$REAL_HOME/.local/bin/DuckAI"
cp -r "$(dirname "$0")"/* "$REAL_HOME/.local/bin/DuckAI/"
rm -f "$REAL_HOME/.local/bin/DuckAI/installer_linux.sh"
chown -R "$REAL_USER:$REAL_USER" "$REAL_HOME/.local/bin/DuckAI"

mkdir -p "$REAL_HOME/.local/share/applications"
cat > "$REAL_HOME/.local/share/applications/duckai.desktop" << EOF
[Desktop Entry]
Name=Duck AI
Exec=$REAL_HOME/.local/bin/DuckAI/DuckAI
Icon=utilities-terminal
Type=Application
Categories=Science;Education;
Comment=Deep Reinforcement Learning simulation
EOF
chown "$REAL_USER:$REAL_USER" "$REAL_HOME/.local/share/applications/duckai.desktop"

echo "{\"variant\": \"$VARIANT\", \"version\": \"$VERSION\"}" > "$REAL_HOME/.local/bin/DuckAI/duckai.json"
chown "$REAL_USER:$REAL_USER" "$REAL_HOME/.local/bin/DuckAI/duckai.json"

echo "Duck AI installed successfully!"
echo "You can now launch it from your application menu."
