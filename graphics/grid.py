"""Создает сетки на поле."""

import pygame

from elements.constants import (
    BLOCK_SIZE,
    FONT_SIZE,
    LEFT_MARGIN,
    LINE_WIDTH,
    UPPER_MARGIN,
)
from graphics.drawing import screen


class Grid:
    """
    Класс для рисования сеток и добавления к ним заголовков, цифр и букв.
    ----------
    Атрибуты:
        title (str): Имя игрока будет отображаться в верхней части его сетки.
        offset (int): Где начинается сетка (количество блоков)
                (обычно 0 для компьютера и 15 для человека)
    ----------
    Методы:
    __draw_grid(): рисует две сетки для обоих игроков
    __add_nums_letters_to_grid(): рисует числа от 1 до 10 по вертикали и добавляет буквы ниже по горизонтали.
        линии для обеих сеток
    __sign_grid(): помещает имена игроков (титулы) в центр над сетками.
    """

    def __init__(
        self,
        *,
        title: str,
        offset: int,
        font: pygame.font.Font,
        letters: list,
        line_color: tuple,
        text_color: tuple,
    ) -> None:
        """
        title(str): Имя игрока будет отображаться в верхней части его сетки.
        offset (int): Где начинается сетка (количество блоков)
        (обычно 0 для компьютера и 15 для человека)
        """
        self.title = title
        self.offset = offset
        self.font = font
        self.letters = letters
        self.line_color = line_color
        self.text_color = text_color
        self.__draw()
        self.__add_numbers_and_letters()
        self.__sign_grid()

    def __draw(self) -> None:
        """
        Рисует две сетки для обоих игроков
        """
        for i in range(11):
            hor_line_start_pos = (LEFT_MARGIN + self.offset * BLOCK_SIZE, UPPER_MARGIN + i * BLOCK_SIZE)
            hor_line_end_pos = (LEFT_MARGIN + (10 + self.offset) * BLOCK_SIZE, UPPER_MARGIN + i * BLOCK_SIZE)
            ver_line_start_pos = (LEFT_MARGIN + (i + self.offset) * BLOCK_SIZE, UPPER_MARGIN)
            ver_line_end_pos = (LEFT_MARGIN + (i + self.offset) * BLOCK_SIZE, UPPER_MARGIN + 10 * BLOCK_SIZE)

            # Horizontal lines
            pygame.draw.line(
                screen,
                self.line_color,
                hor_line_start_pos,
                hor_line_end_pos,
                LINE_WIDTH,
            )
            # Vertical lines
            pygame.draw.line(
                screen,
                self.line_color,
                ver_line_start_pos,
                ver_line_end_pos,
                LINE_WIDTH,
            )

    def __add_numbers_and_letters(self) -> None:
        """
        Рисует цифры от 1 до 10 по вертикали и добавляет буквы ниже по горизонтали
        линии для обеих сеток
        """
        for i in range(10):
            num_ver = self.font.render(str(i + 1), True, self.text_color)
            letters_hor = self.font.render(self.letters[i], True, self.text_color)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()
            numbers_blit_destination = (
                LEFT_MARGIN - (BLOCK_SIZE // 2 + num_ver_width // 2) + self.offset * BLOCK_SIZE,
                UPPER_MARGIN + i * BLOCK_SIZE + (BLOCK_SIZE // 2 - num_ver_height // 2),
            )
            letters_blit_destination = (
                LEFT_MARGIN + i * BLOCK_SIZE + (BLOCK_SIZE // 2 - letters_hor_width // 2) + self.offset * BLOCK_SIZE,
                UPPER_MARGIN + 10 * BLOCK_SIZE,
            )

            # Numbers (vertical)
            screen.blit(num_ver, numbers_blit_destination)
            # Letters (horizontal)
            screen.blit(letters_hor, letters_blit_destination)

    def __sign_grid(self) -> None:
        """
        Помещает имена игроков (титулы) в центр над сетками
        """
        player = self.font.render(self.title, True, self.text_color)
        sign_width = player.get_width()
        screen.blit(
            player,
            (
                LEFT_MARGIN + 5 * BLOCK_SIZE - sign_width // 2 + self.offset * BLOCK_SIZE,
                UPPER_MARGIN - BLOCK_SIZE // 2 - FONT_SIZE,
            ),
        )
