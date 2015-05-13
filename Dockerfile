FROM ubuntu
RUN mkdir /opt/webarya
WORKDIR /opt/webarya
ADD . /opt/webarya
RUN apt-get update && apt-get install -y python-pip && pip install -r requirements.txt
RUN python setup.py install
WORKDIR /opt/webarya/webarya
EXPOSE 80
CMD python webarya.py -p 80
