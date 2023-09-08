FROM python:3.10 as builder

ENV VIRTUAL_ENV=/home/ubuntu/samtools-metrics-sqlite/sms_env/

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./ /opt

WORKDIR /opt
RUN pip install tox && tox -p

FROM python:3.10

COPY --from=builder /opt/dist/*.tar.gz /opt
COPY requirements.txt /opt

WORKDIR /opt

RUN pip install -r requirements.txt \
        && pip install *.tar.gz \
        && rm -f *.tar.gz requirements.txt

ENTRYPOINT ["samtools_metrics_sqlite"]

CMD ["--help"]
