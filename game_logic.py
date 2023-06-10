"""Module for the logic behind the game."""

from random import choice
from typing import Callable

from elements.autoships import AutoShips

# ---COMPUTER DATA-----
computer_available_to_fire_set = {(x, y) for x in range(16, 26) for y in range(1, 11)}
around_last_computer_hit_set = set()

dotted_set_for_computer_not_to_shoot = set()
hit_blocks_for_computer_not_to_shoot = set()
last_hits_list = []
# --------------------

hit_blocks = set()
dotted_set = set()
destroyed_computer_ships = []

human_destroyed_ships_count = {4: 0, 3: 0, 2: 0, 1: 0, "#": 0}
computer_destroyed_ships_count = {4: 0, 3: 0, 2: 0, 1: 0, "#": 0}


def computer_shoots() -> tuple:
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора
    """
    # This global keyword and check for len(computer_available_to_fire_set) is solely for the play again option
    # when all the ships and blocks variables are re-initialized but computer_available_to_fire_set is not.
    global computer_available_to_fire_set
    if not computer_available_to_fire_set:
        computer_available_to_fire_set = {(x, y) for x in range(16, 26) for y in range(1, 11)}

    set_to_shoot_from = computer_available_to_fire_set
    if around_last_computer_hit_set:
        set_to_shoot_from = around_last_computer_hit_set
    # pygame.time.delay(500)
    computer_fired_block = choice(tuple(set_to_shoot_from))
    computer_available_to_fire_set.discard(computer_fired_block)
    return computer_fired_block


def check_hit_or_miss(
    *,
    fired_block: tuple,
    opponents_ships_list: list[list],
    computer_turn: bool,
    opponents_ships_list_original_copy: list,
    opponents_ships_set: set,
    computer: AutoShips,
) -> bool:
    """
    Проверяет, является ли блок, в который стрелял компьютер или человек, попаданием или промахом.
    Обновляет наборы с точками (в пропущенных блоках или в диагональных блоках вокруг блока попадания) и крестиками.
    (в хит-блоках).
    Удаляет уничтоженные корабли из списка кораблей.
    """
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            # This is to put dots before and after a destroyed ship
            # and to draw computer's destroyed ships (which are hidden until destroyed)
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(
                fired_block=fired_block,
                computer_turn=computer_turn,
                diagonal_only=diagonal_only,
            )
            elem.remove(fired_block)
            # This is to check who lost - if ships_set is empty
            opponents_ships_set.discard(fired_block)
            if computer_turn:
                last_hits_list.append(fired_block)
                update_around_last_computer_hit(
                    fired_block=fired_block,
                    computer_hits=True,
                )
            # If the ship is destroyed
            if not elem:
                update_destroyed_ships(
                    ind=ind,
                    computer_turn=computer_turn,
                    opponents_ships_list_original_copy=opponents_ships_list_original_copy,
                )
                if computer_turn:
                    last_hits_list.clear()
                    around_last_computer_hit_set.clear()
                else:
                    # Add computer's destroyed ship to the list to draw it (computer ships are hidden)
                    destroyed_computer_ships.append(computer.ships[ind])
            return True
    add_missed_block_to_dotted_set(
        fired_block=fired_block,
    )
    if computer_turn:
        update_around_last_computer_hit(
            fired_block=fired_block,
            computer_hits=False,
        )
    return False


def update_destroyed_ships(
    *,
    ind: int,
    computer_turn: bool,
    opponents_ships_list_original_copy: list,
) -> None:
    """
    Добавляет блоки до и после корабля в dotted_set, чтобы рисовать на них точки.
    Добавляет все блоки на корабле в набор hit_blocks для рисования крестиков внутри разрушенного корабля.
    """
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(
            fired_block=ship[i],
            computer_turn=computer_turn,
            diagonal_only=False,
        )
    if computer_turn:
        human_destroyed_ships_count[len(ship)] += 1
        human_destroyed_ships_count["#"] += 1
    else:
        computer_destroyed_ships_count[len(ship)] += 1
        computer_destroyed_ships_count["#"] += 1


def update_around_last_computer_hit(
    *,
    fired_block: tuple,
    computer_hits: bool,
) -> None:
    """
    Обновляет around_last_computer_hit_set (используется для выбора компьютера, с которого будет вестись огонь), если он
    попал в корабль, но не уничтожил его). Добавляет к этому набору вертикальные или горизонтальные блоки вокруг
    блок, который был последним ударом. Затем удаляет из набора те блоки, по которым стреляли, но не попали.
    around_last_computer_hit_set заставляет компьютер выбирать правильные блоки, чтобы быстро уничтожить корабль
    вместо случайной стрельбы по совершенно случайным блокам.
    """
    global around_last_computer_hit_set, computer_available_to_fire_set
    if computer_hits and fired_block in around_last_computer_hit_set:
        around_last_computer_hit_set = computer_hits_twice()
    elif computer_hits and fired_block not in around_last_computer_hit_set:
        computer_first_hit(fired_block=fired_block)
    elif not computer_hits:
        around_last_computer_hit_set.discard(fired_block)

    around_last_computer_hit_set -= dotted_set_for_computer_not_to_shoot
    around_last_computer_hit_set -= hit_blocks_for_computer_not_to_shoot
    computer_available_to_fire_set -= around_last_computer_hit_set
    computer_available_to_fire_set -= dotted_set_for_computer_not_to_shoot


def computer_first_hit(*, fired_block: tuple) -> None:
    """
    Добавляет блоки сверху, снизу, справа и слева от места попадания
    компьютером во временный набор, чтобы компьютер мог выбрать следующий снимок.
    Аргументы:
        fired_block (tuple): координаты блока, пораженного компьютером
    """
    x_hit, y_hit = fired_block
    if x_hit > 16:
        around_last_computer_hit_set.add((x_hit - 1, y_hit))
    if x_hit < 25:
        around_last_computer_hit_set.add((x_hit + 1, y_hit))
    if y_hit > 1:
        around_last_computer_hit_set.add((x_hit, y_hit - 1))
    if y_hit < 10:
        around_last_computer_hit_set.add((x_hit, y_hit + 1))


def computer_hits_twice() -> set:
    """
    Добавляет блоки до и после двух или более блоков корабля во временный список
    для компьютера, чтобы закончить корабль быстрее.
    Возвращает:
        set: временный набор блоков, где потенциально должен находиться корабль людей.
        для компьютера, чтобы стрелять из
    """
    last_hits_list.sort()
    new_around_last_hit_set = set()
    for i in range(len(last_hits_list) - 1):
        x1 = last_hits_list[i][0]
        x2 = last_hits_list[i + 1][0]
        y1 = last_hits_list[i][1]
        y2 = last_hits_list[i + 1][1]
        if x1 == x2:
            if y1 > 1:
                new_around_last_hit_set.add((x1, y1 - 1))
            if y2 < 10:
                new_around_last_hit_set.add((x1, y2 + 1))
        elif y1 == y2:
            if x1 > 16:
                new_around_last_hit_set.add((x1 - 1, y1))
            if x2 < 25:
                new_around_last_hit_set.add((x2 + 1, y1))
    return new_around_last_hit_set


def update_dotted_and_hit_sets(
    *,
    fired_block: tuple,
    computer_turn: bool,
    diagonal_only: bool = True,
) -> None:
    """
    Ставит точки в центре диагонали или вокруг блока, в который ударили (человеком или
    по компьютеру). Добавляет все диагональные блоки или выбранный круговой блок в отдельный набор
    блок: нажмите блок (кортеж)
    """
    global dotted_set, hit_blocks
    x, y = fired_block
    a = 15 * computer_turn
    b = 11 + 15 * computer_turn
    # Adds a block hit by computer to the set of his hits to later remove
    # them from the set of blocks available for it to shoot from
    hit_blocks_for_computer_not_to_shoot.add(fired_block)
    # Adds hit blocks on either grid1 (x:1-10) or grid2 (x:16-25)
    hit_blocks.add(fired_block)
    # Adds blocks in diagonal or all-around a block to respective sets
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (not diagonal_only or i != 0 and j != 0) and a < x + i < b and 0 < y + j < 11:
                add_missed_block_to_dotted_set(fired_block=(x + i, y + j))
    dotted_set -= hit_blocks


def add_missed_block_to_dotted_set(*, fired_block: tuple) -> None:
    """
    Добавляет fired_block к набору пропущенных выстрелов (если fired_block является промахом), чтобы потом рисовать на них точки.
    Также необходимо, чтобы компьютер удалял эти точечные блоки из набора доступных блоков, из которых он мог стрелять.
    """
    dotted_set.add(fired_block)
    dotted_set_for_computer_not_to_shoot.add(fired_block)


def is_ship_valid(*, ship_set: set, blocks_for_manual_drawing: set) -> bool:
    """
    Проверяет, не касается ли корабль других кораблей
    Аргументы:
        ship_set (set): набор с кортежами координат новых кораблей.
        blocks_for_manual_drawing (набор): Набор со всеми используемыми блоками для других кораблей, включая все блоки вокруг кораблей.

    Возвращает:
        Bool: True, если корабли не соприкасаются, в противном случае False.
    """
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def validate_ships_numbers(*, ship: list, num_ships_list: list) -> bool:
    """
    Проверяет, не превышает ли корабль определенной длины (1-4) необходимое количество (4-1).

    Аргументы:
        корабль (список): Список с координатами новых кораблей
        num_ships_list (список): список с номерами конкретных кораблей по соответствующим индексам.

    Возвращает:
        Bool: True, если количество кораблей определенной длины не больше необходимого,
            False, если таких кораблей достаточно.
    """
    return (5 - len(ship)) > num_ships_list[len(ship) - 1]


def update_used_blocks(*, ship: list, method: Callable) -> None:
    """
    Добавляет блоки корабля в набор использованных блоков, чтобы не использовать их снова.
    """
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                method((block[0] + i, block[1] + j))
