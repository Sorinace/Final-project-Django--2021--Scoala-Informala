class MyException(Exception):
    pass

def notCopleted():
    raise MyException('Nu ati completat toate raspunsurile!')

def notSaved():
    raise MyException('Testul nu a putut fi salvat!')

def sendError(e):
    raise MyException(str(e))
 