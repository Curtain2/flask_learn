# -*- encoding: utf-8 -*-
"""
@File    : server.py
@Time    : 2022/10/9 15:12
@Author  : Jahan
@Software: PyCharm
"""
import os
import json
import time
from datetime import timedelta

from flask import Flask, request, Response, jsonify, url_for, redirect, render_template, abort, \
    render_template_string, \
    session
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter


class MyIntConverter(BaseConverter):
    """自定义转换器"""

    def __init__(self, url_map):
        super(MyIntConverter, self).__init__(url_map)

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return value * 2


app = Flask("my-app")
app.secret_key = 'F12Zr47j\3yX R~X@H!jLwf/T'
app.url_map.converters['my_int'] = MyIntConverter
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg', 'gif'}


# 筛选上传格式
def allow_file(filename):
    if "." not in filename:
        return "Not Found filename"
    if filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']:
        return filename


@app.route("/")
def hello_word():
    r = request.args.getlist("p")
    return r


@app.route('/register', methods=["GET", "POST"])
def register():
    print(request.headers)
    # get单个user
    print(request.form.get("user"))
    # get list user
    print(request.form.getlist("user"))
    print(request.form.get('password'))
    return "welcome"


@app.route("/add", methods=["POST"])
def add():
    print(request.headers)
    print(type(request.json))
    result = {"sum": request.json["a"] + request.json["b"]}
    resp = Response(json.dumps(result), mimetype="application/json")
    # add resp header
    resp.headers.add("python", "learning flask")
    return jsonify(result)


# 上传图片
@app.route("/uploads", methods=["POST"])
def uploads():
    upload_file = request.files.get("image")
    file_content = request.files['image'].stream.read()
    print(file_content)
    if upload_file and allow_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename))
        return "info is " + request.form.get("info", "") + ".success"
    else:
        return "failed"


# result风格
@app.route("/user/<username>", methods=["GET"])
def username(username):
    print(username)
    print(type(username))
    return "hello " + username


@app.route("/user/<username>/friends")
def friend(username):
    print(username)
    print(type(username))
    return "hello " + username


# 分页
@app.route('/page/<my_int:num>')
def page(num):
    print(num)
    print(url_for('page', num=str(123)))
    return "hello page"


@app.route("/test")
def test():
    print("helloWord")
    print(url_for("user", username="jahan"))
    print(url_for("page", num=str(1), q="jahan123"))
    print(url_for('static', filename='uploads/01.jpg'))
    return "Hello"


@app.route("/test1")
def test1():
    print('this is test1')
    return redirect(url_for("test2"))


@app.route("/test2")
def test2():
    print("this is test2")
    return 'this is test2'


# Jinja2模板
@app.route("/user")
def user():
    info = {
        "name": "jahan",
        "age": 18,
        "height": 178,
        "sex": "M"
    }
    return render_template("user_info.html", page_title="user info", user_info=info)


@app.route("/auth")
def auth():
    abort(401)
    print("用户未授权")


# 自定义错误页面
@app.errorhandler(401)
def page_unauthorized(error):
    return render_template_string('<h1> Unauthorized </h1><h2>{{ error_info }}</h2>', error_info=error), 401


@app.route("/login")
def login():
    page = '''
    <form action="{{ url_for('do_login') }}" method="post">
        <p>name: <input type="text" name="user_name" /></p>
        <input type="submit" value="Submit" />
    </form>
    '''
    return render_template_string(page)


@app.route('/do_login', methods=['POST'])
def do_login():
    name = request.form.get("user_name")
    session["user_name"] = name
    return "session success"


@app.route("/show")
def show():
    return session["user_name"]


@app.route("/logout")
def logout():
    session.pop('user_name', None)
    return redirect(url_for("login"))


@app.route("/add")
def cookie_login():
    res = Response("add cookie")
    res.set_cookie(key="name", value="jahan", expires=time.time() + 6 * 60)
    return res


@app.route("/cookie_show")
def cookie_show():
    return request.cookies.__str__()


@app.route("/del_cookie")
def del_cookie():
    res = Response("del cookie")
    res.set_cookie("name", "", expires=0)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
