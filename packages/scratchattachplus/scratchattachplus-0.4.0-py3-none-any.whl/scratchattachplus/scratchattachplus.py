#import
import datetime
import sys
from typing import Literal
from scratchattach import *
import re
import requests
from enum import Enum

class comment_type(Enum):
    project = 0
    studio = 1
    user = 2

class Studio_report_type(Enum):
    title = 0
    description = 1
    thumbnail = 2

class User_report_type(Enum):
    username = 0
    icon = 1
    about_me = 2
    working_on = 3

def user_report(session:Session,username:str,types:User_report_type) -> None:
    """
    types:
    0:username
    1:icon
    2:about me
    3:working on
    """
    t = ["username","icon","about_me","working_on"]
    res = requests.post(
        f"https://scratch.mit.edu/site-api/users/all/{username}/report/?selected_field={t[types.value]}",
        headers = session._headers,
        cookies = session._cookies,
    )
    if res.status_code == 200:
        return
    raise ResponseError

def studio_report(session:Session,studioid:str,types:Studio_report_type) -> None:
    """
    types:
    0:title
    1:description
    2:thumbnail
    """
    t = ["title","description","thumbnail"]
    res = requests.post(
        f"https://scratch.mit.edu/site-api/galleries/all/{studioid}/report/?selected_field={t[types.value]}",
        headers = session._headers,
        cookies = session._cookies,
    )
    if res.status_code == 200:
        return
    raise ResponseError

def create_student_account(invite_id:str,username:str,password:str,**dict) -> str:
    return scratch_class_from_token(invite_id).create_student_account(username,password,**dict)

"""
class forum:
    def __init__(self,ids:int,session=None,pages:int=1):
        self._response = requests.get(f"https://scratch.mit.edu/discuss/{ids}?page={pages}")
        self.topic_list = re.findall('/discuss/topic/[1234567890]*/',self._response.text)
        self.topic_list = [self.topic_list[num][15:-1] for num in range(len(self.topic_list-1))]
        self.session = session
        return
    def get_topic(self,ids:int,pages:int=1):
        return topic(ids,self.session,pages)

class topic:
    def __init__(self,ids:int,session=None,pages:int=1):
        self._response = requests.get(f"https://scratch.mit.edu/discuss/topic/{ids}?page={pages}")
        self.__find1 = self._response.text.find("/discuss/feeds/topic/")
        self.__find2 = self._response.text[:self.__find1-18].rfind("&raquo;")
        self.title = self._response.text[self.__find2+8:self.__find1-18]
        self.session = session
        return
"""

def _add_method(Class, method, name:str|None=None) -> None:
    if name is None:
        setattr(Class, method.__name__, method)
    else:
        setattr(Class, name, method)



class scratch_class:
    def __init__(self,classid:int,session:Session|None=None,update:bool=True,_token:str|None=None) -> None:
        self.id = classid
        self._session = session
        self.token = _token
        if update:
            self.update()

    def update(self) -> None:
        r = requests.get(f"https://api.scratch.mit.edu/classrooms/{self.id}")
        if r.status_code != 200:
            raise ResponseError
        self._json = r.json()
        self._update_from_dict(self._json)

    def _update_from_dict(self,dict:dict) -> None:
        self.id = dict["id"]
        self.title = dict["title"]
        self.about_class = dict["description"]
        self.working_on = dict["status"]
        self.datetime = datetime.datetime.fromisoformat(dict["date_start"])
        self.author = User(username=dict["educator"]["username"],_session=self._session)
        self.author._update_from_dict(dict["educator"])

    def get_dict(self) -> dict:
        return {"id":self.id,"title":self.title,"description":self.about_class,"status":self.working_on,
                "date_start":self.datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z",
                'author': {'id': self.author.id, 'username': self.author.username, 'scratchteam': self.author.scratchteam,
                           "bio":self.author.about_me,"status":self.author.wiwo,'image': self.author.icon_url[:-9]+"60x60.png"}}

    def create_student_account(self,username:str,password:str,country:str="Japan",year:int=2000,month:int=1,warn:bool=False) -> str:
        # 制作する方法みつけたらdmください
        if not warn:
            input("WARN:現在正しく動作しません。この警告を回避するには 引数:warnをTrueにしてください。 Enterで続行...:")
        if requests.get(f"https://api.scratch.mit.edu/accounts/checkusername/{username}").json()["msg"] != "valid username":
            raise InvalidUsername
        token = get_csrf_token()
        requests.post(f"https://scratch.mit.edu/signup/{self.token}",headers={
            'Referer': f'https://scratch.mit.edu/signup/{self.token}',"x-csrftoken":token,"cookie":f"permissions=%7B%7D;scratchcsrftoken={token}"
        })
        response = requests.post(f"https://scratch.mit.edu/classes/register_new_student/"
                                f"?username={username}&password={password}&birth_month={month}&birth_year={year}&gender=male&country={country}&is_robot=false&" #female
                                f"classroom_id={self.id}&classroom_token={self.token}",
                                headers={'Referer': f'https://scratch.mit.edu/signup/{self.token}',"x-csrftoken":token,"cookie":f"permissions=%7B%7D;scratchcsrftoken={token}"})
        if response.status_code == 200:
            if response.json()[0]["success"]: #さくせすしない！！！
                return response.json()["token"]
        raise ResponseError
        

