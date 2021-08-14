# Author: sphong1
# Class: PostGreSQLSingleton


from flask import g, has_app_context
from shp.lib.basic.pgsql import Pgsql


class Pgsqls:
    instances = {}


    @classmethod
    def get_instance(cls, db_id, **kwargs):
        if has_app_context():
            # flask app으로 실행되는 경우 클래스 변수를 사용하면
            # 이전 request에서 설정되었던 클래스 변수 값이
            # 다음 request에서도 그대로 남아 있게 된다.
            # g 객체를 사용하는 방식으로 대체하고 app.teardown_request에서 해제한다.
            if 'instances' not in g:
                g.instances = {}

            if db_id not in g.instances:
                g.instances[db_id] = Pgsql(db_id, **kwargs)
            elif g.instances[db_id].conn.closed:
                g.instances[db_id].connect(**kwargs)

            return g.instances[db_id]
        else:
            if db_id not in cls.instances:
                cls.instances[db_id] = Pgsql(db_id, **kwargs)
            elif cls.instances[db_id].conn.closed:
                cls.instances[db_id].connect(**kwargs)

            return cls.instances[db_id]
