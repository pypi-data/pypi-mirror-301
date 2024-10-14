import asyncio
from typing import TYPE_CHECKING

import aiomysql
from scrapy.utils.defer import deferred_from_coro

from gzspidertools.common.expend import MysqlPipeEnhanceMixin
from gzspidertools.common.multiplexing import ReuseOperation

__all__ = [
    "AyuAsyncMysqlPipeline",
]

if TYPE_CHECKING:
    from gzspidertools.common.typevars import MysqlConf, slogT


class AyuAsyncMysqlPipeline(MysqlPipeEnhanceMixin):
    mysql_conf: "MysqlConf"
    slog: "slogT"
    pool: aiomysql.Pool
    running_tasks: set

    def open_spider(self, spider):
        assert hasattr(spider, "mysql_conf"), "未配置 Mysql 连接信息！"
        self.running_tasks = set()
        self.slog = spider.slog
        self.mysql_conf = spider.mysql_conf
        return deferred_from_coro(self._open_spider(spider))

    async def _open_spider(self, spider):
        self.pool = await aiomysql.create_pool(
            host=self.mysql_conf.host,
            port=self.mysql_conf.port,
            user=self.mysql_conf.user,
            password=self.mysql_conf.password,
            db=self.mysql_conf.database,
            charset=self.mysql_conf.charset,
            cursorclass=aiomysql.DictCursor,
            autocommit=True,
        )

    async def insert_item(self, item_dict):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                alter_item = ReuseOperation.reshape_item(item_dict)
                new_item = alter_item.new_item
                sql, args = self._get_sql_by_item(
                    table=alter_item.table.name,
                    item=new_item,
                    odku_enable=self.mysql_conf.odku_enable,
                )
                await cursor.execute(sql, args)

    async def process_item(self, item, spider):
        item_dict = ReuseOperation.item_to_dict(item)
        task = asyncio.create_task(self.insert_item(item_dict))
        self.running_tasks.add(task)
        await task
        task.add_done_callback(lambda t: self.running_tasks.discard(t))
        return item

    async def _close_spider(self):
        await self.pool.wait_closed()

    def close_spider(self, spider):
        self.pool.close()
        return deferred_from_coro(self._close_spider())
