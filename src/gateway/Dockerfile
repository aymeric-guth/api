FROM python:3.10.0-bullseye@sha256:3df806bc58898142233afd43c23f98800e39bb93f3204b707b283abe1e247219

# RUN mkdir /src
# ADD ./gateway/src /src
# COPY ./domain/models /src/models
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt


#CMD ["uvicorn", "src.main:app", "--host", "av_gateway", "--port", "8080", "--reload"]
CMD ["uvicorn", "src.main:app", "--host", "av_gateway", "--port", "8080"]
