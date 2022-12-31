# Building Minetest
EnlivenMinetest is mostly oriented around building ENLIVEN, which is
available as a "game" (Lua game for the Minetest engine binary) and
release (Lua+binary+conf)), but you can also use some of the scripts to
build basically any version Minetest (engine) from source.

## Linux
* Open terminal (root is *not* recommended).
* IF you are a decicated server, first run
  `touch $HOME/i_am_dedicated_minetest_server`
* Then (The next command downloads the latest linux-build-kit, CLEARS the
  webapp/linux-build-kit/minetest directory, and compiles the libraries.
  Do not put anything important in that directory--the latter install
  script installs the game to $HOME/minetest and that is the copy of
  minetest you should use (such as via the icon)):
```bash
bash reset-minetest.sh
bash install-mts.sh --client
# defaults to client if $HOME/Desktop/org.minetest.minetest.desktop exists
```

The Minetest icon will be added as:
`$HOME/.local/share/applications/org.minetest.minetest.desktop` (your
window manager should automatically detect the change--if not, you may
need to restart your window manager. If it still doesn't show, contact
the maintainer of your window manager. This works in KDE on Fedora 29.
Workaround: copy the icon from there to your desktop.)


## Linux Server Install or Upgrade
```
cd ~/git/EnlivenMinetest
./reset-minetest-install-source.sh && ./versionize && ./install-mts.sh
# You can leave out `&& ./versionize` if you don't want to keep old
# copies.
```

### Using install-mts.sh
You must first run reset-minetest-install-source.sh to compile the
libraries automatically, or otherwise have run the compile libraries
script in `~/.config/EnlivenMinetest/linux-minetest-kit`, or at least
have already compiled Minetest there. If the minetest or
minetestserver binary (or just minetestserver if client is not enabled)
is not present there (in
`~/.config/EnlivenMinetest/linux-minetest-kit/minetest/bin/`), the
script will try to compile the program before installing or stop if it
cannot.

#### Arguments
- `--clean` is the recommended option, and is the default. It
  erases Bucket_Game and causes ENLIVEN to be remade using Bucket_Game.
  - It backs up skins, but that is not necessary anymore since
    coderskins uses world storage (follow this issue at
    <https://github.com/Poikilos/EnlivenMinetest/issues/382>).
- `--client` installs the client too. Since "install-mts.sh" stands for
  "Install minetestserver," the `--client` option is off by default
  (See the "Configuration Files" section for how to change the default).
