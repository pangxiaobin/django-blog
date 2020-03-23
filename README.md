# HuberyBlog
基于django的博客系统

### 一、下载
```git clone https://github.com/pangxiaobin/django-blog.git```

### 二、环境配置
```
mkvitualenv blog
# 进入项目
cd ./django-blog
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requments.txt
```
### 三、运行项目
```
cd ./HuberBlog
# 添加日志文件
mkdir log && cd log
touch blog_info.log blog_error.log
cd ..
python manage.py migrate
# 创建管理员用户
python manage.py createsuperuser 
```

- 运行redis
- 运行css文件压缩
```
python manage.py compress
```
- 运行项目
```
python manage.py runserver
```
进入后台在博客--》留言--》增加留言 留言id为1

 ### 四、内容添加
登录后台，用刚创建的管理员用户登录
可以后台操作添加首页轮播图和文章
具体的文章标签和分类也都需要后台添加
###　五、其他
网站内有爬虫，需要运行celery 
```
# 调试运行
# 新开一个窗口 进入环境 和 项目下
celery -A HuberyBlog worker -l info
```
要想查看热榜效果 请运行
```
cd apps/hot
python tasks.py
```
