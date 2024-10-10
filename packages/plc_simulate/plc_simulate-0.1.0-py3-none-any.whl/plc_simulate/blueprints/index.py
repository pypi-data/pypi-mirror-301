from flask import Blueprint, render_template

blue_print = Blueprint("index", __name__, url_prefix="/")


# 首页,欢迎页
@blue_print.route("/")
def index():
    return render_template("cyg_welcome.html")
