FROM alpine:3.14.3

RUN wget https://github.com/omerbenamram/evtx/releases/download/v0.7.2/evtx_dump-v0.7.2-x86_64-unknown-linux-musl -O /usr/local/bin/evtx_dump && \
    chmod +x /usr/local/bin/evtx_dump

ENTRYPOINT ["/usr/local/bin/evtx_dump"]
