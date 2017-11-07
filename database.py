from pymongo import MongoClient
from hashlib import sha256
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client.pimo

accounts = db.accounts
memos = db.memos


def add_account(id, pw):
    if accounts.find_one({'id': id}):
        # 중복 id
        return False

    else:
        # 회원 가입
        account = {'id': id, 'pw': sha256(pw.encode('utf-8')).hexdigest()}
        accounts.insert(account)
        return True


def auth_account(id, pw):
    if not accounts.find_one({'id': id, 'pw': sha256(pw.encode('utf-8')).hexdigest()}):
        # 로그인 실패
        return False
    else:
        # 로그인 성공 -> 토큰 반환
        return create_access_token(identity=id)


def load_memos(id):
    memo_list = [i for i in memos.find({'id': id})]
    if memo_list:
        return memo_list
    else:
        return False


def add_memo(id, title, content, latitude, longitute):
    #메모 추가
    memos.insert({
        'id': id,
        'title': title,
        'content': content,
        'latitude': latitude,
        'longitute': longitute
    })
    return True


def update_memo(id, _id, title, content, latitude, longitute):
    delete_memo(_id)
    add_memo(id, title, content, latitude, longitute)
    return True


def delete_memo(_id):
    delete = memos.delete_one({'_id': ObjectId(_id[10:34])})
    if delete.deleted_count:
        # 삭제 완료
        return True
    else:
        # 삭제 실패
        return False


def search_memo(id, search):
    pass
