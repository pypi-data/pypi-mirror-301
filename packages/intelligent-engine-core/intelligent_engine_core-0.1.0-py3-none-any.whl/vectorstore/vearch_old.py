# -*- coding: utf-8 -*-

import copy
import json
import time
import uuid
import asyncio
import requests
import logging
from aiohttp import ClientSession
from typing import Any, Dict, List, Optional, Tuple, Union, Iterable

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


logger = logging.getLogger(__name__)


"""
vearch 限制
- filter 不同条件之间取交集
- 相似度计算可能是负数
- 2023.08.25 数值过滤不支持浮点数
- meta 必须和库里 meta 一样，不能多也不能少

相关信息可参考：https://vearch.readthedocs.io/zh_CN/latest/use_op/op_space.html
"""

# - 数字类：支持大于小于
# - 字符串类：支持判断是否在某个集合
# filter = [{'index1': {'gte': 3}}, {'index2': {'lte': 2}}, {'format1': {'in': ['pdf', 'doc']}}]
DictFilters = List[Dict[str, Dict[str, Union[int, float, List]]]]


class VearchCluster(VectorStore):
    def __init__(
        self,
        router_address: str,
        embedding_function: Embeddings,
        db_name: str,
        space_name: str,
        *,
        master_address: Optional[str] = None,
        text_field: str = "text",
        embedding_field: str = "vector",
        is_brute_search: int = 1,
        min_score: float = -1.0,
        batch_size: int = 100,
        per_batch_delay: float = 0.0,
        async_workers_number: int = 10,
    ):
        self.embedding_function = embedding_function

        # 数据库链接信息
        self.router_address = router_address
        self.master_address = master_address or self.router_address
        self.db_name = db_name
        self.space_name = space_name

        # 最大文档长度
        self.text_length_threshold = 5000

        self.batch_size = batch_size
        self.per_batch_delay: float = per_batch_delay
        # 采用异步方式进行数据上传
        self.async_workers_number = async_workers_number

        # 字段信息，支持数据类型：string, integer, float, vector
        self.text_field = text_field
        self.embedding_field = embedding_field

        # 构造url信息
        self._url_headers = {"content-type": "application/json"}
        self._is_brute_search = is_brute_search
        self._min_score = min_score

        if not self._request_check_db_exist():
            # 库不存在，创建库
            self._request_create_db()

    def _request_create_table_with_metadata(
        self, metadata: Optional[Dict] = None
    ) -> bool:
        logger.info(f"创建表：{self.db_name}/{self.space_name}")

        # 表未提前创建，根据要插入的数据动态创建表结构
        url = f"http://{self.master_address}/space/{self.db_name}/_create"

        vector = self.embedding_function.embed_query("demo_text")
        metadata = metadata if metadata else {}

        # 防止出现无意义的 key
        metadata = {k: v for k, v in metadata.items() if k}

        default_data_type = {str: "string", float: "float", int: "integer"}

        format_dict = {
            field: {
                "index": True,
                "type": default_data_type[type(field_value)],
            }
            for field, field_value in metadata.items()
        }
        format_dict[self.text_field] = {"type": "string"}
        format_dict[self.embedding_field] = {"dimension": len(vector), "type": "vector"}

        data = {
            "name": self.space_name,
            "partition_num": 1,
            "replica_num": 1,
            "engine": {
                "name": "gamma",
                "index_size": 70000,
                "id_type": "String",
                "retrieval_type": "IVFPQ",
                "retrieval_param": {
                    "metric_type": "InnerProduct",
                    "ncentroids": 256,
                    "nsubvector": 32,
                },
            },
            "properties": format_dict,
        }

        request_ret = requests.put(
            url, headers=self._url_headers, data=json.dumps(data)
        )
        if request_ret.status_code != 200:
            logger.info(f"data = {data}")
            raise Exception(
                f"表创建中：请求{url}结果失败，错误信息为：{request_ret.json()}"
            )
        return True

    def _request_check_table_exist(self) -> bool:
        table_info = self._request_get_table_info()
        """
        {'code': 565, 'msg': 'space_notexists'}
        {'code': 200, 'msg': 'success', 
        'data': {'id': 1, 'name': 'sl_ts_space_1', 'version': 2, 'db_id': 2, 'enabled': True, 
        'partitions': [{'id': 1, 'space_id': 1, 'db_id': 2, 'partition_slot': 0, 'replicas': [1]}], 
        'partition_num': 1, 'replica_num': 1, 
        'properties': {
        'feature': {'dimension': 1000, 'type': 'vector'}, 'image_url': {'index': True, 'type': 'string'}}, 
        'engine': {'name': 'gamma', 'index_size': 70000, 'metric_type': 'InnerProduct', 'retrieval_type': 'IVFPQ', 
        'retrieval_param': {'metric_type': 'InnerProduct', 'ncentroids': 256, 'nsubvector': 32}, 
        'id_type': 'String'}, 
        'space_properties': {'feature': {'field_type': 5, 'type': 'vector', 'dimension': 1000, 'option': 1}, 
        'image_url': {'field_type': 4, 'type': 'string', 'index': True, 'option': 1}}}}
        """
        db_space_name = f"{self.db_name}/{self.space_name}"
        if table_info["msg"] == "success":
            logger.info(f"检测表{db_space_name}是否存在：存在")
            return True
        elif table_info["msg"] == "space_notexists":
            # 当前表结构不存在，需要等插入数据时候再建立表结构
            logger.info(f"检测表{db_space_name}是否存在：不存在")
            return False
        else:
            raise Exception(f"无法处理 table_info = {table_info}")

    def _request_check_db_exist(self) -> bool:
        url = f"http://{self.master_address}/db/{self.db_name}"

        request_ret = requests.get(url)
        if request_ret.status_code != 200 and request_ret.status_code != 562:
            raise Exception(f"检测库{self.db_name}中：查询{url}失败，错误信息为：{request_ret.json()}")
        res_dict: dict = request_ret.json()
        if res_dict["msg"] == "success":
            logger.info(f"检测库{self.db_name}是否存在：存在")
            return True
        if res_dict["msg"] == "db_notexists":
            logger.info(f"检测库{self.db_name}是否存在：不存在")
            return False
        raise Exception(f"检测库{self.db_name}中：分析{url}结果失败，错误信息为：{request_ret.json()}")

    def _get_fields_info(self) -> Tuple[Dict, int]:
        # 返回 fields_info 和 embedding_dim
        table_info = self._request_get_table_info()
        # {'text': {'type': 'string'}, 'vector': {'dimension': 1024, 'type': 'vector'}, 'format': {'index': True, 'type': 'string'}}
        fields_info = table_info["data"]["properties"]
        embedding_dim = fields_info[self.embedding_field]["dimension"]

        logger.info(f"获取表信息，字段为：{fields_info} embedding_dim = {embedding_dim}")

        return fields_info, embedding_dim

    def _request_create_db(self) -> bool:
        logger.info(f"创建库：db={self.db_name}")

        url = f"http://{self.master_address}/db/_create"

        data = {"name": self.db_name}

        request_ret = requests.put(
            url, headers=self._url_headers, data=json.dumps(data)
        )
        if request_ret.status_code == 200:
            logger.info(f"创建db={self.db_name} 成功")
            return True

        raise Exception(f"创建db={self.db_name} 失败，错误信息为：{request_ret.json()}")

    def _request_get_table_info(self):
        logger.info(f"获取表信息：{self.db_name}/{self.space_name}")

        url = f"http://{self.master_address}/space/{self.db_name}/{self.space_name}"
        request_ret = requests.get(url)

        if request_ret.status_code != 200 and request_ret.status_code != 565:
            raise Exception(f"获取表信息失败，错误信息为：{request_ret.json()}")

        """
        {'code': 565, 'msg': 'space_notexists'}
        {'code': 200, 'msg': 'success', 'data': 
        {'id': 1, 'name': 'sl_ts_space_1', 'version': 2, 'db_id': 2, 'enabled': True, 
        'partitions': [{'id': 1, 'space_id': 1, 'db_id': 2, 'partition_slot': 0, 'replicas': [1]}], 
        'partition_num': 1, 'replica_num': 1, 
        'properties': {
        'feature': {'dimension': 1000, 'type': 'vector'}, 'image_url': {'index': True, 'type': 'string'}}, 
        'engine': {'name': 'gamma', 'index_size': 70000, 'metric_type': 'InnerProduct', 'retrieval_type': 'IVFPQ', 
        'retrieval_param': {'metric_type': 'InnerProduct', 'ncentroids': 256, 'nsubvector': 32}, 'id_type': 'String'}, 
        'space_properties': {'feature': {'field_type': 5, 'type': 'vector', 'dimension': 1000, 'option': 1}, 
        'image_url': {'field_type': 4, 'type': 'string', 'index': True, 'option': 1}}}}
        """
        return request_ret.json()

    def _parse_filter(self, filter: Optional[DictFilters] = None) -> List:
        if filter is None:
            return []

        # [{'a': {'ge': 100}}, {'a': {'le': 200}}, {'format': {'in': ['pdf', 'doc']}}]
        # [{'a': {'ge': 100, 'le': 200}}, {'format': {'in': ['pdf', 'doc']}}]
        format_filter: Dict[str, Dict : [str, Union[int, float, str, List]]] = {}

        # 合并字段相同的项目
        for filter_item in filter:
            field = list(filter_item.keys())[0]
            field_filter = filter_item[field]
            if field in format_filter.keys():
                format_filter[field].update(field_filter)
            else:
                format_filter[field] = copy.deepcopy(field_filter)

        fields_info, _ = self._get_fields_info()

        # 格式检查，有 gte，lte 的的只能是数字类，有 in 的只能是string类
        result = []
        for field in format_filter.keys():
            # 检查当前字段是否可被索引
            assert (
                field in fields_info.keys()
            ), f"字段 {field} 不在 {fields_info.keys()} 中"

            if (
                "index" not in fields_info[field]
                or fields_info[field]["index"] is False
            ):
                logger.error(f"字段 {field} 不支持索引，无法创建过滤条件")
                continue

            field_filter = format_filter[field]
            assert all(
                [_f in ["lte", "gte", "in", "lt"] for _f in field_filter.keys()]
            ), f"不支持的过滤条件：{field_filter}"
            if "gte" in list(field_filter.keys()) or "lte" in list(field_filter.keys()):
                # 数值字段
                if fields_info[field]["type"] == "integer":
                    new_field_filter = {
                        op: int(value) for op, value in field_filter.items()
                    }
                    d = {"range": {field: new_field_filter}}
                elif fields_info[field]["type"] == "float":
                    new_field_filter = {
                        op: float(value) for op, value in field_filter.items()
                    }
                    d = {"range": {field: new_field_filter}}
                else:
                    raise Exception(
                        f"字段 {field} 类型为 {fields_info[field]['type']}，条件错误"
                    )
                result.append(d)

            if "in" in list(field_filter.keys()):
                assert (
                    fields_info[field]["type"] == "string"
                ), f"字段 {field} 类型为 {fields_info[field]['type']}，条件错误"
                d = {"term": {field: field_filter["in"], "operator": "or"}}
                result.append(d)

        return result

    def _request_search(
        self, arr, filter: Optional[DictFilters] = None, limit: int = 5, **kwargs
    ):
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/_search"

        min_score = (
            kwargs["score_threshold"]
            if "score_threshold" in kwargs
            else self._min_score
        )

        data = {
            "query": {
                "sum": [
                    {
                        "field": self.embedding_field,
                        "feature": arr,
                        "min_score": min_score,
                    }
                ],
                "filter": self._parse_filter(filter),
            },
            "retrieval_param": {"nprobe": 100},
            "size": limit,
            "is_brute_search": self._is_brute_search,
        }
        request_ret = requests.post(
            url, headers=self._url_headers, data=json.dumps(data)
        )
        if request_ret.status_code != 200:
            raise Exception(
                f"检索数据：查询{url}失败，错误信息为：{request_ret.json()}"
            )
        res_dict: Dict = request_ret.json()
        if res_dict["hits"]["total"] > 0:
            return res_dict["hits"]["hits"]
        return []

    def _request_delete_data_by_id(self, data_id) -> bool:
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/{data_id}"
        request_ret = requests.delete(url)
        if request_ret.status_code != 200:
            raise Exception(
                f"基于id删除数据：查询{url}失败，错误信息为：{request_ret.json()}"
            )
        # 进一步判断是否成功删除
        return True

    def _request_get_data_by_id(self, data_id):
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/{data_id}"
        request_ret = requests.get(url)
        if request_ret.status_code != 200:
            raise Exception(
                f"基于id获取数据：查询{url}失败，错误信息为：{request_ret.json()}"
            )

        res_dict = request_ret.json()
        if res_dict["found"]:
            return res_dict["_source"]
        return res_dict

    def _get_insert_request_url_for_batch_data(
        self, insert_dict_list
    ) -> Tuple[str, str]:
        """
        insert_dict_list = [
            {"text": "xxx", "format": "xx", "src": 1.1, "embedding": {"feature": [0.1, 0.1, 0.1, 0.1, 0.1]}},
            {"text": "xxx", "format": "xx", "src": 1.1, "embedding": {"feature": [0.1, 0.1, 0.1, 0.1, 0.1]}}
        ]
        """
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/_bulk"

        insert_dict_strings = []

        # 构建需要插入的数据
        # {"index": {"_id": "v1"}}
        # {"text": "abc", "src": 2.1, "embedding": {"feature": [0.2, 0.1, ...]}}
        # {"index": {"_id": "v1"}}
        # {"text": "def", "src": 2.1, "embedding": {"feature": [0.2, 0.1, ...]}}

        for insert_dict in insert_dict_list:
            _uuid = uuid.uuid4().hex
            uuid_str = {"index": {"_id": _uuid}}
            insert_dict_strings.append(json.dumps(uuid_str))
            insert_dict_strings.append(json.dumps(insert_dict))

        data = "\n".join(insert_dict_strings)

        return url, data

    def _request_delete_space(self) -> str:
        """
        删除表，返回被删除的表名
        """
        url = f"http://{self.master_address}/space/{self.db_name}/{self.space_name}"
        request_ret = requests.delete(url)
        if request_ret.status_code != 200:
            raise Exception(f"删除表：查询{url}失败，错误信息为：{request_ret.json()}")
        return self.space_name

    def delete_space(self) -> Optional[str]:
        """
        删除表，返回被删除的表名
        """
        if self._request_check_table_exist():
            space_name = self._request_delete_space()
            logger.info("删除库表成功")
            return space_name
        else:
            logger.error("表不存在，删除失败")

    async def embedding_worker(
        self,
        name: str,
        document_batch_queue: asyncio.Queue,
        embedding_batch_queue: asyncio.Queue,
        _essential: object,
    ):
        while True:
            logger.debug(f"embedding_worker = {name}, waiting for data")

            document_batch: Dict = await document_batch_queue.get()

            if document_batch == _essential:
                logger.info(f"embedding_worker = {name}, find essential")
                break

            batch_id: int = document_batch["batch_id"]
            texts: List[str] = document_batch["texts"]
            metadatas: List[Dict] = document_batch["metadatas"]

            docs_with_embedding = {
                "batch_id": batch_id,
                "texts": texts,
                "metadatas": metadatas,
                "embeddings": await self.embedding_function.aembed_documents(texts),
            }

            await embedding_batch_queue.put(docs_with_embedding)
            document_batch_queue.task_done()

    @staticmethod
    async def request_url_with_data(url, data) -> List[Dict]:
        async with ClientSession() as session:
            async with session.post(url=url, data=data) as response:
                res = await response.json()
                return res

    async def uploading_worker(
        self,
        name: str,
        embedding_batch_queue: asyncio.Queue,
        result_id_batch_queue: asyncio.Queue,
        _essential: object,
    ):
        while True:
            logger.debug(f"in uploading_worker = {name}, waiting for data")

            doc_with_embedding_batch: Dict = await embedding_batch_queue.get()

            if doc_with_embedding_batch == _essential:
                logger.debug(f"request_pack_worker = {name}, find essential")
                break

            batch_id = doc_with_embedding_batch["batch_id"]
            texts = doc_with_embedding_batch["texts"]
            metadatas = doc_with_embedding_batch["metadatas"]
            embeddings = doc_with_embedding_batch["embeddings"]

            logger.debug(
                f"in request_pack_worker = {name}, uploading batch = {batch_id}, uploaded"
            )

            insert_dict_list = []
            for i in range(len(texts)):
                insert_dict = {
                    self.text_field: texts[i],
                    self.embedding_field: {"feature": embeddings[i]},
                }

                metadata: dict = metadatas[i]
                for key, value in metadata.items():
                    insert_dict[key] = value
                insert_dict_list.append(insert_dict)

            url, data = self._get_insert_request_url_for_batch_data(insert_dict_list)

            r: List[Dict] = await self.request_url_with_data(url, data)
            try:
                inserted_ids = [d["_id"] for d in r]

                result_id_batch_queue.put_nowait(inserted_ids)
                embedding_batch_queue.task_done()
                logger.debug(
                    f"in request_pack_worker = {name}, uploading batch = {batch_id}"
                )
            except Exception as e:
                logger.error(f"r = {r}")
                logger.error(f"data = {data}")
                logger.error(e)
                raise Exception(f"异步uploading_worker操作失败，错误信息为：{e}")

    async def put_texts_worker(
        self,
        texts: Union[Iterable[str], List[str]],
        metadatas: List[dict],
        document_batch_queue: asyncio.Queue,
        _essential: object,
    ):
        logger.debug("put document batch")
        for i in range(0, len(texts), self.batch_size):
            # 记录 batch_id 防止程序中断无法恢复
            _data = {
                "batch_id": i,
                "texts": texts[i : i + self.batch_size],
                "metadatas": metadatas[i : i + self.batch_size],
            }
            await document_batch_queue.put(_data)

    async def add_texts_with_async(
        self,
        texts: Iterable[str],
        metadatas: List[dict],
    ):
        """
        采用异步方式进行上传
        1. 分batch -> document_batch_queue
        2. embedding -> embedding_batch_queue
        3. uploading -> result_id_batch_queue
        """
        logger.info("采用异步方式进行数据 embedding 和上传")

        document_batch_queue = asyncio.Queue(self.async_workers_number)
        embedding_batch_queue = asyncio.Queue(self.async_workers_number)
        result_id_batch_queue = asyncio.Queue()

        _essential = object()
        put_task = asyncio.create_task(
            self.put_texts_worker(texts, metadatas, document_batch_queue, _essential)
        )

        # embedding任务
        embedding_tasks = []
        for worker_id in range(self.async_workers_number):
            task = asyncio.create_task(
                self.embedding_worker(
                    str(worker_id),
                    document_batch_queue,
                    embedding_batch_queue,
                    _essential,
                )
            )
            embedding_tasks.append(task)

        # 上传数据
        uploading_tasks = []
        for _ in range(self.async_workers_number):
            task = asyncio.create_task(
                self.uploading_worker(
                    str(_), embedding_batch_queue, result_id_batch_queue, _essential
                )
            )
            uploading_tasks.append(task)

        await put_task
        for i in range(self.async_workers_number):
            await document_batch_queue.put(_essential)

        for task in embedding_tasks:
            await task

        for i in range(self.async_workers_number):
            await embedding_batch_queue.put(_essential)

        for task in uploading_tasks:
            await task

        result_ids = []
        while not result_id_batch_queue.empty():
            result_ids.extend(result_id_batch_queue.get_nowait())

        return result_ids

    def _request_insert_batch_data(self, insert_dict_list) -> List:
        """
        insert_dict_list = [
            {"text": "xxx", "format": "xx", "src": 1.1, "embedding": {"feature": [0.1, 0.1, 0.1, 0.1, 0.1]}},
            {"text": "xxx", "format": "xx", "src": 1.1, "embedding": {"feature": [0.1, 0.1, 0.1, 0.1, 0.1]}}
        ]
        """
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/_bulk"

        insert_dict_strings = []
        inserted_ids = []

        # 构建需要插入的数据
        # {"index": {"_id": "v1"}}
        # {"text": "abc", "src": 2.1, "embedding": {"feature": [0.2, 0.1, ...]}}
        # {"index": {"_id": "v1"}}
        # {"text": "def", "src": 2.1, "embedding": {"feature": [0.2, 0.1, ...]}}

        for insert_dict in insert_dict_list:
            _uuid = uuid.uuid4().hex
            uuid_str = {"index": {"_id": _uuid}}
            insert_dict_strings.append(json.dumps(uuid_str))
            dumps_data_string = """{}""".format(json.dumps(insert_dict))
            insert_dict_strings.append(dumps_data_string)

            inserted_ids.append(_uuid)

        data = "\n".join(insert_dict_strings)
        data = data.encode("utf-8")

        request_ret = requests.post(url, headers=self._url_headers, data=data)
        if request_ret.status_code != 200:
            # logger.error(insert_dict_strings)
            logger.error(request_ret.json())
            raise Exception(
                f"批量上传数据：查询{url}失败，错误信息为{request_ret.json()}"
            )

        return inserted_ids

    def add_texts_by_batch(
        self, texts: List[str], metadatas: Optional[List[dict]] = None, **kwargs: Any
    ) -> List[str]:
        assert len(texts) == len(metadatas), "text和meta长度不一致"

        text_batches = [
            texts[i : i + self.batch_size]
            for i in range(0, len(texts), self.batch_size)
        ]
        meta_batches = [
            metadatas[i : i + self.batch_size]
            for i in range(0, len(metadatas), self.batch_size)
        ]
        inserted_ids = []

        for _batch_index in range(len(text_batches)):
            text_batch: List[str] = text_batches[_batch_index]
            meta_batch: List[dict] = meta_batches[_batch_index]

            logger.info(f"batch数据上传，进度：{_batch_index + 1}/{len(text_batches)}")
            time_of_embedding_1 = time.time()
            embedding_batches = self.embedding_function.embed_documents(
                texts=text_batch
            )
            time_of_embedding_2 = time.time()
            logger.info(
                f"batch数据上传，embedding完成，耗时{time_of_embedding_2 - time_of_embedding_1:.2f}s"
            )

            insert_dict_list = []
            for i in range(len(text_batch)):
                insert_dict = {
                    self.text_field: text_batch[i],
                    self.embedding_field: {"feature": embedding_batches[i]},
                    **meta_batch[i],
                }
                insert_dict_list.append(insert_dict)

            time_of_inserting_1 = time.time()
            _ids = self._request_insert_batch_data(insert_dict_list)
            time_of_inserting_2 = time.time()

            logger.info(
                f"batch数据上传，应上传量：{len(text_batch)}, 成功上传量：{len(_ids)}, 耗时{time_of_inserting_2 - time_of_inserting_1:.2f}s"
            )
            if len(text_batch) != len(_ids):
                logger.error("部分上传失败")

            if self.per_batch_delay > 0:
                time.sleep(self.per_batch_delay)
                logger.info(f"batch数据上传，中断 {self.per_batch_delay} 秒")

            inserted_ids.extend(_ids)

        return inserted_ids

    def add_texts(
        self, texts: List[str], metadatas: Optional[List[dict]] = None, **kwargs: Any
    ) -> List[str]:
        metadatas = self._ensure_tb_and_align_metadatas(texts, metadatas)

        # if self.async_workers_number > 1:
        #
        #     # 异步 batch_size 上传
        #     inserted_ids = asyncio.get_event_loop().run_until_complete(
        #         self.add_texts_with_async(texts=texts, metadatas=metadatas)
        #     )
        #     return inserted_ids

        # 同步 batch_size 上传
        return self.add_texts_by_batch(texts=texts, metadatas=metadatas, **kwargs)

    def _ensure_tb_and_align_metadatas(
        self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[dict]:
        """
        确定表存在，并对齐metadata，同时
        """

        for _t in texts:
            if len(_t) > self.text_length_threshold:
                raise Exception(f"文本长度超长，当前长度为：{len(_t)}")

        if metadatas is None:
            aligned_metadatas = [{}] * len(texts)
        else:
            aligned_metadatas = copy.deepcopy(metadatas)

        # 检查表是否存在，若不存在，则根据第0个数据初始化表
        if not self._request_check_table_exist():
            self._request_create_table_with_metadata(aligned_metadatas[0])

        # 对齐 documents 中的 meta
        logger.info("开始对齐 meta")
        fields_info, _ = self._get_fields_info()

        example_data = {"string": "", "float": 0.01, "integer": 1}
        meta_example = {
            k: example_data[fields_info[k]["type"]]
            for k in fields_info
            if (k != self.embedding_field and k != self.text_field)
        }
        for metadata in aligned_metadatas:
            if set(meta_example.keys()) != set(metadata.keys()):
                # 保留指定的 keys
                for _key in list(metadata.keys()):
                    if _key not in meta_example:
                        metadata.pop(_key)
                # 添加不包含的 dict
                for _key in list(meta_example.keys()):
                    if _key not in metadata:
                        metadata[_key] = meta_example[_key]
        logger.info("结束对齐 meta")
        return aligned_metadatas

    async def aadd_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        metadatas = self._ensure_tb_and_align_metadatas(texts, metadatas)
        return await self.add_texts_with_async(texts=texts, metadatas=metadatas)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> List[Document]:
        ids, docs = self.similarity_search_with_id(
            query=query, k=k, filter=filter, **kwargs
        )
        return docs

    def similarity_search_with_id(
        self,
        query: str,
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> Tuple[List, List[Document]]:
        target_embedding = self.embedding_function.embed_query(query)
        logger.info(f"检索数据：query={query}, filter={filter}, k={k}")
        return self.similarity_search_by_vector_with_id(
            embedding=target_embedding, k=k, filter=filter, **kwargs
        )

    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> List[Document]:
        ids, docs = self.similarity_search_by_vector_with_id(
            embedding=embedding, k=k, filter=filter, **kwargs
        )
        return docs

    def  similarity_search_by_vector_with_id(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> Tuple[List, List[Document]]:
        ids, docs_with_score = self.similarity_search_by_vector_with_score_and_id(
            embedding=embedding, k=k, filter=filter, **kwargs
        )
        docs = [_doc for _doc, _score in docs_with_score]
        return ids, docs

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        ids, docs_with_score = self.similarity_search_with_score_and_id(
            query=query, k=k, filter=filter, **kwargs
        )
        return docs_with_score

    def similarity_search_with_score_and_id(
        self,
        query: str,
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> Tuple[List, List[Tuple[Document, float]]]:
        embeddings = self.embedding_function.embed_query(text=query)
        ids, docs_with_score = self.similarity_search_by_vector_with_score_and_id(
            embedding=embeddings, k=k, filter=filter, **kwargs
        )
        return ids, docs_with_score

    def similarity_search_by_vector_with_score(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        ids, docs_with_score = self.similarity_search_by_vector_with_score_and_id(
            embedding=embedding, k=k, filter=filter, **kwargs
        )
        return docs_with_score

    def similarity_search_by_vector_with_score_and_id(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[DictFilters] = None,
        **kwargs: Any,
    ) -> Tuple[List, List[Tuple[Document, float]]]:
        # if not self._request_check_table_exist():
        #     raise Exception(f"表未初始化, kwargs={kwargs}")

        res: List[Dict] = self._request_search(
            embedding, filter=filter, limit=k, **kwargs
        )

        # {
        #   '_index': 'sl_docdb',
        #   '_type': 'sl_chunk_space',
        #   '_id': '-7368204553032502245',
        #   '_score': 0.05000000447034836,
        #   '_source': {'format': 'pdf', 'src': 'xxx', 'text': 'xxx'}
        # }

        ids = []
        docs_with_score = []
        for item in res:
            data: Dict = item["_source"]
            score: float = item["_score"]
            page_content = data[self.text_field]
            metadata = {}
            for _k, _v in data.items():
                if _k != self.text_field:
                    metadata[_k] = _v

            doc_id: str = item["_id"]
            document = Document(page_content=page_content, metadata=metadata)

            ids.append(doc_id)
            docs_with_score.append((document, score))

        if len(ids) > 0:
            logger.info(
                f"检索数据成功：length={len(ids)}, docs[0]={docs_with_score[0]}"
            )
        else:
            logger.info("检索数据成功：length=0, 暂未检索到相关信息")

        return ids, docs_with_score

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:
        raise NotImplementedError

    def max_marginal_relevance_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:
        raise NotImplementedError

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> "VearchCluster":
        vearch = cls(embedding_function=embedding, **kwargs)
        vearch.add_texts(texts=texts, metadatas=metadatas)
        return vearch

    def delete(self, ids: Optional[List[str]] = None, **kwargs: Any) -> int:
        logger.info(f"开始数据删除，删除量为：{len(ids)}")
        for data_id in ids:
            self._request_delete_data_by_id(data_id)
        logger.info(f"数据删除完成，删除量为：{len(ids)}")
        return len(ids)

    def delete_by_text(self, text: str, recursion: bool = True) -> int:
        """
        根据指定内容删除数据项, recursion控制是否批量删除，默认批量删除
        """
        if not self._request_check_table_exist():
            raise Exception("表不存在，无法删除指定内容")

        deleted_ids = []

        while True:
            ids, docs = self.similarity_search_with_id(query=text, k=1)
            if len(docs) and docs[0].page_content == text:
                self.delete(ids=ids)
                deleted_ids.extend(ids)
            else:
                break

            if not recursion:
                break

        return len(deleted_ids)

    def delete_by_conditions(self, conditions: List[Dict]) -> List[str]:
        """
        根据字段对数据进行删除
        conditions = [{'src': 'a.txt'}, {'value': 4}]
        """

        if not self._request_check_table_exist():
            return []

        fields_info, _ = self._get_fields_info()

        # 防止条件重复
        keys = set([list(condition.keys())[0] for condition in conditions])
        assert len(keys) == len(conditions), "fields重复"

        # filter = [{'index1': {'gte': 3}}, {'index2': {'lte': 2}}, {'format1': {'in': ['pdf', 'doc']}}]
        filter = []

        for condition in conditions:
            field = list(condition.keys())[0]
            field_value = condition[field]

            assert (
                field in fields_info and fields_info[field]["index"] is True
            ), f"不存在字段{field}或该字段未被索引，无法过滤"  # 确定相关参数在索引中

            if isinstance(field_value, str):
                filter.append({field: {"in": [field_value]}})
            elif isinstance(field_value, int):
                filter.append({field: {"lte": field_value, "gte": field_value}})
            else:
                raise Exception(
                    f"仅支持数据类型 int 和 str，当前数据类型为：{type(field_value)}"
                )

        deleted_ids: List[str] = []

        logger.info(f"开始删除，过滤条件为：{filter}")

        while len(cur_deleted_ids := self._request_delete_by_filter(filter)) > 0:
            logger.info(f"迭代删除中，删除数量：{len(cur_deleted_ids)}, {cur_deleted_ids[:10]}")
            deleted_ids.extend(cur_deleted_ids)

        return deleted_ids
    
    def delete_by_filter(self, filter: DictFilters) -> List[str]:
        """
        根据字段对数据进行删除
        conditions = [{'src': 'a.txt'}, {'value': 4}]
        """

        if not self._request_check_table_exist():
            return []

        deleted_ids: List[str] = []

        logger.info(f"开始删除，过滤条件为：{filter}")

        while len(cur_deleted_ids := self._request_delete_by_filter(filter)) > 0:
            logger.info(f"迭代删除中，删除数量：{len(cur_deleted_ids)}, {cur_deleted_ids[:10]}")
            deleted_ids.extend(cur_deleted_ids)

        return deleted_ids

    def _request_delete_by_filter(self, filter: DictFilters) -> List[str]:
        """
        根据过滤条件对数据进行批量删除
        """
        url = f"http://{self.router_address}/{self.db_name}/{self.space_name}/_delete_by_query"

        data = {
            "query": {"filter": self._parse_filter(filter)},
            "size": self.batch_size,
            "is_brute_search": 1,
            "vector_value": False,
        }
        request_ret = requests.post(
            url, headers=self._url_headers, data=json.dumps(data)
        )
        if request_ret.status_code != 200:
            raise Exception(
                f"基于过滤条件删除数据：查询{url}失败，错误信息为：{request_ret.json()}"
            )
        res_dict: Dict = request_ret.json()
        if "del_num" in res_dict:
            # for vearch 3.3
            if res_dict["del_num"] > 0:
                return res_dict["_id"]
        elif "total" in res_dict:
            # for vearch 3.4
            if res_dict["total"] > 0:
                return res_dict["document_ids"]
        return []

    def clear_tb(self) -> None:
        """
        清空表内所有数据，维持表结构不变
        """
        if not self._request_check_table_exist():
            raise Exception("表不存在，无法删除指定内容")

        cnt = 0
        while True:
            ids, _ = self.similarity_search_with_id(query="demo", k=self.batch_size)
            if len(ids) == 0:
                break
            self.delete(ids=ids)
            logger.info(f"删除中，删除数量：{len(ids)}")
            cnt += len(ids)
        logger.info(f"删除完成，删除数量：{cnt}")
