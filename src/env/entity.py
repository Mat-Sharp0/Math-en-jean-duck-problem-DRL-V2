import numpy as np
import math

class Duck:
    def __init__(self, pos=None):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)

    # --- Move ---
    def move(self, ax, ay, max_distance):
        """
        Move the object by a given action vector (ax, ay), scaled by max_distance.

        The movement is limited such that the object cannot move more than max_distance
        in one step. Very small actions (near zero) are ignored.

        Parameters:
            ax (float): Action along the x-axis.
            ay (float): Action along the y-axis.
            max_distance (float): Maximum distance the object can move in one step.
        """
        action = np.array([ax, ay], dtype=np.float32)
        norm = np.linalg.norm(action)
        if norm < 1e-6:
            return

        # Normalize the action vector
        direction = action / norm

        # Limit the movement distance
        distance = min(norm, 1.0) * max_distance

        self.pos += direction * distance


class Wolf:
    def __init__(self, pos=None):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)
    
    def wolf_move(self, target_pos, center, max_step):
        """
        Move the wolf's position along a circular path toward a target.

        The movement follows the shortest arc on the circle defined by
        the current position relative to the center, and is limited by
        max_step to control the maximum movement per update.

        Parameters:
            target_pos (tuple[float, float]): The target position to move toward.
            center (tuple[float, float]): The center of the circular path.
            max_step (float): Maximum distance the wolf can move along the arc.
        """
        
        # Wolf's offset relative to the circle center
        dx = self.pos[0] - center[0]
        dy = self.pos[1] - center[1]
        radius = (dx*dx + dy*dy)**0.5
        if radius < 1e-8:
            return

        # Direction vector toward the target
        tx = target_pos[0] - center[0]
        ty = target_pos[1] - center[1]
        dist = (tx*tx + ty*ty)**0.5
        if dist < 1e-8:
            return

        # Project the target onto the circle of current radius
        tx = tx * radius / dist
        ty = ty * radius / dist

        # Current and target angles
        angle_current = math.atan2(dy, dx)
        angle_target = math.atan2(ty, tx)

        # Minimal angular difference [-pi, pi]
        delta_angle = angle_target - angle_current
        delta_angle = (delta_angle + math.pi) % (2*math.pi) - math.pi

        # Limit the step according to max_step
        arc_step = max(-max_step, min(delta_angle * radius, max_step))
        step_angle = arc_step / radius

        # Apply 2D rotation to move along the arc
        cos_a = math.cos(step_angle)
        sin_a = math.sin(step_angle)
        self.pos[0] = center[0] + dx * cos_a - dy * sin_a
        self.pos[1] = center[1] + dx * sin_a + dy * cos_a
