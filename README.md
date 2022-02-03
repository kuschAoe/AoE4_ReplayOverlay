# AoE4 ReplayOverlay

**[Download](**https://github.com/kuschAoe/AoE4_ReplayOverlay/releases/download/v0.0.1/AoE4_ReplayOverlay.zip)**

## Usage
1. Start AoE4_ReplayOverlay.exe.
2. Start Age of Empires 4 with the command line argument '-dev'
3. Load a replay.
4. Open the in-game command prompt via CTRL + SHIFT + `.
5. Copy the command provided by AoE4 ReplayOverlay to the system clipboard.
6. Paste it into the in-game command prompt (CTRL + V) and execute it(RETURN).

# A Glimpse Behind The Curtains
## Gathering Data
Age of Empires 4 has an in-game command prompt. By default there is hardly anything noteworthy that can be done with it. However if Age of Empires 4 is started with the command line argument '-dev' a whole host of commands useful for interacting with the game becomes available.

The command prompt basically interprets input as lua scripts with a few minor restrictions(no file access, no debug...). This allows for a script that can extract information from a running game([OverlayDataCollector.lua](**https://github.com/kuschAoe/AoE4_ReplayOverlay/blob/main/src/AoE4LuaScript/OverlayDataCollector.lua**)).

On the down side starting Age of Empires 4 with '-dev' blocks multiplayer including observing ongoing games but it does not block access to replays.

Performance may become an issue if the script becomes too complex.
## Transfer To Overlay
Age of Empires 4 writes everything sent via the lua command 'print' to its 'warnings.log' file located in '~\Documents\My Games\Age of Empires IV', which is then read by the overlay application.

In the future a more sophisticated method may become necessary.
## Displaying
Credit goes to **[Maguro](https://github.com/FluffyMaguro)**. This was built using his **[AoE4 Overlay](https://github.com/FluffyMaguro/AoE4_Overlay)** as foundation.