def scratch_class_from_token(token:str,session:Session|None=None) -> scratch_class:
    c = scratch_class(0,session,False,token)
    r = requests.get(f"https://api.scratch.mit.edu/classtoken/{token}")
    if r.status_code != 200:
        raise ResponseError
    c._update_from_dict(r.json())
    return c

class comment:
    def __init__(self,object:Project|Studio|User,comment_id:int,update:bool=True) -> None:
        if type(object) == Project:
            self.type = comment_type.project
        elif type(object) == Studio:
            self.type = comment_type.studio
        elif type(object) == User:
            self.type = comment_type.user
        else:
            raise TypeError
        self.location = object
        self.id = comment_id
        self.author = None
        if update:
            if self.update() == "429":
                raise ResponseError
        return

    def update_from_dict(self,dicts:dict,*,_parent_id=None) -> None:
        try:
            if self.type == comment_type.user:
                self.id = dicts["CommentID"]
                self.parent_id = None if "hasReplies?" in dicts else _parent_id
                self._reply_to = self.id if self.parent_id is None else self.parent_id
                self.commentee_id = None if self.parent_id is None else dicts["Content"].split(" ")[0].replace("@","")
                self.content = dicts["Content"]
                self.datetime = datetime.datetime.strptime(dicts["Timestamp"],"%Y-%m-%dT%H:%M:%SZ")
                if self.location._session is None:
                    self.author = User(username=dicts["User"])
                else:
                    self.author = User(username=dicts["User"], _session=self.location._session)
                self.reply_count = len(dicts["Replies"]) if "hasReplies?" in dicts else None
                self.replies = []
                if "hasReplies?" in dicts and dicts["hasReplies?"]:
                    self.replies = []
                    for i in dicts["Replies"]:
                        _comment = comment(self.location,i["CommentID"],False)
                        _comment.update_from_dict(i,_parent_id=self.parent_id)
                        self.replies.append(_comment)
            else:
                self.id = dicts["id"]
                self.parent_id = dicts["parent_id"]
                self._reply_to = self.id if self.parent_id is None else self.parent_id
                self.commentee_id = dicts["commentee_id"]
                self.content = dicts["content"]
                self.datetime = datetime.datetime.fromisoformat(dicts["datetime_created"])
                if self.author is None:
                    if self.location._session is None:
                        self.author = User(username=dicts["author"]["username"])
                    else:
                        self.author = User(username=dicts["author"]["username"], _session=self.location._session)
                    self.author._update_from_dict(
                        dict(history={"joined":None},profile={
                            "bio":None,"status":None,"country":None,"images":{"90x90":dicts["author"]["image"][:-9] + "90x90.png"}
                            },**dicts["author"]))
                self.reply_count = dicts["reply_count"]
                self.replies = None
        except Exception as e:
            raise ValueError(e)

    def update(self) -> None:
        if self.type == comment_type.user:
            raise TypeError
        self._json = self.location.get_comment(self.id)
        if self._json is None:
            raise ResponseError
        try:
            self.update_from_dict(self._json)
        except:
            raise ResponseError
        return
    
    def get_dict(self) -> dict:
        return self._json
    
    def update_author(self) -> None:
        if self.author.update() == "429":
            raise ResponseError
        return
    
    def update_replies(self) -> None:
        if self.type == comment_type.user:
            raise TypeError
        else:
            self.replies = []
            for i in self.location.get_comment_replies(comment_id=self.id):
                _comment = comment(self.location,i["id"])
                _comment.update_from_dict(i)
                self.replies.append(_comment)


    
    def report(self) -> None:
        """
        ST IS CRAZY!
        Why does the user page have a different link?

        argument:
        object: scratchattach.Project / scratchattach.Studio / scratchattach.User
        need sessionID

        retuen:
        None:reported
        ResponseError:failed
        """
        headers = self.location._headers.copy()
        headers["cookie"] = self.location._cookies
        headers["x-csrftoken"] = get_csrf_token()
        if self.location._session is None:
            raise NoSessionError
        if self.type == comment_type.project:
            urls = f"https://api.scratch.mit.edu/proxy/project/{self.location.id}/comment/{self.id}/report"
        elif self.type == comment_type.studio:
            urls = f"https://api.scratch.mit.edu/proxy/studio/{self.location.id}/comment/{self.id}/report"
        elif self.type == comment_type.user:
            urls = f"https://scratch.mit.edu/site-api/comments/user/{self.location.username}/rep?id={self.id}"
        else:
            raise TypeError
        posts = requests.post(
            urls,
            headers=headers,
            cookies=self.location._cookies
        )
        if posts.status_code == 200:
            return
        else:
            raise ResponseError
        
    def reply(self, content, commentee:User|str|int|None=None) -> None:
        """
        commentee:mention user
        str:username
        int:userID
        scratchattach.User
        """
        if type(commentee) == User:
            commentee = commentee.id
        elif type(commentee) == str:
            try:
                commentee = get_user(commentee).id
            except:
                raise ResponseError
        elif type(commentee) == int:
            pass
        elif commentee is None:
            commentee = ""
        else:
            raise TypeError
        if self.location._session is None:
            raise NoSessionError
        self.location.reply_comment(content,parent_id=self._reply_to,commentee_id=commentee)
        return
    
    def delete(self) -> None:
        if self.location._session is None:
            raise NoSessionError
        if self.type == comment_type.studio:
            raise TypeError
        self.location.delete_comment(comment_id=self.id)

