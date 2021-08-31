from flask import Flask, render_template, request, url_for
from shp.appmgr.bpr.product.bpr_product import bpr_product
from shp.appmgr.bpr.order.bpr_order import bpr_order
from shp.lib.basic.log import Log


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.register_blueprint(bpr_product)
app.register_blueprint(bpr_order)


@app.route('/')
@app.route('/index')
def index():
    result = {'__name__': __name__}
    return render_template('index/index.html', result=result)


@app.before_request
def before_request():
    # Only the routes registered by app.route are logged.
    # The static folder and nonexistent routes are excluded.
    path = request.path
    if not path.startswith('/static/'):
        try:
            if path == '/':
                url = url_for('index')
            else:
                url = url_for(path.lstrip('/').replace('/', '.'))
        except Exception as err:
            return 'Invalid endpoint!', 404
        else:
            Log.set_logger()
            Log.logging_access()


@app.teardown_request
def teardown_request(exception):
    # If you register the set_logger function in app.before_request,
    # when another request comes in after one request,
    # the previous logger value is maintained and log file handlers are continuously added.
    # The same log is written more and more times, so the created file handler must be removed.
    Log.unset_logger()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
else:
    application = app
