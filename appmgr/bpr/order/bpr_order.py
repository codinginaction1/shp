from flask import Blueprint, render_template


bpr_order = Blueprint('order', __name__, url_prefix='/order', template_folder='../../templates/order')


@bpr_order.route('/order_manage_list')
def order_manage_list():
    return render_template('order_manage_list.html')


@bpr_order.route('/order_report_daily')
def order_report_daily():
    return render_template('order_report_daily.html')
