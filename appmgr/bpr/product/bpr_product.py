from flask import Blueprint, render_template
from shp.appmgr.blo.product.blo_product_manage_list import Blo_product_manage_list


bpr_product = Blueprint('product', __name__, url_prefix='/product', template_folder='../../templates/product')


@bpr_product.route('/product_manage_list_0')
def product_manage_list_0():
    return render_template('product_manage_list_0.html')


@bpr_product.route('/product_manage_list')
def product_manage_list():
    result = Blo_product_manage_list().result
    return render_template('product_manage_list.html', result=result)


@bpr_product.route('/product_category_list')
def product_category_list():
    return render_template('product_category_list.html')
