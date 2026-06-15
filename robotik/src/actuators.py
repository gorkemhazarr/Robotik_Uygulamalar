"""Robotun sağ ve sol motor aktüatörleri."""


class DifferentialDriveActuator:
    """İki tekerlek hızını doğrusal ve açısal hıza dönüştürür."""

    def __init__(
        self,
        left_motor_speed: float,
        right_motor_speed: float,
        wheel_base: float,
    ) -> None:
        if wheel_base <= 0:
            raise ValueError("Tekerlekler arası mesafe sıfırdan büyük olmalıdır.")

        self.left_motor_speed = left_motor_speed
        self.right_motor_speed = right_motor_speed
        self.wheel_base = wheel_base

    @property
    def linear_velocity(self) -> float:
        """İki motorun ortalama doğrusal hızını döndürür."""
        return (self.left_motor_speed + self.right_motor_speed) / 2.0

    @property
    def angular_velocity(self) -> float:
        """Motor hızı farkından oluşan açısal hızı döndürür."""
        return (
            self.right_motor_speed - self.left_motor_speed
        ) / self.wheel_base

    def set_speeds(self, left: float, right: float) -> None:
        """Sağ ve sol motor hızlarını günceller."""
        self.left_motor_speed = left
        self.right_motor_speed = right

    def stop(self) -> None:
        """Her iki motoru durdurur."""
        self.set_speeds(0.0, 0.0)
