from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Users,Types,Goods
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
# 首页
def index(request):
     # 先获取所有的顶级分类
    data = Types.objects.filter(pid=0)
    print(data)
    erdata = []
    for x in data:
        # 获取当前类下的子类
        x.sub = Types.objects.filter(pid=x.id)
        for v in x.sub:
            #获取当前子类下的商品 
            v.goodssub = Goods.objects.filter(typeid=v.id)
            erdata.append(v)

    context = {'typegoodslist':data,'erdata':erdata}
    return render(request,'myhome/index.html',context)
# 列表
def list(request,tid):

    # 根据分类id获取商品信息
    data = Goods.objects.filter(typeid=tid)
    print(data)
    context = {'goodslist':data}
    return render(request,'myhome/list.html',context)
# 搜索
def search(request):

    # 获取搜索参数   
    keywords = request.GET.get(keywords,None)
    if not keywords:
        return HttpResponse('<script>history.back(-1)</script>')
    # 商品的模糊搜索
    data = Goods.objects.filter(title__contains=keywords)        
    context = {'goodslist':data}
    return render(request,'myhome/search.html',context)
# 详情
def info(request, sid):
    try:
        # 根据商品id获取商品信息    
        data = Goods.objects.get(id=sid)
        context = {'ginfo':data}
        return render(request,'myhome/info.html',context)
    except:
        pass
# 登录
def login(request):
    if request.method == 'GET':
        return render(request,'myhome/login.html')
    elif request.method == 'POST':
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
        # 进行登录
        # 根据用户名检测用户对象是否正确，再根据密码判断是否正确
        try:
            ob = Users.objects.get(username == request.POST['username'])
            res = check_password(request.POST['password'],ob.password)
            if res:
                # 密码正确
                request.session['VipUser'] = {'uid':ob.id,'username':ob.username}
                return HttpResponse('<script>alert("登录成功");location.href="/"</script>')
        except:
            pass
            # 密码或用户名错误
        return HttpResponse('<script>alert("密码或用户名错误");history.back(-1)</script>')

# 购物车
# 加入购物车
def addcart(request):
    # 获取商品id,商品购买数量
    sid = request.GET['sid']
    num = int(request.GET['num'])
    # 先获取购物车的商品数据
    data = request.session.get('cart',{})
    # 判断要购物的商品是否已经存在购物车里
    if sid in data.keys():
        # 存在,修改数量
        data[sid]['num'] += num
    else: 
        # 不存在,添加    
        # 定义加入购物车的商品数据格式    
        ob = Goods.objects.get(id=sid)
        goods = {'id':ob.id,'title':ob.title,'price':float(ob.price),'pics':ob.pics,'num':num}
        # print(goods)
        # 把商品加入购物车    
        data[sid] = goods
        # 把购物车存入session
    request.session['cart'] = data
    return HttpResponse('1')
# 购物车列表
def cartlist(request):
    data = request.session['cart'].values()
    return render(request,'myhome/cart.html',{'data':data})

# 删除购物车商品
def delcart(request):
    return HttpResponse('删除商品')

# 修改购物车商品数量
def editcart(request):
    # 获取商品id,商品购买数量
    sid = request.GET['sid']
    num = int(request.GET['num'])
    # 在ｓｅｓｓｉｏｎ获取购物车数据
    data = request.session['cart']
    # 修改
    data[sid]['num'] = num
    # 重新写入ｓｅｓｓｉｏｎ
    request.session['cart'] = data
    return HttpResponse('0')

# 清空购物车
def cartclear(request):
    data = request.session['cart'] = {}    
    return HttpResponse('<script>location.href="/cartlist/"</script>')



# 注册
def register(request):
    if request.method == 'GET':
        return render(request,'myhome/register.html')  
    elif request.method == 'POST':
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
            
    # 接受表单提价的数据
    data = request.POST.copy().dict()
    # 删除掉ｃｓｒｆ验证的字段数据
    del data['csrfmiddlewaretoken']    
    del data['vcode']
    try:
        # 进行密码加密
        data['password'] = make_password(data['password'],None,'pbkdf2_sha256')
        # 执行用户的注册
        ob = Users.objects.create(**data)
        # 记录用户登录的状态　
        request.session['VipUser'] = {'uid':ob.id,'username':ob.username}
        return HttpResponse('<script>alert("注册成功");location.href="/"</script>')
    except:
        pass
    return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')
# 退出
def logout(request):
    request.session['VipUser'] = {}
    return HttpResponse('<script>alert("退出成功");location.href="/"</script>')  
# 验证码
def vcode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 32
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 4), rand_str[0], font=font, fill=fontcolor)
    draw.text((30, 4), rand_str[1], font=font, fill=fontcolor)
    draw.text((55, 4), rand_str[2], font=font, fill=fontcolor)
    draw.text((80, 4), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')