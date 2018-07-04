from django.shortcuts import render
from django.http import HttpResponse
import re
class LoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    # 当把该类实例化的对象，当做方法或函数直接调用时触发
    def __call__(self,request):
        # 当前用户请求的url路径
        u = request.path
        # 定义后台请求的登录验证
        if re.match('/myadmin/',u) and u not in ['/myadmin/login/']:
            # 判断是否登录
            if not request.session.get('_auth_user_id',None):
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/?next='+u+'"</script>')

        # 定义前台请求的登录验证
        # 定义需要登录的ｕｒｌ请求
        urllist = ['/ordercheck/','/addressedit/','/addressadd/','/ordercreate/','/buy/','/buysuccess/','/mycenter/','/myorders/',]
        # 判断当前的请求是否需要登录
        if u in urllist:
            # 验证是否登录
            if not request.session.get('VipUser',None):
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/login/?next='+u+'"</script>')

        response = self.get_response(request)
        return response