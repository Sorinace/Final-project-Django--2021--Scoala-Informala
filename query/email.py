from django.core.mail import send_mail

def emailAssignedTest(email, addres):
  send_mail(
    'Va fost atribuit un test',
    # message
    f"""
    Buna ziua,
        Va rog sa completati testul de la adresa {addres}
        Testul expira in doua saptamani.
    O zi frumoasa,
    Diana Avram 
    """,
    'Diana Avram',
    [email], # 'psiholigia@gmail.com'
    fail_silently=False,
  )