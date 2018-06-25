from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from . typesviews import gettypesorder
from . userviews import uploads
from .. models import Goods,Types
import os
# Create your views here.
def index(request):
    glist = Goods.objects.all()
    context = {'glist':glist}
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
        pic = uploads(request)
        if pic == 1:
            return HttpResponse('<script>alert("图片类型错误");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        # 执行商品的添加
        # 接受表单提交的数据
        data = request.POST.copy().dict()
        # 删除ｃｓｒｆ验证的字段数据
        del data['csrfmiddlewaretoken']
        data['pics'] = pic
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
    pass