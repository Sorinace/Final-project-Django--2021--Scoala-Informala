class MyException(Exception):
    pass

def notCopleted():
    raise MyException('Nu ati completat toate raspunsurile!')

def notValid():
    raise MyException('Testul are date nevalide!')

def notSaved():
    raise MyException('Testul nu a putut fi salvat!')

def toLate():
    raise MyException('Testul nu mai poate fi completat, a expirat!')