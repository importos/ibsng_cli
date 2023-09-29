from typing import Any
from urllib import request, parse
import json
import logging
class IBSngMethod():
    def __init__(self, plugin, method_name):
        self._plugin = plugin
        self._method_name = method_name
        pass
    def __call__(self, **kwds) :
        logging.debug("call method by arguments %s %s %s",self._plugin.get_name(),self._method_name, kwds)
        # request_data = {

        # }
        # data = parse.urlencode(request_data).encode()
        data = {
            "params": kwds,
            "method":"%s.%s"%(self._plugin.get_name(),self._method_name),
        }
        session_id = self._plugin.get_session_id()
        if session_id != None:
            data["params"]["auth_session"]=session_id
        addr = self._plugin.get_post_url()
        logging.debug(addr)
        req = request.Request( addr, data=json.dumps(data).encode("latin-1"))
        resp = request.urlopen(req)
        logging.debug(resp)
        logging.debug(resp.code)
        data = resp.read()
        logging.debug(data)
        obj = json.loads(data)
        logging.debug(obj)
        if obj["error"] != None:
            logging.error(obj["error"])
            # raise Exception(obj["error"])
        return obj["result"],obj
class IBSngPlugin():
    def __init__(self,  ibsng, plugin_name):
        self._ibsng = ibsng
        self._plugin_name = plugin_name
    def get_name(self):
        return self._plugin_name
    def get_post_url(self):
        return self._ibsng.get_post_url()
    def get_session_id(self):
        return self._ibsng.get_session_id()
    def __getattr__ (self, __name: str) -> Any:
        return IBSngMethod(self,__name)
class IBSng():
    def __init__(self):
        self._session = None
        self.__ibs_address = None
        pass
    def get_post_url(self):
        return "http://%s/"%self.__ibs_address
    def set_address(self,ibs_address):
        self.__ibs_address = ibs_address
    def set_session(self,session_id):
        self._session = session_id
    def get_session_id(self):
        return self._session
    def __getattr__ (self, __name: str) -> Any:
        return IBSngPlugin(self,__name)
    # def __getattribute__(self, __name: str) -> Any:
    #     # return 'A'
    #     return IBSngPlugin(self,__name)
# data = parse.urlencode(<your data dict>).encode()
# req = request.Request(<your url>, data=data) # this will make the method "POST"
# resp = request.urlopen(req)