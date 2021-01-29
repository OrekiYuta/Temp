# tjNxK8Z89R8eltxu4CQ4GByX

# qEIlkzoIIgNli6G9gwGEqapDVrDENW3z
# https://cloud.baidu.com/doc/NLP/s/Okahxcw9u

# https://aip.baidubce.com/oauth/2.0/token

import requests
import base64


# https://cloud.baidu.com/doc/NLP/s/Okahxcw9u
def get_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'tjNxK8Z89R8eltxu4CQ4GByX',
        'client_secret': 'qEIlkzoIIgNli6G9gwGEqapDVrDENW3z'
    }

    res = requests.post(url, data)

    # print(res)
    if res.status_code == 200:
        result = res.json()
        # print(result)
        token = result['access_token']

    else:
        print("get token failed")

    return token


# https://cloud.baidu.com/doc/IMAGEPROCESS/s/Mk4i6olx5

# https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime

def anime():
    url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime'
    f = open('tes.jpg', 'rb')
    data = f.read()
    data_encode = base64.b64encode(data)
    params = {"image": data_encode,
              "type": 'anime_mask',
              'mask_id': '1'
              }
    access_token = get_token()
    request_url = url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response.status_code == 200:
        print(response.json())
        data = response.json()
        result = data['image']
        result = base64.b64decode(result)
        f = open('after.jpg', 'wb')
        f.write(result)
        f.close()

# print(get_token())
if __name__ == '__main__':
    anime()