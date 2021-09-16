from shp.lib.basic.pgsql import Pgsql


class Blo_product_manage_list:
    def __init__(self):
        self.select_table()


    def select_table(self):
        dao = Pgsql('db_shp_main')
        query = f"""
SELECT
    product_id,
    product_name,
    product_price
FROM test_product_info
"""
        dao.execute(query)
        self.result = dao.fetchall()
