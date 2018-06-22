__all__ = ['write_to_file']
from datetime import datetime
def write_to_file(string:str):

    new_file = open('./log/%s-log.txt'% (datetime.now().date().isoformat()),'a',encoding='utf-8')
    new_file.write(string)
    new_file.close()