FROM ubuntu:16.04
WORKDIR /HuberyBlog
COPY . .
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& apt-get clean && apt-get update && apt-get install -y python3 \
python3-pip  && apt-get install -y nginx && pip3 install -i \
https://pypi.douban.com/simple/ --upgrade pip && apt-get remove -y \
python3-pip && easy_install3 pip && rm -rf /var/lib/apt/lists/*
RUN pip install -i https://pypi.douban.com/simple/ -r ./requirements.txt
COPY ./hubery_nginx.conf /etc/nginx/conf.d/default.conf
ENV DJANGO_SECRET_KEY fekukruj0n15v9e_zhe$si+^0p!p$hi0m^0fqo#tgot20))a5s
ENV DJANGO_DEBUG False
ENV DJANGO_LOCATION  redis://redis:6379/1
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV EMAIL_HOST_USER 1456819312@qq.com
ENV DEFAULT_RECEIVE_EMAIL 2274858959@qq.com
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

EXPOSE 80
COPY ./docker-support/start.sh /HuberyBlog/start.sh
COPY ./docker-support/init.sh /HuberyBlog/init.sh
RUN chmod +x /HuberyBlog/start.sh
RUN chmod +x /HuberyBlog/init.sh