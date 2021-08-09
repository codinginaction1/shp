from flask import Flask, render_template
from shp.appmgr.bpr.product.bpr_product import bpr_product
from shp.appmgr.bpr.order.bpr_order import bpr_order


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.register_blueprint(bpr_product)
app.register_blueprint(bpr_order)


@app.route('/')
@app.route('/index')
def index():
    result = {'__name__': __name__}
    return render_template('index/index.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
else:
    application = app
