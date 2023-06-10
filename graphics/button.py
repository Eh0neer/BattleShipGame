"""Module for buttons."""

from typing import Optional

import pygame

from elements.constants import BLACK, BLOCK_SIZE, GREEN_BLUE, UPPER_MARGIN, WHITE
from graphics.drawing import screen

pygame.init()


class Button:
    """
    Создает кнопки и печатает поясняющее сообщение для них
    ----------
    Атрибуты:
        __title (str): название кнопки (название)
        __message (str): пояснительное сообщение для печати на экране
        __x_start (int): смещение по горизонтали, где начать рисовать кнопку
        __y_start (int): вертикальное смещение, с которого начинается отрисовка кнопки
        __rect_for_draw (кортеж из четырех целых): прямоугольник кнопки, который нужно нарисовать
        rect (pygame Rect): объект pygame Rect
        __rect_for_button_title (кортеж из двух целых чисел): прямоугольник внутри кнопки для печати в нем текста
        __color (tuple): цвет кнопки (по умолчанию — ЧЕРНЫЙ, при наведении — ЗЕЛЕНЫЙ_СИНИЙ, отключен — СВЕТЛО-СЕРЫЙ)
    ----------
    Методы:
    draw(): рисует кнопку в виде прямоугольника цвета (по умолчанию ЧЕРНЫЙ)
    change_color_on_hover(): рисует кнопку в виде прямоугольника GREEN_BLUE цвета.
    print_message(): печатает пояснительное сообщение рядом с кнопкой
    """

    def __init__(
        self, x_offset: int, button_title: str, message_to_show: str, font: pygame.font.Font, color: tuple = BLACK
    ) -> None:
        self.__title = button_title
        self.__font = font
        self.__title_width, self.__title_height = self.__font.size(self.__title)
        self.__message = message_to_show
        self.__button_width = self.__title_width + BLOCK_SIZE
        self.__button_height = self.__title_height + BLOCK_SIZE
        self.__x_start = x_offset
        self.__y_start = UPPER_MARGIN + 10 * BLOCK_SIZE + self.__button_height
        self.__rect_for_draw = self.__x_start, self.__y_start, self.__button_width, self.__button_height
        self.rect = pygame.Rect(self.__rect_for_draw)
        self.__rect_for_button_title = (
            self.__x_start + self.__button_width / 2 - self.__title_width / 2,
            self.__y_start + self.__button_height / 2 - self.__title_height / 2,
        )
        self.__color = color

    def draw(self, color: Optional[tuple] = None, text_color: tuple = WHITE) -> None:
        """
        Рисует кнопку в виде прямоугольника цвета (по умолчанию ЧЕРНЫЙ)
        Аргументы:
            color (кортеж, необязательный): цвет кнопки. По умолчанию нет (ЧЕРНЫЙ).
        """
        if not color:
            color = self.__color
        pygame.draw.rect(screen, color, self.__rect_for_draw)
        text_to_blit = self.__font.render(self.__title, True, text_color)
        screen.blit(text_to_blit, self.__rect_for_button_title)

    def change_color_on_hover(self, hover_color: tuple = GREEN_BLUE) -> None:
        """
        Кнопка рисует прямоугольник GREEN_BLUE цвета
        """
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.draw(hover_color)

    def print_message(self, text_color: tuple = BLACK) -> None:
        """
        Печатает поясняющее сообщение рядом с кнопкой
        """
        message_width, message_height = self.__font.size(self.__message)
        rect_for_message = (
            self.__x_start / 2 - message_width / 2,
            self.__y_start + self.__button_height / 2 - message_height / 2,
        )
        text = self.__font.render(self.__message, True, text_color)
        screen.blit(text, rect_for_message)
