
import re
from dadata import Dadata
from settings import Settings

class Action():


    def __init__(self):
        self.settings = Settings()
        self.token = self.settings.get_api_key()
        self.lang = self.settings.get_lang()
        self.dadata = Dadata(self.token)


    def main(self):
        print('Привет! Это меню, чтобы сюда попасть, в любой момент набери 0 (ноль)')
        while True:
            print('\nВыбери действие: ')
            print('1. Искать адрес')
            print('2. Изменить настройки')
            print('3. Выйти')
            number = self.get_choice_number(3, '')
            if number == 0:
                continue
            elif number == 1:
                self.get_address_text()
                continue
            elif number == 2:
                self.change_settings()
                continue
            elif number == 3:
                self.exit_program()


    def get_address_text(self):
        while True:
            print('\nВведи адрес')
            string = input()
            if self.check_input_menu(string):
                break
            try:
                result = self.dadata.suggest("address", string, language=self.lang)
            except:
                print('\nНе могу получить доступ к сервису.')
                print('Может быть в настройках не указан ключ?')
                break
            addresses = []
            for addr in result:
                addresses.append(addr['value'])
            if len(addresses) == 0:
                print('\nПо твоему запросу ничего не нашлось. Попробуй еще раз')
                continue
            print('\nВот что нашлось по твоему запросу:')
            for num, addr in enumerate(addresses):
                print(str(num + 1) + ':', addr)
            number = self.get_choice_number(len(addresses), 'Введи номер нужного адреса')
            if number == 0:
                break
            string = result[number-1]['unrestricted_value']
            try:
                result = self.dadata.suggest("address", string, language=self.lang, count=1)
            except:
                print('\nДаже не знаю, что могло пойти не так')
                break
            x = result[0]['data']['geo_lat']
            y = result[0]['data']['geo_lon']
            if x is not None and y is not None:
                print('\n', x, y)
            else:
                print('\nКоординаты неизвестны :(')


    def get_choice_number(self, length, text):
        if text != '':
            print(text)
        while True:
            number = input()
            if self.check_input_menu(number):
                return 0
            try:
                number = int(number)
                if number > 0 and number <= length:
                    return number
                else:
                    print('\nНужно ввести число от 1 до ' + str(length))
                    continue
            except:
                print('\nНужно ввести число от 1 до ' + str(length))
                continue


    def change_settings(self):
        print('\nВыбери настройку:')
        print('1. API ключ')
        print('2. Язык')
        num = self.get_choice_number(2, '')
        if num == 0:
            return None
        elif num == 1:
            self.change_key()
        else:
            self.change_lang()


    def change_key(self):
        print('\nВведи новый ключ')
        while True:
            value = input()
            if self.check_input_menu(value):
                return None
            valid = self.check_key_input(value)
            if valid:
                success = self.settings.change_key(value)
                if success:
                    self.token = value
                    self.dadata = Dadata(self.token)
                    print('\nУспешно!')
                else:
                    print('\nНе получилось :(')
                return None
            else:
                print('\nНедопустимые символы. Попробуй еще раз')
                continue


    def change_lang(self):
        print('\nВыбери язык')
        print('1. ru')
        print('2. en')
        num = self.get_choice_number(2, '')
        if num == 0:
            return None
        if num == 1:
            lang = 'ru'
        else:
            lang = 'en'
        success = self.settings.change_lang(lang)
        if success:
            print('\nУспешно!')
            self.lang = lang
        else:
            print('\nНе получилось :(')
        return None


    def check_input_menu(self, val):
        if val == '0':
            return True
        else:
            return False


    @staticmethod
    def check_key_input(value):
        result = re.findall(r'[a-zA-Z0-9]+', value)
        if len(result) == 1:
            if result[0] == value:
                return True
        return False

    def exit_program(self):
        self.settings.close_connection()
        raise SystemExit



if __name__ == '__main__':
    a = Action()
    a.main()
