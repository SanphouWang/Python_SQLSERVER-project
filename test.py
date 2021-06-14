# Name:WXP
# Time:
import tkinter as tk
from class_SQL import *
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
import adodbapi

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来显示正常中文标签
plt.rcParams['axes.unicode_minus'] = False
# 创建主窗口
window = tk.Tk()
window.title('欢迎使用银行系统')
window.geometry('400x350')
tk.Label(window, text='Account_number:').place(x=70, y=100)  # 创建两个标签
tk.Label(window, text='Password:').place(x=70, y=140)
# 创建ID和pwd输入栏
entry_account_number = tk.Entry(window)
entry_account_number.place(x=180, y=100)
entry_var_usr_pwd = tk.Entry(window, show='*')
entry_var_usr_pwd.place(x=180, y=140)
# 创建两个IP的输入栏
tk.Label(window, text='Database_IP:').place(x=70, y=180)
entry_IP1 = tk.Entry(window)
entry_IP1.place(x=180, y=180)
btn_login = tk.Button(window, text='Login',
                      command=lambda: login(entry_account_number.get(), entry_var_usr_pwd.get(),
                                            entry_IP1.get())).place(x=170, y=230)
port = '1433'
user = 'BANK'
pwd = '123456'
db = 'Bankdbs'


def login(account_number, password, IP):
    global sql
    sql = SQL(IP, port, user, pwd, db)
    flag = sql.login(account_number, password)
    if flag == 1:
        open_op_interface(account_number)
    elif flag == 2:
        messagebox.showinfo(title='错误', message='no such account_number')
    else:
        messagebox.showinfo(title='错误', message='wrong password')


image_jerry = tk.PhotoImage(file='jerry1.gif')


def open_op_interface(account_number):
    window_login = tk.Toplevel(window)
    window_login.geometry('500x350')
    window_login.title('操作界面')
    tk.Label(window_login, text='account_number:').place(x=120, y=150)  # 创建三个标签
    tk.Label(window_login, text='Name:').place(x=280, y=150)
    account_info = sql.select_account(account_number)
    tk.Label(window_login, text=account_info[0]).place(x=230, y=150)
    tk.Label(window_login, text=account_info[3]).place(x=330, y=150)
    # 各种按钮
    tk.Button(window_login, text='Me', command=lambda: Me_interface(account_number)).place(x=80, y=200)
    tk.Button(window_login, text='Business', command=lambda: Business_interface(account_number)).place(x=140, y=200)
    tk.Button(window_login, text='Fortune', command=lambda: fortune_interface(account_number)).place(x=230, y=200)
    tk.Button(window_login, text='income_expenses', command=lambda: income_expense(account_number)).place(x=320, y=200)


def fortune_interface(account_number):
    window_fortune = tk.Toplevel(window)
    window_fortune.geometry('350x250')
    window_fortune.title('Fortune')
    result = sql.fortune(account_number)
    tk.Label(window_fortune, text='Balance:').place(x=90, y=50)
    tk.Label(window_fortune, text=result[0]).place(x=220, y=50)
    tk.Label(window_fortune, text='Financial product1:').place(x=90, y=80)
    tk.Label(window_fortune, text=result[1]).place(x=220, y=80)
    tk.Label(window_fortune, text='Financial product2:').place(x=90, y=110)
    tk.Label(window_fortune, text=result[2]).place(x=220, y=110)
    tk.Label(window_fortune, text='Loan amount:').place(x=90, y=140)
    tk.Label(window_fortune, text=result[3]).place(x=220, y=140)


