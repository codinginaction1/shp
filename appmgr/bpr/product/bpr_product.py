from flask import Blueprint, render_template
from shp.appmgr.blo.product.blo_product_manage_list_1 import Blo_product_manage_list_1


bpr_product = Blueprint('product', __name__, url_prefix='/product', template_folder='../../templates/product')


@bpr_product.route('/product_manage_list_0')
def product_manage_list_0():
    return render_template('product_manage_list_0.html')


@bpr_product.route('/product_manage_list_1', methods=['POST'])
def product_manage_list_1():
    result = Blo_product_manage_list_1().result
    return render_template('product_manage_list_1.html', result=result)


@bpr_product.route('/product_category_list')
def product_category_list():
    return render_template('product_category_list.html')
