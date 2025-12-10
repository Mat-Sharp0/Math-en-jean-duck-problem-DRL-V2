import numpy as np

class EntityLite:
    def __init__(self, pos=None):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)

    # --- Move ---
    def move(self, distance, direction):
        """
        Move in the specify direction.
        distance: distance to move
        direction: direction of movement (absolute)
        """
        delta = np.array([np.cos(np.radians(direction)), np.sin(np.radians(direction))]) * distance
        self.pos += delta

    def move_vector(self, ax, ay, max_distance):
        norm = np.sqrt(ax**2 + ay**2)
        if norm < 1e-6:
            return  # vecteur nul → ne bouge pas

        # Normalisation si nécessaire
        if norm > 1.0:
            ax /= norm
            ay /= norm
            norm = 1.0

        distance = norm * max_distance
        angle = np.arctan2(ay, ax)  # radians
        self.direction = np.degrees(angle) % 360  # mettre à jour la direction du canard

        delta = np.array([np.cos(angle), np.sin(angle)]) * distance
        self.pos += delta


    def move_arc(self, length, radius):
        """
        Move along a circular arc.
        length: length of the arc
        radius: radius of the arc (+ for left, - for right)
        """
        if radius == 0:
            self.forward(length)
            return

        turn_left = radius > 0
        angle_rad = length / abs(radius)
        if not turn_left:
            angle_rad = -angle_rad

        # Center of the circle
        center_angle = self.direction_rad + (np.pi/2 if turn_left else -np.pi/2)
        center = self.pos + np.array([np.cos(center_angle), np.sin(center_angle)]) * abs(radius)

        # vecteur position -> centre
        offset = self.pos - center

        # rotation
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad),  np.cos(angle_rad)]
        ])
        self.pos = center + rotation_matrix @ offset

        # direction update
        self.direction = (self.direction + np.degrees(angle_rad)) % 360.0