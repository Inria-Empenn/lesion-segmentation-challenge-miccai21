FROM python:slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils ca-certificates wget unzip git
RUN update-ca-certificates

WORKDIR /nnunet

RUN pip install nnunet
COPY setup.sh /nnunet
COPY FlairMSSegModel.zip /nnunet

RUN mkdir -p /nnunet/data/input/nnUNet_raw_data
RUN mkdir -p /nnunet/data/input/nnUNet_preprocessed
RUN mkdir -p /nnunet/data/output

ENV nnUNet_raw_data_base=/nnunet/data/input/
ENV nnUNet_preprocessed=/nnunet/data/input/nnUNet_preprocessed
ENV RESULTS_FOLDER=/nnunet/data/output/

RUN nnUNet_install_pretrained_model_from_zip FlairMSSegModel.zip
