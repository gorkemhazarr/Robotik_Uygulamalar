"""Simülasyon arayüzünde kullanılan yardımcı bileşenler."""

import pygame

from config import (
    INFO_PANEL_HEIGHT,
    OBSTACLE_LABEL_FONT_SIZE,
    PANEL_BACKGROUND_COLOR,
    PANEL_BORDER_COLOR,
    PANEL_FONT_SIZE,
    PANEL_HEIGHT,
    PANEL_MARGIN,
    PANEL_TEXT_COLOR,
)


class InfoPanel:
    """Sensör, motor ve robot durumunu ekranın üstünde gösterir."""

    def __init__(self, screen_width: int) -> None:
        self.background_rect = pygame.Rect(
            0,
            0,
            screen_width,
            INFO_PANEL_HEIGHT,
        )
        self.rect = pygame.Rect(
            PANEL_MARGIN,
            PANEL_MARGIN,
            screen_width - PANEL_MARGIN * 2,
            PANEL_HEIGHT,
        )
        self.font = pygame.font.Font(None, PANEL_FONT_SIZE)
        self.obstacle_font = pygame.font.Font(
            None,
            OBSTACLE_LABEL_FONT_SIZE,
        )

    def draw(
        self,
        surface: pygame.Surface,
        sensor_readings: dict[str, float],
        left_motor_speed: float,
        right_motor_speed: float,
        robot_status: str,
    ) -> None:
        """Güncel simülasyon değerlerini iki satır halinde çizer."""
        pygame.draw.rect(
            surface,
            PANEL_BACKGROUND_COLOR,
            self.background_rect,
        )
        pygame.draw.line(
            surface,
            PANEL_BORDER_COLOR,
            (0, INFO_PANEL_HEIGHT - 1),
            (surface.get_width(), INFO_PANEL_HEIGHT - 1),
            width=2,
        )
        pygame.draw.rect(
            surface,
            PANEL_BACKGROUND_COLOR,
            self.rect,
            border_radius=6,
        )
        pygame.draw.rect(
            surface,
            PANEL_BORDER_COLOR,
            self.rect,
            width=2,
            border_radius=6,
        )

        sensor_text = (
            f"Ön: {sensor_readings['front']:.1f} px   "
            f"Sol: {sensor_readings['left']:.1f} px   "
            f"Sağ: {sensor_readings['right']:.1f} px"
        )
        motor_text = (
            f"Sol motor: {left_motor_speed:.1f}   "
            f"Sağ motor: {right_motor_speed:.1f}   "
            f"Durum: {robot_status}"
        )

        first_line = self.font.render(sensor_text, True, PANEL_TEXT_COLOR)
        second_line = self.font.render(motor_text, True, PANEL_TEXT_COLOR)
        surface.blit(first_line, (self.rect.x + 10, self.rect.y + 7))
        surface.blit(second_line, (self.rect.x + 10, self.rect.y + 31))
