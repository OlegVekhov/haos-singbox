FROM python:3.12-slim-bookworm
ARG BUILD_ARCH
ARG SING_BOX_VERSION=1.14.4
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl tar && rm -rf /var/lib/apt/lists/*
RUN set -eux; \
    case "${BUILD_ARCH}" in amd64) TARGET=amd64;; aarch64) TARGET=arm64;; armv7) TARGET=armv7;; *) echo "unsupported arch: ${BUILD_ARCH}"; exit 1;; esac; \
    curl -fL --retry 3 "https://github.com/SagerNet/sing-box/releases/download/v${SING_BOX_VERSION}/sing-box-${SING_BOX_VERSION}-linux-${TARGET}.tar.gz" -o /tmp/sb.tar.gz; \
    tar xzf /tmp/sb.tar.gz -C /tmp; \
    install -m 0755 "/tmp/sing-box-${SING_BOX_VERSION}-linux-${TARGET}/sing-box" /usr/local/bin/sing-box; \
    /usr/local/bin/sing-box version; \
    rm -rf /tmp/sb.tar.gz "/tmp/sing-box-${SING_BOX_VERSION}-linux-${TARGET}"
COPY run.py /opt/run.py
LABEL io.hass.type="addon"
CMD ["python3", "-u", "/opt/run.py"]
