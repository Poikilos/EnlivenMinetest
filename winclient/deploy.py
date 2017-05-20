#!/usr/bin/env python
import os
#import filever

try:
    input = raw_input
except NameError:
    pass

def path_join(names):
    result = names[0]
    for i in range(1, len(names)):
        result = os.path.join(result, names[i])
    return result

profile_path = None
if "HOME" in os.environ:
    profile_path = os.environ["HOME"]
elif "USERPROFILE" in os.environ:
    profile_path = os.environ["USERPROFILE"]
else:
    try_path = "C:\\Users\\jgustafson"
    if not os.path.isdir(try_path): try_path = "C:\\Users\\Owner"
    
    print("WARNING: no HOME or USERPROFILE found, reverting to '" +
        try_path + "'")
    profile_path = try_path
#region user settings
deploy_path = "C:\\Games\\ENLIVEN-deploy"
installer_deploy_path = path_join( [profile_path, "ownCloud", "www",
                                  "expertmultimedia", "downloads"] )
installer_name = "install-ENLIVEN.exe"
#endregion user settings

installer_path = os.path.join(installer_deploy_path, installer_name)

if not os.path.isdir(installer_deploy_path):
    print("#WARNING: does not exist:")
print("installer_deploy_path: " + installer_deploy_path)

#this is a waste--it just shows 0.0.0.0 though iss file has version
#if os.path.isfile(installer_path):
    #numbers=filever.get_version_number(installer_path)
    #major,minor,subminor,revision = numbers
    #print(".".join([str (i) for i in numbers]))

if not os.path.isdir(deploy_path):
    os.makedirs(deploy_path)
games_path = os.path.join(deploy_path, "games")
game_path = os.path.join(games_path, "ENLIVEN")
if not os.path.isdir(game_path):
    print("")
    print("ERROR: ENLIVEN must first be installed from web sources" +
          " using the provided 'install' script in the etc/change*"
          " folder and placed in " + game_path)
    exit(1)
else:
    print("game_path: " + game_path)
mods_path = os.path.join(game_path, "mods")
if not os.path.isdir(deploy_path):
    os.makedirs(mods_path)
