from game_ui import AnimatedText, UI
from game_player import Player
from os import getcwd, stat, system
from os.path import exists, isfile
from random import choices
from time import sleep

# Класс реализующий игровую механику;
class Game:
    # путь к файлу с конфигурациями игры;
    RESOURCES_PATH = "{}/configs.dat".format(getcwd())
    # путь к файлу с справочной информацией;
    RULES_PATH = "{}/rules.dat".format(getcwd())
    
    def __init__(self):
        # загрузка игровых констант из файла configs.dat;
        self.load_resources()
        # проверка валидности игровых констант;
        self.validate_constants()
        # создание заготовки для надписей;
        self.ANIMATED_TITLE = AnimatedText()
        # подключение конструктора меню и рисование игрового окна;
        self.INTERFACE = UI()

    def load_resources(self): # загрузка игровых констант из файла configs.dat;
        # проверка валидности адреса файла configs.dat;
        if exists(self.RESOURCES_PATH):
            # проверка является ли configs.dat файлом;
            if isfile(self.RESOURCES_PATH):
                # проверка наличия игровых констант в файле configs.dat;
                if stat(self.RESOURCES_PATH):
                    file = open(self.RESOURCES_PATH, "rb")
                    if file:
                        # загрузка данных из файла: чтение данных с кодировкой utf-8 (воизбежание ошибок чтения);
                        lines = [line.strip() for line in file.read().decode("utf-8").split("\n") if ":" in line]
                        # закрытие файла с настройками;
                        file.close()
                        # преобразование данных из файла в словарь констант;
                        for line in range(len(lines)):
                            # проверка валидности данных;
                            if ":" in lines[line]:
                                if lines[line].count(":") == 1:
                                    # парсинг игровых констант;
                                    (key, value) = [i.strip() for i in lines[line].split(":")]
                                    if value.isnumeric():
                                        # парсинг констант типа int;
                                        self.__dict__[key] = int(value)
                                    else:
                                        if "." in value:
                                            # парсинг констант типа float;
                                            (num1, num2) = [i.strip() for i in value.split(".")]
                                            if num1.isnumeric() and num2.isnumeric():
                                                self.__dict__[key] = float(value)
                                        else:
                                            # парсинг констант типа str;
                                            self.__dict__[key] = value
                            else:
                                input("Game->load_templates: Невалидное значение шаблона ({}).".format(line + 1)) # номер строки с незагруженой константой;
                                break
                        return True
                    else:
                        input("Game->load_resources: Файл с конфигурациями не загружен ({}).".format(self.RESOURCES_PATH))
                else:
                    input("Game->load_resources: Файл с конфигурациями пуст ({})".format(self.RESOURCES_PATH))
            else:
                input("Game->load_resources: Путь {} указывает не на файл с конфигурациями.".format(self.RESOURCES_PATH))
        else:
            input("Game->load_resources: Файл с конфигурациями отсутствует ({}).".format(self.RESOURCES_PATH))
        exit(1)

    def validate_constants(self): # валидация игровых констант;
        # группировка игровых констант (полей) для дальнейшей проверки;
        constants = (self.MIN_HEALTH_LEVEL,         # уровень минимального здоровья игрока;
                     self.MAX_HEALTH_LEVEL,         # уровень максимального здоровья игрока;
                     self.HEALTH_LIMIT,             # уровень здоровья компьютера, для увеличения шансов на исцеление;
                     self.MIN_NAME_SIZE,            # минимальный размер имени игрока;
                     self.MAX_NAME_SIZE,            # максимальный размер имени игрока;
                     self.MIN_LOW_DAMAGE,           # нижняя граница умеренного урона игрока;
                     self.MAX_LOW_DAMAGE,           # верхняя граница умеренного урона игрока;
                     self.MIN_HIGH_DAMAGE,          # нижняя граница большого урона игрока;
                     self.MAX_HIGH_DAMAGE,          # верхняя граница большого урона игрока;
                     self.MIN_HEAL_LEVEL,           # нижняя граница исцеления игрока;
                     self.MAX_HEAL_LEVEL,           # верхняя граница исцеления игрока;
                     self.LOW_DAMAGE_PROBABILITY,   # базовая вероятность выбора умеренного урона;
                     self.HIGH_DAMAGE_PROBABILITY,  # базовая вероятность выбора большого урона;
                     self.CURRENT_HEAL_PROBABILITY) # базовая вероятность выбора исцеления;
        # провека наличия всех констант;
        if None not in constants:
            # проверка валидности формата целочисленных констант;
            if False not in [type(i) == int for i in constants[:11]]:
                # особое условия для минимального уровня здоровья игрока;
                if False not in constants[1:] and constants[0] >= 0:
                    # проверка валидности границ размера имени игрока;
                    if self.MAX_NAME_SIZE > self.MIN_NAME_SIZE:
                        # проверка валидности значения минимального уровня здоровья игрока;
                        if min(constants) == self.MIN_HEALTH_LEVEL:
                            # проверка валидности значения максимального уровня здоровья игрока;
                            if max(constants) == self.MAX_HEALTH_LEVEL:
                                # проверка валидности значений умеренного урона и исцеления;
                                if self.MIN_LOW_DAMAGE == self.MIN_HEAL_LEVEL and self.MAX_LOW_DAMAGE == self.MAX_HEAL_LEVEL:
                                    # проверка валидности уровня умеренного и большого урона;
                                    if self.MAX_HIGH_DAMAGE > self.MAX_LOW_DAMAGE > self.MIN_LOW_DAMAGE > self.MIN_HIGH_DAMAGE:
                                        # проверка валидности формата констант вероятностей;
                                        if False not in [type(i) == float for i in constants[11:]]:
                                            # сумма вероятностей всех ходов должна быть равна 1;
                                            if round(sum(constants[11:14]), 3) == 1.000:
                                                # проверка валидности формата названия игры;
                                                if type(self.GAME_TITLE) == str:
                                                    # проверка валидности названия игры;
                                                    if len(self.GAME_TITLE):
                                                        return True # все константы валидны;
                                                    else:
                                                        input("Game->validate_constants: Название игры не задано.")
                                                else:
                                                    input("Game->validate_constants: Невалидный формат названия игры.")
                                            else:
                                                input("Game->validate_constants: Сумма вероятностей ходов компьютера не равна 1.")
                                        else:
                                            input("Game->validate_constants: Невалидый формат вероятностей ходов компьютера.")
                                    else:
                                        input("Game->validate_constants: Невалидные уровни умеренного и большого урона.")
                                else:
                                    input("Game->validate_constants: Невалидные уровни исцеления.")
                            else:
                                input("Game->validate_constants: Невалидный максимальный уровень здоровья.")
                        else:
                            input("Game->validate_constants: Невалидный минимальный уровень здоровья.")
                    else:
                        input("Game->validate_constants: Невалидные размеры имен игроков.")
                else:
                    input("Game->validate_constants: Константы кроме минимального уровня здоровья равны 0.")
            else:
                input("Game->validate_constants: Невалидный формат уровней здоровья и урона.")
        else:
            input("Game->validate_constants: Не все константы заданы.")
        return False # есть невалидные константы;
    
    def start(self): # запуск игры;
        # анимированый вывод надписи с названием игры:
        self.ANIMATED_TITLE.convert(self.GAME_TITLE)
        self.ANIMATED_TITLE.WIDTH = len(self.GAME_TITLE)
        self.ANIMATED_TITLE.bordered(node = "#", borders = ("=","|","|","="), fill = " ")
        # установка размера UI по ширине надписи и настройка размеров консоли;
        self.INTERFACE.WIDTH = len(self.ANIMATED_TITLE.VALUE[0])
        self.INTERFACE.HEIGHT = len(self.ANIMATED_TITLE.VALUE) * 2
        system("mode con cols={} lines={}".format(self.INTERFACE.WIDTH, self.INTERFACE.HEIGHT))
        # печать названия игры;
        self.ANIMATED_TITLE.animate_cmd(pause = 0.05)
        # задержка в 3 секунды;
        sleep(3)
        while True:
            # очистка окна консоли и настройка его размеров, выбор одного пунктов главного меню;
            system("cls")
            system("mode con cols={} lines={}".format(self.INTERFACE.WIDTH, self.INTERFACE.HEIGHT))
            option = self.INTERFACE.menu_creator("ГЛАВНОЕ МЕНЮ:", {1:"ИГРАТЬ", 2:"ТЕСТ", 3:"СПРАВКА", 4:"ВЫХОД"}, border = ("=", "|", "|", "="), align = "^")
            if option == 1:
                # запуск игры в режиме Игрок (человек) - Компьютер;
                self.play()
            if option == 2:
                # запуск игры в режиме Игрок (компьютер) - Компьютер;
                self.play(True)
            if option == 3:
                # вывод справочной информации об игре;
                self.rules()
            if option == 4:
                # выход из игры;
                print("Выход через 3 секунды...")
                sleep(3)
                exit(1)

    def play(self, auto = False): # запуск игрового процесса;
        # создание игрока 1 с именем Игрок и уровнем здоровья MAX_HEALTH_LEVEL;
        self.PLAYER_1 = Player("Игрок", self.MAX_HEALTH_LEVEL)
        # проверка валидности игрока 1: границы размера имени и уровня здоровья игрока 1;
        if self.PLAYER_1.validate({"min":self.MIN_NAME_SIZE, "max":self.MAX_NAME_SIZE}, {"min":self.MIN_HEALTH_LEVEL, "max":self.MAX_HEALTH_LEVEL}):
            # создание игрока 2 с именем Компьютер и уровнем здоровья MAX_HEALTH_LEVEL;
            self.PLAYER_2 = Player("Компьютер", self.MAX_HEALTH_LEVEL)
            # проверка валидности игрока 2: границы размера имени и уровня здоровья игрока 2;
            if self.PLAYER_2.validate({"min":self.MIN_NAME_SIZE, "max":self.MAX_NAME_SIZE}, {"min":self.MIN_HEALTH_LEVEL, "max":self.MAX_HEALTH_LEVEL}):
                # особое условие: уровень здоровья обоих игроков в начале игры одинаковый, иначе аварийное завершение программы;
                if self.PLAYER_1.HEALTH != self.PLAYER_2.HEALTH:
                    input("У \"{}\" и \"{}\" разные уровни здоровья в начале игры. ажмите любую клавишу...".format(self.PLAYER_1.NAME, self.PLAYER_2.NAME))
                    exit(1)
                # открітие журнала игровіх ходов и запуск игрового цикла;
                file = open("{}/last_game_history.txt".format(getcwd()), "w")
                while True:
                    # очистка екрана;
                    system("cls")
                    # условие окончания игры: уровень здоровья одного из игроков достиг минимального уровня здоровья (например, 0%);
                    if not (self.PLAYER_1.HEALTH > 0) or not (self.PLAYER_2.HEALTH > 0):
                        break
                    # запись в журнал информации о текущем состоянии здоровья игроков;
                    file.write("{}({:03}%)\t\t{}({:03}%)\n".format(self.PLAYER_1.NAME, self.PLAYER_1.HEALTH, self.PLAYER_2.NAME, self.PLAYER_2.HEALTH))
                    # установка урона/исцеления, выбор очередности хода;
                    damage = 0
                    queue = choices([self.PLAYER_1, self.PLAYER_2], weights=[0.5, 0.5])[0]
                    # ходит игрок 1;
                    if queue.NAME == self.PLAYER_1.NAME:
                        # ход совершается автоматически (без участия Игрока);
                        if auto:
                            damage = self.auto_step(self.PLAYER_1)
                        # ход совершается в ручном режиме (с участием Игрока);
                        else:
                            damage = self.user_step()
                        # корректировка уровня здоровья игроков;
                        if damage > 0:
                            # исцеление игрока 1;
                            self.PLAYER_1.heal(damage, self.MAX_HEALTH_LEVEL)
                        else:
                            # урон Компьютеру;
                            self.PLAYER_2.hurt(damage, self.MIN_HEALTH_LEVEL)
                    # ходит игрок 2;
                    else:
                        # ход совершается автоматически;
                        damage = self.auto_step(self.PLAYER_2)
                        if damage is None:
                            # если уровень здоровья Компьютера не задан, то невозможно оценить урон;
                            input("Game->play: Уровень здоровья {} не задан. Нажмите любую клавишу для выхода...".format(self.PLAYER_2.NAME))
                            exit(1)
                        elif damage > 0:
                            # исцеление игрока 2;
                            self.PLAYER_2.heal(damage, self.MAX_HEALTH_LEVEL)
                        else:
                            # урон Игроку 1;
                            self.PLAYER_1.hurt(damage, self.MIN_HEALTH_LEVEL)
                    # вывод игрового окна с результатами хода;
                    self.INTERFACE.print_window(queue, self.PLAYER_1, self.PLAYER_2, damage)
                    # запись результатов хода в журнал;
                    if damage > 0:
                        file.write("{}->{}: +{:03}%\n".format(queue.NAME, self.PLAYER_2.NAME if queue.NAME != self.PLAYER_1.NAME else self.PLAYER_1.NAME, damage))
                    else:
                        file.write("{}->{}: -{:03}%\n".format(queue.NAME, self.PLAYER_2.NAME if queue.NAME == self.PLAYER_1.NAME else self.PLAYER_1.NAME, abs(damage)))
                    if not auto:
                        # ожидание перехода к следующему ходу (работает только в ручном режиме);
                        input("Нажмите любую клавишу для следующего хода...")
                    else:
                        # ожидание перехода к следующему ходу (работает только в ручном режиме);
                        print("Следующий ход через 5 секунд...")
                        # задержка в 5 секунд;
                        sleep(5)
                    #;
                    system("cls")
                #;
                file.close()
                #;
                self.complete()
    
    def low_damage(self): # генератор умеренного урона;
        if None not in (self.MIN_LOW_DAMAGE, self.MAX_LOW_DAMAGE):
            if self.MAX_LOW_DAMAGE > self.MIN_LOW_DAMAGE:
                # генерация случайного умеренного урона;
                return -choices(range(self.MIN_LOW_DAMAGE, self.MAX_LOW_DAMAGE + 1))[0]
            else:
                input("Game->low_damage: Невалидные границы умеренного урона.")
        else:
            input("Game->low_damage: Границы умеренного урона не установлены.")

    def high_damage(self): # генератор большого урона;
        if None not in (self.MIN_HIGH_DAMAGE, self.MAX_HIGH_DAMAGE):
            if self.MAX_HIGH_DAMAGE > self.MIN_HIGH_DAMAGE:
                # генерация случайного большого урона;
                return -choices(range(self.MIN_HIGH_DAMAGE, self.MAX_HIGH_DAMAGE + 1))[0]
            else:
                input("Game->high_damage: Невалидные границы большого урона.")
        else:
            input("Game->high_damage: Границы большого урона не установлены.")

    def heal(self): # генератор очков исцеления;
        if None not in (self.MIN_HEAL_LEVEL, self.MAX_HEAL_LEVEL):
            if self.MAX_HEAL_LEVEL > self.MIN_HEAL_LEVEL:
                # генерация случайного уровня исцеления;
                return choices(range(self.MIN_HEAL_LEVEL, self.MAX_HEAL_LEVEL + 1))[0]
            else:
                input("Game->heal: Невалидные границы исцеления.")
        else:
            input("Game->heal: Границы исцеления не установлены.")

    def auto_step(self, player): # генерация случайного хода согласно заданых вероятностей;
        if player is not None:
            # первичные шансы на выбор определенного хода; 
            step_weights = [self.LOW_DAMAGE_PROBABILITY, self.HIGH_DAMAGE_PROBABILITY, self.CURRENT_HEAL_PROBABILITY]
            if player.NAME == self.PLAYER_2.NAME:
                if player.HEALTH < self.HEALTH_LIMIT:
                    # переоценка шансов на выбор определенного хода если уровень здоровья игрока упал ниже допустимого;
                    step_weights[0] = self.CURRENT_HEAL_PROBABILITY
                    step_weights[1] = self.HIGH_DAMAGE_PROBABILITY
                    step_weights[2] = self.LOW_DAMAGE_PROBABILITY
            # генерация случайного хода;
            return choices((self.low_damage(), self.high_damage(), self.heal()), step_weights)[0]
        input("Game->auto_step: Игрок которому выпал ход не задан.")

    def user_step(self): # генерация хода в ручном режиме;
        # выбор хода в ручном режиме;
        option = self.INTERFACE.menu_creator("ВЫБЕРИТЕ ОДИН ИЗ ДОСТУПНЫХ ХОДОВ:",
                                             {1:"УМЕРЕННЫЙ УРОН", 2:"БОЛЬШОЙ УРОН", 3:"ИСЦЕЛЕНИЕ"},
                                             border = ("=", "|", "|", "="))
        if option == 1:
            # умеренный урон;
            return self.low_damage()
        elif option == 2:
            # большой урон;
            return self.high_damage()
        else:
            # исцеление;
            return self.heal()

    def rules(self): # вывод справочных данных;
        # валидация адреса файла с спрвочной информацией;
        if exists(self.RULES_PATH):
            # проверка находится ли файл со справкой по указаному адресу;
            if isfile(self.RULES_PATH):
                # проверка наличия информации в файле;
                if stat(self.RULES_PATH):
                    file = open(self.RULES_PATH, "rb")
                    if file:
                        # загрузка данных из файла;
                        lines = [line.strip("\ufeff") for line in file.read().decode("utf-8").split("\n") if line.strip()]
                        lines = [line.strip() for line in lines]
                        file.close()
                        # вывод описания и правил игры на екран;
                        self.ANIMATED_TITLE.WIDTH = max([len(line) for line in lines]) + 2           # ширина окна;
                        tmp = []
                        self.ANIMATED_TITLE.VALUE = [lines[0]]
                        self.ANIMATED_TITLE.bordered("#", ("=","|","|",""), fill=" ", align="<")
                        tmp.append("\n".join(self.ANIMATED_TITLE.VALUE))
                        for line in range(1, len(lines) - 1):
                            self.ANIMATED_TITLE.VALUE = [lines[line]]
                            self.ANIMATED_TITLE.bordered("#", ("","|","|",""), fill=" ", align="<")
                            tmp.append("\n".join(self.ANIMATED_TITLE.VALUE))
                        self.ANIMATED_TITLE.VALUE = [lines[-1]]
                        self.ANIMATED_TITLE.bordered("#", ("","|","|","="), fill=" ", align="<")
                        tmp.append("\n".join(self.ANIMATED_TITLE.VALUE))
                        # настройка ширины окна консоли;
                        system("mode con cols={} lines={}".format(self.ANIMATED_TITLE.WIDTH + 2, len(lines) + 5))
                        # вывод справки;
                        print("\n".join(tmp))
                        input("\nНажмите любую клавишу для возврата в меню...")
                        return True
                    else:
                        input("Game->load_rules: Файл с правилами игры не загружен ({}).".format(self.RULES_PATH))
                else:
                    input("Game->load_rules: Файл с правилами игры пуст ({})".format(self.RULES_PATH))
            else:
                input("Game->load_rules: Путь {} указывает не на файл с правилами игры.".format(self.RULES_PATH))
        else:
            input("Game->load_rules: Файл с правилами игры отсутствует ({}).".format(self.RULES_PATH))
        exit(1)

    def complete(self): # завершение программы;
        # вывод надписи об окончании игры;
        info = "Игра окончена!"
        self.ANIMATED_TITLE.convert(info)
        self.ANIMATED_TITLE.WIDTH = len(info) + 2
        self.ANIMATED_TITLE.bordered("#", ("","|","|","="))
        self.INTERFACE.WIDTH = len(self.ANIMATED_TITLE.VALUE[0])
        self.INTERFACE.HEIGHT = len(self.ANIMATED_TITLE.VALUE) + 2
        system("mode con cols={} lines={}".format(self.INTERFACE.WIDTH, self.INTERFACE.HEIGHT))
        self.ANIMATED_TITLE.animate_cmd(pause = 0.001)
        sleep(2)
        # вывод надписи о победителе игры;
        info = "ПОБЕДИЛ {}!".format(self.PLAYER_1.NAME if self.PLAYER_1.HEALTH > 0 else self.PLAYER_2.NAME)
        self.ANIMATED_TITLE.convert(info)
        self.ANIMATED_TITLE.WIDTH = len(info) + 2
        self.ANIMATED_TITLE.bordered("#", ("=","|","|","="))
        self.INTERFACE.WIDTH = len(self.ANIMATED_TITLE.VALUE[0])
        self.INTERFACE.HEIGHT = len(self.ANIMATED_TITLE.VALUE) + 2
        system("mode con cols={} lines={}".format(self.INTERFACE.WIDTH, self.INTERFACE.HEIGHT))
        self.ANIMATED_TITLE.animate_cmd(pause = 0.001)
        print("Возврат в меню через 3 секунды...")
        sleep(3)

