"""Simülasyon dünyası ve dikdörtgen engeller."""

import pygame

from config import (
    ACTIVE_AREA_RECT,
    BACKGROUND_COLOR,
    OBSTACLE_BORDER_COLOR,
    OBSTACLE_COLOR,
    OBSTACLE_LABEL_COLOR,
    WORLD_BORDER_COLOR,
    WORLD_BORDER_THICKNESS,
)


class World:
    """Engelleri ve simülasyon alanının sınırlarını yönetir."""

    def __init__(self, size: tuple[int, int]) -> None:
        self.width, self.height = size
        self.active_area = pygame.Rect(ACTIVE_AREA_RECT)
        self.obstacles: list[pygame.Rect] = self._create_default_obstacles()
        self.boundaries: list[pygame.Rect] = self._create_boundaries()

    def _create_default_obstacles(self) -> list[pygame.Rect]:
        """Başlangıçta ekranda bulunacak engelleri oluşturur."""
        return [
            pygame.Rect(120, 125, 170, 45),
            pygame.Rect(390, 115, 50, 180),
            pygame.Rect(610, 140, 180, 45),
            pygame.Rect(170, 335, 60, 145),
            pygame.Rect(350, 420, 210, 50),
            pygame.Rect(680, 335, 55, 170),
        ]

    def _create_boundaries(self) -> list[pygame.Rect]:
        """Aktif alanın dışını dört sanal duvar olarak tanımlar."""
        area = self.active_area

        return [
            pygame.Rect(0, 0, self.width, area.top),
            pygame.Rect(0, area.bottom, self.width, self.height - area.bottom),
            pygame.Rect(0, area.top, area.left, area.height),
            pygame.Rect(area.right, area.top, self.width - area.right, area.height),
        ]

    @property
    def collision_rects(self) -> tuple[pygame.Rect, ...]:
        """Sensör ve çarpışma kontrollerinde kullanılacak tüm yüzeyler."""
        return tuple(self.obstacles + self.boundaries)

    def add_obstacle(self, rect: pygame.Rect) -> None:
        """Dünyaya yeni bir dikdörtgen engel ekler."""
        self.obstacles.append(rect.copy())

    def draw(
        self,
        surface: pygame.Surface,
        label_font: pygame.font.Font | None = None,
    ) -> None:
        """Dünya sınırlarını ve bütün engelleri ekrana çizer."""
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.active_area)

        for obstacle in self.obstacles:
            pygame.draw.rect(surface, OBSTACLE_COLOR, obstacle)
            pygame.draw.rect(surface, OBSTACLE_BORDER_COLOR, obstacle, width=2)

            if label_font is not None:
                label = label_font.render(
                    "Engel",
                    True,
                    OBSTACLE_LABEL_COLOR,
                )
                surface.blit(label, label.get_rect(center=obstacle.center))

        pygame.draw.rect(
            surface,
            WORLD_BORDER_COLOR,
            self.active_area,
            width=WORLD_BORDER_THICKNESS,
        )
