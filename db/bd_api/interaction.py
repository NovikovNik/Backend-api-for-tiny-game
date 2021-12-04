from db.bd_api.exceptions import UserNotFoundException
from db.models.models import Base, User, Hero
from db.client.client import MySQLConnection

class DbInteraction:
    
        def  __init__(self, host, user, password, db_name, rebuild_db):
            self.mysql_connection = MySQLConnection(
                host=host,
                password=password,
                db_name=db_name,
                rebuild_db=rebuild_db,
                user=user
            )
            
            self.engine = self.mysql_connection.connection.engine
            
            if rebuild_db:
                self.create_table_users()
                self.create_table_heroes()
            
        def create_table_users(self):
            if not self.engine.has_table(self.engine, 'users'):
                table_object = [User.__table__]
                Base.metadata.create_all(self.engine, tables=table_object)
            else:
                self.mysql_connection.execute_query('DROP TABLE IF EXISTS users')
                Base.metadata.tables('users').create(self.engine)
                
        def create_table_heroes(self):
            if not self.engine.has_table(self.engine, 'heroes'):
                table_object = [Hero.__table__]
                Base.metadata.create_all(self.engine, tables=table_object)
            else:
                self.mysql_connection.execute_query('DROP TABLE IF EXISTS heroes')
                Base.metadata.tables('heroes').create(self.engine)
                
        def add_user_info(self, username, password, email):
            user = User(
                username = username,
                password = password,
                email = email
            )
            
            self.mysql_connection.session.add(user)
            return self.get_user_info(username)
        
        def get_user_info(self, username):
            user = self.mysql_connection.session.query(User).filter_by(username=username).first()
            if user:
                self.mysql_connection.session.expire_all()
                return {'username': user.username, 'email': user.email, 'password': user.password}
            else:
                raise UserNotFoundException()

        def edit_user_info(self,username, new_username=None, new_email=None, new_password=None):
            user = self.mysql_connection.session.query(User).filter_by(username=username).first()
            if user:
                if new_username is not None:
                    user.username = new_username
                if new_email is not None:
                    user.email = new_email
                if new_password is not None:
                    user.password = new_password
                return self.get_user_info(username)
            else:
                raise UserNotFoundException
                
if __name__ == '__main__':
    db = DbInteraction(
        host = 'niknovikov.ru',
        user='u1528046_nik',
        password='Criterian21',
        db_name='u1528046_test_bd',
        rebuild_db=True
    )

    db.add_user_info('test','test','test@email')