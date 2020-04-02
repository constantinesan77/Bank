import random
import psycopg2
import db


try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "P@ssw0rd",
        host = "127.0.0.1",
        database = "bank")
    
    print("Data base connected successfully")
except(Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)



class users:
    first_name = ''
    last_name = ''
    balance = 0

    def account_creation(self):
        self.first_name = input("Enter your name: ")
        self.last_name = input("Enter your last name: ")
        while True:
            self.pesel = input("Enter your pesel:  ")
            if len(self.pesel) == 11 and self.pesel.isdigit()==True:
                break
            else:
                print ("pesel should have 11 digits or be without letters")
        self.balance = input("How much money you wanna deposit: ")
        self.account_number = self.number_random_account()
        self.card_number = self.number_random_card()
        self.pin_code = self.number_random_pincode()

        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY   NOT NULL ,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        pesel BIGINT,
        balance REAL,
        account_number NUMERIC,
        card_number BIGINT,
        pin_code INT
        );''')

        cursor.close()
        c = connection.cursor()
        c.execute('''INSERT INTO users(first_name,last_name,pesel,balance,account_number,card_number,pin_code) VALUES (%s,%s,%s,%s,%s,%s,%s)''',(self.first_name,self.last_name,self.pesel,self.balance,self.account_number,self.card_number,self.pin_code))
        connection.commit()
        count = c.rowcount
        print (count, "Record inserted successfully into mobile table")
        c.close()
        connection.close()
        
    
    
    def number_random_account(self):
        num = '0123456789'
        ls = list (num)
        random.shuffle(ls)
        unique_number = ''.join([random.choice(ls) for x in range(24)]) 
        return unique_number


    
    def number_random_card(self):
        num = '0123456789'
        ls = list (num)
        random.shuffle(ls)
        unique_number_2 = ''.join([random.choice(ls) for y in range(12)])
        return unique_number_2


    
    def number_random_pincode(self):
        num = '0123456789'
        ls = list (num)
        random.shuffle(ls)
        pin_code = ''.join([random.choice(ls) for y in range(4)])
        return pin_code
        

    def balance_acc(self):
        auth = input("enter you pin code: ")
        cursor = connection.cursor()
        cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
        result = cursor.fetchone()[0]
        while (result==True):
            auth = input("enter you pin code: ")
            cursor = connection.cursor()
            cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
            result = cursor.fetchone()[0]
            print(result)
            cursor.close()
            break
        
        else:
            print("incorrect pin code")


    def deposit_money(self):
        auth = input("enter you pin code: ")
        cursor = connection.cursor()
        cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
        result = cursor.fetchone()[0]
        while (result==True):
            print("How much money you wanna deposit?")
            deposit = input()
            balance_b = int(deposit)
            check = connection.cursor()
            check.execute('''SELECT balance FROM users WHERE pin_code = %s;''',(auth,))
            record = check.fetchone()[0]
            balance_a = int(record)
            balance_end = balance_a + balance_b
            cursor_deposit = connection.cursor()
            cursor_deposit.execute(''' UPDATE users SET balance = %s WHERE pin_code = %s;''',(balance_end,auth,))
            cursor_deposit.close()
            check.close()
            connection.commit()
            connection.close()
            print('Your balance is {}'.format(balance_end))
            break
        else:
            print('Incorrect pin')
            connection.close()
        return True
    
    def withdraw_money(self):
        auth = input("enter you pin code: ")
        cursor = connection.cursor()
        cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
        result = cursor.fetchone()[0]
        while (result==True):
            print("How much money you wanna withdraw?")
            deposit = input()
            balance_b = int(deposit)
            check = connection.cursor()
            check.execute('''SELECT balance FROM users WHERE pin_code = %s;''',(auth,))
            record = check.fetchone()[0]
            balance_a = int(record)
            balance_end = balance_a - balance_b
            cursor_deposit = connection.cursor()
            cursor_deposit.execute(''' UPDATE users SET balance = %s WHERE pin_code = %s;''',(balance_end,auth,))
            cursor_deposit.close()
            check.close()
            connection.commit()
            print('Your balance is {}'.format(balance_end))
            break
        else:
            print('Incorrect pin')
            connection.close()
        
    def deleteAccount(self):
        auth = input("enter you pin code: ")
        cursor = connection.cursor()
        cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
        result = cursor.fetchone()[0]
        if result==True:
            delete_cursor = connection.cursor()
            delete_cursor.execute('''DELETE * FROM users WHERE pin_code = %s ;''' , (auth,))
            print("your data has been successfully deleted ")
        else:
            print("incorrect pin code")
    

    def modification_account(self):
        auth = input("enter you pin code: ")
        cursor = connection.cursor()
        cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(auth,))
        result = cursor.fetchone()[0]
        if result==True:
            name = input("write down your new name: ")
            name_cursor = connection.cursor()
            name_cursor.execute ('''UPDATE users SET first_name = %s WHERE pin_code = %s;''',(name,auth,))
            name_cursor.close()
            surname = input("write down your new surname: ")
            surname_cursor = connection.cursor()
            surname_cursor.execute('''UPDATE users SET last_name = %s WHERE pin_code = %s;''',(surname,auth,))
            connection.commit()
            surname_cursor.close()

            print("your data has been updated")
        else:
            print("incorrect pin code")

    
    def auth_account(self):
        lastname = input("enter your last name: ")
        cursor_name = connection.cursor()
        cursor_name.execute('''SELECT EXISTS(SELECT last_name FROM users WHERE last_name = %s); ''' ,(lastname,))
        check_name = cursor_name.fetchone()[0]
        while (check_name == True):
            print("enter your pin")
            pin = input ("enter your pin: ")
            cursor = connection.cursor()
            cursor.execute('''SELECT EXISTS(SELECT pin_code FROM users WHERE pin_code = %s);''' ,(pin,))
            check = cursor.fetchone()[0]
            while (check == True):
                print("correct")
                print("authentication is completed")
                cursor.close()
                cursor_name.close()
                connection.close()
                break
            
            else:
                print("incorrect")
            break
        else:
            print("incorrect")
    

        
    


def writeAccount():
    account = users()
    account.account_creation()

def Enter_to_account():
    account = users()
    account.auth_account()
def deposit_account():
    account = users()
    account.deposit_money()
def withdraw_account():
    account = users()
    account.withdraw_money()
def balance_account():
    account = users()
    account.balance_acc()
def delete_account():
    account = users()
    account.deleteAccount()
def modify_account():
    account = users()
    account.modification_account()



def intro():
    print("\t\t\t\t**********************")
    print("\t\t\t\tBANK MANAGEMENT SYSTEM")
    print("\t\t\t\t**********************")

ch=''
num=0
intro()

while ch != 7:
    #system("cls");
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT AMOUNT")
    print("\t3. WITHDRAW AMOUNT")
    print("\t4. BALANCE ENQUIRY")
    print("\t5. CLOSE AN ACCOUNT")
    print("\t6. MODIFY AN ACCOUNT")
    print("\t7. EXIT")
    print("\tSelect Your Option (1-7) ")
    ch = input()
    #system("cls");
    
    if ch == '1':
        writeAccount()
    elif ch =='2':
        deposit_account()
    elif ch == '3':
        withdraw_account()
    elif ch == '4':
        balance_account()
    elif ch == '5':
        delete_account()
    elif ch == '6':
        modify_account()
    elif ch == '7':
        print("\tThanks for using bank managemnt system")
        break
    else :
        print("Invalid choice")
    
    ch = input("Enter your choice : ")



        




        

