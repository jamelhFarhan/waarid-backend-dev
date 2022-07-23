###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.2-alpine

# set work directory 
WORKDIR /usr/src/app

# set environment variables 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    --update \
    g++ \
    gcc \
    git \
    jpeg-dev \
    zlib-dev \
    musl-dev \
    openssl \
    libffi-dev \
    libressl-dev \
    postgresql-dev \
    libstdc++ \
    libxslt-dev \
    freetype-dev \
    linux-headers \
    python3-dev

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --default-timeout=100 future

#########
# FINAL #
#########

# pull official base image
# FROM python:3.8.2-alpine

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
# RUN apt update && apt install -y --no-install-recommends netcat && \
#    apt autoremove -y && \
#    apt clean && \
#    rm -rf /var/lib/apt/lists/*

# install dependencies
# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --no-cache /wheels/*

# set work directory
# WORKDIR /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy our django project
COPY ./shipment .

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]