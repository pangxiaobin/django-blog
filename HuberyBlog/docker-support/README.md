### docker部署
#### 1.安装docker和docker-compose
- 安装参考地址 https://yeasy.gitbook.io/docker_practice/
#### 2.构建并启动容器
```shell
cd ./django-blog/HuberyBlog
# 创建镜像并运行
# 加参数 -d  后台启动 docker-compose up -d
docker-compose up

# 新打开一个终端
# 初始化数据库
docker-compose run --rm web ./init.sh
# 进入容器(huberyblog_web_1 为容器名,具体可使用docker container ls 查看)
docker exec -it huberyblog_web_1 bash

# 启动服务
./start.sh
# 退出容器
exit 
```
#### 访问127.0.0.0.1:80 可看到首页内容 默认管理员账号:admin 密码:123456
