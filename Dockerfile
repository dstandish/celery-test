FROM quay.io/astronomer/astro-runtime:10.0.0

USER root
RUN apt-get update && apt-get install -y patch patchutils
RUN set -ex; \
    cd /usr/local/lib/python3.11/site-packages/kombu; \
    cat /usr/local/airflow/kombu-patch.patch | patch -u -p2;
USER astro

