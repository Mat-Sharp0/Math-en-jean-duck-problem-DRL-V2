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
        action = np.array([ax, ay], dtype=np.float32)
        norm = np.linalg.norm(action)

        if norm < 1e-6:
            return

        direction = action / max(norm, 1.0)
        distance = min(norm, 1.0) * max_distance

        self.pos += direction * distance

    def move_point_along_arc(pos, center, arc_length):
        """
        Déplace un point le long d'un arc de cercle.

        pos: np.array([x, y]) ou None
        center: np.array([cx, cy])
        arc_length: longueur de l'arc (peut être négative)

        Retourne: np.array([x_final, y_final])
        """

        pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)
        center = np.array(center, dtype=np.float64)

        offset = pos - center

        radius = np.linalg.norm(offset)
        if radius == 0.0:
            raise ValueError("Le point ne peut pas être confondu avec le centre")

        angle = arc_length / radius

        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        rotation = np.array([
            [cos_a, -sin_a],
            [sin_a,  cos_a]
        ], dtype=np.float64)

        new_pos = center + rotation @ offset

        return new_pos