def get_comments(objects:Project|Studio|User, limit:int=40, offset:int=0) -> list[comment]:
    if type(objects) == User:
        dicts = objects.comments(page=offset+1, limit=limit)
    else:
        dicts = objects.comments(limit=limit, offset=offset)
    comment_list = []
    for i in dicts:
        if type(objects) == User:
            _comment = comment(objects,i["CommentID"],False)
        else:
            _comment = comment(objects,i["id"],False)
        _comment.update_from_dict(i)
        comment_list.append(_comment)
    return comment_list

def _get_comment_object(self,comment_id:int) -> comment:
    return comment(self,comment_id)
_get_comment_object.__name__ = "get_comment_object"

def _report_comment(self:Project|Studio|User,comment_id:int) -> None:
    if self._session is None:
        raise NoSessionError
    return comment(self,comment_id,False).report()
_report_comment.__name__ = "report_comment"

def _studio_report(self:Studio,type:Studio_report_type) -> None:
    if self._session is None:
        raise NoSessionError
    return studio_report(self._session,self.id,type)
_studio_report.__name__ = "report"

def _user_report(self:User,type:User_report_type) -> None:
    if self._session is None:
        raise NoSessionError
    return user_report(self._session,self.username,type)
_user_report.__name__ = "report"

def _comments_object(self,limit=40,offset=0) -> list[comment]:
    return get_comments(self,limit,offset)
_comments_object.__name__ = "comments_object"

_add_method(Project,_get_comment_object)
_add_method(Studio,_get_comment_object)
_add_method(User,_get_comment_object)
_add_method(Project,_report_comment)
_add_method(Studio,_report_comment)
_add_method(User,_report_comment)
_add_method(Studio,_studio_report,"report")
_add_method(User,_user_report,"report")
_add_method(Project,_comments_object)
_add_method(Studio,_comments_object)
_add_method(User,_comments_object)