def Me_interface(account_number):
    personal_info = sql.Me(account_number)
    window_Me = tk.Toplevel()
    window_Me.title('Me')
    window_Me.geometry('400x420')
    # 加载头像
    canvas = tk.Canvas(window_Me, width=150, height=150)
    canvas.create_image(0, 10, anchor='nw', image=image_jerry)
    canvas.pack(side='top')
    # tk.Button(window_Me, text='Change image', command=lambda: Change_image(account_number)).place(x=150, y=160)
    tk.Label(window_Me, text='Real Name').place(x=110, y=200)
    tk.Label(window_Me, text=personal_info[0]).place(x=220, y=200)
    tk.Label(window_Me, text='Age').place(x=110, y=230)
    tk.Label(window_Me, text=personal_info[1]).place(x=220, y=230)
    tk.Label(window_Me, text='Gender').place(x=110, y=260)
    tk.Label(window_Me, text=personal_info[2]).place(x=220, y=260)
    tk.Label(window_Me, text='Credit Points').place(x=110, y=290)
    tk.Label(window_Me, text=personal_info[3]).place(x=220, y=290)
    tk.Label(window_Me, text='Phone number').place(x=110, y=320)
    tk.Label(window_Me, text=personal_info[4]).place(x=220, y=320)
    tk.Label(window_Me, text='Pay password').place(x=110, y=350)
    tk.Label(window_Me, text=personal_info[5]).place(x=220, y=350)


def Business_interface(account_number):
    window_Business = tk.Toplevel()
    window_Business.geometry('250x300')
    window_Business.title('业务')
    tk.Button(window_Business, text='withdraw', command=lambda: withdraw(account_number)).place(x=100, y=20)
    tk.Button(window_Business, text='deposit', command=lambda: deposit(account_number)).place(x=100, y=70)
    tk.Button(window_Business, text='trans', command=lambda: trans(account_number)).place(x=100, y=120)
    tk.Button(window_Business, text='Loan', command=lambda: loan(account_number)).place(x=100, y=170)
    tk.Button(window_Business, text='repay', command=lambda: repay(account_number)).place(x=100, y=220)

def Change_image(account_number):
    default_dir = r"C:\学习资料\数据库\数据库大作业"
    file_path = tk.filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    with open(file_path, "rb") as f:
        img_bin = f.read()  # 内容读取
        print(img_bin)
        sql.Change_profile_image(img_bin,account_number)
        print('success')


def withdraw(account_number):
    window_withdraw = tk.Toplevel()
    window_withdraw.geometry('250x180')
    window_withdraw.title('取款')

    def process(much, account_number):
        result = sql.withdraw(much, account_number)
        if result == '1':
            messagebox.showinfo(title='success', message='successfully withdraw')
        else:
            # window_withdraw.destroy()
            messagebox.showinfo(title='error', message='balance is not enough')

    tk.Label(window_withdraw, text='金额').place(x=30, y=40)
    entry_much = tk.Entry(window_withdraw)
    entry_much.place(x=70, y=40)
    tk.Button(window_withdraw, text='withdraw', command=lambda: process(entry_much.get(), account_number)).place(x=90,
                                                                                                                 y=100)


def deposit(account_number):
    window_deposit = tk.Toplevel()
    window_deposit.geometry('250x180')
    window_deposit.title('存款')

    def process(account_number, much):
        if sql.deposit(account_number, much):
            messagebox.showinfo(title='success', message='successfully deposit')

    tk.Label(window_deposit, text='金额').place(x=30, y=40)
    entry_much = tk.Entry(window_deposit)
    entry_much.place(x=70, y=40)
    tk.Button(window_deposit, text='deposit', command=lambda: process(account_number, entry_much.get())).place(x=90,
                                                                                                               y=100)


def trans(account_number):
    window_trans = tk.Toplevel()
    window_trans.geometry('250x180')
    window_trans.title('转账')
    tk.Label(window_trans, text='金额').place(x=20, y=40)
    entry_much = tk.Entry(window_trans)
    entry_much.place(x=80, y=40)
    tk.Label(window_trans, text='转入账户').place(x=20, y=80)
    entry_To_number = tk.Entry(window_trans)
    entry_To_number.place(x=80, y=80)

    def process(account_number, much, To_number):
        msg = sql.trans(account_number, much, To_number)
        if msg == '1':
            messagebox.showinfo(title='success', message='Successfully trans')
        elif msg == '2':
            messagebox.showinfo(title='error', message='No such To_number')
        else:
            messagebox.showinfo(title='error', message='Balance is not enough')

    tk.Button(window_trans, text='Trans',
              command=lambda: process(account_number, entry_much.get(), entry_To_number.get())).place(x=90, y=120)


