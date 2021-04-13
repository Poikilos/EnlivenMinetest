#!/bin/bash
if [ -z "$CONF_PATH" ]; then
    CONF_PATH="$HOME/.config/EnlivenMinetest/remote.rc"
fi

if [ -f "$CONF_PATH" ]; then
    . "$CONF_PATH"
fi

_is_conf_ok=true
if [ -z "$REMOTE_HOST" ]; then
    echo "* REMOTE_HOST...not set."
    _is_conf_ok=false
else
    echo "* REMOTE_HOST...OK (\"$REMOTE_HOST\")."
fi
if [ -z "$REMOTE_USER" ]; then
    echo "* REMOTE_USER...not set."
    _is_conf_ok=false
else
    echo "* REMOTE_USER...OK (\"$REMOTE_USER\")."
fi
if [ -z "$REMOTE_WORLD" ]; then
    echo "* REMOTE_WORLD...not set."
    _is_conf_ok=false
else
    echo "* REMOTE_WORLD...OK (\"$REMOTE_WORLD\")."
fi
if [ -z "$REMOTE_WORLD_PATH" ]; then
    echo "* REMOTE_WORLD_PATH...not set."
    _is_conf_ok=false
else
    echo "* REMOTE_WORLD_PATH...OK (\"$REMOTE_WORLD_PATH\")."
fi
if [ -z "$LOCAL_WORLD_COPY_PATH" ]; then
    echo "* LOCAL_WORLD_COPY_PATH...not set."
    _is_conf_ok=false
else
    echo "* LOCAL_WORLD_COPY_PATH...OK (\"$LOCAL_WORLD_COPY_PATH\")."
fi
if [ -z "$LOCAL_UNPRIV_USER" ]; then
    echo "* LOCAL_UNPRIV_USER...not set."
    _is_conf_ok=false
else
    echo "* LOCAL_UNPRIV_USER...OK (\"$LOCAL_UNPRIV_USER\")."
fi
if [ "@$_is_conf_ok" != "@true" ]; then
    cat << END
Error: You must set the following in "$CONF_PATH" or the environment first (any that are blank below are not set):

REMOTE_HOST="$REMOTE_HOST"
REMOTE_USER="$REMOTE_USER"
REMOTE_WORLD="$REMOTE_WORLD"
REMOTE_WORLD_PATH="$REMOTE_WORLD_PATH"
LOCAL_WORLD_COPY_PATH="$LOCAL_WORLD_COPY_PATH"
LOCAL_UNPRIV_USER="$LOCAL_UNPRIV_USER"
END
    exit 1
fi
ssh $REMOTE_USER@$REMOTE_HOST "/opt/minebest/mtbin/minetest-stop $REMOTE_WORLD"
ssh $REMOTE_USER@$REMOTE_HOST "/opt/minebest/mtbin/minetest-list"
echo "* running 'rsync -rt --info=progress2 $REMOTE_USER@$REMOTE_HOST:$REMOTE_WORLD_PATH/ $LOCAL_WORLD_COPY_PATH'..."
rsync -rt --info=progress2 $REMOTE_USER@$REMOTE_HOST:$REMOTE_WORLD_PATH/ $LOCAL_WORLD_COPY_PATH
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
fi
printf "* setting owner of \"$LOCAL_WORLD_COPY_PATH\" to $LOCAL_UNPRIV_USER:$LOCAL_UNPRIV_USER..."
chown $LOCAL_UNPRIV_USER:$LOCAL_UNPRIV_USER -R "$LOCAL_WORLD_COPY_PATH"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
fi
ssh $REMOTE_USER@$REMOTE_HOST "/opt/minebest/mtbin/minetest-start $REMOTE_WORLD"
ssh $REMOTE_USER@$REMOTE_HOST "/opt/minebest/mtbin/minetest-list"
