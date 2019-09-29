from os import getcwd, system, stat
from os.path import isfile, exists
from time import sleep

class AnimatedText:
    """-------------------------------------------------------------------------------------------------------
Класс создания игровых надписей
-------------------------------------------------------------------------------------------------------
1) Поля:
-------------------------------------------------------------------------------------------------------
* PATH(str) - путь из текущей папки модуля к файлу с шаблонами символов, чисел и отдельных спецзнаков;
* VALUE(list) - хранилище для надписи;
* WIDTH(int) - ширина надписи (в символах).
-------------------------------------------------------------------------------------------------------
2) Методы:
-------------------------------------------------------------------------------------------------------
2.1) __init__() - создание екземпляра класса, заготовки для хранения надписи.
                  Входные параметры: нет.
                  Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.2) load_templates() - загрузка шаблонов символов, чисел и отдельных спецзнаков из файла PATH.
                        Входные параметры: нет.
                        Выходные параметры:
                        * словарь TEMPLATES.
-------------------------------------------------------------------------------------------------------
2.3) convert(word) - конвертация символной строки в надпись, создает поле VALUE для сохранения надписи
                     в классе. 
                     Входные параметры:
                     * word(str) - символьная строка (None по умолчанию).
                     Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.4) bordered(node, borders, fill, align) - обрамляет надпись рамкойи пересохраняет её в поле класса
                                            VALUE.
                                            Входные параметры:
                                            * node(str) - обозначение углов рамки, при построении гран-
                                                          иц надписи;
                                            * borders(set) - набор обозначений границ надписи (верхняя,
                                                             левая, правая, нижняя);
                                            * fill(str) - заполнитель пространства между границами и
                                                          данными;
                                            * align(str) - виравнивание данных между границами рамки.
                                            Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.4) animate_cmd(pause) - вывод надписи построчно, с установленной задержкой времени.
                          Входные параметры:
                          * pause - задержка времени между выводом строк в сек. (1 сек. по умолчанию).
                          Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------"""

    PATH = "{}/char_templates.dat".format(getcwd())

    def __init__(self):
        # загрузка шаблонов символов необходимых для создания надписей;
        self.load_templates()
        # пустая заготовка для хранения надписи;
        self.VALUE = None
        # ширина надписи;
        self.WIDTH = None
    
    def load_templates(self):
        # проверка валидности адреса с файлом шаблонов;
        if exists(self.PATH):
            # проверка наличия файла с шаблонами по заданому адресу;
            if isfile(self.PATH):
                # проверка наличия шаблонов в файле;
                if stat(self.PATH):
                    file = open(self.PATH, "rb")
                    if file:
                        # загрузка шаблонов из файла;
                        lines = [line.strip("\ufeff") for line in file.read().decode("utf-8").split("\n") if line.strip()]
                        file.close()
                        # преобразование данных из файла в словарь надписей;
                        self.__dict__["TEMPLATES"] = dict()
                        for line in range(len(lines)):
                            # проверка валидности шаблона из файла;
                            if ":" in lines[line] and lines[line].count(":") == 1:
                                (key, value) = [item.strip() for item in lines[line].split(":")]
                                key = " " if key == "" else key
                                # сохранение шаблона в словарь;
                                self.__dict__["TEMPLATES"][key] = value
                            else:
                                input(lines[line])
                                input("PaintText->load_templates: Невалидное значение шаблона ({}).".format(line + 1))
                                exit(1)
                        # количество полей в классе еквивалентно количеству значений загруженых из файла;
                        if not (len(self.__dict__["TEMPLATES"]) == len(lines)):
                            input("AnimatedText->load_templates: Данные с файла шаблонов потеряны ({})!".format(len(self.__dict__["TEMPLATES"])))
                    else:
                        input("AnimatedText->load_templates: Файл с шаблонами не загружен ({}).".format(self.PATH))
                else:
                    input("AnimatedText->load_templates: Файл с шаблонами пуст ({})".format(self.PATH))
            else:
                input("AnimatedText->load_templates: Путь {} указывает не на файл с шаблонами.".format(self.PATH))
        else:
            input("AnimatedText->load_templates: Файл с шаблонами отсутствует ({}).".format(self.PATH))

    def convert(self, word = None):
        # установка строки с текстом для перевода в надпись объязательна;
        if word is not None:
            rows = len(self.__dict__["TEMPLATES"]["sep"].split(".")) # высота надписи;
            # проверка валидности формата строки для перевода;
            if type(word) == str:
                # проверка размера строки;
                if len(word): # не пустая;
                    # активация заготовки;
                    self.VALUE = []
                    # перевод символов строки в верхний регистр, так как все символы в словаре надписей в верхнем регистре;
                    word = word.upper()
                    for i in range(len(word)):
                        # если символ строки найден в словаре надписей,
                        # то перевести символ строки в символ надписи;
                        if word[i] in self.__dict__["TEMPLATES"]: 
                            self.VALUE.append(self.__dict__["TEMPLATES"][word[i]].split("."))
                        # условие для вставки межсимвольного разделителя;
                        if i != len(word)-1:
                            self.VALUE.append(self.__dict__["TEMPLATES"]["sep"].split("."))
                    # сборка и сохранение надписи;
                    self.VALUE = ["".join([j[i] for j in self.VALUE]) for i in range(rows)]
            else:
                # пустая надпись (без данных);
                self.VALUE = [""] * rows
        else:
            input("AnimatedText->convert: Текст для перевода не задан.")

    def bordered(self, node = "#", borders=("", "", "", ""), fill=" ", align="<"):
        # обязательное условие для обрамления - ширина надписи;
        if self.WIDTH is not None:
            # проверка валидности формата надписи;
            if type(self.VALUE) == list:
                # корректировка ширины надписи: если фактическая ширина
                # надписи больше указаной, то заменить на фактическую;
                if len(self.VALUE[0]) > (self.WIDTH - 2 * len(node)):
                    self.WIDTH = len(self.VALUE[0])
                # пере
                tmp = []
                # формирование верхней границы надписи: node borders[0] node;
                if borders[0]:
                    tmp.append("".join([node,
                                        borders[0] * (self.WIDTH - 2 * len(node) + 2),
                                        node]))
                # формирование боковых границ надписи: borders[1] строка_данных borders[2];
                for i in self.VALUE:
                    tmp.append("".join([borders[1],
                                        "{:{}{}{}}".format(i, fill, align, self.WIDTH - 2 * len(node) + 2),
                                        borders[2]]))
                # формирование нижней границы надписи: node borders[3] node;
                if borders[3]:
                    tmp.append("".join([node, borders[3] * (self.WIDTH - 2 * len(node) + 2), node]))
                self.VALUE = tmp # переcохранение надписи;
            else:
                input("AnimatedText->bordered: Невалидный формат надписи.")
        else:
            input("AnimatedText->bordered: Заготовка надписи не создана.")

    def animate_cmd(self, pause = 0.1):
        # проверка наличия надписи;
        if self.VALUE is not None:
            for i in range(1, len(self.VALUE) + 1):
                # построчный вывод надписи с накоплением строк;
                print("\n".join(self.VALUE[:i]))
                # условие для очистки экрана консоли (анимация);
                if i < len(self.VALUE):
                    # очистка экрана консоли;
                    system("cls")
                # пауза между выводом строк надписи;
                sleep(pause)
        else:
            input("AnimatedText->animate_cmd: Заготовка анимированого текста не создана.")

