from database import Database

db = Database('crop')

# if(not db.isExist(table_name='users', data=('temp.gmail.com', 'temp.gmail.com'))):
#     db.insert(tableName='users', data=('tim', 'joe', 'temp.gmail.com'))
# db.insert(tableName='users', data=('tim1', 'joe1'))
# db.insert(tableName='users', data=('tim2', 'joe2'))

# db.insert(tableName='contact', data=('udbhav', 'udbhav@gmail.com', '', 'Nice website'))

# print(db.validate(table_name='users', data=('temp.gmail.com', 'temp.gmail.com', 'joe')))

# db.display(table_name='users')
db.display(table_name='contact')
# db.getId(tableName='users', value='luckyudbhav@gmail.com')
db.insert(tableName='orders', data=('pineapple', 1, 10, 1, 'udbhav', 'vizag', 123456789, 123))
db.display(table_name='orders')