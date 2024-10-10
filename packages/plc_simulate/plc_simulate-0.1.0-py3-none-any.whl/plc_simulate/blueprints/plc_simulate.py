from inovance_tag.exception import PLCWriteError, PLCReadError
from inovance_tag.tag_communication import TagCommunication
from flask import Blueprint, request, render_template

blue_print = Blueprint("plc_simulate", __name__)


# plc 模拟页面
@blue_print.route("/plc_simulate", methods=["GET", "POST"])
def plc_simulate():
    if request.method == "GET":
        return render_template("cyg_plc_simulate.html")


# 操作返回数据
@blue_print.route("/operation_submit", methods=["GET", "POST"])
def operation_submit():
    if request.method == "POST":
        form_data = request.get_json()
        plc_ip = form_data.get("plc_ip")
        tag_instance = TagCommunication(plc_ip)
        tag_instance.communication_open()
        tag_name = form_data.get("tag_name")
        operation_type = form_data.get("operation_type")
        data_type = form_data.get("data_type")
        if operation_type == "read":
            try:
                read_value = tag_instance.execute_read(tag_name, data_type)
            except PLCReadError:
                return {"value": "读取失败, plc未连接"}
            return {"value": read_value}
        else:
            write_value = form_data.get("write_value")
            try:
                write_state = tag_instance.execute_write(tag_name, data_type, write_value)
            except PLCWriteError:
                return {"value": "写入失败, plc未连接"}
            if write_state == tag_instance.TAResult.ERR_NOERROR:
                return {"value": "写入成功"}
            return {"value": "plc连接了, 但是写入失败"}