class UI:
    """----------------------------------------------------------------------------------------------------
Класс для формирования игрового интерфейса
----------------------------------------------------------------------------------------------------
Шаблон игрового окна в консоли:
      #===========#===============================================================#===========#
      #  ИГРОК 1  #                        ХОДИТ XXXXXXXXX                        #  ИГРОК 2  #
      #===========#===============================================================#===========#
      # XXXXXXXXX #```````````````````````````````````````````````````````````````# XXXXXXXXX #
      #===========#```````````````````````````````````````````````````````````````#===========#
      # ЗДОРОВЬЕ  #```````````````````````````````````````````````````````````````# ЗДОРОВЬЕ  #
      #===========#```````````````````````````````````````````````````````````````#===========#
      #   000 %   #```````````````````````````````````````````````````````````````#   000 %   #
      #===========#===============================================================#===========#
      #XXXXXXXXXXX#                   ИНФОРМАЦИЯ О СДЕЛАНОМ ХОДЕ                  #XXXXXXXXXXX#
      #===========#===============================================================#===========#
----------------------------------------------------------------------------------------------------
1) Поля:
----------------------------------------------------------------------------------------------------
* HEIGHT - высота окна консоли;
* TITLE - поле, в котором хранится екземпляр класса AnimatedText;
* WIDTH - ширина окна консоли.
----------------------------------------------------------------------------------------------------
2) Методы:
----------------------------------------------------------------------------------------------------
2.1) __init__() - создание екземпляра текущего класса, ширину и высоту консольного окна, екземпляра
                  класса AnimatedText.
                  Входные данные: нет.
                  Выходные данные: нет.
----------------------------------------------------------------------------------------------------
2.2) menu_creator(title, items, menu_type) - генератор меню для выбоа одного из нескольких значений. 
                                             Входные данные:
                                             * title(str) - заголовок меню;
                                             * items(dict) - пункты меню (в формате номер(int):знач-
                                                             ение(str);
                                             * menu_type(str) - вертикальное "vertical" / горизонта-
                                                                льное "horizontal" меню (vertical по
                                                                умолчанию).
                                             Выходные данные:
                                             * option(int) - номер пункта меню из items.
----------------------------------------------------------------------------------------------------
2.3) print_window(queue, player_1, player_2, damage) - генератор игрового окна (вывод на екран).
                                                       Входные данные:
                                                       * queue(Player) - объект класса Player;
                                                       * player_1(Player) - объект класса Player
                                                                            (игрок 1);
                                                       * player_2(Player) - объект класса Player
                                                                            (игрок 2);
                                                       * damage(int) - размер урона / исцеления.
                                                       Выходные данные: нет.
----------------------------------------------------------------------------------------------------"""
    def __init__(self):
        # создание переменной для указания высоты окна консоли;
        self.HEIGHT = None
        # подключение класса работы с надписями;
        self.TITLE = AnimatedText()
        # создание переменной для указания ширины окна консоли;
        self.WIDTH = None

    def menu_creator(self, title, items, menu_type = "vertical", node = "#", border=("", "", "", ""), fill = " ", align = "<"):
        if None not in (title, items):
            if type(title) == str: # проверка формата заголовка меню;
                if len(title):
                    if type(items) == dict: # роверка формата пунктов меню;
                        if len(items): #;
                            self.TITLE.WIDTH = self.WIDTH - 2
                            while True:  # цикл повторяется до тех пор пока не будет выбран валидный пункт меню;
                                # вывод заголовка меню с центрированием и границами:
                                self.TITLE.VALUE = [title] # установка;
                                self.TITLE.bordered(node, border, fill, align) # обрамление;
                                print("\n".join(self.TITLE.VALUE)) # сборка и вывод;
                                if menu_type == "horizontal": # вывод горизонтального меню;
                                    # генератор пункта меню в формате №) название, соединение через пробел и установка для центрирования;
                                    self.TITLE.VALUE = [" ".join(["{}) {}".format(key, items[key]) for key in sorted(items)])]
                                    self.TITLE.bordered(node, ("", border[1], border[2], border[3]), fill, align) # обрамление;
                                if menu_type == "vertical": # вывод вертикального меню;
                                    tmp = []
                                    for key in sorted(items):
                                        self.TITLE.VALUE = ["{}) {}".format(key, items[key])] # генератор пункта меню в формате №) название;
                                        self.TITLE.bordered(node, ("", border[1], border[2], ""), fill, align) # обрамление;
                                        tmp.extend(self.TITLE.VALUE) # сохранение формы пункта;
                                    tmp.extend(["#{}#".format("=" * (self.WIDTH-2))]) # нижняя граниица меню;
                                    self.TITLE.VALUE = tmp # установка пунктов для центрирования;
                                print("\n".join(self.TITLE.VALUE)) # сборка и вывод пунктов меню;
                                option = input(":> ").strip() # выбор пользователя;
                                if option:
                                    if option.isnumeric(): # проверка формата выбраного значения;
                                        if int(option) in items: # валидация выбраного значения;
                                            return int(option) # возвращение номера выбраного пункта меню;
                                        else:
                                            input("Выбраный пункт отсутствует в списке выбора.")
                                    else:
                                        input("Вы должны ввести числовое значение.")
                                else:
                                    input("Вы не сделали выбор.")
                                system("cls")
                        else:
                            input("menu_creator: Пункты меню отсутствуют.")
                    else:
                        input("menu_creator: Невалидный формат пунктов меню.")
                else:
                    input("menu_creator: Невалидное значение заголовка меню.")
            else:
                input("menu_creator: Невалидный формат заголовка меню.")
        else:
            input("menu_creator: Заголовок и пункты меню не заданы.")
        '''
    def menu_creator(self, title = None, items = None, menu_type = "vertical", node = "#", borders=("", "", "", ""), fill = " ", align = "<"):
        # заголовок и пункты меню объязательны для установки;
        if None not in (title, items):
            # проверка валидности формата заголовка меню;
            if type(title) == str:
                # проверка валидности размера заголовка меню;
                if len(title):
                    # проверка валидности формата упаковки пунктов меню;
                    if type(items) == dict:
                        # проверка наличия пунктов меню;
                        if len(items):
                            # цикл повторяется до тех пор пока не будет выбран валидный пункт меню;
                            while True:
                                # вывод заголовка меню c границами:
                                self.TITLE.VALUE = [title]                             # установка;
                                self.TITLE.bordered(node, borders, fill) # обрамление;
                                print("\n".join(self.TITLE.VALUE))                     # сборка и вывод;
                                # вывод пунктов меню горизонтально;
                                if menu_type == "horizontal":
                                    # генератор пункта меню в формате №) название;
                                    self.TITLE.VALUE = [" ".join(["{}) {}".format(key,
                                                                                  items[key]) for key in sorted(items)])]
                                    self.TITLE.bordered(node, borders, fill) # обрамление;
                                # вывод пунктов меню вертикально;
                                if menu_type == "vertical":
                                    tmp = []
                                    for key in sorted(items):
                                        # генератор пункта меню в формате №) название;
                                        self.TITLE.VALUE = ["{}) {}".format(key, items[key])]
                                        # обрамление;
                                        self.TITLE.bordered(node, borders, fill)
                                        # сохранение формы пункта;
                                        tmp.extend(self.TITLE.VALUE)
                                    #  установка нижней граниицы меню;
                                    tmp.append(["#{}#".format("=" * (self.WIDTH - 2))])
                                    self.TITLE.VALUE = tmp
                                # сборка и вывод пунктов меню;
                                print("\n".join(self.TITLE.VALUE))
                                # выбор пользователя;
                                option = input(":> ").strip()
                                if option:
                                    # проверка формата выбраного значения;
                                    if option.isnumeric():
                                        # валидация выбраного значения;
                                        if int(option) in items:
                                            return int(option) # возвращение номера выбраного пункта меню;
                                        else:
                                            input("Выбраный пункт отсутствует в списке выбора.")
                                    else:
                                        input("Вы должны ввести числовое значение.")
                                else:
                                    input("Вы не сделали выбор.")
                                system("cls")
                        else:
                            input("menu_creator: Пункты меню отсутствуют.")
                    else:
                        input("menu_creator: Невалидный формат пунктов меню.")
                else:
                    input("menu_creator: Невалидное значение заголовка меню.")
            else:
                input("menu_creator: Невалидный формат заголовка меню.")
        else:
            input("menu_creator: Заголовок и пункты меню не заданы.")
    '''
    def print_window(self, queue = None, PLAYER_1 = None, PLAYER_2 = None, damage = None):
        # значения очередности хода, игроков, урона / исцеления обязательны для установки;
        if None not in (queue, PLAYER_1, PLAYER_2, damage):
            # подготовка информационного сообщения о том, кто из игроков ходил;
            info1 = "ХОДИТ {}".format(queue.NAME)
            # проверка валидности формата урона;
            if type(damage) == int:
                # подготовка сообщения о результате хода игрока и генерация надписи;
                info2 = None
                # получен урон;
                if damage < 0:
                    info2 = "{} ПОЛУЧИЛ УРОН {:03}%".format(PLAYER_2.NAME if PLAYER_1.NAME == queue.NAME else PLAYER_1.NAME, damage)
                    # abs(damage) так как урон отрицателен;
                    self.TITLE.convert("-{:03}%".format(abs(damage)))
                # исцеление;
                elif damage > 0:
                    info2 = "{} ИСЦЕЛЕН (+{:03}%)".format(queue.NAME, damage)
                    self.TITLE.convert("+{:03}%".format(damage))
                # окно в отсутствии ходов;
                else:
                    info2 = "" #;
                    self.TITLE.convert("") #;
                # ширина правой колонки согласно шаблону (в описании класса);
                right_column_width = 11
                # ширина центральной колонки равна ширине надписи + 2 для отступа от границ ;
                center_column_width = len(self.TITLE.VALUE[0]) + 2
                # ширина левой колонки согласно шаблону (в описании класса);
                left_column_width = 11
                # вычисление ширины окна консоли (подгоняется под ширину игрового окна);
                self.WIDTH = left_column_width + center_column_width + right_column_width + 4
                self.HEIGHT = 14
                # изменение размера консольного окна;
                system("mode con cols={} lines={}".format(self.WIDTH, self.HEIGHT))
                # 1 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:=^{}}".format("",                                center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
                # 2 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ИГРОК 1",                         left_column_width),
                                              "{: ^{}}".format(info1,                             center_column_width),
                                              "{: ^{}}".format("ИГРОК 2",                         right_column_width)])))
                # 3 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:=^{}}".format("",                                center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
                # 4 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ИМЯ",                             left_column_width),
                                              "{: ^{}}".format(self.TITLE.VALUE[0],               center_column_width),
                                              "{: ^{}}".format("ИМЯ",                             right_column_width)])))
                # 5 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:`^{}}".format(self.TITLE.VALUE[1],               center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
                # 6 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format(PLAYER_1.NAME,                     left_column_width),
                                              "{:`^{}}".format(self.TITLE.VALUE[2],               center_column_width),
                                              "{: ^{}}".format(PLAYER_2.NAME,                     right_column_width)])))
                # 7 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:`^{}}".format(self.TITLE.VALUE[3],               center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
                # 8 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ЗДОРОВЬЕ",                        left_column_width),
                                              "{:`^{}}".format(self.TITLE.VALUE[4],               center_column_width),
                                              "{: ^{}}".format("ЗДОРОВЬЕ",                        right_column_width)])))
                # 9 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:=^{}}".format("",                                center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
                # 10 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("{:03} %".format(PLAYER_1.HEALTH), left_column_width),
                                              "{: ^{}}".format(info2,                             center_column_width),
                                              "{: ^{}}".format("{:03} %".format(PLAYER_2.HEALTH), right_column_width)])))
                # 11 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("",                                left_column_width),
                                              "{:=^{}}".format("",                                center_column_width),
                                              "{:=^{}}".format("",                                right_column_width)])))
            else:
                input("Game->print_window: Невалидный формат очередности хода.")
        else:
            input("Game->print_window: Очередность хода или уровень урона не заданы.")
