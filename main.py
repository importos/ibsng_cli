
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
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory


session = PromptSession(history=FileHistory('.ibsng_history'))

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
        if itm.startswith( "__"):
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
    
def load_module(path):
    if path[-1]is None:
        name = ("modules"+(".".join(path[:-1])))[:-3]
    else:
        name = ("modules"+(".".join(path)))[:-3]

    module = importlib.import_module(name)
    logging.debug(str(module))
    return module
def parse_commands(commnads_text):
    global path

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
    

    logging.debug("Start HHHHHHHHHHHHHHH")
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
    logging.debug("Stop HHHHHHHHHHHHHHH")

    
    logging.debug(str([(lexer)]))
    return lexer

def compile_commands(parsed_commands):
    l1 = get_commands_list()
    logging.debug(str([(l1)]))
    if (len(parsed_commands)>0) and (parsed_commands[0]=="/"):
        parsed_commands.pop(0)
        req_path = [""]
    else:
        req_path = path.copy()
    for itm in req_path:
        if itm in l1:
            l1 = l1[itm]

    req_type= "path"

    cnt =0 
    for itm in parsed_commands:
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
            req_path.append(None)
            logging.error("Bad command")
            break
    for i in range(cnt):
        parsed_commands.pop(0)
    arguments = {}
    if req_type == "command":
        eq = False
        name = None
        for itm in parsed_commands:
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
        return [{"path":req_path,"type":req_type,"start":0,"end":0}]
    elif req_type == "command":
        return [{"path":req_path,"arguments":arguments,"type":req_type,"start":0,"end":0}]


class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        logging.debug(document.cursor_position)
        logging.debug(document.text)
        # print(document.)
        lex = parse_commands(document.text)
        req = compile_commands(lex)

        logging.debug(str(["NNNNN",lex,req]))
        l1 = get_commands_list()
        l2 = l1
        for cmd in req:
            # if (document.cursor_position >=cmd["start"])and( document.cursor_position<=cmd["end"]):
            if 1:
                logging.debug("AAAAAAAAAAA")
                if cmd["type"]=="path":
                    for itm in cmd["path"][1:]:
                        logging.debug(str(["IIIIIIIIIII",itm]))
                        
                        if itm is not None:
                            l2 = l2[itm]
                elif cmd["type"]=="command":
                    module = load_module(cmd["path"])
                    l2 = getattr(module,"arguments")
                    logging.debug(str(["RRRRRRRRRRRR",l2]))
                    l2 = [x[0] for x in l2]
                    # continue
                    # l2 = l2[itm]
        # filter(lambda x:True,l1)
        logging.debug(str(["LLLLLLLLLLLLL",l2]))
        l1 = []
        filter_text = lex[-1] if len(lex)>0 else ""
        for itm in l2:
            if itm.startswith(filter_text):
                if itm.endswith(".py"):
                    l1.append(Completion(itm[:-3],-1*len(filter_text)))
                else:
                    l1.append(Completion(itm,-1*len(filter_text)))
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
    text = session.prompt(message, completer=completer, style=style, color_depth=ColorDepth.TRUE_COLOR,
                  complete_while_typing=True)
    if text == "exit" :
        break
    else:
        l1 = get_commands_list()
        lex = parse_commands(text)
        req = compile_commands(lex)
        for cmd in req:
            if cmd["type"]=="path":
                if cmd["path"][-1] is None:
                    path = cmd["path"][:-1]
                else:
                    path = cmd["path"]
            elif cmd["type"]=="command":
                print(cmd)
                try:
                    module = load_module(cmd["path"])
                    func = getattr(module,"call") 
                    res = func(ibs, cmd["arguments"])
                    print(res)
                except Exception as e:
                    print(e)
                    logging.exception("run command")

            
    print('You said: %s' % text)

