"""Pygame simulasyonunun ana giris noktasi."""

import pygame

from config import (
    BACKGROUND_COLOR,
    FPS,
    ROBOT_INITIAL_LEFT_SPEED,
    ROBOT_INITIAL_RIGHT_SPEED,
    ROBOT_RADIUS,
    ROBOT_START_ANGLE,
    ROBOT_START_X,
    ROBOT_START_Y,
    ROBOT_WHEEL_BASE,
    SCREEN_SIZE,
    WINDOW_TITLE,
)
from controller import ObstacleAvoidanceController
from robot import Robot
from utils import InfoPanel
from world import World


def main() -> None:
    """Simulasyon penceresini baslatir ve ana donguyu calistirir."""
    pygame.init()

    transparent_icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.display.set_icon(transparent_icon)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    world = World(SCREEN_SIZE)
    robot = Robot(
        x=ROBOT_START_X,
        y=ROBOT_START_Y,
        angle=ROBOT_START_ANGLE,
        radius=ROBOT_RADIUS,
        active_area=world.active_area,
        left_motor_speed=ROBOT_INITIAL_LEFT_SPEED,
        right_motor_speed=ROBOT_INITIAL_RIGHT_SPEED,
        wheel_base=ROBOT_WHEEL_BASE,
    )
    controller = ObstacleAvoidanceController()
    info_panel = InfoPanel(SCREEN_SIZE[0])

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        reset_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    reset_requested = True

        if not running:
            break

        if reset_requested:
            robot.reset()
            controller.reset()

        robot.update_sensors(world.collision_rects)
        controller.update(robot, robot.sensor_readings, dt)
        if not reset_requested:
            robot.update(dt, world.obstacles)
            robot.update_sensors(world.collision_rects)

        screen.fill(BACKGROUND_COLOR)
        world.draw(screen, info_panel.obstacle_font)

        previous_clip = screen.get_clip()
        screen.set_clip(world.active_area)
        robot.draw_sensors(screen)
        robot.draw(screen)
        screen.set_clip(previous_clip)

        info_panel.draw(
            screen,
            sensor_readings=robot.sensor_readings,
            left_motor_speed=robot.left_motor_speed,
            right_motor_speed=robot.right_motor_speed,
            robot_status=controller.current_action,
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
