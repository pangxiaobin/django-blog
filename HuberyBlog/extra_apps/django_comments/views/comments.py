from __future__ import absolute_import

from django import http
from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

import django_comments
from blog.models import Blog
from django_comments import signals
from django_comments.views.utils import next_redirect, confirmation_view

# 添加这两个引用，为了返回json数据
from django.http import HttpResponse
import json
from HuberyBlog import settings

from asynchronous_send_mail import send_mail

# 添加返回json的方法，json结构有3个参数（code:返回码,is_success:是否处理成功,message:消息内容）
def ResponseJson(code, is_success, message):
    data = {'code': code, 'success': is_success, 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")


class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})


@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated:
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        # return CommentPostBadRequest("Missing content_type or object_pk field.")
        return ResponseJson(503, False, 'Missing content_type or object_pk field.')
    try:
        model = apps.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        # return CommentPostBadRequest(
        #    "Invalid content_type value: %r" % escape(ctype))
        return ResponseJson(504, False, "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        # return CommentPostBadRequest(
        #    "The given content-type %r does not resolve to a valid model." % escape(ctype))
        return ResponseJson(505, False,
                            "The given content-type %r does not resolve to a valid model." % escape(ctype))
    except ObjectDoesNotExist:
        # return CommentPostBadRequest(
        #    "No object matching content-type %r and object PK %r exists." % (
        #        escape(ctype), escape(object_pk)))
        return ResponseJson(506, False,
                            "No object matching content-type %r and object PK %r exists." % (escape(ctype),
                                                                                             escape(object_pk)))
    except (ValueError, ValidationError) as e:
        # return CommentPostBadRequest(
        #    "Attempting go get content-type %r and object PK %r exists raised %s" % (
        #        escape(ctype), escape(object_pk), e.__class__.__name__))
        return ResponseJson(507, False,
                            "Attempting go get content-type %r and object PK %r exists raised %s" % (escape(ctype),
                                                                                                     escape(object_pk),
                                                                                                     e.__class__.__name__))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = django_comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        # return CommentPostBadRequest(
        #    "The comment form failed security verification: %s" % escape(str(form.security_errors())))
        return ResponseJson(508, False, "The comment form failed security verification: %s" %
                            escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
            # These first two exist for purely historical reasons.
            # Django v1.0 and v1.1 allowed the underscore format for
            # preview templates, so we have to preserve that format.
            "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s_preview.html" % model._meta.app_label,
            # Now the usual directory based template hierarchy.
            "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.model_name),
            "comments/%s/preview.html" % model._meta.app_label,
            "comments/preview.html",
        ]
        # return render(request, template_list, {
        #         "comment": form.data.get("comment", ""),
        #         "form": form,
        #         "next": data.get("next", next),
        #     },
        # )
        return ResponseJson(509, False, form.data.get("comment", ""))

    # Otherwise create the comment
    comment = form.get_comment_object(site_id=get_current_site(request).id)
    comment.ip_address = request.META.get("REMOTE_ADDR", None) or None

    # 增加回复的字段
    comment.root_id = data.get('root_id', 0)
    comment.reply_to = data.get('reply_to', 0)
    comment.reply_name = data.get('reply_name', '')

    if request.user.is_authenticated:
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response is False:
            # return CommentPostBadRequest(
            #     "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)
            return ResponseJson(510, False,
                                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )
    try:
        # 判断评论对象是否Wie博文
        if str(comment.content_type) == '文章':  # 模型的verbose_name
            blog = Blog.objects.filter(id=comment.object_pk).first()
            subject = ''
            message = ''
            from_mail = settings.DEFAULT_FROM_EMAIL
            recipient_list = []
            html_message = ''
            if int(comment.root_id) == 0:
                subject = '[Hubery的博客]博文评论'
                temp = loader.get_template('email/comment.html')
                recipient_list.append('2274858959@qq.com')
                data = {
                    'user_name': blog.uid.username,
                    'comment_name': comment.user_name,
                    'blog_title': blog.title,
                    'blog_url': 'http://127.0.0.0:8000/blog/read/?blogid=%s' % blog.id,
                    'comment_content': comment.comment

                }
                html_message = temp.render(data)
            else:
                subject = '[Hubery的博客]博文回复'
                temp = loader.get_template('email/replay.html')
                recipient_list.append(comment.user_email)
                # 获取评论对象，找到回复对应的评论
                data = {
                    'replay_name': comment.reply_name,
                    'comment_name': comment.user_name,
                    'blog_title': blog.title,
                    'blog_url': 'http://127.0.0.0:8000/blog/read/?blogid=%s' % blog.id,
                    'comment_content': comment.comment

                }
                html_message = temp.render(data)
            send_mail(subject, message, from_mail, recipient_list=recipient_list,
                      fail_silently=False, html_message=html_message)
        elif str(comment.content_type) == '留言':
            subject = ''
            message = ''
            from_mail = settings.DEFAULT_FROM_EMAIL
            recipient_list = []
            html_message = ''
            if int(comment.root_id) == 0:
                subject = '[Hubery的博客]留言板评论'
                temp = loader.get_template('email/comment.html')
                recipient_list.append('2274858959@qq.com')
                data = {
                    'user_name': 'hubery',
                    'comment_name': comment.user_name,
                    'blog_title': '留言板',
                    'blog_url': 'http://127.0.0.0:8000/blog/message_board/',
                    'comment_content': comment.comment

                }
                html_message = temp.render(data)
            else:
                subject = '[Hubery的博客]博文回复'
                temp = loader.get_template('email/replay.html')
                recipient_list.append(comment.user_email)
                # 获取评论对象，找到回复对应的评论
                data = {
                    'replay_name': comment.reply_name,
                    'comment_name': comment.user_name,
                    'blog_title': '留言评论',
                    'blog_url': 'http://127.0.0.0:8000/blog/message_board/',
                    'comment_content': comment.comment

                }
                html_message = temp.render(data)
            send_mail(subject, message, from_mail, recipient_list=recipient_list,
                      fail_silently=False, html_message=html_message)
        else:
            pass
    except Exception as e:
        print(e)

    # return next_redirect(request, fallback=next or 'comments-comment-done',
    #                     c=comment._get_pk_val())
    return ResponseJson(200, True, 'comment success')


comment_done = confirmation_view(
    template="comments/posted.html",
    doc="""Display a "comment was posted" success page."""
)
