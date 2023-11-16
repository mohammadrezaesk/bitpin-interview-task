FROM python:3.9.16

RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get -y install tzdata && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime
RUN apt-get install -y git vim curl --fix-missing
RUN apt-get install -y gettext libgettextpo-dev
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install -y netcat --fix-missing

RUN mkdir /code
WORKDIR /code

RUN pip install --ignore-installed poetry==1.3.1
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /code/

# to prevent poetry from installing my actual app,
# and keep docker able to cache layers
RUN mkdir -p /code/temp/code
RUN touch /code/temp/code/__init__.py

RUN poetry install -n

# now actually copy the real contents of my app
COPY . .

ENTRYPOINT ["sh", "./scripts/docker-entrypoint.sh"]
