After editing /home/owner/git/EnlivenMinetest/Bucket_Game-branches/dye-redrawn-vs-220114/./mods/codercore/dye/textures/dye_red.png, then create a patch by running:
diff -u /home/owner/git/EnlivenMinetest/Bucket_Game-base/dye-redrawn-vs-220114/./mods/codercore/dye/textures/dye_red.png /home/owner/git/EnlivenMinetest/Bucket_Game-branches/dye-redrawn-vs-220114/./mods/codercore/dye/textures/dye_red.png > /home/owner/git/EnlivenMinetest/dye-redrawn-vs-220114.patch

* getting parent of /home/owner/minetest/bucket_game-211114a/./mods/codercore/dye/textures/dye_red.png...
* updating /home/owner/git/EnlivenMinetest/Bucket_Game-base/dye-redrawn-vs-220114/./mods/codercore/dye/textures/dye_red.png
* creating /home/owner/git/EnlivenMinetest/Bucket_Game-branches/dye-redrawn-vs-220114/./mods/codercore/dye/textures/dye_red.png
* updating LICENSE '/home/owner/git/EnlivenMinetest/Bucket_Game-base/dye-redrawn-vs-220114/./mods/codercore/dye/license.txt'...

To apply, set BUCKET_GAME then:
```
cd EnlivenMinetest && git pull && rsync -rt Bucket_Game-branches/dye-redrawn-vs-220114/ $BUCKET_GAME
```
