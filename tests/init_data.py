from app import db
from app.models import UserAccount

def init_test_data():
    # PASSWORD: 'nocontabanconmiastucia',
    user1 = UserAccount(
        id=99,
        first_name='Roberto',
        father_surname='Gomez',
        mother_surname='Bolañoz',
        gender='M',
        email='chespirito@example.com',
        birth_date='1929-02-21',
        cellphone='5514632156',
        salt='$6$xCHIfAYEYR2uN2vy',
        hashed_password='pbkdf2:sha256:150000$Pdwux4CrvfEq5tto$b6059e8ee60837d290bf024b72d7cc3cebb105024a05413a6c4ebdc5c6ed0e0d'
    )
    users = (user1,)
    for u in users:
        db.session.add(u)
    db.session.commit()
