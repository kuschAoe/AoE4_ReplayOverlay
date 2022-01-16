# AoE4 Overlay
 
* **[DOWNLOAD HERE](https://github.com/FluffyMaguro/AoE4_Overlay/releases/download/1.2.0/AoE4_Overlay.zip)** (Windows)
* Or run the script with Python 3.6+ (Windows/Mac/Linux)

![Screenshot](https://i.imgur.com/eN2zJ3c.jpg)

**Use cases:**

1. Showing information about your opponents and teammates while you play
2. Personal statistics
3. Separate overlay for streaming (as html, very customizable via CSS/JS).
4. Information about players that are streaming and don't have any overlay

API calls are done through [AoEIV.net](https://aoeiv.net/). For questions and issues visit my [discord server](https://discord.gg/FtGdhqD).

# Screenshots

Build order widget:

![Screenshot](https://i.imgur.com/SnR3p7d.png)

Settings:

![Screenshot](https://i.imgur.com/hhH8R72.png)

Game history:

![Screenshot](https://i.imgur.com/L1V1wp2.png)

Rating history:

![Screenshot](https://i.imgur.com/QqojOJI.png)

Last 24 hours:

![Screenshot](https://i.imgur.com/8ODqTrw.png)

Various stats:

![Screenshot](https://i.imgur.com/aGXRnT2.png)

Build order tab:

![Screenshot](https://i.imgur.com/zuAdlX6.png)

Built-in randomizer:

![Screenshot](https://i.imgur.com/tV4dMfi.png)

# Streaming
To use the custom streaming overlay simply drag the `overlay.html` file to OBS or other streaming software. The file is located in `src/html` directory in the app folder. Move and rescale as necessary once some game information is shown.

![Screenshot](https://i.imgur.com/BK9AC6h.png)

If drag & drop doesn't work, add new source to your scene manually. The source type will be `Browser` and point to a local file `overlay.html`.

Overlay active:

![Screenshot](https://i.imgur.com/gNbxJBY.png)

* Streaming overlay supports team games as well
* The streaming overlay can be fully customized with CSS and JS, see the next section.
* The override tab can be used to change the information on the overlay. This might be useful when casting from replays or changing a player's barcode to their actual name.

![Screenshot](https://i.imgur.com/f1OGmyz.png)

Or change values to something completely different

![Screenshot](https://i.imgur.com/02YsXdI.png)

# Customization

1. **Overlay position and font size** can be changed in the app.

2. **Build order** font and position can be changed in the app. 
   But other attributres can be also customized in `config.json` (click `File/config & logs` in the app):

    `"bo_bg_opacity": 0.5,` controls its background opacity (default: 0.5 = 50%; accepts values between 0 and 1)

    `"bo_showtitle": true,` sets whether build order name is visible (accepts true/false)

    `"bo_title_color": "orange",` changes the color of build order name (title), also accepts hex and rgb values as string


3. **Team colors** can be changed in the `config.json`. Colors are stored as a list of RGBA colors for team 1, 2, and so on.

    ```json
    "team_colors": [
        [74, 255, 2, 0.35],
        [3, 179, 255, 0.35],
        [255, 0, 0, 0.35]
      ]
    ```

1. **Streaming overlay** customization can be done via `custom.css` and `custom.js` in the `html` folder in app directory. These files will not be overridden with an app update. Look at `main.css` to see what you can change. In `custom.js` you can define this function that runs after each update.

    ```javascript
    function custom_func(data) {
        console.log("These are all the player data:", data);
    }
    ```

# Changelog & releases

[Here](https://github.com/FluffyMaguro/AoE4_Overlay/releases)