from flask import Blueprint, render_template
import psycopg2
import psycopg2.extras
from shp.lib.basic.pgsql import Pgsql


bpr_product = Blueprint('product', __name__, url_prefix='/product', template_folder='../../templates/product')


@bpr_product.route('/product_manage_list')
def product_manage_list():
    dao = Pgsql('db_shp_main')
    query = f"""
SELECT
    product_id,
    product_name,
    product_price
FROM test_product_info
"""
    dao.execute(query)
    result = dao.fetchall()
    return render_template('product_manage_list.html', result=result)


@bpr_product.route('/product_category_list')
def product_category_list():
    return render_template('product_category_list.html')
