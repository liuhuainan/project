from django.shortcuts import render
from django.http import HttpResponse
# from myadmin.models import Users,
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def index(request):
    return render(request,'myadmin/index.html')
# # 登录
# def login(request):
#     if request.method == 'GET':
#         return render(request,'myadmin/login.html')
#     elif request.method == 'POST':
#         # 执行登录
#          # 根据用户名检测用户对象是否正确，再根据密码判断是否正确
#         try:
#             ob = User.objects.get(username = request.POST['username'])
#             res = check_password(request.POST['password'],ob.password)
#             # print(ob)
#             # return HttpResponse('登录成功')
#             if res:
#                 # 密码正确
#                 request.session['AdminUser'] = {'uid':ob.id,'username':ob.username}
#                 return HttpResponse('<script>alert("登录成功");location.href="/myadmin/"</script>')
#         except:
#             pass
#             # 密码或用户名错误
#         return HttpResponse('<script>alert("密码或用户名错误");history.back(-1)</script>')
# # 退出
# def logout(request):
    request.session['AdminUser'] = {}
    return HttpResponse('<script>alert("退出成功");location.href="/myadmin/login/"</script>')