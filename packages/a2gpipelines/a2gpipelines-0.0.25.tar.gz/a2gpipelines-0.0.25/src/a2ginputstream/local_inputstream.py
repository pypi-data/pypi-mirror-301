from datetime import datetime, timedelta
from enum import Enum
import hashlib
import os
import json
from uuid import UUID
import requests
from a2ginputstream.inputstream import INSERTION_MODE, Inputstream, InputstreamStatus
from jsonschema import Draft4Validator
from dateutil import parser
import logging

logger = logging.getLogger("InputstreamClient")
logger.setLevel(logging.DEBUG)

# Environment production
A2G_DATA_URL        = os.environ.get("DATA_URL"         , "https://v2streams.a2g.io")
A2G_QUERY_MANAGER   = os.environ.get("QUERY_MANAGER"    , "https://v2streams.a2g.io")  
A2G_INPUTSTREAM_URL = os.environ.get("INPUTSTREAM_URL"  , "https://v2apigateway.a2g.io")
verify_https=True
# Environment development
# A2G_DATA_URL        = os.environ.get("DATA_URL", "https://localhost:1008")
# A2G_QUERY_MANAGER   = os.environ.get("QUERY_MANAGER", "http://localhost:1012")
# A2G_INPUTSTREAM_URL = os.environ.get("INPUTSTREAM_URL", "https://localhost:1000")

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return super().default(obj)


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args ,**kargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj:dict):
        for k, v in obj.items():
            if isinstance(v, str) and 'T' in v and '-' in v and ':' in v and len(v) < 40:
                try:
                    dv = parser.parse(v)
                    dt = dv.replace(tzinfo=None)
                    obj[k] = dt
                except:
                    pass
        return obj


class CacheManager:
    duration_inputstream:int
    duration_data:int

    def __init__(self, cache_options: dict | None = None):
        if cache_options is None:
            self.duration_data = 60 * 24
            self.duration_inputstream = 60 * 24
        else:
            self.duration_data = cache_options.get("duration_data", 60 * 24)
            self.duration_inputstream = cache_options.get("duration_inputstream", 60 * 24)

        # create cache directories
        if not os.path.exists(".a2g_cache"):
            os.mkdir(".a2g_cache")
            os.mkdir(".a2g_cache/data")
        

    def get_inputstream(self, ikey:str) -> Inputstream | None:
        """
        return Inputstream if exists in cache and is not expired
        otherwise return None
        params:
            ikey: str
        """
        file_name = f".a2g_cache/inputstreams/{ikey}.json"
        if os.path.exists(file_name):
            logger.info(f"Inputstream - Ikey: {ikey}, Checking cache expiration...")
            data = json.loads(open(file_name, "r").read(), cls=CustomJsonDecoder)
            if datetime.utcnow() < data["duration"]:
                logger.info(f"Inputstream - Ikey: {ikey}, from cache")
                return Inputstream(**data["inputstream"])
            else:
                logger.info(f"Inputstream - Ikey: {ikey}, Cache expired, removing file...")
                os.remove(file_name)
                return None
        return None


    def set_inputstream(self, inputstream:Inputstream):
        cache_register = {
            "inputstream": inputstream.get_dict(),
            "duration": datetime.utcnow() + timedelta(minutes=self.duration_inputstream)
        }

        file_name = inputstream.Ikey
        if not os.path.exists(f".a2g_cache/inputstreams/"): os.mkdir(f".a2g_cache/inputstreams/")
        open(f".a2g_cache/inputstreams/{file_name}.json", "w+").write(json.dumps(cache_register, cls=CustomJSONEncoder))


    def get_data(self, ikey:str, hash_query:str) -> list[dict] | None:
        """
        return data if exists in cache and is not expired
        otherwise return None
        params:
            ikey: str
            query: dict
        """
        file_name = f".a2g_cache/data/{ikey}/{hash_query}.json"
        index_ttl_file = f".a2g_cache/data/ttl_index.json"
        if os.path.exists(file_name) and os.path.exists(index_ttl_file):

            # check if cache is expired
            logger.info(f"Data - Ikey: {ikey}, Checking cache expiration...")
            index = json.loads(open(index_ttl_file, "r").read(), cls=CustomJsonDecoder)
            ttl_key = f"{ikey}_{hash_query}"
            if ttl_key in index:
                ttl = index[ttl_key]
                if datetime.utcnow() > ttl:
                    logger.info(f"Data - Ikey: {ikey}, Cache expired, removing file...")
                    os.remove(file_name)
                    return None

            # recover data from cache
            try:
                logger.info(f"Data - Ikey: {ikey}, Recovering data from cache...")
                data = json.loads(open(file_name, "r").read(), cls=CustomJsonDecoder)
                logger.info(f"Data - Ikey: {ikey}, from cache")
                return data
            except Exception as e:
                logger.error(f"Error reading cache file: {file_name} - {e}", stack_info=True)
                if os.path.exists(file_name): os.remove(file_name)
                return None
        else:
            if os.path.exists(file_name): os.remove(file_name)
            return None
    

    def set_data(self, ikey:str, hash_query:str, data:list[dict]):
        # update ttl index
        ttl_key = f"{ikey}_{hash_query}"
        ttl = datetime.utcnow() + timedelta(minutes=self.duration_data)
        index_file = f".a2g_cache/data/ttl_index.json"
        if os.path.exists(index_file):
            index = json.loads(open(index_file, "r").read(), cls=CustomJsonDecoder)
            index[ttl_key] = ttl
            open(index_file, "w+").write(json.dumps(index, cls=CustomJSONEncoder))
        else:
            open(index_file, "w+").write(json.dumps({ttl_key: ttl}, cls=CustomJSONEncoder))

        # save data
        file_name = f".a2g_cache/data/{ikey}/{hash_query}.json"
        if not os.path.exists(f".a2g_cache/")               : os.mkdir(f".a2g_cache/")
        if not os.path.exists(f".a2g_cache/data/")          : os.mkdir(f".a2g_cache/data/")
        if not os.path.exists(f".a2g_cache/data/{ikey}/")   : os.mkdir(f".a2g_cache/data/{ikey}/")
        open(file_name, "w+").write(json.dumps(data, cls=CustomJSONEncoder))



