FROM ubuntu:jammy as base

COPY    setup-mongo /setup/

RUN     apt update && apt -y install wget gpg && \
        wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc |  gpg --dearmor | tee /usr/share/keyrings/mongodb.gpg > /dev/null && \
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
        apt update && \
        apt -y install mongodb-org && \
        mkdir /data/db -p && \
        mongod --fork --logpath /var/log/mongod.log && \
        bash /setup/setup-mongo
        
COPY    sylva-etl_*_all.deb /setup/

RUN     apt -y install /setup/sylva-etl_*_all.deb && \
        mkdir /home/sylva/incoming && \
        mkdir /home/sylva/archive && \
        mkdir /home/sylva/trash && \
        mkdir /home/sylva/testdata && \
        mkdir /home/sylva/tests

COPY    testdata /home/sylva/testdata
COPY    tests /home/sylva/tests

RUN     mongod --fork --auth --logpath /var/log/mongod.log && \
        bash /home/sylva/tests/prep-clearmongo && \
        bash /home/sylva/tests/test-archive && \
        bash /home/sylva/tests/prep-clearmongo && \
        bash /home/sylva/tests/test-params