from django.shortcuts import render,reverse
from django.http import HttpResponse
from .. models import Orders
from django.contrib.auth.decorators import permission_required

# Create your views here.
# @permission_required('myadmin.show_orders',raise_exception = True)
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
            orderlist = Orders.objects.filter(
                Q(id__contains=keywords)|
                Q(totalprice__contains=keywords)|    
                Q(totalnum__contains=keywords)                                
            )
        elif types == 'id':
            # 按照订单id搜索
            orderlist = Orders.objects.filter(id__contains=keywords)
        elif types == 'status':
            # 按照订单状态搜索
            orderlist = Orders.objects.filter(status__contains=keywords)
        elif types == 'totalprice':
            # 按照价格搜索
            orderlist = Orders.objects.filter(totalprice__contains=keywords)
        elif types == 'totalnum':
            # 按照数量搜索
            orderlist = Orders.objects.filter(totalnum__contains=keywords)
    else:
        # 获取所有用户数据
        orderlist = Orders.objects.all()
       
    # print(orderlist)
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分类页　参数１　数据集合　参数２　每页显示条数
    paginator = Paginator(orderlist,5)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    olist = paginator.page(p)
    context = {'orderlist':olist}
    return render(request,'myadmin/orders/list.html',context)
# @permission_required('myadmin.edit_orders',raise_exception = True)
def edit(request):
    uid = request.GET.get('uid',None)           
    olist = Orders.objects.get(id=uid)
    if request.method == 'GET':
        context = {'olist':olist}
        return render(request,'myadmin/orders/edit.html',context)
    elif request.method == 'POST':
        try:
            olist.status = request.POST['status']
            # print(olist)
            olist.save()
        # return HttpResponse('订单修改')
            return HttpResponse('<script>alert("修改订单成功");location.href="'+reverse('myadmin_orders_index')+'"</script>')
                        
        except:
            return HttpResponse('<script>alert("修改订单状态失败");history.back(-1)</script>')