def scratchattach_requests(conn:CloudConnection,content:str|list,**options) -> list[str]:
    #読み込み
    encoded = ""
    if "logging" in options:
        if_log = bool(options["logging"])
    else:
        if_log = False
    if "encode_list" in options: #  is F8FF
        encode_list = list(""+options["encode_list"])
    else:
        encode_list = list("""1234567890 aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ*/.,!"§$%_-(´)`?<@#~;:+&|^'""")
    if if_log:
        print("encode中...")
    #エンコード開始
    if "argument_separator" in options:
        argument_separator = options["argument_separator"]
    else:
        argument_separator = "&"

    if type(content) == list:
        content = argument_separator.join(content)
    for i in content:
        try:
            encoded = encoded + str(encode_list.index(i)) #探す
        except: #なかった！！！
            if if_log:
                print(f"encode:文字{i}はencodeできません。")
            raise encodeerror
    if if_log:
        print(f"encode完了:{encoded}")
    #エンコード終わり
    if "reqest_id" in options:
        reqest_id = options["reqest_id"]
    else:
        reqest_id = random.randint(100000, 999999)
    if "max_length" in options:
        max_length = options["max_length"]
    else:
        max_length = 245
    if "requests_ver" in options:
        requests_ver = options["requests_ver"]
    else:
        requests_ver = "TO_HOST"
    #りくえすと
    if len(encoded) < max_length:
        conn.set_var(requests_ver,f"{encoded}.{reqest_id}") #1回でいける
        if if_log:
            print(f"リクエスト完了:{encoded}")
    else: #2回以上必要
        while len(encoded) != 0: #残りが0になるまで
            if len(encoded) < max_length: #あと1でいける
                conn.set_var(requests_ver,f"{encoded}.{reqest_id}")
                if if_log:
                    print(f"リクエスト完了:{encoded}")
                encoded = ""
            else: #まだ残りある
                conn.set_var(requests_ver,f"-{encoded[:max_length]}.{reqest_id}")
                if if_log:
                    print(f"リクエスト完了:{encoded[:max_length]}")
                encoded = encoded[max_length:]
    if if_log:
        print(f"レスポンス読み込み中...")
    if "timeout" in options:
        timeout = time.time() + options["timeout"]
    else:
        timeout = time.time() + 10
    if "response_var" in options:
        response_var = options["response_var"]
    else:
        response_var = [f"FROM_HOST_{i+1}" for i in range(9)]
    #読み込み開始
    status = "LOADING"
    response_list = []
    while timeout > time.time() and status != "DONE":
        cloud_get = get_cloud(conn.project_id)
        for i in response_var:
            cloud_response = cloud_get[i]
            if f"{reqest_id}" in f"{cloud_response}": #自分のか
                if not cloud_response in response_list: #まだ処理してない?
                    if cloud_response[-4:] == "2222": #エンコード必要
                        response_list.append(cloud_response)
                        need_encode = True
                        status = "DONE"
                        if if_log:
                            print(f"レスポンス{cloud_response}を獲得/end")
                    elif cloud_response[-4:] == "3222": #エンコード不必要
                        response_list.append(cloud_response)
                        need_encode = False
                        status = "DONE"
                        if if_log:
                            print(f"レスポンス{cloud_response}を獲得/end")
                    else:
                        while not len(response_list) > int(cloud_response[-4:-1]): #リストの数が足りない
                            response_list.append("")
                        response_list[int(cloud_response[-4:-1])-1] = cloud_response
                        if if_log:
                            print(f"レスポンス{cloud_response}を獲得")
    if timeout < time.time():
        raise "TIMEOUT"
    #一つの文字列に戻す
    if if_log:
        print(f"デコード中...")
    response_zip = ""
    for i in response_list:
        i = str(i)
        response_zip = response_zip + i.split(".")[0]
    #デコード
    if "new_line_id" in options:
        new_line_id = str(options["new_line_id"])
    else:
        new_line_id = "89"
    if need_encode:
        response = [""]
        response_zip = [response_zip[i:i+2] for i in range(0, len(response_zip), 2)]
        for i in response_zip:
            if i == new_line_id:
                response.append("")
            else:
                response[-1] = response[-1] + encode_list[int(i)]
        if if_log:
            print(f"完了!:{response}")
        return response
    else:
        if if_log:
            print(f"完了!:{response_zip}")
        return [response_zip]

