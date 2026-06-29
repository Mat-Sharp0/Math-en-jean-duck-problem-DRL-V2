import numpy as np
import math

class Duck:
    """Duck agent class"""
    def __init__(self, pos=None):
        """
        pos: initial position [x, y], as an np.array
        direction: angle in degrees, 0 = positive x-axis
        """
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)

 
    def move(self, ax, ay, max_distance, radius):
        action = np.array([ax, ay], dtype=np.float32)
        norm = np.linalg.norm(action)
        if norm < 1e-6:
            return

        direction = action / norm

        distance = min(norm, 1.0) * max_distance

        new_pos = self.pos + direction * distance

        self.pos = np.clip(np.linalg.norm(new_pos), 0, radius + 0.05) / np.linalg.norm(new_pos) * new_pos if np.linalg.norm(new_pos) > 0 else new_pos


class Wolf:
    """Wolf agent class"""
    def __init__(self, pos=None):
        self.pos = np.array(pos if pos is not None else [0.0, 0.0], dtype=np.float64)
    
    def wolf_move(self, target_pos, center, max_step):
        dx = self.pos[0] - center[0]
        dy = self.pos[1] - center[1]
        radius = (dx*dx + dy*dy)**0.5
        if radius < 1e-8:
            return

        tx = target_pos[0] - center[0]
        ty = target_pos[1] - center[1]
        dist = (tx*tx + ty*ty)**0.5
        if dist < 1e-8:
            return
        
        tx = tx * radius / dist
        ty = ty * radius / dist

        angle_current = math.atan2(dy, dx)
        angle_target = math.atan2(ty, tx)

        delta_angle = angle_target - angle_current
        delta_angle = (delta_angle + math.pi) % (2*math.pi) - math.pi

        arc_step = max(-max_step, min(delta_angle * radius, max_step))
        step_angle = arc_step / radius

        cos_a = math.cos(step_angle)
        sin_a = math.sin(step_angle)
        self.pos[0] = center[0] + dx * cos_a - dy * sin_a
        self.pos[1] = center[1] + dx * sin_a + dy * cos_a