def loan(account_number):
    window_loan = tk.Toplevel()
    window_loan.geometry('250x250')
    window_loan.title('贷款')
    tk.Label(window_loan, text='金额').place(x=20, y=40)
    entry_much = tk.Entry(window_loan)
    entry_much.place(x=80, y=40)
    tk.Label(window_loan, text='还款日期').place(x=20, y=80)
    entry_repay_date = tk.Entry(window_loan)
    entry_repay_date.place(x=80, y=80)

    def process(account_number, amount, repay_date):
        msg = sql.loan(account_number, amount, repay_date)
        if msg == '1':
            messagebox.showinfo(title='error', message='credit points too low')
        elif msg == '2':
            messagebox.showinfo(title='success', message='successfully loan')

    tk.Button(window_loan, text='Loan',
              command=lambda: process(account_number, entry_much.get(), entry_repay_date.get())).place(x=90, y=120)


def repay(account_number):
    loan_msg = sql.select_loan(account_number)
    window_repay = tk.Toplevel()
    window_repay.geometry('500x200')
    window_repay.title('还款')
    sb = tk.Scrollbar(window_repay)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    top = 'loan_ID    amount      loan_data     repay_date'
    lb = tk.Listbox(window_repay, yscrollcommand=sb.set, width=40)
    lb.insert(tk.END, top)
    for i in loan_msg:
        msg = f'{i[0]}        {i[1]}        {i[2]}     {i[3]}'
        lb.insert(tk.END, msg)

    def process(account_number, loan_ID):
        message = sql.repay(account_number, loan_ID)
        if message == '1':
            window_repay.destroy()
            messagebox.showinfo(title='success', message='successfully repay')

        else:
            messagebox.showinfo(title='error', message='balance is not enough')

    tk.Label(window_repay, text='Loan_ID:').place(x=60, y=30)
    entry_Loan_ID = tk.Entry(window_repay)
    entry_Loan_ID.place(x=20, y=60)
    tk.Button(window_repay, text='Repay', command=lambda: process(account_number, entry_Loan_ID.get())).place(x=60,
                                                                                                              y=110)
    lb.pack(side=tk.RIGHT, fill=tk.BOTH)
    sb.config(command=lb.yview)


def income_expense(account_number):
    window_income_expense = tk.Toplevel()
    window_income_expense.geometry('500x200')
    window_income_expense.title('收支记录')
    sb = tk.Scrollbar(window_income_expense)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    lb = tk.Listbox(window_income_expense, yscrollcommand=sb.set, width=50)
    msg = sql.select_income_expense(account_number)
    top = 'flow_ID  inc_or_exp     amount     date             type'
    lb.insert(tk.END, top)
    for i in msg:
        strings = f'{i[1]}    {i[2]}             {i[4]}        {i[5]}       {i[3]}'
        lb.insert(tk.END, strings)
    lb.pack(side=tk.RIGHT, fill=tk.BOTH)
    sb.config(command=lb.yview)

    # 可视化
    def To_visual():
        income_data = {
            'type': [i[3] for i in msg if i[2] == 'inc'],
            'amount': [float(i[4]) for i in msg if i[2] == 'inc']
        }
        expense_data = {
            'type': [i[3] for i in msg if i[2] == 'exp'],
            'amount': [float(i[4]) for i in msg if i[2] == 'exp']
        }
        income_dataframe = pd.DataFrame(income_data, columns=['type', 'amount'])
        expense_dataframe = pd.DataFrame(expense_data, columns=['type', 'amount'])
        income = income_dataframe['amount'].groupby(income_dataframe['type']).sum()
        expense = expense_dataframe['amount'].groupby(expense_dataframe['type']).sum()
        explode = (0.05,) * len(income)
        # 绘制收入饼状图
        plt.subplot(121)
        plt.pie(income.values, labels=income.index, explode=explode, startangle=60, autopct='%1.1f%%')
        plt.title('收入数据饼状图')
        explode = (0.05,) * len(expense)
        # 绘制支出饼状图
        plt.subplot(122)
        plt.pie(expense.values, labels=expense.index, explode=explode, startangle=60, autopct='%1.1f%%')
        plt.title('支出数据饼状图')
        plt.show()

    tk.Button(window_income_expense, text='可视化', command=lambda: To_visual()).place(x=40, y=80)


window.mainloop()  # 主窗口循环
