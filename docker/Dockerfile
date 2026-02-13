FROM python:3.13 AS builder
WORKDIR /app
COPY --chmod=0110 requirements.txt requirements.txt

# install curl with soar for health checks
RUN wget -qO- "https://raw.githubusercontent.com/pkgforge/soar/main/install.sh" | sh
RUN export PATH="$PATH:/usr/local/bin:/opt/soar/bin"

RUN soar install curl  

RUN pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian13:debug-nonroot AS runtime
WORKDIR /

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Set PYTHONPATH to include the site-packages dir in sys.path
ENV PYTHONPATH="/usr/local/lib/python3.13/site-packages"
# r-x permissions for nonroot user.
COPY --chown=nonroot:nonroot --chmod=0550 ./app ./app

# bring curl to the runtime image for health checks
# r-- permissions for nonroot user.
COPY --from=builder --chown=nonroot:nonroot --chmod=0110 /root/.local/share/soar/bin/curl /usr/bin/curl

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD [ "curl", "-f", "http://localhost:8080/" ]

EXPOSE 8080

ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app", "--proxy-headers", "--no-server-header"]


## Set this variable on the docker-compose file with the nginx ip or the network CIRD range
#   --forwarded-allow-ips TEXT      Comma separated list of IPs to trust with
#                                   proxy headers. Defaults to the
#                                   $FORWARDED_ALLOW_IPS environment variable if
#                                   available, or '127.0.0.1'.
