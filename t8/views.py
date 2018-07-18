from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from .my_util import get_random_str


def send_my_email(req):
    title ='中国联通'
    message ='你的手机已欠费'
    from_email =settings.DEFAULT_FROM_EMAIL
    reciever =['360970943@qq.com',]
    send_mail(title,message,from_email,reciever)
    return HttpResponse('ok')
def send_email_v1(req):
    title ='阿里巴巴'
    msg =''
    email_from =settings.DEFAULT_FROM_EMAIL
    reciever =['360970943@qq.com',]
    template =loader.get_template('email.html')
    html_str =template.render({'msg':'双击666'})
    send_mail(title,msg,email_from,reciever,html_message=html_str)
    return HttpResponse('OK')
def verify(req):
    if req.method =='GET':
        return render(req,'verify.html')
    else:
        email =req.POST.get('email')
        random_str =get_random_str()
        url ='http://120.77.46.173:12348/t8/active'+random_str
        tmp =loader.get_template('active.html')
        html_str =tmp.render({'url':url})
        title = '阿里巴巴'
        msg = ''
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = ['360970943@qq.com', ]
        send_mail(title,msg,email_from,reciever,html_message=html_str)
        return HttpResponse('OK')