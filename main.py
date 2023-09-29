
import libs
import logging
# import bashlex
import shlex
import importlib
logging.basicConfig(level=logging.DEBUG,filename="temp.log",filemode="w")
ibs = libs.IBSng()
ibs.set_address("127.0.0.1:1237")
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.output import ColorDepth

style = Style.from_dict({
    # User input (default text).
    '':          '#ff0066',

    # Prompt.
    'username': '#884444',
    'at':       '#00aa00',
    'colon':    '#0000aa',
    'pound':    '#00aa00',
    'host':     '#00ffff bg:#444400',
    'path':     'ansicyan underline',
})

message = [
    ('class:username', 'anonymous'),
    ('class:at',       '@'),
    ('class:host',     'localhost'),
    ('class:colon',    ':'),
    ('class:path',     '/'),
    ('class:pound',    '# '),
]




from prompt_toolkit import prompt
from prompt_toolkit.completion import Completion, Completer

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
import os
module_path = os.path.join (os.path.abspath(os.path.dirname(__file__)),"modules")

path = ['']
username = "anonymous"
address = "localhost"
def get_commands_list(path = path):
    o1 = {}
    l1 = os.listdir(module_path)
    for itm in l1:
        if itm == "__init__.py":
            continue
        o2 = {}
        if os.path.isdir(os.path.join(module_path,itm)):
            if os.path.isfile(os.path.join(module_path,itm,"__init__.py")):
                l2 = os.listdir(os.path.join(module_path,itm))
                for itm1 in l2:
                    if itm1 == "__init__.py":
                        continue
                    if itm1.endswith(".py"):
                        o2[itm1]={}
                pass
        o1[itm] = o2
    return o1
class dots:
    def __init__(self,number) -> None:
        self.number = number
        pass
    def __str__(self) -> str:
        return "dots %d"%self.number
    def __repr__(self) -> str:
        return "dots %d"%self.number
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value,dots):
            return self.number == __value.number
        return False
def parse_commands(commnads_text):
    global path
    l1 = get_commands_list()

    lexer = []
    if commnads_text:
        logging.debug("for parse")
        try:
            lexer = list(shlex.shlex(commnads_text, posix= True))
            logging.debug(str([(lexer)]))
        except:
            logging.exception("eeee")
    # if commnads_text:
    #     parts =  bashlex.parse(commnads_text)
    #     for itm in parts:
    #         logging.debug(itm)
    
    if (len(lexer)>0) and (lexer[0]=="/"):
        lexer.pop(0)
        req_path = [""]
    else:
        req_path = path.copy()
    
    while True: 
        if "." not in lexer:
            break
        ind1 = lexer.index(".")
        cnt = 0 
        while lexer[ind1]==".":
            cnt+=1
            lexer.pop(ind1)
        lexer.insert(ind1,dots(cnt))
    while dots(2) in lexer:
        ind1 = lexer.index(dots(2))
        lexer.pop(ind1)
        if ind1>0:
            lexer.pop(ind1-1)

    
    logging.debug(str([(lexer)]))
    logging.debug(str([(l1)]))

    for itm in req_path:
        if itm in l1:
            l1 = l1[itm]

    req_type= "path"

    cnt =0 
    for itm in lexer:
        logging.debug(str(["AAAAAAAAAAAAAAAAAA",itm,itm in l1]))
        if itm == "":
            continue
        elif itm in l1:
            logging.debug(str([req_type,itm,l1,l1[itm]]))
            l1 = l1[itm]
            req_path.append(itm)
            cnt +=1
        elif itm+".py" in l1:
            req_type = "command"
            logging.debug(str([req_type,itm,l1[itm+".py"]]))
            req_path.append(itm+".py")
            cnt +=1
        else:
            logging.error("Bad command")
            break
    for i in range(cnt):
        lexer.pop(0)
    arguments = {}
    if req_type == "command":
        eq = False
        name = None
        for itm in lexer:
            logging.debug(str(["fff",itm]))
            if eq :
                if name is not None:
                    arguments[name]= itm
                    name = None
                    eq = False
                else:
                    logging.error("Bad syntax")
            else:

                if itm == "=":
                    eq = True
                else:
                    if name is None:
                        name = itm
                    else:
                        arguments[name]=None
                        name = itm
        if name is not None:
            arguments[name]=None



    if len(req_path)>1 and req_path[0]!="":
        req_path.insert(0,"")
    if req_type == "path":
        return [{"path":req_path,"type":req_type,"start":0,"end":len(commnads_text)}]
    elif req_type == "command":
        return [{"path":req_path,"arguments":arguments,"type":req_type,"start":0,"end":len(commnads_text)}]

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        return []
        logging.debug(document.cursor_position)
        logging.debug(document.text)
        # print(document.)
        req = parse_commands(document.text)
        l1 = get_commands_list()
        l2 = l1
        for cmd in req:
            if (document.cursor_position >=cmd["start"])and( document.cursor_position<=cmd["end"]):
                logging.debug("AAAAAAAAAAA")
                # for itm in cmd["path"]:
                    # continue
                    # l2 = l2[itm]
        # filter(lambda x:True,l1)
        l1 = [Completion(x) for x in l2]
        return iter(l1)
completer = MyCompleter()
# completer = None
text = FormattedText([
    ('#ff0066', 'Hello'),
    ('', ' '),
    ('#44ff00 italic', 'World'),
])
print_formatted_text(text, style=style)
while True:
    message[0]=('class:path',     username)
    message[2]=('class:path',     address)
    message[4]=('class:path',     "/".join(path))
    print(path)
    text = prompt(message, completer=completer, style=style, color_depth=ColorDepth.TRUE_COLOR,
                  complete_while_typing=True)
    if text == "exit" :
        break
    else:
        l1 = get_commands_list()
        req = parse_commands(text)
        for cmd in req:
            if cmd["type"]=="path":
                path = cmd["path"]
            elif cmd["type"]=="command":
                print(cmd)
                try:
                    name = ("modules"+(".".join(cmd["path"])))[:-3]
                    module = importlib.import_module(name)
                    print(module)
                    func = getattr(module,"call") 
                    res = func(ibs, cmd["arguments"])
                    print(res)
                except Exception as e:
                    print(e)
                    logging.exception("run command")

            
    print('You said: %s' % text)

