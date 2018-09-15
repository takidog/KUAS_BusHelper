import requests
import bus
import os,sys
import time,datetime
import Config
import platform
class Core():
    def __init__(self,config_file='Config.cfg'):
        """init Config in Core Class
        default=Config.cfg

        more info in dev.md
        """
        # Normal status
        self.degug = 1
        self.log_ = 0
        #
        #Check Config_file and load config
        conf = Config.config(config_file)
        if conf.get('Debug','debug_mode') != False and conf.get('Debug','debug_mode') != '1':
            self.degug = 0
        if conf.get('Debug','log') != False and conf.get('Debug','log') != '0':
            self.log_ = 1
        #


        #get System type
        if platform.system() == 'Windows':
            self.System = 0
        else:
            self.System = 1
        #

        self.Session = requests.session()
        

    def log(self,text="",clear=0,No_time=0):
        if self.degug != 1:
            return True
        if clear ==1:
            if self.System == 1:
                os.system('cls')
            if self.System == 0:
                os.system('clear')
        
        if No_time == 0:
            text ="[%s] "%time.strftime("%Y-%m-%d %H:%M")+text     
        print(text)
        if self.log_ == 1:
            with open('log.txt', 'a') as log_file:
                log_file.write(text+'\n')
    ######check part
    def server_check(self):
        if bus.status() != 200:
            self.log('Maybe KUAS server is down QQ \nwait for min...and try again!')
            return False
        return True
    def Login_check(self,Account,Password):
        try:
            return bus.login(self.Session,Account,Password)
        except Exception as e:
            self.log("Login Error KUASID:%s"%self.Account)
        return False
    def all_check(self):
        #check server status and KUAS Login
        if self.server_check() == False:
            time.sleep(5)
            sys.exit()
        else:
            self.log("Server status  Pass")
        
        if self.Login_check() == False:
            time.sleep(5)
            sys.exit()
        else:
            self.log("KUAS login     Pass")
            return True
    #####

    def get_reserve_bus(self,No_show=0):
        if No_show == 1:
            self.degug = 1
        self.log("查詢已預約車次")
        try:
            res = bus.reserve(self.Session)
            #print(res)
            self.log('\n共預約 %s 個車次\n'%len(res))
            res_re = []
            for i in res:
                if i['end'] == "燕巢":
                    bus_text = "建工 >>> 燕巢"
                    typ = "A"
                else:
                    bus_text = "燕巢 >>> 建工"
                    typ = "B"
                
                tx = "\n發車時間:%s \n前往:%s \n"%(i['time'],bus_text)
                data = {'time':i['time'],'carryType':typ,'cancelKey':i['cancelKey']}
                res_re.append(data)
                self.log(tx,No_time=1)
            if No_show == 1:
                self.degug = 0
            return res_re
        except Exception as e:
            self.log("search error")
            if No_show == 1:
                self.degug = 0
            return False

    def search(self,year,mouth,day,first="全部"):
        diff= datetime.date.today() - datetime.date(year,mouth,day)
        #if 2 weeks (14 days) difference, will return False
        if diff.days > 14:
            #self.log("search >14 days I can't search QQ")
            return False
        res = bus.query(self.Session,year,mouth,day,first)
        #print(res)    
        res_text = "%s/%s\n"%(str(mouth),str(day))
        for i in res:
            #text = 'Bus ID:%s 時間:%s 前往:%s '%(i['busId'],i['Time'],i['endStation'])
            res_text += 'Bus ID:%s 時間:%s 前往:%s \n'%(i['busId'],i['Time'],i['endStation'])
            #self.log(text)
        return res_text
    def unbook(self,cancelKey):
        res = bus.book(self.Session,int(cancelKey),"un") 
        self.log(res['message'])
        return res['message']
        
    def book(self,busID):
        res = bus.book(self.Session,busID) 
        self.log(res['message'])
        return res['message']

if __name__ == "__kmain__":
    #core.get_reserve_bus()
    #core.search(2018,9,12,'建工')
    #core.search(2018,9,11,'燕巢')
    #core.book()
    #core.unbook()
    #datetime.date.today().isoweekday()
    core = Core()
    core.all_check()
    while True:
        text = "========\n1 : 查詢目前預約\n2 : 查詢日期車次(14天內)\n3 : 指定日期車次搭車\n4 : 取消車次\n8 : 離開\n========\n"
        inp = input(text)
        if inp == '1':
            core.get_reserve_bus()
        elif inp == '2':
            an = input('輸入2018/01/12  像這樣 =U=\n')
            where = input ('輸入 A/B  \nA:建工>>>燕巢\nB:燕巢>>>建工\nC:全部顯示!\n')
            if len(an.split('/')) == 3:
                if where.upper() == "A":
                    t = '建工'
                elif where.upper() == "B":
                    t = '燕巢'
                elif where.upper() == "C":
                    t = '全部'
                year,mouth,days = an.split('/')
                core.search(int(year),int(mouth),int(days),t)
        elif inp == '3':
            an = input('指定的Bus ID 是...?  (不知道可以輸入End回到主選單)\n')
            if an.upper() == "END":
                pass
            else:
                core.book(int(an))

        elif inp == '4':
            print('目前預約的班次如下!')
            res = core.get_reserve_bus(No_show=1)
            print("取消哪個班次呢")
            c= 0
            for i in range(1,len(res)+1):
                if res[c]['carryType'] == "A":
                    bus_text = "建工 >>> 燕巢"
                else:
                    bus_text = "燕巢 >>> 建工"
                print("%i--出發時間 : %s  %s  "%(i,res[c]['time'],bus_text))
                c += 1
            an = int(input())
            if an not in range(1,len(res)+1):
                print("輸入數字哦><")
            else:
                an -= 1
                core.unbook(int(res[an]['cancelKey']))
                # relogin   I don't know Why unbook always disconnect ...
                core.all_check()


        elif inp == '8':
            print("Bye~")
            sys.exit()
        