# butterfly_rearrange_patch-vs-220422-002

E-mail from Poikilos to OldCoder 2022-04-25:
> I could never find where they were used in the code. Apparently they
> are not. I wondered why they were there and who made them. A long time
> ago you told me you commissioned someone to make them, if I understood
> correctly. I suggest using the butterflies as the inventory images. The
> upstream "mobs_sky" 3D butterflies don't have an inventory image at
> all. In any version of the mobs_sky mod or in bucket_game, holding a
> butterfly in inventory results in a white square.
> . . .

This patch:
- Resolves #554 The default_cloud.png texture used for items without an inventory image such as butterfly is a blank white square.
- Resolves #539 Butterflies (each of the 4 butterfly textures) from codermobs has a false edge (cut curve) due to scaling.

The model must be exported as follows to avoid bone orientation glitches:
- Download and extract the special version of B3DExport from: https://github.com/minetest/B3DExport
- Blender 2.8, Preferences, Add-ons:
  - In the search box type B3D, expand any that appear, then click Remove.
  - Install, choose the extracted py file.
  - In the search box type B3D and enable the special version.

To apply, set BUCKET_GAME then:
cd EnlivenMinetest && git pull && rsync -rtv Bucket_Game-branches/butterfly_rearrange_patch-vs-220422-002/ $BUCKET_GAME
rm $BUCKET_GAME/mods/codermobs/codermobs/projects/unused/butterfly_poikilos-blender3.0-nonworking.blend
mv -v $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly_0?.png $BUCKET_GAME/mods/codermobs/codermobs/projects/unused/
mv -v $BUCKET_GAME/mods/codermobs/codermobs/models/codermobs_butterfly.x $BUCKET_GAME/mods/codermobs/codermobs/projects/unused/

Then exclude the projects folder from distribution to save space.

# Omit the following commands in case they are now used by the better 3d butterflies (the textures now all have the same orientation if the patch above was applied):
#rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly1.png
#rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly2.png
#rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly3.png
#rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly4.png
