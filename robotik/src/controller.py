"""Sensör verilerine dayalı basit engelden kaçma kontrolü."""

import math
from typing import TYPE_CHECKING

import pygame

from config import (
    CRITICAL_DISTANCE,
    FORWARD_SPEED,
    REVERSE_DURATION,
    REVERSE_SPEED,
    SAFE_DISTANCE,
    SIDE_RISK_DISTANCE,
    TURN_SPEED,
    WALL_AVOID_DISTANCE,
    WALL_DETOUR_DISTANCE,
    WALL_ESCAPE_RELEASE_DISTANCE,
    WALL_ESCAPE_SPEED,
    WALL_FINE_TURN_SPEED,
    WALL_TURN_TOLERANCE,
)

if TYPE_CHECKING:
    from robot import Robot


class ObstacleAvoidanceController:
    """Ultrasonik ölçümlere göre robotun motor hızlarını belirler."""

    def __init__(
        self,
        safe_distance: float = SAFE_DISTANCE,
        critical_distance: float = CRITICAL_DISTANCE,
        forward_speed: float = FORWARD_SPEED,
        turn_speed: float = TURN_SPEED,
        reverse_speed: float = REVERSE_SPEED,
        reverse_duration: float = REVERSE_DURATION,
        wall_avoid_distance: float = WALL_AVOID_DISTANCE,
        wall_detour_distance: float = WALL_DETOUR_DISTANCE,
        wall_escape_release_distance: float = WALL_ESCAPE_RELEASE_DISTANCE,
        side_risk_distance: float = SIDE_RISK_DISTANCE,
        wall_escape_speed: float = WALL_ESCAPE_SPEED,
        wall_fine_turn_speed: float = WALL_FINE_TURN_SPEED,
        wall_turn_tolerance: float = WALL_TURN_TOLERANCE,
    ) -> None:
        if critical_distance < 0 or safe_distance <= critical_distance:
            raise ValueError(
                "Güvenli mesafe, kritik mesafeden büyük olmalıdır."
            )
        if reverse_duration < 0:
            raise ValueError("Geri manevra süresi negatif olamaz.")

        self.safe_distance = safe_distance
        self.critical_distance = critical_distance
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        self.reverse_speed = reverse_speed
        self.reverse_duration = reverse_duration
        self.wall_avoid_distance = wall_avoid_distance
        self.wall_detour_distance = wall_detour_distance
        self.wall_escape_release_distance = wall_escape_release_distance
        self.side_risk_distance = side_risk_distance
        self.wall_escape_speed = wall_escape_speed
        self.wall_fine_turn_speed = wall_fine_turn_speed
        self.wall_turn_tolerance = wall_turn_tolerance
        self.reverse_time_remaining = 0.0
        self.wall_escape_active = False
        self.wall_detour_heading: float | None = None
        self.wall_detour_start: pygame.Vector2 | None = None
        self.obstacle_turn_direction: str | None = None
        self.current_action = "bekliyor"

    def reset(self) -> None:
        """Controller durumunu başlangıç değerlerine döndürür."""
        self.reverse_time_remaining = 0.0
        self.wall_escape_active = False
        self.wall_detour_heading = None
        self.wall_detour_start = None
        self.obstacle_turn_direction = None
        self.current_action = "bekliyor"

    def update(
        self,
        robot: "Robot",
        sensor_readings: dict[str, float],
        dt: float,
    ) -> None:
        """Sensör mesafelerini değerlendirip motor hızlarını günceller."""
        if dt < 0:
            raise ValueError("Zaman adımı negatif olamaz.")

        front = sensor_readings["front"]
        left = sensor_readings["left"]
        right = sensor_readings["right"]
        minimum_wall_clearance = min(robot.wall_clearances.values())

        if minimum_wall_clearance <= self.wall_avoid_distance:
            self.wall_escape_active = True

        if (
            self.wall_escape_active
            and minimum_wall_clearance >= self.wall_escape_release_distance
        ):
            self.wall_escape_active = False
            self.wall_detour_heading = None
            self.wall_detour_start = None

        if self.wall_escape_active:
            self.reverse_time_remaining = 0.0
            self.obstacle_turn_direction = None
            self._escape_wall(robot)
        elif self.reverse_time_remaining > 0:
            self.reverse_time_remaining = max(
                0.0,
                self.reverse_time_remaining - dt,
            )
            self._reverse(robot)
        elif front <= self.critical_distance:
            self.reverse_time_remaining = self.reverse_duration
            self._reverse(robot)
        elif front <= self.safe_distance:
            if self.obstacle_turn_direction is None:
                self.obstacle_turn_direction = (
                    "left" if left > right else "right"
                )

            if self.obstacle_turn_direction == "left":
                self._turn_left(robot)
            else:
                self._turn_right(robot)
        else:
            self.obstacle_turn_direction = None
            if left <= self.side_risk_distance:
                self._turn_right(robot)
            elif right <= self.side_risk_distance:
                self._turn_left(robot)
            else:
                self._move_forward(robot)

    def _escape_wall(
        self,
        robot: "Robot",
    ) -> None:
        """Robotu kararlı biçimde aktif alanın merkezine yöneltir."""
        if robot.last_move_blocked and robot.last_collision_normal is not None:
            self._start_wall_detour(robot)

        if (
            self.wall_detour_heading is not None
            and self.wall_detour_start is not None
            and pygame.Vector2(robot.position).distance_to(
                self.wall_detour_start
            ) >= self.wall_detour_distance
        ):
            self.wall_detour_heading = None
            self.wall_detour_start = None

        target_angle = self.wall_detour_heading
        if target_angle is None:
            target_x, target_y = robot.active_area.center
            target_angle = math.atan2(
                robot.y - target_y,
                target_x - robot.x,
            )
        angle_error = (
            target_angle - robot.angle + math.pi
        ) % math.tau - math.pi

        self._turn_toward_target(robot, angle_error)
        self.current_action = "Duvardan kaçıyor"

    def _start_wall_detour(self, robot: "Robot") -> None:
        """Duvar ve engel köşesinden uzaklaşan geçici bir yön oluşturur."""
        center_direction = (
            pygame.Vector2(robot.active_area.center)
            - pygame.Vector2(robot.position)
        )
        if center_direction.length_squared() > 0:
            center_direction = center_direction.normalize()

        escape_direction = (
            center_direction
            + robot.last_collision_normal * 1.5
        )
        clearances = robot.wall_clearances

        if clearances["left"] <= self.wall_escape_release_distance:
            escape_direction.x = max(escape_direction.x, 0.0)
        if clearances["right"] <= self.wall_escape_release_distance:
            escape_direction.x = min(escape_direction.x, 0.0)
        if clearances["top"] <= self.wall_escape_release_distance:
            escape_direction.y = max(escape_direction.y, 0.0)
        if clearances["bottom"] <= self.wall_escape_release_distance:
            escape_direction.y = min(escape_direction.y, 0.0)

        if escape_direction.length_squared() == 0:
            escape_direction = center_direction

        self.wall_detour_heading = math.atan2(
            -escape_direction.y,
            escape_direction.x,
        )
        self.wall_detour_start = pygame.Vector2(robot.position)

    def _turn_toward_target(
        self,
        robot: "Robot",
        angle_error: float,
    ) -> None:
        """Robotu hedef açıya döndürür, hizalanınca ileri hareket ettirir."""
        if abs(angle_error) <= self.wall_turn_tolerance:
            robot.left_motor_speed = self.wall_escape_speed
            robot.right_motor_speed = self.wall_escape_speed
        else:
            turn_speed = (
                self.wall_fine_turn_speed
                if abs(angle_error) < 0.20
                else self.turn_speed
            )
            if angle_error > 0:
                robot.left_motor_speed = -turn_speed
                robot.right_motor_speed = turn_speed
            else:
                robot.left_motor_speed = turn_speed
                robot.right_motor_speed = -turn_speed

    def _move_forward(self, robot: "Robot") -> None:
        robot.left_motor_speed = self.forward_speed
        robot.right_motor_speed = self.forward_speed
        self.current_action = "İleri gidiyor"

    def _turn_left(self, robot: "Robot") -> None:
        robot.left_motor_speed = -self.turn_speed
        robot.right_motor_speed = self.turn_speed
        self.current_action = "Sola dönüyor"

    def _turn_right(self, robot: "Robot") -> None:
        robot.left_motor_speed = self.turn_speed
        robot.right_motor_speed = -self.turn_speed
        self.current_action = "Sağa dönüyor"

    def _reverse(self, robot: "Robot") -> None:
        robot.left_motor_speed = -self.reverse_speed
        robot.right_motor_speed = -self.reverse_speed
        self.current_action = "Geri manevra"
