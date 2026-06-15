"""Mobil robot modelinin görsel temsili."""

import math
from collections.abc import Sequence

import pygame

from actuators import DifferentialDriveActuator
from config import (
    FRONT_SENSOR_ANGLE,
    LEFT_SENSOR_ANGLE,
    RIGHT_SENSOR_ANGLE,
    ROBOT_BORDER_COLOR,
    ROBOT_COLOR,
    ROBOT_DIRECTION_COLOR,
    SENSOR_MAX_DISTANCE,
)
from sensors import UltrasonicSensor


class Robot:
    """Dairesel mobil robotun konumunu ve yönünü temsil eder."""

    def __init__(
        self,
        x: float,
        y: float,
        angle: float,
        radius: int,
        active_area: pygame.Rect,
        left_motor_speed: float,
        right_motor_speed: float,
        wheel_base: float,
    ) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = radius
        self.start_x = x
        self.start_y = y
        self.start_angle = angle
        self.initial_left_motor_speed = left_motor_speed
        self.initial_right_motor_speed = right_motor_speed
        self.active_area = active_area.copy()
        self.last_move_blocked = False
        self.last_collision_normal: pygame.Vector2 | None = None
        self.actuator = DifferentialDriveActuator(
            left_motor_speed=left_motor_speed,
            right_motor_speed=right_motor_speed,
            wheel_base=wheel_base,
        )
        self.sensors = {
            "front": UltrasonicSensor(
                "front",
                FRONT_SENSOR_ANGLE,
                SENSOR_MAX_DISTANCE,
            ),
            "left": UltrasonicSensor(
                "left",
                LEFT_SENSOR_ANGLE,
                SENSOR_MAX_DISTANCE,
            ),
            "right": UltrasonicSensor(
                "right",
                RIGHT_SENSOR_ANGLE,
                SENSOR_MAX_DISTANCE,
            ),
        }

    @property
    def position(self) -> tuple[float, float]:
        """Robot merkezinin konumunu döndürür."""
        return self.x, self.y

    @property
    def left_motor_speed(self) -> float:
        """Sol motor hızını döndürür."""
        return self.actuator.left_motor_speed

    @left_motor_speed.setter
    def left_motor_speed(self, speed: float) -> None:
        self.actuator.left_motor_speed = speed

    @property
    def right_motor_speed(self) -> float:
        """Sağ motor hızını döndürür."""
        return self.actuator.right_motor_speed

    @right_motor_speed.setter
    def right_motor_speed(self, speed: float) -> None:
        self.actuator.right_motor_speed = speed

    @property
    def sensor_readings(self) -> dict[str, float]:
        """Sensör adlarını son ölçülen mesafelerle eşleştirir."""
        return {
            name: sensor.distance
            for name, sensor in self.sensors.items()
        }

    @property
    def wall_clearances(self) -> dict[str, float]:
        """Robot gövdesi ile aktif alan duvarları arasındaki boşlukları verir."""
        return {
            "left": self.x - self.radius - self.active_area.left,
            "right": self.active_area.right - self.x - self.radius,
            "top": self.y - self.radius - self.active_area.top,
            "bottom": self.active_area.bottom - self.y - self.radius,
        }

    def update(
        self,
        dt: float,
        obstacles: Sequence[pygame.Rect] = (),
    ) -> None:
        """Motor hızlarına göre robotun konumunu ve yönünü günceller."""
        if dt < 0:
            raise ValueError("Zaman adımı negatif olamaz.")

        self.last_move_blocked = False
        self.last_collision_normal = None
        previous_position = self.position
        linear_velocity = self.actuator.linear_velocity
        angular_velocity = self.actuator.angular_velocity

        self.angle = (self.angle + angular_velocity * dt) % math.tau
        self.x += math.cos(self.angle) * linear_velocity * dt
        self.y -= math.sin(self.angle) * linear_velocity * dt

        collision_normal = self._collision_normal(obstacles)
        if self._keep_inside_active_area() or collision_normal is not None:
            self.x, self.y = previous_position
            self.actuator.stop()
            self.last_move_blocked = True
            self.last_collision_normal = collision_normal

    def reset(self) -> None:
        """Robotun konumunu, yönünü ve motorlarını başlangıca döndürür."""
        self.x = self.start_x
        self.y = self.start_y
        self.angle = self.start_angle
        self.last_move_blocked = False
        self.last_collision_normal = None
        self.actuator.set_speeds(
            self.initial_left_motor_speed,
            self.initial_right_motor_speed,
        )

    def update_sensors(self, obstacles: tuple[pygame.Rect, ...]) -> None:
        """Bütün ultrasonik sensörlerin ölçümlerini yeniler."""
        for sensor in self.sensors.values():
            sensor.measure(
                robot_position=self.position,
                robot_angle=self.angle,
                robot_radius=self.radius,
                obstacles=obstacles,
            )

    def _keep_inside_active_area(self) -> bool:
        """Robot merkezini güvenli hareket alanına clamp eder."""
        minimum_x = self.active_area.left + self.radius
        maximum_x = self.active_area.right - self.radius
        minimum_y = self.active_area.top + self.radius
        maximum_y = self.active_area.bottom - self.radius
        old_position = self.position

        self.x = max(minimum_x, min(self.x, maximum_x))
        self.y = max(minimum_y, min(self.y, maximum_y))
        return self.position != old_position

    def _collision_normal(
        self,
        obstacles: Sequence[pygame.Rect],
    ) -> pygame.Vector2 | None:
        """Temas varsa engelden robot merkezine bakan birim vektörü döndürür."""
        for obstacle in obstacles:
            nearest_x = max(obstacle.left, min(self.x, obstacle.right))
            nearest_y = max(obstacle.top, min(self.y, obstacle.bottom))
            normal = pygame.Vector2(
                self.x - nearest_x,
                self.y - nearest_y,
            )
            if normal.length_squared() < self.radius ** 2:
                if normal.length_squared() == 0:
                    normal = pygame.Vector2(self.position) - obstacle.center
                if normal.length_squared() == 0:
                    normal = pygame.Vector2(1.0, 0.0)
                return normal.normalize()

        return None

    def draw_sensors(self, surface: pygame.Surface) -> None:
        """Robotun bütün sensör ışınlarını ekrana çizer."""
        for sensor in self.sensors.values():
            sensor.draw(surface)

    def draw(self, surface: pygame.Surface) -> None:
        """Robot gövdesini ve baktığı yönü ekrana çizer."""
        center = (round(self.x), round(self.y))

        pygame.draw.circle(surface, ROBOT_COLOR, center, self.radius)
        pygame.draw.circle(
            surface,
            ROBOT_BORDER_COLOR,
            center,
            self.radius,
            width=2,
        )

        line_length = self.radius + 12
        direction_end = (
            round(self.x + math.cos(self.angle) * line_length),
            round(self.y - math.sin(self.angle) * line_length),
        )
        pygame.draw.line(
            surface,
            ROBOT_DIRECTION_COLOR,
            center,
            direction_end,
            width=5,
        )
        pygame.draw.circle(surface, ROBOT_DIRECTION_COLOR, direction_end, 4)
