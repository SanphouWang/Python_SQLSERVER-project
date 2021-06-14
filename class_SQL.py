# Name:WXP
# Time:
import pymssql
import adodbapi


class SQL(object):
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host + ':' + self.port, user=self.user, password=self.pwd,database=self.db, charset="GBK")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        if resList != None:
            return resList
        else:
            return "error"

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecProcedure(self, procedure, parameters):
        cur = self.__GetConnect()
        msg = cur.callproc(procedure, parameters)
        self.conn.commit()
        self.conn.close()
        return msg

    # -------------------------------------------------------------------------
    def login(self, account_number, password):
        result = self.ExecQuery('select account_number,password from account')
        if (account_number, password) in result:
            return 1
        elif account_number not in [x[0] for x in result]:
            return 2  # no such account_number
        else:
            return 3  # wrong password

    # 查询account表中account的全部信息
    def select_account(self, account_number):
        result = self.ExecQuery('select * from account where account_number=' + account_number)
        return result[0]

    def Me(self, account_number):
        result = self.ExecQuery(
            'select real_name,age,gender,credit_points,phone_number,pay_password from personal_info where '
            'account_number=' + account_number)
        return result[0]

    def deposit(self, account_number, much):
        parameters = (account_number, float(much))
        x = self.ExecProcedure('deposit', parameters)
        return 1

    def fortune(self, account_number):
        result = self.ExecQuery(
            'select balance,financial_product1,financial_product2,loan_amount from fortune where account_number='
            + account_number)
        return result[0]

    def withdraw(self, much, account_number):
        parameters = (account_number, float(much), pymssql.output(str))
        result = self.ExecProcedure('withdraw', parameters)
        return result[-1]

    def trans(self, account_number, much, To_number):
        flag = 0
        parameters = (account_number, float(much), To_number, pymssql.output(str))
        result = self.ExecProcedure('trans', parameters)
        return result[-1]

    def loan(self, account_number, amount, repay_date):
        credit_points = self.ExecQuery(
            'select credit_points from personal_info  where account_number =' + account_number)
        credit_points = float(credit_points[0][0])
        parameters = (account_number, float(amount), credit_points, repay_date, pymssql.output(str))
        result = self.ExecProcedure('loans', parameters)
        return result[-1]

    def repay(self, account_number, loan_ID):
        balance = self.fortune(account_number)
        balance = float(balance[0])

    def select_loan(self, account_number):
        msg = self.ExecQuery(
            'select loan_ID,amount,loan_date,repay_date from loan where account_number=' + account_number)
        return msg

    def repay(self, account_number, loan_ID):
        balance = self.ExecQuery('select balance from fortune where account_number =' + account_number)
        balance = float(balance[0][0])
        parameters = (loan_ID, balance, account_number, pymssql.output(str))
        result = self.ExecProcedure('repay', parameters)
        return result[-1]

    def select_income_expense(self, account_number):
        result = self.ExecQuery('select * from income_expense where account_number=' + account_number)
        return result

    def Change_profile_image(self, image_b, account_number):
        # parameters = (image_b, account_number)
        # result = self.ExecProcedure('Change_profile_image', parameters)
        cur = self.__GetConnect()
        cur.execute("update account set profile_image='%s'; where account_number= '%s'; " %
                    (adodbapi.Binary(image_b), account_number))
        self.conn.close()
        return 1
