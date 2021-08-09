from flask import Blueprint, render_template
import psycopg2
import psycopg2.extras


bpr_product = Blueprint('product', __name__, url_prefix='/product', template_folder='../../templates/product')


@bpr_product.route('/product_manage_list')
def product_manage_list():
    cf = {
        'host': 'database-2.cdyzomagbni2.ap-northeast-2.rds.amazonaws.com',
        'port': 5432,
        'user': 'postgres',
        'password': 'your_password',
        'dbname': 'db_shp_main'
    }
    conn = psycopg2.connect(host=cf['host'], port=cf['port'], user=cf['user'], password=cf['password'], dbname=cf['dbname'])
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = f"""
SELECT
    product_id,
    product_name,
    product_price
FROM test_product_info
"""
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('product_manage_list.html', result=result)


@bpr_product.route('/product_category_list')
def product_category_list():
    return render_template('product_category_list.html')