_add_method(CloudConnection,scratchattach_requests)


def user_ok(username:str) -> bool:
    r = requests.get(f"https://api.scratch.mit.edu/accounts/checkusername/{username}")
    if r.json()["msg"] == "valid username":
        return True
    else:
        return False

def create_project(session:Session) -> int|str :
    data = {'targets': [{'isStage': True, 'name': 'Stage', 'variables': {'`jEk@4|i[#Fk?(8x)AV.-my variable': ['my variable', 0]}, 'lists': {}, 'broadcasts': {}, 'blocks': {}, 'comments': {}, 'currentCostume': 0, 'costumes': [{'name': 'backdrop1', 'dataFormat': 'svg', 'assetId': 'cd21514d0531fdffb22204e0ec5ed84a', 'md5ext': 'cd21514d0531fdffb22204e0ec5ed84a.svg', 'rotationCenterX': 240, 'rotationCenterY': 180}], 'sounds': [{'name': 'pop', 'assetId': '83a9787d4cb6f3b7632b4ddfebf74367', 'dataFormat': 'wav', 'format': '', 'rate': 44100, 'sampleCount': 1032, 'md5ext': '83a9787d4cb6f3b7632b4ddfebf74367.wav'}], 'volume': 100, 'layerOrder': 0, 'tempo': 60, 'videoTransparency': 50, 'videoState': 'on', 'textToSpeechLanguage': None}, {'isStage': False, 'name': 'Sprite1', 'variables': {}, 'lists': {}, 'broadcasts': {}, 'blocks': {}, 'comments': {}, 'currentCostume': 0, 'costumes': [{'name': 'costume1', 'bitmapResolution': 1, 'dataFormat': 'svg', 'assetId': 'bcf454acf82e4504149f7ffe07081dbc', 'md5ext': 'bcf454acf82e4504149f7ffe07081dbc.svg', 'rotationCenterX': 48, 'rotationCenterY': 50}, {'name': 'costume2', 'bitmapResolution': 1, 'dataFormat': 'svg', 'assetId': '0fb9be3e8397c983338cb71dc84d0b25', 'md5ext': '0fb9be3e8397c983338cb71dc84d0b25.svg', 'rotationCenterX': 46, 'rotationCenterY': 53}], 'sounds': [{'name': 'Meow', 'assetId': '83c36d806dc92327b9e7049a565c6bff', 'dataFormat': 'wav', 'format': '', 'rate': 44100, 'sampleCount': 37376, 'md5ext': '83c36d806dc92327b9e7049a565c6bff.wav'}], 'volume': 100, 'layerOrder': 1, 'visible': True, 'x': 0, 'y': 0, 'size': 100, 'direction': 90, 'draggable': False, 'rotationStyle': 'all around'}], 'monitors': [], 'extensions': [], 'meta': {'semver': '3.0.0', 'vm': '1.2.22', 'agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}}
    header = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "mode": "cors",
        "credentials": "include",
        "referrer": "https://scratch.mit.edu/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        }
    r = requests.post("https://projects.scratch.mit.edu/",json=data,headers=header,cookies=session._cookies)
    if r.status_code == 200:
        return r.json()['content-name']
    raise CreateProjectError
    
_add_method(Session,create_project)

class ResponseError(requests.HTTPError):
    """
    サーバーからの返答で失敗した時に送出されます。
    """
class NoSessionError(Exception):
    """
    セッションが必要な関数で、セッションが登録されていないときに送出されます。
    """

class InvalidUsername(Exception):
    """
    ユーザー名が無効である
    """

class CreateProjectError(requests.HTTPError):
    """
    プロジェクトの作成失敗時に発生
    """

class encodeerror(ValueError):
    pass

class request_timeout(requests.HTTPError):
    pass

del _add_method