# запуск игры; 
if __name__ == "__main__":
    Game().start()
"""---------------------------------------------------------------------------------------------------------------------
Класс реализующий игровую механику
---------------------------------------------------------------------------------------------------------------------
1) Поля:
---------------------------------------------------------------------------------------------------------------------
* RESOURCES_PATH - путь к файлу конфигураций;
* RULES_PATH - путь к файлу с справкой;
* ANIMATED_TITLE - заготовка для построения надписи;
* INTERFACЕ - подключение UI;
* MIN_HEALTH_LEVEL - уровень минимального здоровья игрока;
* MAX_HEALTH_LEVEL - уровень максимального здоровья игрока;
* HEALTH_LIMIT - уровень здоровья компьютерадля увеличения шансов на исцеление;
* MIN_NAME_SIZE - минимальный размер имени игрока;
* MAX_NAME_SIZE - максимальный размер имени игрока;
* MIN_LOW_DAMAGE - нижняя граница умеренного урона игрока;
* MAX_LOW_DAMAGE - верхняя граница умеренного урона игрока;
* MIN_HIGH_DAMAGE - нижняя граница большого урона игрока;
* MAX_HIGH_DAMAGE - верхняя граница большого урона игрока;
* MIN_HEAL_LEVEL - нижняя граница исцеления игрока;
* MAX_HEAL_LEVEL - верхняя граница исцеления игрока;
* LOW_DAMAGE_PROBABILITY - базовая вероятность выбора умеренного урона;
* HIGH_DAMAGE_PROBABILITY - базовая вероятность выбора большого урона;
* CURRENT_HEAL_PROBABILITY - базовая вероятность выбора исцеления.
---------------------------------------------------------------------------------------------------------------------
2) Методы:
---------------------------------------------------------------------------------------------------------------------
2.1) load_resources() - загрузка игровых констант из файла configs.dat.
---------------------------------------------------------------------------------------------------------------------
2.2) validate_constants() - валидацияигровых констант.
---------------------------------------------------------------------------------------------------------------------
2.3) start() - запуск игры.
---------------------------------------------------------------------------------------------------------------------
2.4) play(auto = False) - запуск игрового процесса:
                          Входные данные:
                          * auto - режим игры автоматический (True) / ручной (False) (False по умолчанию).
                          Выходные данные: нет.
---------------------------------------------------------------------------------------------------------------------
2.5) low_damage() - генератор умеренного урона.
---------------------------------------------------------------------------------------------------------------------
2.6) high_damage() - генератор большого урона.
---------------------------------------------------------------------------------------------------------------------
2.7) heal() - генератор очков исцеления.
---------------------------------------------------------------------------------------------------------------------
2.8) auto_step(player) - генерация случайного хода согласно заданых вероятностей.
---------------------------------------------------------------------------------------------------------------------
2.9) user_step() - генерация хода в ручном режиме.
---------------------------------------------------------------------------------------------------------------------
2.10) rules() - вывод справочных данных.
---------------------------------------------------------------------------------------------------------------------
2.11) complete() - завершение программы.
---------------------------------------------------------------------------------------------------------------------"""
