FROM dyne/devuan:chimaera
# An absolute path for COPY doesn't work ('/' is removed from the beginning).
COPY linux-minetest-kit.zip /opt
COPY lmk.rc /opt
COPY build-lmk.sh /opt
COPY install-minetest-build-deps.sh /opt
RUN apt-get update
RUN apt-get install -y unzip
RUN apt-get install -y perl
RUN unzip /opt/linux-minetest-kit.zip -d /opt
# RUN  apt-get install -y sudo
# RUN curl https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/install-minetest-build-deps.sh --output /opt/install-minetest-build-deps.sh
# RUN chmod +x /opt/install-minetest-build-deps.sh
RUN /opt/install-minetest-build-deps.sh
