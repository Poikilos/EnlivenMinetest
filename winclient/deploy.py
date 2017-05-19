#!/usr/bin/env python
import os
deploy_path = "C:\\Games\\ENLIVEN-deploy"
if not os.path.isdir(deploy_path):
    os.makedirs(deploy_path)
games_path = os.path.join(deploy_path, "games")
game_path = os.path.join(games_path, "ENLIVEN")
mods_path = os.path.join(game_path, "mods")
if not os.path.isdir(deploy_path):
    os.makedirs(mods_path)
