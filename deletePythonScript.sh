# Delete the LaunchAgent Configuration: Remove the XML file so macOS forgets the task ever existed on future restarts:
rm ~/Library/LaunchAgents/com.steamdeckmonitor.plist
# Delete Your Project Files and Logs: Delete the Python script and the two log files it created:
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm "$PROJECT_DIR/STEAM_DECK_NOTIFICATION.py"
rm "$PROJECT_DIR/Logs/steam_deck.log"
rm "$PROJECT_DIR/Logs/steam_deck_err.log"
# Delete the State File: Clear the temporary file used to track stock status:
rm -f /tmp/steamdeck_multi_state.json
# Your Mac is now exactly as it was before we started.