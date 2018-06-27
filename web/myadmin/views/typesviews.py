from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types
# Create your views here.
def gettypesorder():
    # 获取所有分类信息
    tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    for x  in tlist:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            t = Types.objects.get(id=x.pid)
            x.pname = t.name
        num  = x.path.count(',')-1
        x.name = (num*'|----')+x.name
    return tlist
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
            tlist = Types.objects.filter(
                Q(name__contains=keywords)
            )
        elif types == 'name':
            # 按照商品名搜索
            tlist = Types.objects.filter(name__contains=keywords)

    else:
        tlist = gettypesorder()
    # context = {'tlist':tlist}
    from django.core.paginator import Paginator
    # 实例化分类页　参数１　数据集合　参数２　每页显示条数
    paginator = Paginator(tlist,10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    ulist = paginator.page(p)
    # 分配数据
    context = {'tlist':ulist}
    # 加载模板
    return render(request,'myadmin/types/list.html',context)
def add(request):
    if request.method == 'GET':
        tlist = gettypesorder()
        context = {'tlist':tlist}
        # 显示添加页面
        return render(request,'myadmin/types/add.html',context)
    elif request.method == 'POST':
        # 执行分类添加
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        if ob.pid == 0:
            ob.path = '0,'
        else:
            # 根据当前父级ｉｄ获取ｐａｔｈ在添加当前父级ｉｄ
            t = Types.objects.get(id=ob.pid)
            ob.path = t.path+str(ob.pid)+','
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

def delete(request):
    tid = request.GET.get('uid',None)
    # 判断当前类下是否有子类
    num = Types.objects.filter(pid=tid).count()
    if num != 0:
        data = {'msg':'当前类下有子类,不能删除','code':1}
    else:
        # 判断当前类下是否有商品
        ob = Types.objects.get(id=tid)
        ob.delete()
        data = {'msg':'删除成功','code':0}
    return JsonResponse(data)
def edit(request):
    tid = request.GET.get('uid',None)
    # 获取对象数据
    ob = Types.objects.get(id=tid)
    if request.method == 'GET':
        if ob.pid == 0:
            ob.pname = '顶级分类'
        else:
            ob.pname = Types.objects.get(id=ob.pid).name
        # 分配数据
        # tinfo = gettypesorder()
        context = {'tinfo':ob}
        # 显示编辑页面
        return render(request,'myadmin/types/edit.html',context)
    elif request.method == 'POST':
        try:
            ob.name = request.POST['name']
            ob.save()
            return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_types_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("更新失败");location.href="'+reverse('myadmin_types_edit')+'?uid='+str(ob.id)+'"</script>')
