from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from . typesviews import gettypesorder
from . userviews import uploads
from .. models import Goods,Types
import os
# Create your views here.
def index(request):
    # 获取搜索条件
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否具有搜索条件
    # print(types,keywords)
    if types:
        if types == 'all':
            # 有搜索条件
            from django.db.models import Q
            glist = Goods.objects.filter(
                Q(title__contains=keywords)|
                Q(price__contains=keywords)|
                Q(store__contains=keywords)|
                Q(clicknum__contains=keywords)       
            )
        elif types == 'title':
            # 按照商品名搜索
            glist = Goods.objects.filter(title__contains=keywords)
        elif types == 'price':
            # 按照商品价格搜索
            glist = Goods.objects.filter(price__contains=keywords)
        elif types == 'store':
            # 按照库存搜索
            glist = Goods.objects.filter(store__contains=keywords)
        elif types == 'clicknum':
            # 按照点击搜索
            glist = Goods.objects.filter(clicknum__contains=keywords)
    else:
        # 获取所有用户数据
        glist = Goods.objects.all()
    # context = {'glist':glist}
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分类页　参数１　数据集合　参数２　每页显示条数
    paginator = Paginator(glist,10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    ulist = paginator.page(p)
    # 分配数据
    context = {'glist':ulist}
    # 加载模板
    return render(request,'myadmin/goods/list.html',context)
def add(request):
    if request.method == 'GET':
        tlist = gettypesorder()
        context = {'tlist':tlist}
        return render(request,'myadmin/goods/add.html',context)

    elif request.method == 'POST':
        # 先判断是否有图片上传
        if not request.FILES.get('pic',None):
            return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')
        pics = uploads(request)
        if pics == 1:
            return HttpResponse('<script>alert("图片类型错误");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        # 执行商品的添加
        # 接受表单提交的数据
        data = request.POST.copy().dict()
        # 删除ｃｓｒｆ验证的字段数据
        del data['csrfmiddlewaretoken']
        data['pics'] = pics
        data['typeid'] = Types.objects.get(id=data['typeid'])
        # 执行商品创建
        ob = Goods.objects.create(**data)
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')

def delete(request):
    try:
        uid = request.GET.get('uid',None)
        print(uid)
        ob = Goods.objects.get(id=uid)
        # print(ob)
        # 判断当前商品是否有图像，有删除
        if ob.pics:
            os.remove('.'+ob.pics)
        ob.delete()
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}
    return JsonResponse(data)
def edit(request):
    # 接收参数
    uid = request.GET.get('uid',None)    
    # 获取对象
    ob = Goods.objects.get(id=uid)
    # print(ob)
    if request.method == 'GET':
        # 分配数据
        context = {'uinfo':ob}
        # 显示编辑页面
        return render(request,'myadmin/goods/edit.html',context)
    elif request.method == 'POST':
        try:
            # 判断是否上传了新的图片
            if request.FILES.get('pic',None):
                if ob.pics:
                    # 如果使用的不是默认图,则删除之前上传的头像
                    os.remove('.'+ob.pics)
                # 执行上传
                ob.pics = uploads(request)
                print(ob.pics)
            ob.title = request.POST['title']
            ob.descr = request.POST['descr']
            ob.price = request.POST['price']
            ob.store = request.POST['store']
            ob.save()
            return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("更新失败");location.href="'+reverse('myadmin_goods_list')+'"</script>')
                      
        