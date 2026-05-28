# syntax=docker/dockerfile:1

# Оновити digest: docker pull ubuntu:noble &&
# docker inspect --format='{{index .RepoDigests 0}}' ubuntu:noble
FROM ubuntu:noble

ARG DEBIAN_FRONTEND="noninteractive"

RUN apt update && apt install -y software-properties-common && \
    add-apt-repository universe && \
    rm -rf /var/lib/apt/lists/*

COPY apt-packages.in /tmp/apt.in
RUN apt update && \
  grep -vE '^\s*#' /tmp/apt.in | xargs apt install --no-install-recommends -y && \
  rm -rf /var/lib/apt/lists/* && apt-get clean -y && rm /tmp/apt.in && \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  locale-gen

ENV TZ=Etc/UTC
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en

# sudo без пароля — тільки dev
RUN echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ARG CONTAINER_USER=developer
ARG WORKSPACE_FOLDER=/workspace

# Звільняємо UID 1000 для коректного remap на WSL
RUN if id ubuntu >/dev/null 2>&1; then \
      userdel -r ubuntu && groupdel ubuntu 2>/dev/null || true; \
    fi && \
    useradd -s /bin/bash -m ${CONTAINER_USER} && \
    echo "\nexport PROMPT_COMMAND=\"history -a; history -n\n\"" >> /home/${CONTAINER_USER}/.bashrc

USER ${CONTAINER_USER}

# --user щоб pip не вимагав root після USER switch
RUN pip install --user --no-cache-dir ruff mypy pytest