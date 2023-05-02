from models import *

with db:
    db.create_tables([User])

print('DONE')
