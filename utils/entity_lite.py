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
    
    def wolf_move(
        self,
        target_pos: np.ndarray,
        center: np.ndarray,
        radius: float,
        max_step: float
    ):
        """
        Déplace self.pos le long du cercle vers le point du cercle
        le plus proche de A, par le plus court arc.
        """

        target_pos = np.array(target_pos, dtype=np.float64)
        center = np.array(center, dtype=np.float64)

        CA = target_pos - center
        norm_CA = np.linalg.norm(CA)

        if norm_CA < 1e-8:
            return

        target = center + radius * (CA / norm_CA)

        def angle(p):
            v = p - center
            return np.arctan2(v[1], v[0])

        angle_B = angle(self.pos)
        angle_target = angle(target)

        delta_angle = angle_target - angle_B
        delta_angle = (delta_angle + np.pi) % (2 * np.pi) - np.pi

        arc_remaining = delta_angle * radius

        arc_step = np.clip(arc_remaining, -max_step, max_step)

        self.pos = self.move_point_along_arc(
            self.pos,
            center,
            arc_step
        )