class A2GHttpClient():

    def __init__(self, token:str):
        self.token = token


    def get_inputstream_by_ikey(self, ikey:str) -> Inputstream:
        try:
            headers = { "Authorization": f"A2G {self.token}"}
            res = requests.get(A2G_INPUTSTREAM_URL + f"/Inputstream/Ikey/{ikey}", headers=headers, verify=verify_https)
            logger.info(f"Getting inputstream {ikey} from A2G...")
            if res.status_code != 200:
                logger.info(res.status_code, res.text) 
                if res.status_code == 404: raise Exception("Inputstream not found, please check your ikeyd")
                if res.status_code == 401: raise Exception("Unauthorized: please check your token or access permissions")
                if res.status_code == 403: raise Exception("Forbidden: please check your access permissions")
                raise Exception("Error getting inputstream")
            content = res.json(cls=CustomJsonDecoder)
            if not content["success"]: raise Exception(content["errorMessage"])
            return Inputstream(from_response=True, **content["data"])
        except Exception as e:
            raise e
        

    def find(self, ikey:str, query:dict, delete_id:bool=True) -> dict:
        try:
            logger.info("Downloading data from A2G...")
            hearders = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey,
                'Content-Type': 'application/json'
            }

            res = requests.post(A2G_QUERY_MANAGER + "/QueryData/ExecutionPlanningFind", 
                data = json.dumps(query, cls=CustomJSONEncoder), 
                headers=hearders, 
                verify=verify_https
            )
            if res.status_code != 200: 
                raise Exception(f"Error getting execution planning {res.status_code} {res.content}")
            

            content = res.json(cls=CustomJsonDecoder)
            if not content["success"]: raise Exception(content["errorMessage"])

            total_query     = content["data"]["total"]
            page_size       = content["data"]["size"]
            if total_query == 0:
                logger.info("No data found with the query provided.")
                return []
            
            downloaded_docs = 0
            page            = 1
            total_batchs    = (total_query // page_size) + 1
            docs            = []

            if content["data"]['stage'] != None:
                stage = content["data"]["stage"].replace('_',' -> ')
                logger.info(f"The query stages are {stage}")
                logger.info(F"The index used in query is {content['data']['indexName']}")
            else:
                logger.info(f"Complex query the explain was not saved")
            logger.info(f"Total documents to download {total_query}.")
            logger.info(f"Batch 0/{total_batchs}")

       
            my_body = {
                "delete_id": delete_id,
                "query": json.dumps(query, cls=CustomJSONEncoder) 
            }
                
            while downloaded_docs < total_query:
                res = requests.post(A2G_QUERY_MANAGER + "/QueryData/FindAll", 
                    data=json.dumps(my_body, cls=CustomJSONEncoder), 
                    headers=hearders, 
                    verify=verify_https, 
                    params={"page": page, "pageSize": page_size
                })
                if res.status_code != 200: raise Exception(f"Error downloading inputstream data {res.status_code}")
                content = res.json(cls=CustomJsonDecoder)
                if not content["success"]: raise Exception(content["errorMessage"])
                logger.info(f"Batch {page}/{total_batchs}")
                downloaded_docs += content["data"]["size"]
                docs += content["data"]["data"]
                page += 1

            logger.info(f"Data downloaded, total docs: {total_query}")
            return docs
        except Exception as e:
            raise e


    def find_one(self, ikey:str, query:dict) -> list[dict]:
        try:
            hearders = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey,
                'Content-Type': 'application/json'
            }
            res = requests.post(A2G_QUERY_MANAGER + "/QueryData/FindOne", 
                data=json.dumps(query, cls=CustomJSONEncoder),
                headers=hearders, 
                verify=verify_https
            )
            if res.status_code != 200: raise Exception(f"Error getting inputstream {res.status_code} {res.content}")
            content = res.json(cls=CustomJsonDecoder)
            if not content["success"]: raise Exception(content["errorMessage"])
            return content["data"]
        except Exception as e:
            raise e
        

    def aggregate(self, ikey:str, pipeline: list[dict]) -> list[dict]:
        try:
            hearders = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey,
                'Content-Type': 'application/json'
            }

            if not isinstance(pipeline, list):                      raise Exception("Invalid pipeline, must be a list")
            if not all(isinstance(x, dict) for x in pipeline):      raise Exception("Invalid pipeline, the steps must be dictionaries")
            #if len(pipeline) == 0:                                  raise Exception("Invalid pipeline, length must be greater than 0" )
            if any("$out" in x or "$merge" in x for x in pipeline): raise Exception("Invalid pipeline, write operations not allowed"  )


            res = requests.post(A2G_QUERY_MANAGER + "/QueryData/ExecutionPlanningAggregate", 
                data = json.dumps(pipeline, cls=CustomJSONEncoder), 
                headers=hearders, 
                verify=verify_https
            )
            if res.status_code != 200: 
                raise Exception(f"Error getting execution planning {res.status_code} {res.content}")
            

            content = res.json(cls=CustomJsonDecoder)
            if not content["success"]: raise Exception(content["errorMessage"])
            
            total_query     = content["data"]["total"]
            page_size       = content["data"]["size"]

            total_batchs    = (total_query // page_size) + 1
            logger.info(f"Total documents to download {total_query}.")
            logger.info(f"Batch 1/{total_batchs}")

            downloaded_docs = 0
            page            = 1
            total_batchs    = (total_query // page_size) + 1
            docs            = []
            while downloaded_docs < total_query:
                res = requests.post(A2G_QUERY_MANAGER + "/QueryData/Aggregate", 
                    data=json.dumps(pipeline, cls=CustomJSONEncoder),
                    headers=hearders, 
                    verify=verify_https
                )

                if res.status_code != 200: raise Exception(f"Error getting inputstream data {res.status_code} {res.content}")
                content = res.json(cls=CustomJsonDecoder)
                if not content["success"]: raise Exception(content["errorMessage"])
                logger.info(f"Batch {page}/{total_batchs}")
                downloaded_docs += content["data"]["size"]
                docs += content["data"]["data"]
                page += 1
                
            logger.info(f"Data downloaded, total docs: {total_query}")    
            return docs#content["data"]
        except Exception as e:
            raise e


    def insert(self, ikey:str, data:list[dict], mode:INSERTION_MODE, wait_response:bool) -> tuple[int, str]:
        try:
            headers = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey
            }

            if mode == INSERTION_MODE.REPLACE: 
                headers["Replace"] = "true"
                headers["Transaction"] = "false"

            elif mode == INSERTION_MODE.INSERT_UNORDERED: 
                headers["Replace"] = "false"
                headers["Transaction"] = "false"

            elif mode == INSERTION_MODE.TRANSACTION:
                headers["Replace"] = "false"
                headers["Transaction"] = "true"

            if wait_response: headers["WaitResponse"] = "true"

            res = requests.post(A2G_DATA_URL + "/Data/Insert", headers=headers, json=data, verify=verify_https)
            if res.status_code != 200: raise Exception(f"Error to insert data in inputstream {res.status_code} {res.text}")
            return res.status_code, res.text
        except Exception as e:
            raise e


    def remove_documents(self, ikey:str, query:dict) -> int:
        try:
            logger.info("Removing data from A2G...")
            hearders = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey,
                'Content-Type': 'application/json'
            }

            if len(query) == 0: 
                raise Exception("Query is empty, please provide a valid query, if you desire to delete all documents, use the delete_all method.")

            response = requests.post(A2G_QUERY_MANAGER + "/QueryData/RemoveDocuments", 
                data=json.dumps(query, cls=CustomJSONEncoder), 
                headers=hearders, 
                verify=verify_https
            )
            if response.status_code != 200: 
                raise Exception(f"Error to remove data in inputstream {response.status_code} {response.content}")
            res_object = response.json(cls=CustomJsonDecoder)
            if not res_object["success"]: raise Exception(res_object["errorMessage"])

            content = res_object["data"]
            deleted_docs = content["docs_affected"]
            logger.info(f"Operation complete, total docs deleted: {deleted_docs}")

            return deleted_docs
        except Exception as e:
            raise e


    def clear_inputstream(self, ikey:str) -> int:
        try:
            logger.info("Removing all data from A2G...")
            hearders = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey
            }

            response = requests.post(A2G_DATA_URL + f"/QueryData/Clear", headers=hearders, verify=verify_https)
            if response.status_code != 200:
                raise Exception(f"Error to remove all data in inputstream {response.status_code} {response.content}")
            res_object = response.json(cls=CustomJsonDecoder)
            if not res_object["success"]: raise Exception(res_object["errorMessage"])
            
            content = res_object["data"]
            deleted_docs = content["docs_affected"]
            logger.info(f"Operation complete, total docs deleted: {deleted_docs}")
            return deleted_docs
        except Exception as e:
            raise e



