from os import getcwd, system, stat
from os.path import isfile, exists
from time import sleep

class AnimatedText:
    """-------------------------------------------------------------------------------------------------------
Класс создания игровых надписей
-------------------------------------------------------------------------------------------------------
1) Поля:
-------------------------------------------------------------------------------------------------------
* path(str) - путь из текущей папки модуля к файлу с шаблонами символов, чисел и отдельных спецзнаков;
* value(list) - хранилище для надписи;
* width(int) - ширина надписи (в символах).
-------------------------------------------------------------------------------------------------------
2) Методы:
-------------------------------------------------------------------------------------------------------
2.1) __init__() - создание екземпляра класса, заготовки для хранения надписи.
     Входные параметры: нет.
     Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.2) load_templates() - загрузка шаблонов символов, чисел и отдельных спецзнаков из файла path.
     Входные параметры: нет.
     Выходные параметры:
     * словарь templates.
-------------------------------------------------------------------------------------------------------
2.3) convert(word) - конвертация символной строки в надпись, создает поле value для сохранения надписив классе. 
     Входные параметры:
     * word(str) - символьная строка (None по умолчанию).
     Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.4) bordered(node, borders, fill, align) - обрамляет надпись рамкойи пересохраняет её в поле класса
     value.
     Входные параметры:
     * node(str) - обозначение углов рамки, при построении границ надписи;
     * borders(set) - набор обозначений границ надписи (верхняя, левая, правая, нижняя);
     * fill(str) - заполнитель пространства между границами и данными;
     * align(str) - виравнивание данных между границами рамки.
     Выходные параметры: нет.
-------------------------------------------------------------------------------------------------------
2.4) animate_cmd(pause) - вывод надписи построчно, с установленной задержкой времени.
     Входные параметры:
     * pause - задержка времени между выводом строк в сек. (1 сек. по умолчанию).
     Выходные параметры: нетsSsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss.
-------------------------------------------------------------------------------------------------------"""

    path = "{}/char_templates.dat".format(getcwd())

    def __init__(self):
        # загрузка шаблонов символов необходимых для создания надписей;
        self.load_templates()
        # пустая заготовка для хранения надписи;
        self.value = None
        # ширина надписи;
        self.width = None
    
    def load_templates(self):
        # проверка валидности адреса с файлом шаблонов;
        if exists(self.path):
            # проверка наличия файла с шаблонами по заданому адресу;
            if isfile(self.path):
                # проверка наличия шаблонов в файле;
                if stat(self.path):
                    file = open(self.path, "rb")
                    if file:
                        # загрузка шаблонов из файла;
                        lines = [line.strip("\ufeff") for line in file.read().decode("utf-8").split("\n") if line.strip()]
                        file.close()
                        # преобразование данных из файла в словарь надписей;
                        self.__dict__["templates"] = dict()
                        for line in range(len(lines)):
                            # проверка валидности шаблона из файла;
                            if ":" in lines[line] and lines[line].count(":") == 1:
                                (key, value) = [item.strip() for item in lines[line].split(":")]
                                key = " " if key == "" else key
                                # сохранение шаблона в словарь;
                                self.__dict__["templates"][key] = value
                            else:
                                input(lines[line])
                                input("PaintText->load_templates: Невалидное значение шаблона ({}).".format(line + 1))
                                exit(1)
                        # количество полей в классе еквивалентно количеству значений загруженых из файла;
                        if not (len(self.__dict__["templates"]) == len(lines)):
                            input("AnimatedText->load_templates: Данные с файла шаблонов потеряны ({})!".format(len(self.__dict__["templates"])))
                    else:
                        input("AnimatedText->load_templates: Файл с шаблонами не загружен ({}).".format(self.path))
                else:
                    input("AnimatedText->load_templates: Файл с шаблонами пуст ({})".format(self.path))
            else:
                input("AnimatedText->load_templates: Путь {} указывает не на файл с шаблонами.".format(self.path))
        else:
            input("AnimatedText->load_templates: Файл с шаблонами отсутствует ({}).".format(self.path))

    def convert(self, word = None):
        # установка строки с текстом для перевода в надпись объязательна;
        if word is not None:
            rows = len(self.__dict__["templates"]["sep"].split(".")) # высота надписи;
            # проверка валидности формата строки для перевода;
            if type(word) == str:
                # проверка размера строки;
                if len(word): # не пустая;
                    # активация заготовки;
                    self.value = []
                    # перевод символов строки в верхний регистр, так как все символы в словаре надписей в верхнем регистре;
                    word = word.upper()
                    for i in range(len(word)):
                        # если символ строки найден в словаре надписей,
                        # то перевести символ строки в символ надписи;
                        if word[i] in self.__dict__["templates"]: 
                            self.value.append(self.__dict__["templates"][word[i]].split("."))
                        # условие для вставки межсимвольного разделителя;
                        if i != len(word)-1:
                            self.value.append(self.__dict__["templates"]["sep"].split("."))
                    # сборка и сохранение надписи;
                    self.value = ["".join([j[i] for j in self.value]) for i in range(rows)]
            else:
                # пустая надпись (без данных);
                self.value = [""] * rows
        else:
            input("AnimatedText->convert: Текст для перевода не задан.")

    def bordered(self, node="#", borders=("", "", "", ""), fill=" ", align="<"):
        # обязательное условие для обрамления - ширина надписи;
        if self.width is not None:
            # проверка валидности формата надписи;
            if type(self.value) == list:
                # корректировка ширины надписи: если фактическая ширина
                # надписи больше указаной, то заменить на фактическую;
                if len(self.value[0]) > (self.width - 2 * len(node)):
                    self.width = len(self.value[0])
                # пере
                tmp = []
                # формирование верхней границы надписи: node borders[0] node;
                if borders[0]:
                    tmp.append("".join([node,
                                        borders[0] * (self.width - 2 * len(node) + 2),
                                        node
                                        ]
                                       )
                               )
                # формирование боковых границ надписи: borders[1] строка_данных borders[2];
                for i in self.value:
                    tmp.append("".join([borders[1],
                                        "{:{}{}{}}".format(i, fill, align, self.width - 2 * len(node) + 2),
                                        borders[2]
                                        ]
                                       )
                               )
                # формирование нижней границы надписи: node borders[3] node;
                if borders[3]:
                    tmp.append("".join([node, borders[3] * (self.width - 2 * len(node) + 2), node]))
                self.value = tmp # переcохранение надписи;
            else:
                input("AnimatedText->bordered: Невалидный формат надписи.")
        else:
            input("AnimatedText->bordered: Заготовка надписи не создана.")

    def animate_cmd(self, pause=0.1):
        # проверка наличия надписи;
        if self.value is not None:
            for i in range(1, len(self.value) + 1):
                # построчный вывод надписи с накоплением строк;
                print("\n".join(self.value[:i]))
                # условие для очистки экрана консоли (анимация);
                if i < len(self.value):
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
2.2) menu_creator(title, items, menu_type, borbers, fill, align) - генератор меню для выбоа одного
                                                                   из нескольких значений. 
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
        self.height = None
        # подключение класса работы с надписями;
        self.title = AnimatedText()
        # создание переменной для указания ширины окна консоли;
        self.width = None

    def menu_creator(self, title, items, menu_type="vertical", node="#", border=("", "", "", ""), fill=" ", align="<"):
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
                            self.title.width = self.width - 2
                            # цикл повторяется до тех пор пока не будет выбран валидный пункт меню;
                            while True:
                                # вывод заголовка меню c границами:
                                # установка;
                                self.title.value = [title]
                                # обрамление;
                                self.title.bordered(node, border, fill, align)
                                # сборка и вывод;
                                print("\n".join(self.title.value))
                                # вывод пунктов меню горизонтально;
                                if menu_type == "horizontal":
                                    # генератор пункта меню в формате №) название, соединение через пробел и установка для центрирования;
                                    self.title.value = [" ".join(["{}) {}".format(key, items[key]) for key in sorted(items)])]
                                    # обрамление;
                                    self.title.bordered(node, ("", border[1], border[2], border[3]), fill, align)
                                # вывод пунктов меню вертикально;
                                if menu_type == "vertical":
                                    tmp = []
                                    for key in sorted(items):
                                        # генератор пункта меню в формате №) название;
                                        self.title.value = ["{}) {}".format(key, items[key])]
                                        # обрамление;
                                        self.title.bordered(node, ("", border[1], border[2], ""), fill, align)
                                        # сохранение формы пункта;
                                        tmp.extend(self.title.value)
                                    #  установка нижней граниицы меню;
                                    tmp.extend(["#{}#".format("=" * (self.width-2))])
                                    # установка пунктов для центрирования;
                                    self.title.value = tmp
                                # сборка и вывод пунктов меню;
                                print("\n".join(self.title.value))
                                # выбор пользователя;
                                option = input(":> ").strip()
                                if option:
                                    # проверка формата выбраного значения;
                                    if option.isnumeric():
                                        # валидация выбраного значения;
                                        if int(option) in items:
                                            # возвращение номера выбраного пункта меню;
                                            return int(option)
                                        else:
                                            input("Выбраный пункт отсутствует в списке выбора.")
                                    else:
                                        input("Вы должны ввести числовое значение.")
                                else:
                                    input("Вы не сделали выбор.")
                                system("cls")
                        else:
                            input("UI->menu_creator: Пункты меню отсутствуют.")
                    else:
                        input("UI->menu_creator: Невалидный формат пунктов меню.")
                else:
                    input("UI->menu_creator: Невалидное значение заголовка меню.")
            else:
                input("UI->menu_creator: Невалидный формат заголовка меню.")
        else:
            input("UI->menu_creator: Заголовок и пункты меню не заданы.")

    def print_window(self, queue=None, player_1=None, player_2=None, damage=None):
        # значения очередности хода, игроков, урона / исцеления обязательны для установки;
        if None not in (queue, player_1, player_2, damage):
            # подготовка информационного сообщения о том, кто из игроков ходил;
            info1 = "ХОДИТ {}".format(queue.name)
            # проверка валидности формата урона;
            if type(damage) == int:
                # подготовка сообщения о результате хода игрока и генерация надписи;
                info2 = None
                # получен урон;
                if damage < 0:
                    info2 = "{} ПОЛУЧИЛ УРОН -{:03}%".format(player_2.name if player_1.name == queue.name else player_1.name, abs(damage))
                    # abs(damage) так как урон отрицателен;
                    self.title.convert("-{:03}%".format(abs(damage)))
                # исцеление;
                elif damage > 0:
                    info2 = "{} ИСЦЕЛЕН (+{:03}%)".format(queue.name, damage)
                    self.title.convert("+{:03}%".format(damage))
                # окно в отсутствии ходов;
                else:
                    info2 = ""
                    self.title.convert("")
                # ширина правой колонки согласно шаблону (в описании класса);
                right_column_width = 11
                # ширина центральной колонки равна ширине надписи + 2 для отступа от границ ;
                center_column_width = len(self.title.value[0]) + 2
                # ширина левой колонки согласно шаблону (в описании класса);
                left_column_width = 11
                # вычисление ширины окна консоли (подгоняется под ширину игрового окна);
                self.width = left_column_width + center_column_width + right_column_width + 4
                self.height = 14
                # изменение размера консольного окна;
                system("mode con cols={} lines={}".format(self.width, self.height))
                # 1 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:=^{}}".format("", center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 2 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ИГРОК 1", left_column_width),
                                              "{: ^{}}".format(info1, center_column_width),
                                              "{: ^{}}".format("ИГРОК 2", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 3 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:=^{}}".format("", center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 4 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ИМЯ", left_column_width),
                                              "{: ^{}}".format(self.title.value[0], center_column_width),
                                              "{: ^{}}".format("ИМЯ", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 5 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:`^{}}".format(self.title.value[1], center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 6 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format(player_1.name, left_column_width),
                                              "{:`^{}}".format(self.title.value[2], center_column_width),
                                              "{: ^{}}".format(player_2.name, right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 7 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:`^{}}".format(self.title.value[3], center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 8 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("ЗДОРОВЬЕ", left_column_width),
                                              "{:`^{}}".format(self.title.value[4], center_column_width),
                                              "{: ^{}}".format("ЗДОРОВЬЕ", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 9 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:=^{}}".format("", center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 10 строка шаблона;
                print("#{}#".format("#".join(["{: ^{}}".format("{:03} %".format(player_1.health), left_column_width),
                                              "{: ^{}}".format(info2, center_column_width),
                                              "{: ^{}}".format("{:03} %".format(player_2.health), right_column_width)
                                              ]
                                             )
                                    )
                      )
                # 11 строка шаблона;
                print("#{}#".format("#".join(["{:=^{}}".format("", left_column_width),
                                              "{:=^{}}".format("", center_column_width),
                                              "{:=^{}}".format("", right_column_width)
                                              ]
                                             )
                                    )
                      )
            else:
                input("UI->print_window: Невалидный формат очередности хода.")
        else:
            input("UI->print_window: Очередность хода или уровень урона не заданы.")
