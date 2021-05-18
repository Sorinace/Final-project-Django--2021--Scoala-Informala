class MyException(Exception):
    pass

def incomplet():
    raise MyException('Nu ati completat toate raspunsurile!')