import json

from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'login.html')


def login(request):
    try:
        if request.method != 'POST':
            raise Exception('无效的请求方式')

        # 获取数据
        body_decode = request.body.decode()
        data = json.loads(body_decode)

        # 验证数据
        nickname = data.get('nickname', '')
        if nickname == '':
            raise Exception('缺少用户名')

        # 数据验证，返回auth
        auth = nickname

        return JsonResponse({'status': 1, 'auth': auth})

    except Exception as e:
        return JsonResponse({'status': 0, 'message': str(e)})


def chat(request):
    return render(request, 'chat.html')
