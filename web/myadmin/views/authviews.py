from django.shortcuts import render,reverse
from django.http import HttpResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate,login,logout


# Create your views here.
# 管理员添加
def useradd(request):
    if request.method == 'GET':
        # 获取所有组
        glist = Group.objects.all()
        context = {'glist':glist}
        return render(request,'auth/user/add.html',context)
    elif request.method == 'POST':
        # 执行管理员添加
        # 判断是否创建超级管理员
        if request.POST['is_superuser'] == '1':

            ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
        else:
            ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
        # 进行添加
        ob.save()
        # 判断是否需要为用户分配组 
        gs = request.POST.getlist('gs',None)
        if gs:
            # 给当前用户分组
            ob.groups.set(gs)
            ob.save()
        return HttpResponse('<script>alert("管理员添加成功");location.href="'+reverse('auth_user_list')+'"</script>')
        
# 管理员列表
def userlist(request):
    # 获取所有管理员
    data = User.objects.all()
    context = {'ulist':data}
    return render(request,'auth/user/list.html',context)

# 管理员删除
def userdel(request,uid):
    # 获取管理员id
    data = User.objects.get(id=uid)
    data.delete()
    # return HttpResponse('<script>location.href="/myadmin/auth/user/list"</script>')
    return HttpResponse('<script>alert("管理员删除成功");location.href="'+reverse('auth_user_list')+'"</script>')

# 组添加
def groupadd(request):
    if request.method == 'GET':
        # 读取所有权限信息,并排除以Can开头的系统默认生成权限
        perms = Permission.objects.exclude(name__istartswith='Can')
        context = {'perms':perms}
        return render(request,'auth/group/add.html',context)
    elif request.method == 'POST':
        # 创建组
        g = Group(name=request.POST['name'])
        g.save()
        # 获取选择的所有权限
        prms  = request.POST.getlist('prms',None)
        # 判断是否需要给组添加权限
        if prms:
            # 给组分配权限
            g.permissions.set(prms)
            g.save()
        # print('aa')
        return HttpResponse('<script>alert("组添加成功");location.href="'+reverse('auth_group_list')+'"</script>')
        
# 组列表
def grouplist(request):
    data = Group.objects.all()
    context = {'glist':data}
    return render(request,'auth/group/list.html',context)
# 编辑组
def groupedit(request,gid):
    # 获取当前组的信息
    ginfo = Group.objects.get(id=gid)
    if request.method == 'GET':
     
        # print(ginfo.permissions.all())

        # 读取所有权限信息,并排除已经有的权限
        perms = Permission.objects.exclude(group=ginfo).exclude(name__istartswith='Can')

        context ={'ginfo':ginfo,'perms':perms}
        return render(request,'auth/group/edit.html',context)
    elif request.method == 'POST':
        # 修改组名
        ginfo.name = request.POST['name']
        # 判断是否有权限
        prms  = request.POST.getlist('prms',None)
        #全部删除,在添加
        ginfo.permissions.clear()
        if prms:
            # 添加权限
            ginfo.permissions.set(prms)
        ginfo.save()
        return HttpResponse('<script>alert("组修改成功");location.href="'+reverse('auth_group_list')+'"</script>')

# 登录页面
def mylogin(request):
    # 如果访问当前页面的请求方式为GET ,则返回一个登录页面
    if request.method == 'GET':
        return render(request,'myadmin/login.html')

    elif request.method == 'POST':

        # 执行登录
        # 使用django提供的后台用户验证方法
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user:
            #登录
            login(request,user)
            return HttpResponse('<script>location.href="/myadmin/"</script>')

        return HttpResponse('<script>alert("用户名或密码不存在");location.href="/myadmin/login/"</script>')
    # return HttpResponse('登录')


def mylogout(request):
    # 退出登录
    logout(request)
    return HttpResponse('<script>alert("退出登录成功");location.href="/myadmin/login/"</script>')
