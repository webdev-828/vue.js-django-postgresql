FROM python:3
ENV PYTHONUNBUFFERED 1
ENV APP_USER invtask
ENV APP_ROOT /code
RUN mkdir /code
RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}
WORKDIR ${APP_ROOT}
ADD requirements/* /code/
RUN pip install -r /code/dev.txt
USER ${APP_USER}
ADD . ${APP_ROOT}
