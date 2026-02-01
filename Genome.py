import random
import math

class Genome:
    """Neural network genome with feedforward evaluation and weight mutation only
            (No connection mutation)"""
    
    def __init__(self):
        self.nodes = [
            {"id": 0, "type": "input",  "label": "BIRD_Y"},
            {"id": 1, "type": "input",  "label": "PIPE_DIST"},
            {"id": 2, "type": "input",  "label": "PIPE_TOP"},
            {"id": 3, "type": "input",  "label": "PIPE_BOTTOM"},
            {"id": 4, "type": "input",  "label": "BIRD_VEL"},
            {"id": 5, "type": "input",  "label": "BIAS"},
            {"id": 6, "type": "output", "label": "JUMP"}
        ]
        self.connections = [
            {"in": 0, "out": 6, "weight": random.uniform(-2, 2), "enabled": True},
            {"in": 1, "out": 6, "weight": random.uniform(-2, 2), "enabled": True},
            {"in": 2, "out": 6, "weight": random.uniform(-2, 2), "enabled": True},
            {"in": 3, "out": 6, "weight": random.uniform(-2, 2), "enabled": True},
            {"in": 4, "out": 6, "weight": random.uniform(-2, 2), "enabled": True},
            {"in": 5, "out": 6, "weight": random.uniform(-2, 2), "enabled": True}
        ]
        self.fitness = 0

    def feed_forward(self, inputs):
        # Map inputs to their IDs
        node_values = {i: inputs[i] for i in range(5)}
        node_values[5] = 1.0  # BIAS

        # Simple weighted sum
        node_sum = 0.0
        for conn in self.connections:
            if conn["enabled"]:
                node_sum += node_values[conn["in"]] * conn["weight"]
        
        return self.sigmoid(node_sum)

    def sigmoid(self, x):
        """Sigmoid activation function with clipping"""
        x = max(-10, min(10, x))
        return 1 / (1 + math.exp(-x))

    def mutate_weights(self, perturb_rate=0.9, perturb_power=0.1):
        """Mutate connection weights"""
        for conn in self.connections:
            if random.random() < 0.8:  # 80% chance to mutate
                if random.random() < perturb_rate:
                    conn["weight"] += random.uniform(-perturb_power, perturb_power)
                else:
                    conn["weight"] = random.uniform(-2, 2)

    def copy(self):
        """Create a deep copy of this genome"""
        new_genome = Genome()
        new_genome.nodes = [node.copy() for node in self.nodes]
        new_genome.connections = [conn.copy() for conn in self.connections]
        new_genome.fitness = self.fitness
        return new_genome