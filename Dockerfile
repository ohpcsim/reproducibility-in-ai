# Pin the base image by digest. Get it with:
#   docker pull ubuntu:24.04 && docker inspect --format '{{index .RepoDigests 0}}' ubuntu:24.04
FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# Pin the installer version (see github.com/conda-forge/miniforge/releases).
ARG MINIFORGE_VERSION=26.9.4-2
RUN curl -fsSL -o /tmp/miniforge.sh \
      https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-aarch64.sh \
    && bash /tmp/miniforge.sh -b -p /opt/conda && rm /tmp/miniforge.sh
# Build the environment from the lock, not from environment.yml.
COPY explicit-linux-aarch64.txt /tmp/
RUN /opt/conda/bin/conda create -y -n repro-gpu --file /tmp/explicit-linux-aarch64.txt \
    && /opt/conda/bin/conda clean -afy
ENV PATH=/opt/conda/envs/repro-gpu/bin:$PATH
COPY verify_gpu.py /opt/verify_gpu.py
CMD ["python", "/opt/verify_gpu.py"]
