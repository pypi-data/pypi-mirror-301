# coding:utf-8
from tools_hjh.Tools import locattime, echo


def main():
    log = Log('test.log')
    log.info('a', 'b', 1)


class Log():
    """ 简单的日志类 """

    def __init__(self, filepath):
        self.filepath = filepath

    def info(self, *text):
        print(locattime(), 'info', text)
        echo((locattime(), 'info', text), self.filepath)
        
    def warning(self, *text):
        print(locattime(), 'warning', text)
        echo((locattime(), 'warning', text), self.filepath)
        
    def error(self, *text):
        print(locattime(), 'error', text)
        echo((locattime(), 'error', text), self.filepath)

        
if __name__ == '__main__': 
    main()
