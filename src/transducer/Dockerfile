FROM python:3.10.0-bullseye@sha256:3df806bc58898142233afd43c23f98800e39bb93f3204b707b283abe1e247219

# RUN mkdir /src
RUN mkdir /logs

COPY ./transducer/requirements.txt /src/requirements.txt
# COPY ./av_protocol/ /src/av_protocol/

RUN pip3 install -r /src/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "av_transducer", "--port", "8080", "--reload"]