# -*- coding: utf-8 -*-

from django.http import HttpResponse

from testmodel.models import test


# 数据库操作
def testdb(request):
    test1 = test(first_name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")