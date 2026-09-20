# Steam Deck Refurbished Stock Tracker

This program checks Steam's refurbished Steam Deck inventory for the United States, France, and Germany. When installed as a macOS LaunchAgent, it runs once at login and then every 15 minutes.

## Files

- Saved LaunchAgent: `$HOME/Programs/steamDeckNotifier/com.steamdeckmonitor.plist`
- Python program: `$HOME/Programs/steamDeckNotifier/STEAM_DECK_NOTIFICATION.py`
- Standard log: `$HOME/Programs/steamDeckNotifier/Logs/steam_deck.log`
- Error log: `$HOME/Programs/steamDeckNotifier/Logs/steam_deck_err.log`
- Active LaunchAgent location (only when enabled): `$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist`
- LaunchAgent label: `com.steamdeckmonitor`

## Reactivate the tracker

Open Terminal and run:

```bash
mkdir -p "$HOME/Library/LaunchAgents"
cp "$HOME/Programs/steamDeckNotifier/com.steamdeckmonitor.plist" \
  "$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist"
plutil -lint "$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist"
launchctl bootstrap "gui/$(id -u)" \
  "$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist"
```

Because the plist contains `RunAtLoad`, the tracker should run once immediately after it is loaded. It will then run every 900 seconds (15 minutes).

If `bootstrap` says the service is already loaded, unload it using the temporary-disable commands below and then run the reactivation commands again.

## Check whether it is active

```bash
launchctl print "gui/$(id -u)/com.steamdeckmonitor"
```

If active, this prints the LaunchAgent details. If disabled or unloaded, it reports that the service could not be found.

## Run one check manually

This does not install or enable the LaunchAgent:

```bash
/usr/bin/python3 "$HOME/Programs/steamDeckNotifier/STEAM_DECK_NOTIFICATION.py"
```

## Temporarily disable it again

```bash
launchctl bootout "gui/$(id -u)" \
  "$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/com.steamdeckmonitor.plist"
```

These commands remove only the active LaunchAgent copy. The saved plist, Python program, logs, and configuration remain in `$HOME/Programs/steamDeckNotifier` for later use.

## View recent logs

```bash
tail -n 50 "$HOME/Programs/steamDeckNotifier/Logs/steam_deck.log"
tail -n 50 "$HOME/Programs/steamDeckNotifier/Logs/steam_deck_err.log"
```

## Important

`$HOME/Programs/steamDeckNotifier/deletePythonScript.sh` is intended for permanent deletion. Do not run it when you only want to disable the tracker temporarily.
