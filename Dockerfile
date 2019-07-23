FROM python:3.6

ENV APP_DIR_NAME DynamicQoS
ENV APP_PATH /opt/$APP_DIR_NAME

#installing django
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN rm requirements.txt
#installing scapy
RUN git clone https://github.com/secdev/scapy.git
WORKDIR scapy
RUN python setup.py install

#adding entrypoint scripts
COPY docker-entrypoint.sh /
COPY create_superuser.py /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

#adding the django project
RUN mkdir -p $APP_PATH
COPY $APP_DIR_NAME $APP_PATH

