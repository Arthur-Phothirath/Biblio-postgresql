from db.connect import Crud

def blockBorrow(userId):
    query = "SELECT can_borrow, ban FROM member WHERE id = {};".format(userId)
    print(Crud.fetchOne(query))
    if Crud.fetchOne(query)[0] == False:
        return True
    if Crud.fetchOne(query)[1] == True:
        return True
    