import sqlite3

def sql_check (file='data.db'):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE NKUST
            (Account           CHAR(32)    NOT NULL,
            Password            CHAR(16)     NOT NULL,
            Telegram_chatID        INT      NOT NULL);''')
    except:
        pass
    conn.commit()
    conn.close()
    
def sql_execute(execute,value,file='data.db'):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("%s  VALUES (%s)"%(execute,value));
    conn.commit()
    conn.close()
def chatID_check(chatID,file='data.db'):
    conn = sqlite3.connect(file)
    for row in conn.execute("select Telegram_chatID from NKUST where Telegram_chatID='%s'"%chatID):
        return True
    conn.close()
    return False

def getNKUST_Acc(chatID,file='data.db'): 
    # this def is same of chatID_check , I isolate these because I don't belive any BUG XDD 
    conn = sqlite3.connect(file)
    for row in conn.execute("select Account ,Password from NKUST where Telegram_chatID='%s'"%chatID):
        return list(row)
    conn.close()
    return None

if __name__ == "__main__":
    sql_check()
    sql_execute("INSERT INTO NKUST (Account,Password,Telegram_chatID)","127934,'122pass',23456")
    z = chatID_check('23456')  
    print(z)