from flask import Flask, request, jsonify, Response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from json import dumps

from database import *


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    JWTManager(app)
    return app

_app = create_app()


@_app.route('/signup', methods=['POST'])
def signup():
    # 회원가입
    req = request.json
    status = add_account(req['id'], req['pw'])

    if status:
        return '', 201
    else:
        return '', 204


@_app.route('/auth', methods=['POST'])
def auth():
    # 토큰 받아오기
    req = request.json
    status = auth_account(req['id'], req['pw'])

    if status:
        return jsonify({
            'access_code': status
        }), 201
    else:
        return jsonify({
            'msg': 'Authentication Failed.'
        }), 401


@_app.route('/load_memo', methods=['GET'])
@jwt_required
def load_memo_():
    memo_list = load_memos(get_jwt_identity())
    if memo_list:
        return jsonify(str(memo_list)), 200
    else:
        return '', 204


@_app.route('/add_memo', methods=['POST'])
@jwt_required
def add_memo_():
    req = request.json
    add_memo(get_jwt_identity(), req['title'], req['content'], req['latitude'], req['longitute'])
    return '', 201


@_app.route('/update_memo', methods=['POST'])
@jwt_required
def update_memo_():
    req = request.json
    update_memo(get_jwt_identity(), req['_id'], req['title'], req['content'], req['latitude'], req['longitute'])
    return '', 201


@_app.route('/delete_memo', methods=['DELETE'])
@jwt_required
def delete_memo_():
    delete = delete_memo(request.json['_id'])
    if delete:
        return '', 200
    else:
        return '', 204


@_app.route('/check_jwt', methods=['GET'])
@jwt_required
def check():
    return get_jwt_identity()


if __name__ == '__main__':
    _app.run(host='0.0.0.0', port=_app.config['PORT'])
