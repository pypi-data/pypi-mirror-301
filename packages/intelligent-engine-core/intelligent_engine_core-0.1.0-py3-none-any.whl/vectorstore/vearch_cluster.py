from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, Union

import numpy as np
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from vearch.config import Config
from vearch.core.vearch import Vearch as VearchCore
from vearch.filter import Condition, FieldValue, Filter
from vearch.schema.field import Field
from vearch.schema.index import HNSWIndex, ScalarIndex
from vearch.schema.space import SpaceSchema
from vearch.utils import DataType, MetricType, VectorInfo
from urllib.parse import urlparse, urlunparse

DEFAULT_TOPN = 4

def ensure_url_protocol(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # 默认使用 'http' 协议
        parsed_url = urlparse(f'http://{url}')
    return urlunparse(parsed_url)

class VearchCluster(VectorStore):
    _DEFAULT_SPACE_NAME = "langchain_vearch"
    _DEFAULT_CLUSTER_DB_NAME = "cluster_client_db"  
    
    @staticmethod
    def check_new_version(router_adress: str) -> str:
        import httpx
        import re
        url = ensure_url_protocol(router_adress)
        resp = httpx.get(url)
        if resp.status_code != 200:
            master_adress = url.replace("router", "master")
            resp = httpx.get(master_adress)
            if resp.status_code != 200:
                raise Exception(f"访问异常:{resp.text}")

        match = re.search(r'"build_version":"v([\d\.]+)"', resp.text)
        if match:
            build_version = match.group(1)
            major, minor, *patch = map(int, build_version.split('.'))
            if (major, minor) > (3, 5):
                return True
            elif (major, minor) == (3, 5) and (patch and patch[0] > 0):
                return True
            else:
                return False
                
        raise Exception(f"异常：未检查到版本号")
        
    def __new__(cls, router_address, *args, **kwargs):
        is_new_version = VearchCluster.check_new_version(router_address)
        if is_new_version:
            instance = super().__new__(cls)
            return instance
        else:
            from vectorstore.vearch_old import VearchCluster as VearchOldCluster
            master_address = kwargs.pop("master_address", router_address.replace("router", "master"))
            return VearchOldCluster(router_address=router_address, master_address=master_address, **kwargs)


    def __init__(
        self,
        router_address: Optional[str],
        embedding_function: Embeddings,
        db_name: str = _DEFAULT_CLUSTER_DB_NAME,
        space_name: str = _DEFAULT_SPACE_NAME,
        **kwargs
    ) -> None:
        """Initialize vearch vector store"""
        if router_address is None:
            raise ValueError("Please input router url of vearch")
        if not db_name:
            db_name = self._DEFAULT_CLUSTER_DB_NAME
            db_name += "_"
            db_name += str(uuid.uuid4()).split("-")[-1]
        self.using_db_name = db_name
        self.url = ensure_url_protocol(router_address)
        self.vearch = VearchCore(Config(host=self.url))
        if not space_name:
            space_name = self._DEFAULT_SPACE_NAME
            space_name += "_"
            space_name += str(uuid.uuid4()).split("-")[-1]
        self.using_space_name = space_name
        self.embedding_func = embedding_function

    @property
    def embeddings(self) -> Optional[Embeddings]:
        return self.embedding_func

    @classmethod
    def from_documents(
        cls: Type[VearchCluster],
        documents: List[Document],
        embedding: Embeddings,
        router_address: Optional[str] = None,
        db_name: str = _DEFAULT_CLUSTER_DB_NAME,
        space_name: str = _DEFAULT_SPACE_NAME,
        **kwargs: Any,
    ) -> VearchCluster:
        """Return Vearch VectorStore"""

        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]

        return cls.from_texts(
            texts=texts,
            embedding=embedding,
            metadatas=metadatas,
            router_address=router_address,
            db_name=db_name,
            space_name=space_name,
            **kwargs,
        )

    @classmethod
    def from_texts(
        cls: Type[VearchCluster],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        router_address: Optional[str] = None,
        db_name: str = _DEFAULT_CLUSTER_DB_NAME,
        space_name: str = _DEFAULT_SPACE_NAME,
        **kwargs: Any,
    ) -> VearchCluster:
        """Return Vearch VectorStore"""

        vearch = cls(
            embedding_function=embedding,
            router_address=router_address,
            db_name=db_name,
            space_name=space_name,
        )
        vearch.add_texts(texts=texts, metadatas=metadatas, **kwargs)
        return vearch

    def _get_matadata_field(self, metadatas: Optional[List[dict]] = None):
        field_list = []
        if metadatas:
            for key, value in metadatas[0].items():
                if isinstance(value, int):
                    field_list.append({"field": key, "type": "int"})
                    continue
                if isinstance(value, str):
                    field_list.append({"field": key, "type": "str"})
                    continue
                if isinstance(value, float):
                    field_list.append({"field": key, "type": "float"})
                    continue
                else:
                    raise ValueError("Please check data type,support int, str, float")
        return field_list

    def _create_space_schema(self, dim: int) -> SpaceSchema:
        filed_list_add = self.field_list
        type_dict = {
            "int": DataType.INTEGER,
            "str": DataType.STRING,
            "float": DataType.FLOAT,
        }
        fields = [
            Field(
                "text_embedding",
                DataType.VECTOR,
                HNSWIndex("vec_idx", MetricType.Inner_product, 32, 64),
                dimension=dim,
            ),
            Field("text", DataType.STRING),
        ]
        for fi in filed_list_add:
            fields.append(
                Field(
                    fi["field"],
                    type_dict[fi["type"]],
                    index=ScalarIndex(fi["field"] + "_idx"),
                )
            )
        space_schema = SpaceSchema(self.using_space_name, fields)
        return space_schema

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """
        Returns:
            List of ids from adding the texts into the vectorstore.
        """

        embeddings = None
        if self.embedding_func is not None:
            embeddings = self.embedding_func.embed_documents(list(texts))
        if embeddings is None:
            raise ValueError("embeddings is None")
        self.field_list = self._get_matadata_field(metadatas)

        # check database
        if not self.vearch.is_database_exist(self.using_db_name):
            create_db_result = self.vearch.create_database(self.using_db_name)
            if not create_db_result.is_success():
                raise ValueError("create db failed!!!")

        # check space
        space_exist, _, _ = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if not space_exist:
            create_space_result = self.vearch.create_space(
                self.using_db_name, self._create_space_schema(len(embeddings[0]))
            )
            if not create_space_result.is_success():
                raise ValueError("create space failed!!!")

        docid = []
        if embeddings is not None and metadatas is not None:
            meta_field_list = [f["field"] for f in self.field_list]
            for text, metadata, embed in zip(texts, metadatas, embeddings):
                profiles: dict[str, Any] = {}
                profiles["text"] = text
                for f in meta_field_list:
                    profiles[f] = metadata[f]
                em_np = np.array(embed)
                profiles["text_embedding"] = (em_np / np.linalg.norm(em_np)).tolist()
                insert_result = self.vearch.upsert(
                    self.using_db_name, self.using_space_name, [profiles]
                )
                if insert_result.is_success():
                    docid.append(insert_result.document_ids[0]["_id"])
                    continue
                else:
                    retry_insert_result = self.vearch.upsert(
                        self.using_db_name, self.using_space_name, [profiles]
                    )
                    if not retry_insert_result.is_success():
                        raise RuntimeError(
                            f"Upsert twice failed: {retry_insert_result.msg}"
                        )
                    docid.append(retry_insert_result.document_ids[0]["_id"])
                    continue
        return docid

    def _get_field_list_from_c(self):
        pass

    def _parse_filter(self, filter: Optional[Dict[str, Any]]) -> Optional[Filter]:
        if filter is None:
            return None


        if len(filter) == 0 or "operator" not in filter.keys() or "conditions" not in filter.keys():
            return None

        filter_operator = filter["operator"]

        filter_conditions = []
        for condition in filter["conditions"]:
            filter_conditions.append(
                Condition(
                    condition["operator"],
                    FieldValue(condition["field"], condition["value"]),
                )
            )

        return Filter(operator=filter_operator, conditions=filter_conditions)

    def similarity_search(
        self,
        query: str,
        k: int = DEFAULT_TOPN,
        filter: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """
        Return docs most similar to query.
        为了兼容新老版本，filter有两种格式：
        新版本：
            filter = {
                "operator": "AND",
                "conditions":[
                    {"operator": "IN", "field": "book_name", "value": ["For Whom the Bell Tolls",]},
                    {"operator": ">=", "field": "book_num", "value": "25",},
                    {"operator": "<=", "field": "book_num", "value": "9",},
                ]
            }
        旧版本：
            filter = [
                {'book_name': {'in': ["For Whom the Bell Tolls"]}},
                {'book_num': {'gte': 9}}, 
                {'book_num': {'lte': 25}}
            ]
        """
        docs_and_scores = self.similarity_search_with_score(
            query, k, filter=filter, **kwargs
        )
        return [doc for doc, _ in docs_and_scores]

    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = DEFAULT_TOPN,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """The most k similar documents and scores of the specified query.
        Args:
            embeddings: embedding vector of the query.
            k: The k most similar documents to the text query.
        Returns:
            The k most similar documents to the specified text query.
            0 is dissimilar, 1 is the most similar.
        """
        docs_and_scores = self.similarity_search_by_vector_with_score(
            embedding, k, filter=filter, **kwargs
        )
        return [doc for doc, _ in docs_and_scores]

    def similarity_search_by_vector_with_score(
        self,
        embedding: List[float],
        k: int = DEFAULT_TOPN,
        filter: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        embed = np.array(embedding)
        space_exist, _, schemas = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if not space_exist:
            raise RuntimeError("space not exist")

        meta_field_list = [
            item.name for item in schemas.fields if item.name != "text_embedding"
        ]
        vector = VectorInfo("text_embedding", (embed / np.linalg.norm(embed)).tolist())

        query_result = self.vearch.search(
            self.using_db_name,
            self.using_space_name,
            [
                vector,
            ],
            fields=meta_field_list,
            limit=k,
            filter=self._parse_filter(filter) if isinstance(filter, Dict) else self._transform_filter(filter),
            **kwargs,
        )
        if not query_result.is_success():
            raise RuntimeError(f"search failed: {query_result.msg}")
        if not query_result.documents:
            return []
        res = query_result.documents[0]
        results: List[Tuple[Document, float]] = []
        for item in res:
            content = ""
            meta_data = {}
            score = item["_score"]
            for item_key in item:
                if item_key == "text":
                    content = item[item_key]
                    continue
                if item_key in meta_field_list:
                    meta_data[item_key] = item[item_key]
                    continue
            tmp_res = (Document(page_content=content, metadata=meta_data), score)
            results.append(tmp_res)
        return results

    def similarity_search_with_score(
        self,
        query: str,
        k: int = DEFAULT_TOPN,
        filter: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        """The most k similar documents and scores of the specified query.
        Args:
            embeddings: embedding vector of the query.
            k: The k most similar documents to the text query.
            min_score: the score of similar documents to the text query
        Returns:
            The k most similar documents to the specified text query.
            0 is dissimilar, 1 is the most similar.
        """

        if self.embedding_func is None:
            raise ValueError("embedding_func is None!!!")
        embeddings = self.embedding_func.embed_query(query)

        return self.similarity_search_by_vector_with_score(
            embeddings, k, filter=filter, **kwargs
        )

    def _similarity_search_with_relevance_scores(
        self,
        query: str,
        k: int = 4,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        return self.similarity_search_with_score(query, k, **kwargs)

    async def _asimilarity_search_with_relevance_scores(
        self,
        query: str,
        k: int = 4,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        return await self.asimilarity_search_with_score(query, k, **kwargs)

    def delete(
        self,
        ids: Optional[List[str]] = None,
        filter: Filter | None = None,
        **kwargs: Any,
    ) -> Optional[bool]:
        """Delete the documents which have the specified ids.

        Args:
            ids: The ids of the embedding vectors.
            **kwargs: Other keyword arguments that subclasses might use.
        Returns:
            Optional[bool]: True if deletion is successful.
            False otherwise, None if not implemented.
        """

        # if ids is None or ids.__len__() == 0:
        #     return None
        result = self.vearch.delete(
            self.using_db_name, self.using_space_name, ids, filter=filter, **kwargs
        )
        if result.is_success():
            return True
        else:
            return False

    def delete_by_conditions(
        self, 
        conditions: List[Dict[str, Any]]
    ) -> List[str]:
        """
        通过简单的conditions，将值相等的数据删除
        conditions = [{'src': 'a.txt'}, {'value': 4}]
        """
        space_exist, _, schemas = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if not space_exist:
            raise RuntimeError("space not exist")

        # 防止条件重复
        keys = set([list(condition.keys())[0] for condition in conditions])
        assert len(keys) == len(conditions), "fields重复"
        
        meta_field_list = {
            item.name: item for item in schemas.fields if item.name != "text_embedding"
        }
        format_conditions = []
        for condition in conditions:
            field = list(condition.keys())[0]
            field_value = condition[field]
            assert (
                field in meta_field_list.keys() and meta_field_list[field].index is not None
            ), f"不存在字段{field}或该字段未被索引，无法过滤"  # 确定相关参数在索引中

            if isinstance(field_value, str):
                format_conditions.append(
                    Condition(
                        operator = "IN",
                        fv = FieldValue(field, [field_value]),
                    )
                )
            elif isinstance(field_value, int):
                format_conditions.append(
                    Condition(
                        operator = "<=",
                        fv = FieldValue(field, field_value),
                    )
                )
                format_conditions.append(
                    Condition(
                        operator = ">=",
                        fv = FieldValue(field, field_value),
                    )
                )
            else:
                raise Exception(f"仅支持数据类型 int 和 str，当前数据类型为：{type(field_value)}")


        filter = Filter(operator="AND", conditions=format_conditions)
        return self.delete(filter=filter)

    def delete_by_filter(
        self, 
        filter: List[Dict[str, Dict[str, Union[int, float, List]]]]
    ) -> List[str]:
        """
        根据filter进行删除
        """
        space_exist, _, _ = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if not space_exist:
            raise RuntimeError("space not exist")

        filter = self._transform_filter(filter)
        
        return self.delete(filter=filter)
    
    def _transform_filter(
        self, 
        old_filter: Optional[List[Dict[str, Dict[str, Union[int, float, List]]]]] = None
    ) -> Optional[Filter]:
        # old_filter = [{'index1': {'gte': 3}}, {'index2': {'lte': 2}}, {'format1': {'in': ['pdf', 'doc']}}]
        if old_filter is None or len(old_filter) == 0:
            return None
        
        op_map = {"gte": ">=", "lte": "<=", "gt": ">", "lt": "<"}
        new_filter = []
        for filter in old_filter:
            
            for key, value in filter.items():
                for op, v in value.items():
                    if isinstance(v, list):
                        assert op == "in", f"filter:{filter}, key should be 'in'"
                        operator = "IN"
                    elif isinstance(v, list):
                        assert op in op_map.keys(), "not support op {op}"
                        operator = op_map[op],
                        
                    new_filter.append(
                        Condition(
                            operator = operator,
                            fv = FieldValue(key, v),
                        )
                    )
        return Filter(operator="AND", conditions=new_filter)
        

    def get(
        self,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Document]:
        """Return docs according ids.

        Args:
            ids: The ids of the embedding vectors.
        Returns:
            Documents which satisfy the input conditions.
        """

        space_exist, _, schemas = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if not space_exist:
            raise RuntimeError("space not exist")

        meta_field_list = [
            item.name for item in schemas.fields if item.name != "text_embedding"
        ]

        results: Dict[str, Document] = {}

        if ids is None or ids.__len__() == 0:
            return results
        docs_detail = self.vearch.query(self.using_db_name, self.using_space_name, ids)
        if not docs_detail.is_success():
            raise RuntimeError("search failed!!!")

        for record in docs_detail.documents:
            if "code" in record.keys():
                continue
            content = ""
            meta_info = {}
            for field in record:
                if field == "text":
                    content = record[field]
                    continue
                elif field in meta_field_list:
                    meta_info[field] = record[field]
                    meta_field_list.remove(field)
                    continue
            results[record["_id"]] = Document(page_content=content, metadata=meta_info)
        return results

    def delete_space(self) -> Optional[str]:
        """
        删除表
        """
        space_exist, _, schemas = self.vearch.is_space_exist(
            self.using_db_name, self.using_space_name
        )
        if space_exist:
            self.vearch.drop_space(self.using_db_name, self.using_space_name)
            
    def delete_db(self) -> Optional[str]:
        """
        删除库
        """
        if self.vearch.is_database_exist(self.using_db_name):
            self.vearch.drop_database(self.using_db_name)

if __name__ == "__main__":
    import time
    import uuid

    import dotenv
    dotenv.load_dotenv(verbose=True)
    from langchain_core.documents import Document
    from langchain_openai.embeddings import OpenAIEmbeddings

    docs = [
        Document(page_content="北京", metadata={"catogory": "city"}),
        Document(page_content="上海", metadata={"catogory": "city"}),
        Document(page_content="iphone", metadata={"catogory": "things"}),
        Document(page_content="电视", metadata={"catogory": "things"}),
    ]

    embedding_function = OpenAIEmbeddings(
        model="text-embedding-ada-002-2",
        openai_api_base="http://gpt-proxy.jd.com/v1",
    )

    db_name = "test_db_liutao"
    space_name = "test_space_liutao"
    #33: "open-query-bsc-router.vectorbase.svc.ht1.n.jd.local"
    #35: "http://aigc-9n-dev-router.vectorbase.svc.ht10.n.jd.local"
    vectorstore = VearchCluster.from_documents(
        docs,
        embedding=embedding_function,
        router_address="open-query-bsc-router.vectorbase.svc.ht1.n.jd.local",
        db_name=db_name,
        space_name=space_name,
    )

    time.sleep(2)

    # retriever = vectorstore.as_retriever(
    #     search_type="similarity_score_threshold",
    #     search_kwargs={"k": 3, "score_threshold": 0.7},
    # )
    # result = retriever.invoke("深圳")
    # print(f"0.7: {result}")
    # retriever.search_kwargs["score_threshold"] = 0.8
    # result = retriever.invoke("深圳")
    # print(f"0.8: {result}")
    # retriever.search_kwargs["score_threshold"] = 0.9
    # result = retriever.invoke("深圳")
    # print(f"0.9: {result}")
    filter = [
        {'catogory': {'in': ["city"]}},
    ]
    # filter = {
    #     "operator": "AND",
    #     "conditions":[
    #         {"operator": "IN", "field": "catogory", "value": ["city", "things"]},
    #     ]
    # }
    doc = vectorstore.similarity_search(query="hi", k=10,filter=filter)
    print(f"doc:{len(doc)}\n{doc}")
    conditions = [{'catogory': 'city'}]
    doc = vectorstore.delete_by_conditions(conditions=conditions)
    # conditons = [
    #     Condition(operator="IN", fv=FieldValue(field="catogory", value=["city"])),
    # ]
    # filter = Filter(operator="AND", conditions=conditons)
    # vectorstore.delete(filter=filter)

    doc = vectorstore.similarity_search(query="hi", k=10, filter=filter)
    print(f"after delete doc:{len(doc)}\n{doc}")

    vectorstore.delete_by_filter(filter=[{'catogory': {'in': ["things"]}}])
    doc = vectorstore.similarity_search(query="hi", k=10)
    print(f"after delete doc:{len(doc)}\n{doc}")
    vectorstore.delete_space()
