import random

class Fire:
    def __init__(self, height, sparks, delay, n_leds):
        """
        :param height: The height of the fire. Smaller values = taller flames.
        :param sparks: Number of sparks to ignite. Higher = more frequent sparks.
        :param delay: Delay between sparks. Smaller = shorter delays.
        :param n_leds: Number of LEDs.
        """
        self._height = height
        self._sparks = sparks
        self._delay = delay
        self._size = n_leds
        self._heat = [0] * n_leds

    def apply_to(self, data):
        # Cool down every cell a little
        for i in range(self._size):
            cooldown = self._random(0, (self._height * 10) // self._size + 2)

            if cooldown > self._heat[i]:
                self._heat[i] = 0
            else:
                self._heat[i] -= cooldown

        # Heat from below drifts up and diffuses a little
        for k in range(self._size - 1, 1, -1):
            self._heat[k] = (self._heat[k - 1] +
                            self._heat[k - 2] +
                            self._heat[k - 2]) // 3

        # Randomly ignite new sparks near the bottom
        if self._random(0, 255) < self._sparks:
            y = self._random(0, 7)
            if y < self._size:
                self._heat[y] = self._random(160, 255)

        # Map heat to LED colors
        for j in range(self._size):
            r, g, b = self._heat_color(self._heat[j])
            data[j].set_rgb(r, g, b)

    def reset(self):
        for i in range(self._size):
            self._heat[i] = 0

    def _heat_color(self, temperature):
        # Scale 0–255 → 0–191
        t192 = (temperature * 192) // 255

        # Ramp from 0..63 → 0..252
        heatramp = (t192 & 0x3F) << 2

        # Hottest third
        if t192 > 0x80:
            return (255, 255, heatramp)

        # Middle third
        elif t192 > 0x40:
            return (255, heatramp, 0)

        # Coolest third
        else:
            return (heatramp, 0, 0)

    def _random(self, low, high):
        return random.randint(low, high - 1)