FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ARG MINIFORGE_VERSION=26.9.4-2
RUN curl -fsSL -o /tmp/miniforge.sh \
      "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-$(uname -m).sh" \
    && bash /tmp/miniforge.sh -b -p /opt/conda && rm /tmp/miniforge.sh
COPY lock.txt /tmp/
RUN /opt/conda/bin/conda create -y -n repro-gpu --file /tmp/lock.txt \
    && /opt/conda/bin/conda clean -afy
ENV PATH=/opt/conda/envs/repro-gpu/bin:$PATH
COPY verify_gpu.py /opt/verify_gpu.py
CMD ["python", "/opt/verify_gpu.py"]
