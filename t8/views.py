from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, send_mass_mail
from django.template import loader
from .my_util import get_random_str
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import logging
logger = logging.getLogger('django')
# Create your views here.

def send_my_email(req):
    title = "阿里offer"
    msg = "恭喜你获得酱油一瓶"
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        'liuda@1000phone.com',
    ]
    # 发送邮件
    send_mail(title, msg, email_from, reciever)
    return HttpResponse("ok")

def send_email_v1(req):
    title = "阿里offer"
    msg = " "
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        'liuda@1000phone.com',
    ]
    # 加载模板
    template = loader.get_template('email.html')
    # 渲染模板
    html_str = template.render({'msg': '双击666'})
    print(html_str)
    # 发送邮件
    send_mail(title, msg, email_from, reciever, html_message=html_str)
    return HttpResponse("ok")

def verify(req):
    if req.method == "GET":
        return render(req, 'verify.html')
    else:
        param = req.POST
        email = param.get("email")
        # 生成随机字符
        random_str = get_random_str()
        # 拼接验证连接
        url = "http://sharemsg.cn:12348/t8/active/" + random_str
        # 加载激活模板
        tmp = loader.get_template('active.html')
        # 渲染
        html_str = tmp.render({'url': url})

        # 准备邮件数据
        title = "阿里offer"
        msg = " "
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = [
            email,
        ]
        send_mail(title, msg, email_from, reciever, html_message=html_str)
        # 记录 token对应的邮箱是谁
        cache.set(random_str, email, 120)
        return HttpResponse("ok")


def active(req, random_str):
    # 拿参数对应缓存数据
    res = cache.get(random_str)
    if res:
        # 通过邮箱找到对应用户
        # 给用户的状态字段做更新 从未激活态变成激活状态

        return HttpResponse(res+"激活成功")
    else:
        return HttpResponse("验证连接无效")


def send_many_email(req):
    title = "阿里offer"
    content1 = "恭喜你获得酱油一瓶"
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever1 = [
        'liuda@1000phone.com',
        '554468924@qq.com'
    ]
    content2 = "well done !!!"
    # 邮件1
    msg1 = (title, content1, email_from, reciever1)
    # 邮件2
    msg2 = ("小伙子", content2, email_from, ['360970943@qq.com', 'liuda@1000phone.com'])

    send_mass_mail((msg1, msg2), fail_silently=True)
    return HttpResponse("ok")

def test_log(req):
    logger.info("要下课了")
    return HttpResponse("好开心")

# @csrf_exempt #去掉校验
@csrf_protect
def my_csrf(req):
    if req.method == "GET":
        return render(req, 'jifen.html')
    else:
        params = req.POST
        msg = "给{u_name}充值了{num}".format(
            u_name=params.get('u_name'),
            num=params.get("num")
        )
        print(msg)
        return HttpResponse("ok")