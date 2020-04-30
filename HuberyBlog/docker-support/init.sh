#!/bin/bash
cd /HuberyBlog
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
echo "from user.models import UserInfo; UserInfo.objects.create_superuser('admin', 'admin@example.com', '123456')" | python3 manage.py shell
echo "from blog.models import MessageBoard; MessageBoard.objects.get_or_create(id=1, name='message')" | python3 manage.py shell
python3 ./apps/hot/tasks.py

