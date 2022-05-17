# ilights
Add industrial lights to Minetest.
## License
CC BY-SA 4.0
Copyright (c) 2014 DanDuncombe, (c) 2019 VanessaE
## History
This branch is the old CC version of the code, with new textures cherry
picked.
```
git clone https://gitlab.com/poikilos/ilights ilights
cd ilights && \
    git checkout -b old-license-branch 5a4cc589 && \
    git cherry-pick 6398d89b80a0bb20da9908babe04599a38a7e0f8
mv ilights_lamp_bulb_off.png ../
mv ilights_lamp_lens_off.png ../
git reset --hard
# ^ reset to avoid "unmerged" due to conflict
mv ../ilights_lamp_bulb_off.png ./
mv ../ilights_lamp_lens_off.png ./
```
## Tasks
- [ ] actually use the new textures (add the ability to turn them off
  or require power)
