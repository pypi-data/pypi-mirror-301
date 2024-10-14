import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Any

import scrapy
from scrapy.http.request import NO_CALLBACK
from scrapy.utils.defer import maybe_deferred_to_future
from scrapy.utils.python import to_bytes

from gzspidertools.common.multiplexing import ReuseOperation
from gzspidertools.common.utils import ToolsForAyu
from gzspidertools.config import logger
from gzspidertools.items import DataItem

__all__ = [
    "FilesDownloadPipeline",
    "files_download_by_scrapy",
]

if TYPE_CHECKING:
    from scrapy import Spider

    from gzspidertools.common.typevars import DataItemModeStr


async def files_download_by_scrapy(
    spider: "Spider",
    file_path: str,
    file_url: str,
    item: Any,
    key: str,
    mode: "DataItemModeStr" = "namedtuple",
):
    request = scrapy.Request(file_url, callback=NO_CALLBACK)
    response = await maybe_deferred_to_future(spider.crawler.engine.download(request))
    if response.status != 200:
        return item

    headers_dict = ToolsForAyu.get_dict_form_scrapy_req_headers(
        scrapy_headers=response.headers
    )
    content_type = headers_dict.get("Content-Type")
    file_format = content_type.split("/")[-1].replace("jpeg", "jpg")
    file_guid = hashlib.sha1(to_bytes(file_url)).hexdigest()
    filename = f"{file_path}/{file_guid}.{file_format}"
    Path(filename).write_bytes(response.body)

    # Store file in item.
    if mode == "namedtuple":
        item[key] = DataItem(key_value=filename, notes=f"{key} 文件存储路径")
    else:
        item[key] = filename


class FilesDownloadPipeline:
    def __init__(self, file_path=None):
        self.file_path = file_path

    @classmethod
    def from_crawler(cls, crawler):
        _file_path = crawler.settings.get("FILES_STORE", None)
        assert _file_path is not None, "未配置 FILES_STORE 存储路径参数！"

        if not Path.exists(_file_path):
            logger.warning(f"FILES_STORE: {_file_path} 路径不存在，自动创建所需路径！")
            Path(_file_path).mkdir(parents=True)
        return cls(file_path=_file_path)

    async def process_item(self, item, spider):
        item_dict = ReuseOperation.item_to_dict(item)
        judge_item = next(iter(item_dict.values()))
        file_url_keys = {
            key: value for key, value in item_dict.items() if key.endswith("_file_url")
        }
        if ReuseOperation.is_namedtuple_instance(judge_item):
            for key, value in file_url_keys.items():
                await files_download_by_scrapy(
                    spider, self.file_path, value.key_value, item, f"{key}_local"
                )
        else:
            for key, value in file_url_keys.items():
                await files_download_by_scrapy(
                    spider, self.file_path, value, item, f"{key}_local", "normal"
                )

        return item
