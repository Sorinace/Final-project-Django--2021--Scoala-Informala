class MyException(Exception):
    pass

def notCopleted():
    raise MyException('Nu ati completat toate raspunsurile!')

def notValid():
    raise MyException('Testul nu are date valide!')

def notSaved():
    raise MyException('Testul nu a putut fi salvat!')

def toLate():
    raise MyException('Testul nu mai poate fi completat, a expirat!')

def done():
    raise MyException('Acest test a fost deja completat!')

def sendError(e):
    raise MyException(str(e))
 