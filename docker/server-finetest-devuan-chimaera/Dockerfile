FROM linux-minetest-kit/libraries-devuan-chimaera
COPY build-and-check.sh /opt
WORKDIR /opt/linux-minetest-kit
# RUN ./mtcompile-program.pl --build --finetest --server
# ^ Always returns 1, so:
RUN /opt/build-and-check.sh
