ARG BUILD_ARCH
FROM python:3.12-alpine
ARG BUILD_ARCH
ARG SING_BOX_VERSION=1.14.4
RUN apk add --no-cache ca-certificates tar && \
    case "$BUILD_ARCH" in amd64) TARGET=amd64;; aarch64) TARGET=arm64;; armv7) TARGET=armv7;; *) echo "unsupported arch: $BUILD_ARCH"; exit 1;; esac && \
    wget -q "https://github.com/SagerNet/sing-box/releases/download/v${SING_BOX_VERSION}/sing-box-${SING_BOX_VERSION}-linux-${TARGET}.tar.gz" -O /tmp/sb.tar.gz && \
    tar xzf /tmp/sb.tar.gz -C /tmp && \
    install -m 0755 "/tmp/sing-box-${SING_BOX_VERSION}-linux-${TARGET}/sing-box" /usr/local/bin/sing-box && \
    rm -rf /tmp/sb.tar.gz /tmp/sing-box-${SING_BOX_VERSION}-linux-${TARGET}
COPY app.py /opt/app.py
COPY ui.html /opt/ui.html
COPY run.sh /run.sh
RUN chmod +x /run.sh
LABEL io.hass.type="addon"
CMD ["/run.sh"]
