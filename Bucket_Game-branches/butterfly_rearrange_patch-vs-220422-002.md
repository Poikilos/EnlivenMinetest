# butterfly_rearrange_patch-vs-220422-002

Resolves #554 The default_cloud.png texture used for items without an inventory image such as butterfly is a blank white square.
Resolves #539 Butterflies (each of the 4 butterfly textures) from codermobs has a false edge (cut curve) due to scaling.

E-mail from Poikilos to OldCoder 2022-04-25:
> I could never find where they were used in the code. Apparently they
> are not. I wondered why they were there and who made them. A long time
> ago you told me you commissioned someone to make them, if I understood
> correctly. I suggest using the butterflies as the inventory images. The
> upstream "mobs_sky" 3D butterflies don't have an inventory image at
> all. In any version of the mobs_sky mod or in bucket_game, holding a
> butterfly in inventory results in a white square. I suggest using these
> unused images to fix the problem.

To apply, set BUCKET_GAME then:
cd EnlivenMinetest && git pull \
 && rsync -rtv Bucket_Game-branches/butterfly_rearrange_patch-vs-220422-002/ $BUCKET_GAME


# Omit the following commands in case they can be used for something (like better 3d butterflies):
rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly1.png
rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly2.png
rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly3.png
rm $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_butterfly4.png
