import datetime
from db.connect import Crud

def checkBorrow(userId):
    queryCheckReturn = "SELECT * FROM ticket WHERE member_id = {} AND return_date IS NULL;".format(userId)
    if queryCheckReturn:
        ticket = Crud.fetchOne(queryCheckReturn)
        # compare borrow_date + 30 days with today
        if ticket is not None:
            if ticket[4] + datetime.timedelta(days=30) < datetime.date.today():
                query = "UPDATE member SET can_borrow = FALSE WHERE id = {};".format(userId)
                Crud.mutation(query)
                print("You can't borrow, please check if you have any book that not returned in due time")
            else:
                print("You can borrow")
    else:
        query = "UPDATE member SET can_borrow = TRUE WHERE id = {};".format(userId)
        Crud.mutation(query)