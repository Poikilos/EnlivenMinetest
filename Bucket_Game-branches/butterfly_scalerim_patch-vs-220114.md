# butterfly_scalerim_patch-vs-220114
See "butterfly_rearrange_patch-vs-220114" instead.

## Size
The size has been reverted to the original 16x16 size since they look better that way. Issue [ENI 539](https://github.com/poikilos/EnlivenMinetest/issues/539) is present in the 32x32 version of the images that were upscaled in later versions of bucket_game (at least as early as 190620). Even if reverted to 16x16 then upscaled using scalerim to fix the issue, the images need some hand work to fix some blocky parts otherwise they may look odd. The original 16x16 version looks more natural since the (original author's) hand work was done at that resolution.

To upscale images in butterfly_scalerim_patch-vs-220114:
```
# Use BUCKET_GAME if the patch is already applied (set it correctly in the line below)
# BUCKET_GAME=
cd ~/git/EnlivenMinetest/Bucket_Game-branches/butterfly_scalerim_patch-vs-220114
# cd $BUCKET_GAME
cd mods/codermobs/codermobs/textures
i=1
# Loop: See <https://www.cyberciti.biz/faq/unix-for-loop-1-to-10/>
while [ $i -ne 4 ]
do
    i=$(($i+1))
    scalerim codermobs_butterfly$i.png codermobs_butterfly$i-scaled.png --force --command scalex
    if [ $? -ne 0 ]; then
        echo "Error: 'scalerim codermobs_butterfly$i.png codermobs_butterfly$i-scaled.png --force --command scalex' failed in \"`pwd`\""
        exit 1
    fi
    mv -f codermobs_butterfly$i-scaled.png codermobs_butterfly$i.png
    echo "* scaled codermobs_butterfly$i.png"
done
echo Done
```


