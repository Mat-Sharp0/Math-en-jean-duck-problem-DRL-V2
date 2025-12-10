import numpy as np

class EntityLite:
    def __init__(self, pos=None):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)

    # --- Move ---
    def move(self, ax, ay, max_distance):
        norm = np.sqrt(ax**2 + ay**2)
        if norm < 1e-6:
            return

        if norm > 1.0:
            ax /= norm
            ay /= norm
            norm = 1.0

        distance = norm * max_distance
        angle = np.arctan2(ay, ax)
        delta = np.array([np.cos(angle), np.sin(angle)]) * distance
        self.pos += delta
