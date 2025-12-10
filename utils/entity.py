import numpy as np

class Entity:
    def __init__(self, pos=None, direction=0.0):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)
        self.direction = direction % 360.0  # degrés

    # --- Utilities ---
    @property
    def direction_rad(self):
        return np.radians(self.direction)

    def _normalize_dir(self):
        self.direction %= 360.0

    # --- Direction ---
    def set_direction(self, direction):
        self.direction = direction % 360.0

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 360.0

    # --- Move ---
    def forward(self, distance):
        """
        Move forward in the current direction.
        distance: distance to move
        """
        delta = np.array([np.cos(self.direction_rad), np.sin(self.direction_rad)]) * distance
        self.pos += delta

    def move(self, distance, direction):
        """
        Move in the specify direction.
        distance: distance to move
        direction: direction of movement (absolute)
        """
        self.set_direction(direction)
        self.forward(distance)

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