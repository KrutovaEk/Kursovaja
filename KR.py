import time
import requests
from tqdm import tqdm
import json
from time import sleep
from urllib.parse import urlencode

# OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
# user_id = ID Vk
# params = {
#     'client_id':user_id,
#     'redirect_uri':'https://oauth.vk.com/blank.html',
#     'display':'page',
#     'scope':'status, photos',
#     'response_type':'token'
# }
# access_tokens =f'{OAUTH_BASE_URL}?{ urlencode(params)}'
# print(access_tokens)


class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

#    def users_info(self):
#        url = 'https://api.vk.com/method/users.get'
#        params = {'user_ids': self.id}
#        response = requests.get(url, params={**self.params, **params})
#        return response.json()

   def save_photo(self, user_id, count=5):
       self.count=count
       url_photo = 'https://api.vk.com/method/photos.get'
       params = {
           'user_id':  user_id,
           'album_id': 'wall',
           'rev': False,
            'extended': True,
            'photo_sizes': True,
            'access_token': access_token,
            'count': count,
            'v': '5.131'
            }
       res = requests.get(url_photo, params=params)
       res_str = res.json()
       res_str_response = res_str['response']['items']
       list = {}
       fail_f=[]
    #    fail={}
       for item in tqdm(res_str_response):
            fail={}
            if not item['likes']['count'] in list:
                name=item['likes']['count']
            else:
                name=str(item['likes']['count'])+'_lk_'+time.strftime("%d_%b_%Y_%H_%M_%S", time.localtime(item['date']))
            ght=0
            l=''
            s=''
            sizes_response=item['sizes']
            for j in sizes_response:
                if  j['height']>ght:
                    ght=j['height']
                    l=j['url']
                    s=j['type']
                    # print(ght,l)
                else:
                    ght=ght
                    l=l
                    s=s
            list[name]=l
            fail['file_name']=name
            fail["size"]=s
            fail_f.append(fail) 

            sleep(0.5)

       return list, fail_f
   
   def fail_f(self, fail): 
       self.fail=fail
       fail_foto={}
       for i in range(len(fail)):
           fail_foto[i]=fail[i]
       #print(fail_foto)
       fail_foto_json = json.dumps(fail_foto)

       with open("fail_foto.json", "w") as my_file:
           my_file.write(fail_foto_json)

class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def ivk(self):
        per= 'https://cloud-api.yandex.net/v1/disk/resources'
        fer= {'Authorization': 'OAuth ' + token}
        path={'path':'IVK' }
        res=requests.put(per, headers=fer, params=path)
        # print(res.status_code)
    def upload(self, list):
        self.list = list
        #print(list)

     

        for key, value in tqdm(list.items()): 
            per= 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            fer= {'Authorization': 'OAuth ' + token}
            #print(key)
            path={'path':f'IVK/{key}',
                   'url':value}
            res=requests.post(per, headers=fer, params=path)
            
            # print(res.status_code)
            sleep(0.5)


if __name__ == '__main__':
   
    access_token = # токен VK
    user_id = # ID VK
    vk = VK(access_token, user_id)
    s=vk.save_photo(user_id, 6)[0]
    f=vk.save_photo(user_id, 6)[1]
    vk.fail_f(f)
    # print(vk.save_photo(user_id, 4))
    
    token = # токен Яндекс Диска
    uploader = YaUploader(token)
    result = uploader.ivk()
    result = uploader.upload(s)

    










