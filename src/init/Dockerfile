FROM python:3.10.0-bullseye@sha256:3df806bc58898142233afd43c23f98800e39bb93f3204b707b283abe1e247219

RUN mkdir /src
ADD src /src
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt

CMD ["python", "-u", "/src/main.py"]