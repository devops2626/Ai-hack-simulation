FROM alpine:3.19
RUN apk add --no-cache perl=5.36.0-r0 perl-dev gcc musl-dev make
WORKDIR /benchmark
COPY setup.sh /setup.sh
RUN /setup.sh
