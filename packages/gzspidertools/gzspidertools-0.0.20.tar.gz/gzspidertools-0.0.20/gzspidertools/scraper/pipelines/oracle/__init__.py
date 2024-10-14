from typing import TYPE_CHECKING

from gzspidertools.common.expend import OraclePipeEnhanceMixin
from gzspidertools.common.multiplexing import ReuseOperation

__all__ = ["AyuOraclePipeline"]

if TYPE_CHECKING:
    from oracledb.connection import Connection
    from oracledb.cursor import Cursor

    from gzspidertools.common.typevars import AlterItem


class AyuOraclePipeline(OraclePipeEnhanceMixin):
    conn: "Connection"
    cursor: "Cursor"

    def open_spider(self, spider):
        assert hasattr(spider, "oracle_conf"), "未配置 Oracle 连接信息！"
        self.conn = self._connect(spider.oracle_conf)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        item_dict = ReuseOperation.item_to_dict(item)
        alter_item = ReuseOperation.reshape_item(item_dict)
        self.insert_item(alter_item)
        return item

    def insert_item(self, alter_item: "AlterItem"):
        """通用插入数据

        Args:
            alter_item: 经过转变后的 item
        """
        if not (new_item := alter_item.new_item):
            return

        sql = self._get_sql_by_item(table=alter_item.table.name, item=new_item)
        # no err handing
        self.cursor.execute(sql, tuple(new_item.values()))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
