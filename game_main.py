from game_ui import AnimatedText, UI
from game_player import Player
from os import getcwd, stat, system
from os.path import exists, isfile
from random import choices
from time import sleep

class Game:
    """---------------------------------------------------------------------------------------------------------------------
Класс реализующий игровую механику
---------------------------------------------------------------------------------------------------------------------
1) Поля:
---------------------------------------------------------------------------------------------------------------------
* resources_path - путь к файлу конфигураций;
* rules_path - путь к файлу с справкой;
* animated_title - заготовка для построения надписи;
* interfacе - подключение ui;
* min_health_level - уровень минимального здоровья игрока;
* max_health_level - уровень максимального здоровья игрока;
* health_limit - уровень здоровья компьютерадля увеличения шансов на исцеление;
* min_name_size - минимальный размер имени игрока;
* max_name_size - максимальный размер имени игрока;
* min_low_damage - нижняя граница умеренного урона игрока;
* max_low_damage - верхняя граница умеренного урона игрока;
* min_high_damage - нижняя граница большого урона игрока;
* max_high_damage - верхняя граница большого урона игрока;
* min_heal_level - нижняя граница исцеления игрока;
* max_heal_level - верхняя граница исцеления игрока;
* low_damage_probability - базовая вероятность выбора умеренного урона;
* high_damage_probability - базовая вероятность выбора большого урона;
* current_heal_probability - базовая вероятность выбора исцеления.
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
     Входные данные:
     * player - оюъект типа Player.
     Выходные данные:
     * damage - уровень урона / исцеления;
---------------------------------------------------------------------------------------------------------------------
2.9) user_step() - генерация хода в ручном режиме.
---------------------------------------------------------------------------------------------------------------------
2.10) rules() - вывод справочных данных.
---------------------------------------------------------------------------------------------------------------------
2.11) complete() - завершение программы.
---------------------------------------------------------------------------------------------------------------------"""
    # путь к файлу с конфигурациями игры;
    resources_path = "{}/configs.dat".format(getcwd())
    # путь к файлу с справочной информацией;
    rules_path = "{}/rules.dat".format(getcwd())
    
    def __init__(self):
        # загрузка игровых констант из файла configs.dat;
        self.load_resources()
        # проверка валидности игровых констант;
        self.validate_constants()
        # создание заготовки для надписей;
        self.animated_title = AnimatedText()
        # подключение конструктора меню и рисование игрового окна;
        self.interface = UI()

    def load_resources(self):
        # проверка валидности адреса файла configs.dat;
        if exists(self.resources_path):
            # проверка является ли configs.dat файлом;
            if isfile(self.resources_path):
                # проверка наличия игровых констант в файле configs.dat;
                if stat(self.resources_path):
                    file = open(self.resources_path, "rb")
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
                                        self.__dict__[key.lower()] = int(value)
                                    else:
                                        if "." in value:
                                            # парсинг констант типа float;
                                            (num1, num2) = [i.strip() for i in value.split(".")]
                                            if num1.isnumeric() and num2.isnumeric():
                                                self.__dict__[key.lower()] = float(value)
                                        else:
                                            # парсинг констант типа str;
                                            self.__dict__[key.lower()] = value
                            else:
                                # номер строки с незагруженой константой;
                                input("Game->load_templates: Невалидное значение шаблона ({}).".format(line + 1))
                                break
                        return True
                    else:
                        input("Game->load_resources: Файл с конфигурациями не загружен ({}).".format(self.resources_path))
                else:
                    input("Game->load_resources: Файл с конфигурациями пуст ({})".format(self.resources_path))
            else:
                input("Game->load_resources: Путь {} указывает не на файл с конфигурациями.".format(self.resources_path))
        else:
            input("Game->load_resources: Файл с конфигурациями отсутствует ({}).".format(self.resources_path))
        exit(1)

    def validate_constants(self):
        # группировка игровых констант (полей) для дальнейшей проверки;
        constants = (# уровень минимального здоровья игрока;
                     self.min_health_level,
                     # уровень максимального здоровья игрока;
                     self.max_health_level,
                     # уровень здоровья компьютера, для увеличения шансов на исцеление;
                     self.health_limit,
                     # минимальный размер имени игрока;
                     self.min_name_size,
                     # максимальный размер имени игрока;
                     self.max_name_size,
                     # нижняя граница умеренного урона игрока;
                     self.min_low_damage,
                     # верхняя граница умеренного урона игрока;
                     self.max_low_damage,
                     # нижняя граница большого урона игрока;
                     self.min_high_damage,
                     # верхняя граница большого урона игрока;
                     self.max_high_damage,
                     # нижняя граница исцеления игрока;
                     self.min_heal_level,
                     # верхняя граница исцеления игрока;
                     self.max_heal_level,
                     # базовая вероятность выбора умеренного урона;
                     self.low_damage_probability,
                     # базовая вероятность выбора большого урона;
                     self.high_damage_probability,
                     # базовая вероятность выбора исцеления;
                     self.current_heal_probability)
        # провека наличия всех констант;
        if None not in constants:
            # проверка валидности формата целочисленных констант;
            if False not in [type(i) == int for i in constants[:11]]:
                # особое условия для минимального уровня здоровья игрока;
                if False not in constants[1:] and constants[0] >= 0:
                    # проверка валидности границ размера имени игрока;
                    if self.max_name_size > self.min_name_size:
                        # проверка валидности значения минимального уровня здоровья игрока;
                        if min(constants) == self.min_health_level:
                            # проверка валидности значения максимального уровня здоровья игрока;
                            if max(constants) == self.max_health_level:
                                # проверка валидности значений умеренного урона и исцеления;
                                if self.min_low_damage == self.min_heal_level and self.max_low_damage == self.max_heal_level:
                                    # проверка валидности уровня умеренного и большого урона;
                                    if self.max_high_damage > self.max_low_damage > self.min_low_damage > self.min_high_damage:
                                        # проверка валидности формата констант вероятностей;
                                        if False not in [type(i) == float for i in constants[11:]]:
                                            # сумма вероятностей всех ходов должна быть равна 1;
                                            if round(sum(constants[11:14]), 3) == 1.000:
                                                # проверка валидности формата названия игры;
                                                if type(self.game_title) == str:
                                                    # проверка валидности названия игры;
                                                    if len(self.game_title):
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
    
    def start(self):
        # анимированый вывод надписи с названием игры:
        self.animated_title.convert(self.game_title)
        self.animated_title.width = len(self.game_title)
        self.animated_title.bordered(node="#", borders=("=","|","|","="), fill=" ")
        # установка размера UI по ширине надписи и настройка размеров консоли;
        self.interface.width = len(self.animated_title.value[0])
        self.interface.HEIGHT = len(self.animated_title.value) * 2
        system("mode con cols={} lines={}".format(self.interface.width, self.interface.HEIGHT))
        # печать названия игры;
        self.animated_title.animate_cmd(pause=0.05)
        # задержка в 3 секунды;
        sleep(3)
        while True:
            # очистка окна консоли и настройка его размеров, выбор одного пунктов главного меню;
            system("cls")
            system("mode con cols={} lines={}".format(self.interface.width, self.interface.HEIGHT))
            option = self.interface.menu_creator("ГЛАВНОЕ МЕНЮ:", {1:"ИГРАТЬ", 2:"ТЕСТ", 3:"СПРАВКА", 4:"ВЫХОД"}, border=("=","|","|","="), align="^")
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

    def play(self, auto=False):
        # создание игрока 1 с именем Игрок и уровнем здоровья MAX_HEALTH_LEVEL;
        self.player_1 = Player("Игрок", self.max_health_level)
        # проверка валидности игрока 1: границы размера имени и уровня здоровья игрока 1;
        if self.player_1.validate({"min":self.min_name_size, "max":self.max_name_size}, {"min":self.min_health_level, "max":self.max_health_level}):
            # создание игрока 2 с именем Компьютер и уровнем здоровья MAX_HEALTH_LEVEL;
            self.player_2 = Player("Компьютер", self.max_health_level)
            # проверка валидности игрока 2: границы размера имени и уровня здоровья игрока 2;
            if self.player_2.validate({"min":self.min_name_size, "max":self.max_name_size}, {"min":self.min_health_level, "max":self.max_health_level}):
                # особое условие: уровень здоровья обоих игроков в начале игры одинаковый, иначе аварийное завершение программы;
                if self.player_1.health != self.player_2.health:
                    input("У \"{}\" и \"{}\" разные уровни здоровья в начале игры. ажмите любую клавишу...".format(self.player_1.name, self.player_2.name))
                    exit(1)
                # открітие журнала игровіх ходов и запуск игрового цикла;
                file = open("{}/last_game_history.txt".format(getcwd()), "w")
                while True:
                    # очистка екрана;
                    system("cls")
                    # условие окончания игры: уровень здоровья одного из игроков достиг минимального уровня здоровья (например, 0%);
                    if not (self.player_1.health > 0) or not (self.player_2.health > 0):
                        break
                    # запись в журнал информации о текущем состоянии здоровья игроков;
                    file.write("{}({:03}%)\t\t{}({:03}%)\n".format(self.player_1.name, self.player_1.health, self.player_2.name, self.player_2.health))
                    # установка урона/исцеления, выбор очередности хода;
                    damage = 0
                    queue = choices([self.player_1, self.player_2], weights=[0.5, 0.5])[0]
                    # ходит игрок 1;
                    if queue.name == self.player_1.name:
                        # ход совершается автоматически (без участия Игрока);
                        if auto:
                            damage = self.auto_step(self.player_1)
                        # ход совершается в ручном режиме (с участием Игрока);
                        else:
                            damage = self.user_step()
                        # корректировка уровня здоровья игроков;
                        if damage > 0:
                            # исцеление игрока 1;
                            self.player_1.heal(damage, self.max_health_level)
                        else:
                            # урон Компьютеру;
                            self.player_2.hurt(damage, self.min_health_level)
                    # ходит игрок 2;
                    else:
                        # ход совершается автоматически;
                        damage = self.auto_step(self.player_2)
                        if damage is None:
                            # если уровень здоровья Компьютера не задан, то невозможно оценить урон;
                            input("Game->play: Уровень здоровья {} не задан. Нажмите любую клавишу для выхода...".format(self.player_2.name))
                            exit(1)
                        elif damage > 0:
                            # исцеление игрока 2;
                            self.player_2.heal(damage, self.max_health_level)
                        else:
                            # урон Игроку 1;
                            self.player_1.hurt(damage, self.min_health_level)
                    # вывод игрового окна с результатами хода;
                    self.interface.print_window(queue, self.player_1, self.player_2, damage)
                    # запись результатов хода в журнал;
                    if damage > 0:
                        file.write("{}->{}: +{:03}%\n".format(queue.name, self.player_2.name if queue.name != self.player_1.name else self.player_1.name, damage))
                    else:
                        file.write("{}->{}: -{:03}%\n".format(queue.name, self.player_2.name if queue.name == self.player_1.name else self.player_1.name, abs(damage)))
                    if not auto:
                        # ожидание перехода к следующему ходу (работает только в ручном режиме);
                        input("Нажмите любую клавишу для следующего хода...")
                    else:
                        # ожидание перехода к следующему ходу (работает только в ручном режиме);
                        print("Следующий ход через 5 секунд...")
                        # задержка в 5 секунд;
                        sleep(5)
                    system("cls")
                file.close()
                # вывод результатов игры;
                self.complete()
    
    def low_damage(self):
        if None not in (self.min_low_damage, self.max_low_damage):
            if self.max_low_damage > self.min_low_damage:
                # генерация случайного умеренного урона;
                return -choices(range(self.min_low_damage, self.max_low_damage + 1))[0]
            else:
                input("Game->low_damage: Невалидные границы умеренного урона.")
        else:
            input("Game->low_damage: Границы умеренного урона не установлены.")

    def high_damage(self):
        if None not in (self.min_high_damage, self.max_high_damage):
            if self.max_high_damage > self.min_high_damage:
                # генерация случайного большого урона;
                return -choices(range(self.min_high_damage, self.max_high_damage + 1))[0]
            else:
                input("Game->high_damage: Невалидные границы большого урона.")
        else:
            input("Game->high_damage: Границы большого урона не установлены.")

    def heal(self):
        if None not in (self.min_heal_level, self.max_heal_level):
            if self.max_heal_level > self.min_heal_level:
                # генерация случайного уровня исцеления;
                return choices(range(self.min_heal_level, self.max_heal_level + 1))[0]
            else:
                input("Game->heal: Невалидные границы исцеления.")
        else:
            input("Game->heal: Границы исцеления не установлены.")

    def auto_step(self, player):
        if player is not None:
            # первичные шансы на выбор определенного хода; 
            step_weights = [self.low_damage_probability, self.high_damage_probability, self.current_heal_probability]
            if player.name == self.player_2.name:
                if player.health < self.health_limit:
                    # переоценка шансов на выбор определенного хода если уровень здоровья игрока упал ниже допустимого;
                    step_weights[0] = self.current_heal_probability
                    step_weights[1] = self.high_damage_probability
                    step_weights[2] = self.low_damage_probability
            # генерация случайного хода;
            return choices((self.low_damage(), self.high_damage(), self.heal()), step_weights)[0]
        input("Game->auto_step: Игрок которому выпал ход не задан.")

    def user_step(self):
        # выбор хода в ручном режиме;
        option = self.interface.menu_creator("ВЫБЕРИТЕ ОДИН ИЗ ДОСТУПНЫХ ХОДОВ:", {1:"УМЕРЕННЫЙ УРОН", 2:"БОЛЬШОЙ УРОН", 3:"ИСЦЕЛЕНИЕ"}, border=("=", "|", "|", "="))
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
        if exists(self.rules_path):
            # проверка находится ли файл со справкой по указаному адресу;
            if isfile(self.rules_path):
                # проверка наличия информации в файле;
                if stat(self.rules_path):
                    file = open(self.rules_path, "rb")
                    if file:
                        # загрузка данных из файла;
                        lines = [line.strip("\ufeff") for line in file.read().decode("utf-8").split("\n") if line.strip()]
                        lines = [line.strip() for line in lines]
                        file.close()
                        # вывод описания и правил игры на екран;
                        # ширина окна;
                        self.animated_title.width = max([len(line) for line in lines]) + 2
                        tmp = []
                        self.animated_title.value = [lines[0]]
                        self.animated_title.bordered("#", ("=","|","|",""), fill=" ", align="<")
                        tmp.append("\n".join(self.animated_title.value))
                        for line in range(1, len(lines) - 1):
                            self.animated_title.value = [lines[line]]
                            self.animated_title.bordered("#", ("","|","|",""), fill=" ", align="<")
                            tmp.append("\n".join(self.animated_title.value))
                        self.animated_title.value = [lines[-1]]
                        self.animated_title.bordered("#", ("","|","|","="), fill=" ", align="<")
                        tmp.append("\n".join(self.animated_title.value))
                        # настройка ширины окна консоли;
                        system("mode con cols={} lines={}".format(self.animated_title.width + 2, len(lines) + 5))
                        # вывод справки;
                        print("\n".join(tmp))
                        input("\nНажмите любую клавишу для возврата в меню...")
                        return True
                    else:
                        input("Game->load_rules: Файл с правилами игры не загружен ({}).".format(self.rules_path))
                else:
                    input("Game->load_rules: Файл с правилами игры пуст ({})".format(self.rules_path))
            else:
                input("Game->load_rules: Путь {} указывает не на файл с правилами игры.".format(self.rules_path))
        else:
            input("Game->load_rules: Файл с правилами игры отсутствует ({}).".format(self.rules_path))
        exit(1)

    def complete(self):
        # вывод надписи об окончании игры;
        info = "Игра окончена!"
        self.animated_title.convert(info)
        self.animated_title.width = len(info) + 2
        self.animated_title.bordered("#", ("=","|","|","="))
        self.interface.width = len(self.animated_title.value[0])
        self.interface.height = len(self.animated_title.value) + 2
        system("mode con cols={} lines={}".format(self.interface.width, self.interface.height))
        self.animated_title.animate_cmd(pause=0.001)
        sleep(2)
        # вывод надписи о победителе игры;
        info = "ПОБЕДИЛ {}!".format(self.player_1.name if self.player_1.health > 0 else self.player_2.name)
        self.animated_title.convert(info)
        self.animated_title.width = len(info) + 2
        self.animated_title.bordered("#", ("=","|","|","="))
        self.interface.width = len(self.animated_title.value[0])
        self.interface.height = len(self.animated_title.value) + 2
        system("mode con cols={} lines={}".format(self.interface.width, self.interface.height))
        self.animated_title.animate_cmd(pause=0.001)
        print("Возврат в меню через 3 секунды...")
        sleep(3)

# запуск игры; 
if __name__ == "__main__":
    Game().start()
