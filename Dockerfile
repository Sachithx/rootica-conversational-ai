FROM python:3.8

ENV PYTHONPATH=/rootica-conversational-ai

WORKDIR /rootica-conversational-ai

COPY requirements.txt /rootica-conversational-ai/requirements.txt

RUN pip3 --no-cache-dir --use-deprecated=legacy-resolver install -r /rootica-conversational-ai/rasa_requirements.txt

COPY . ./
EXPOSE 5005
EXPOSE 5055

ARG AWS_DEFAULT_REGION
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY