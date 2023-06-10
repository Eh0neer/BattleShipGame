"""Автоматически создает человеческие корабли."""

from random import choice, randint


class AutoShips:
    """
    Случайное создание всех кораблей игрока на сетке
    ----------
    Атрибуты:
        offset (int): Место начала сетки (в количестве блоков).
                (обычно 0 для компьютера и 15 для человека)
        available_blocks (набор кортежей): координаты всех блоков
                которые доступны для создания кораблей (обновляются каждый раз, когда создается корабль)
        ships_set (множество кортежей): все блоки, которые заняты кораблями
        ships (список списков): список всех отдельных кораблей (в виде списков)
    ----------
    Методы:
        __create_start_block(available_blocks):
            Случайным образом выбирает блок, с которого начнется создание корабля.
            Случайно выбирает горизонтальный или вертикальный тип корабля.
            Случайным образом выбирает направление (от стартового блока) - прямое или обратное.
            Возвращает три случайно выбранных значения
        __create_ship(number_of_blocks, available_blocks):
            Создает корабль заданной длины (количество_блоков), начиная со стартового блока
                возвращенного предыдущим методом, используя тип корабля и направление (изменяя его
                если выходит за пределы сетки), возвращенные предыдущим методом.
                Проверяет, является ли корабль действительным (не примыкает к другим кораблям и находится в пределах сетки)
                и добавляет его в список кораблей.
            Возвращает: список кортежей с координатами нового корабля.
        __get_new_block_for_ship(self, coor, direction, orientation, ship_coordinates):
            Проверяет, находятся ли новые отдельные блоки, добавляемые к кораблю в предыдущем методе.
                находятся в пределах сетки, в противном случае изменяет направление.
            Возвращает:
                направление (int): прямое или обратное
                увеличивает/уменьшает координаты последнего/первого блока в строящемся корабле
        __is_ship_valid(new_ship):
            Проверяет, все ли координаты корабля находятся в пределах доступного набора блоков.
            Возвращает: True или False
        __add_new_ship_to_set(new_ship):
            Добавляет все блоки из списка корабля в набор ships_set.
        __update_available_blocks_for_creating_ships(new_ship):
            Удаляет все блоки, занятые кораблем и вокруг него, из набора доступных блоков.
        __populate_grid():
            Создает необходимое количество кораблей каждого типа, вызывая метод create_ship.
                Добавляет каждый корабль в список кораблей, ships_set и обновляет доступные блоки.
            Возвращает: список всех кораблей
    """

    def __init__(self, offset: int) -> None:
        """
        Параметры:
        offset (int): Где начинается сетка (количество блоков)
                (обычно 0 для компьютера и 15 для человека)
        available_blocks (набор кортежей): координаты всех блоков
                доступные для создания кораблей (обновляются каждый раз при создании корабля)
        ship_set (набор кортежей): все блоки, занятые кораблями
        корабли (список списков): список всех отдельных кораблей (в виде списков)"""

        self.offset = offset
        self.available_blocks = {(x, y) for x in range(1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.__populate_grid()
        self.orientation = None
        self.direction = None

    def __create_start_block(self, available_blocks: set[tuple]) -> tuple:
        """
        Случайным образом выбирает блок, с которого начинается создание корабля.
        Случайным образом выбирает горизонтальный или вертикальный тип корабля
        Случайным образом выбирает направление (от начального блока) - прямо или наоборот
        Аргументы:
            available_blocks (набор кортежей): координаты всех блоков
                доступные для создания кораблей (обновляются каждый раз при создании корабля)
        Возвращает:
            int: x координата случайного блока
            int: координата y случайного блока
            int: 0=горизонтально (изменить x), 1=вертикально (изменить y)
            int: 1=прямой, -1=обратный
        """
        self.orientation = randint(0, 1)
        # -1 is left or down, 1 is right or up
        self.direction = choice((-1, 1))
        x, y = choice(tuple(available_blocks))
        return x, y, self.orientation, self.direction

    def __create_ship(self, number_of_blocks: int, available_blocks: set[tuple]) -> list:
        """
        Создает корабль заданной длины (number_of_blocks), начиная с начального блока
                возвращается предыдущим методом, используя тип корабля и направление (изменив его
                при выходе за пределы сетки) возвращается предыдущим методом.
                Проверяет, действителен ли корабль (не рядом с другими кораблями и в пределах сетки)
                и добавляет его в список кораблей.
        Аргументы:
            number_of_blocks (int): длина необходимого корабля
            available_blocks (набор): свободные блоки для создания кораблей
        Возвращает:
            list: список кортежей с координатами нового корабля
        """
        ship_coordinates = []
        x, y, self.orientation, self.direction = self.__create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not self.orientation:
                self.direction, x = self.__get_new_block_for_ship(x, self.direction, self.orientation, ship_coordinates)
            else:
                self.direction, y = self.__get_new_block_for_ship(y, self.direction, self.orientation, ship_coordinates)
        if self.__is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.__create_ship(number_of_blocks, available_blocks)

    def __get_new_block_for_ship(self, coor: int, direction: int, orientation: int, ship_coordinates: list) -> tuple:
        """
        Проверяет, добавляются ли новые отдельные блоки к кораблю предыдущим методом.
                находятся внутри сетки, в противном случае меняет направление.
        Аргументы:
            coor (int): координата x или y для увеличения/уменьшения
            направление (целое): 1 или -1
            ориентация (целое): 0 или 1
            ship_coordinates (список): координаты недостроенного корабля
        Возвращает:
            направление (int): прямое или обратное
            увеличенная/уменьшенная координата последнего/первого блока строящегося корабля (int)
        """
        self.direction = direction
        self.orientation = orientation
        if (coor <= 1 - self.offset * (self.orientation - 1) and self.direction == -1) or (
            coor >= 10 - self.offset * (self.orientation - 1) and self.direction == 1
        ):
            self.direction *= -1
            return self.direction, ship_coordinates[0][self.orientation] + self.direction
        return self.direction, ship_coordinates[-1][self.orientation] + self.direction

    def __is_ship_valid(self, new_ship: list) -> bool:
        """
        Проверьте, все ли координаты корабля находятся в пределах набора доступных блоков.
        Аргументы:
            new_ship (список): список кортежей с координатами вновь созданного корабля
        Возвращает:
            bool: правда или ложь
        """
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def __add_new_ship_to_set(self, new_ship: list) -> None:
        """
        Добавляет все блоки в списке кораблей в ship_set
        Аргументы:
            new_ship (список): список кортежей с координатами вновь созданного корабля
        """
        self.ships_set.update(new_ship)

    def __update_available_blocks_for_creating_ships(self, new_ship: list) -> None:
        """
        Удаляет все блоки, занятые кораблем и вокруг него, из набора доступных блоков
        Аргументы:
            new_ship ([type]): список кортежей с координатами вновь созданного корабля
        """
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if self.offset < (elem[0] + k) < 11 + self.offset and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard((elem[0] + k, elem[1] + m))

    def __populate_grid(self) -> list:
        """
        Создает необходимое количество кораблей каждого типа, вызывая метод create_ship.
                Добавляет каждый корабль в список кораблей, ship_set и обновляет доступные блоки.
        Возвращает:
            list: второй список всех кораблей
        """
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.__create_ship(number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.__add_new_ship_to_set(new_ship)
                self.__update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list
