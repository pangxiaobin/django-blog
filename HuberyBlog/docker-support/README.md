### docker部署
#### 1.安装docker和docker-compose
- 安装参考地址 https://yeasy.gitbook.io/docker_practice/
#### 2.构建并启动容器
```shell
# 创建镜像并运行
# 加参数 -d  后台启动 docker-compose up -d
docker-compose up

# 初始化数据库
docker-compose run --rm web ./init.sh
# 进入容器
docker exec -it huberyblog_web bash
# 启动服务
./start.sh
# 退出容器
exit 
```
#### 访问127.0.0.0.1:80 可看到首页内容