class LocalInputstream:

    def __init__(self, token:str, cache_options:dict = None):
        """
        Constructor for LocalInputstream
        :param token: Token to authenticate with A2G
        :param cache_options: { duration_data: int, duration_inputstream: int } | None
        """        
        self.a2g_client = A2GHttpClient(token) 
        self.cache_manager = CacheManager(cache_options)


    def __get_inputstream(self, ikey:str) -> Inputstream:
        inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
        return inputstream
    

    def __get_data(self, ikey:str, query, mode:str, cache:bool, delete_id:bool=True) -> list[dict]:
        _ = self.__get_inputstream(ikey)
        query_str = json.dumps(query, cls=CustomJSONEncoder)
        query_hash = hashlib.sha256(query_str.encode()).hexdigest()
        data = self.cache_manager.get_data(ikey, query_hash) if cache else None
        if data is None:
            if   mode == "find"     :   data = self.a2g_client.find(ikey, query, delete_id)
            elif mode == "find_one" :   data = self.a2g_client.find_one(ikey, query)
            elif mode == "aggregate":   data = self.a2g_client.aggregate(ikey, query)
            logger.info(f"Caching data ... ikey: {ikey}, query: {query_str}")
            self.cache_manager.set_data(ikey, query_hash, data)
            logger.info(f"Data - Ikey: {ikey}, Data cached")
        return data


    def get_inputstream_schema(self, ikey:str) -> dict:
        """
        return Inputstream schema
        params:
            ikey: str
            cache: bool = True -> if True, use cache if exists and is not expired
        """
        inputstream = self.__get_inputstream(ikey)
        return json.loads(inputstream.Schema)


    def find(self, ikey:str, query:dict, cache:bool=True,delete_id:bool=True):
        """
        return data from inputstream
        params:
            ikey: str
            query: dict
            cache: bool = True -> if True, use cache if exists and is not expired
        """
        mode = "find"
        return self.__get_data(ikey, query, mode, cache,delete_id)


    def find_one(self, ikey:str, query:dict, cache:bool=True):
        """
        return one data from inputstream
        params:
            collection: str
            query: dict
        """
        mode = "find_one"
        return self.__get_data(ikey, query, mode, cache)   
     

    def get_data_aggregate(self, ikey:str, query: list[dict], cache:bool=True):
        """
        return data from inputstream
        params:
            ikey: str
            query: list[dict]
        """
        mode = "aggregate"
        return self.__get_data(ikey, query, mode, cache)  
    

    def insert_data(self, ikey:str, data:list[dict], mode:INSERTION_MODE = INSERTION_MODE.REPLACE, wait_response = True, batch_size:int=1000, cache:bool=True):
        """
        validate data against inputstream JsonSchema and insert into inputstream collection
        params:
            ikey: str
            data: list[dict]
            mode: INSERTION_MODE = INSERTION_MODE.REPLACE -> insertion mode
            wait_response: bool = True -> if True, wait for response from server
            batch_size: int = 1000 -> batch size for insert data
            cache: bool = True -> if True, use cache if exists and is not expired
        """
        inputstream:Inputstream = self.__get_inputstream(ikey)
        if type(data) is not list: raise Exception("Data must be a list of dictionaries")
        data_parsed = json.loads(json.dumps(data, cls=CustomJSONEncoder)) 
        if inputstream.Status == InputstreamStatus.Undiscovered: #raise Exception("Inputstream undiscovered")
            #logger.info("")
            logger.warning("Inputstream undiscovered, you must dicovered the schema first")
            return False
        elif inputstream.Status == InputstreamStatus.Exposed: #raise Exception("Inputstream undiscovered")
            logger.warning("Inputstream discovered")

            schema = json.loads(inputstream.Schema)
            schema_validator = Draft4Validator(schema=schema)

            # validate data against schema
            i = 0
            for d in data_parsed: 
                try:
                    schema_validator.validate(d)
                    i += 1
                except Exception as e:
                    logger.error(f"Error validating data: {e}")
                    raise e
        # if inputstream.Status == InputstreamStatus.Undiscovered: #raise Exception("Inputstream undiscovered")
        #     logger.warning("Inputstream undiscovered")
        # insert data into inputstream collection in batch size of 1000
        # TODO: Optimizar para asyncio
        for i in range(0, len(data_parsed), batch_size):
            code, message = self.a2g_client.insert(ikey, data_parsed[i:i+batch_size], mode, wait_response)
            batch_size_aux = batch_size if i+batch_size < len(data_parsed) else len(data_parsed) - i
            logger.info(f"batch {(i//batch_size) + 1}, docs: [{i} - {i+batch_size_aux}] - {code} - {message}")

            

    def remove_documents(self, ikey:str, query:dict) -> int:
        """
        delete data from inputstream
        params:
            ikey: str
            query: dict
        """
        docs = self.a2g_client.remove_documents(ikey, query)
        return docs

    
    def clear_inputstream(self, ikey:str) -> int:
        """
        delete all data from inputstream
        params:
            ikey: str
        """
        docs = self.a2g_client.clear_inputstream(ikey)
        return docs
