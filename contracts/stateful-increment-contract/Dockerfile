FROM python:alpine3.8
RUN pip install requests
ADD contract.py /
ADD run.sh /
RUN chmod +x run.sh
RUN apk add --no-cache --update iptables
RUN apk add --no-cache curl
CMD exec /bin/sh -c "trap : TERM INT; (while true; do sleep 1000; done) & wait"