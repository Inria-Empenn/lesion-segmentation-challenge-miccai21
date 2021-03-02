FROM python:slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils ca-certificates wget unzip git git-lfs
RUN update-ca-certificates

WORKDIR /anima/

RUN wget -q https://github.com/Inria-Visages/Anima-Public/releases/download/v4.0.1/Anima-Ubuntu-4.0.1.zip
RUN unzip Anima-Ubuntu-4.0.1.zip
RUN git lfs install
RUN git clone --depth 1 https://github.com/Inria-Visages/Anima-Scripts-Public.git
RUN git clone --depth 1 https://github.com/Inria-Visages/Anima-Scripts-Data-Public.git
RUN mkdir /root/.anima/

COPY config.txt /root/.anima

RUN mkdir /data/

ENTRYPOINT ["python", "/anima/Anima-Scripts-Public/ms_lesion_semgentation/animaLongitudinalPreprocessing.py"]