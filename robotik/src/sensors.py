"""Sanal ultrasonik mesafe sensörü."""

import math
from collections.abc import Sequence

import pygame

from config import SENSOR_CLEAR_COLOR, SENSOR_HIT_COLOR, SENSOR_POINT_COLOR


class UltrasonicSensor:
    """Belirli bir yönde ışın göndererek en yakın engeli ölçer."""

    def __init__(
        self,
        name: str,
        relative_angle: float,
        max_distance: float,
    ) -> None:
        if max_distance <= 0:
            raise ValueError("Maksimum sensör mesafesi sıfırdan büyük olmalıdır.")

        self.name = name
        self.relative_angle = math.radians(relative_angle)
        self.max_distance = max_distance
        self.distance = max_distance
        self.origin = pygame.Vector2()
        self.end_point = pygame.Vector2()
        self.detected = False

    def measure(
        self,
        robot_position: tuple[float, float],
        robot_angle: float,
        robot_radius: float,
        obstacles: Sequence[pygame.Rect],
    ) -> float:
        """Işının ilk çarptığı dikdörtgene olan mesafeyi ölçer."""
        sensor_angle = robot_angle - self.relative_angle
        direction = pygame.Vector2(
            math.cos(sensor_angle),
            -math.sin(sensor_angle),
        )

        robot_center = pygame.Vector2(robot_position)
        self.origin = robot_center + direction * robot_radius
        nearest_distance = self.max_distance

        for obstacle in obstacles:
            hit_distance = self._ray_rect_distance(
                self.origin,
                direction,
                obstacle,
            )
            if hit_distance is not None:
                nearest_distance = min(nearest_distance, hit_distance)

        self.distance = nearest_distance
        self.detected = nearest_distance < self.max_distance
        self.end_point = self.origin + direction * nearest_distance
        return self.distance

    @staticmethod
    def _ray_rect_distance(
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        rect: pygame.Rect,
    ) -> float | None:
        """Işın ile eksen hizalı dikdörtgenin ilk kesişimini hesaplar."""
        near = -math.inf
        far = math.inf

        for start, step, minimum, maximum in (
            (origin.x, direction.x, rect.left, rect.right),
            (origin.y, direction.y, rect.top, rect.bottom),
        ):
            if math.isclose(step, 0.0, abs_tol=1e-9):
                if start < minimum or start > maximum:
                    return None
                continue

            first = (minimum - start) / step
            second = (maximum - start) / step
            axis_near, axis_far = sorted((first, second))
            near = max(near, axis_near)
            far = min(far, axis_far)

            if near > far:
                return None

        if far < 0:
            return None

        distance = max(near, 0.0)
        return distance if distance <= far else None

    def draw(self, surface: pygame.Surface) -> None:
        """Ölçüm ışınını ve varsa çarpışma noktasını çizer."""
        color = SENSOR_HIT_COLOR if self.detected else SENSOR_CLEAR_COLOR
        pygame.draw.line(surface, color, self.origin, self.end_point, width=2)

        if self.detected:
            pygame.draw.circle(surface, SENSOR_POINT_COLOR, self.end_point, 4)
