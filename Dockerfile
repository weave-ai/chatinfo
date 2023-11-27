# Stage 0
FROM ghcr.io/weave-ai/images/python:3.11-dev

RUN pip install \
	streamlit \
	langchain \
	openai==0.28.1 \
	--user 

WORKDIR /work
COPY app_langchain.py .
COPY typing.css .

# State 1
FROM ghcr.io/weave-ai/images/python:3.11

COPY --from=0 /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=0 /work /work

WORKDIR /work

ENV STREAMLIT_SERVER_ADDRESS 0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS False

ENTRYPOINT ["python3", "-m", "streamlit", "run"]

CMD ["app_langchain.py"]
