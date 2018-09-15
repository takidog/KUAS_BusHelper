import configparser
class config:
    def __init__(self,Config_file='Config.cfg'):
        self.conf = configparser.ConfigParser()
        self.conf.read(Config_file)

    def get(self,sections,key):
        if sections not in self.conf.sections():
            return False
        elif key not in self.conf.options(sections):
            return False
        return self.conf.get(sections,key)

if __name__ == "__main__":
    conf = config()
    #a = conf.get('KUAS_Default','account')
    print(conf.get('Telegram','api'))