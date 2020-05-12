#!/bin/bash
mkdir -p ~/Downloads \
  && cd ~/Downloads \
  && wget -O reset-minetest-install-source.sh https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/reset-minetest-install-source.sh \
  && chmod +x reset-minetest-install-source.sh \
  && wget -O install-mts https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/install-mts.sh \
  && chmod +x install-mts.sh \
  && ./reset-minetest-install-source.sh \
  && ./install-mts.sh
