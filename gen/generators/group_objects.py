"""
Network group object generators
"""

import random

from utils.ip_utils import generate_random_ip, generate_random_subnet


def _generate_literal():
    """Generate a random literal value - either an IP address or a network with prefix."""
    if random.choice([True, False]):
        return generate_random_ip()
    else:
        return generate_random_subnet()


def generate_network_groups(network_groups_number, available_objects, reuse=False):
    """
    Generate network group objects with sequential names, random object references,
    and random literal values.
    Each network group contains 3-5 objects (if available) and 3-5 literals.

    Args:
        network_groups_number: Number of network groups to generate
        available_objects: List of object names that can be referenced (hosts, networks, ranges, network_groups)
        reuse: If True, previously generated network groups can be referenced as objects by subsequent ones
    """
    network_groups = []

    for i in range(1, network_groups_number + 1):
        # Select random objects from available objects (if any exist)
        if available_objects:
            num_objects = random.randint(3, 5)
            if len(available_objects) < num_objects:
                selected_objects = available_objects.copy()
            else:
                selected_objects = random.sample(available_objects, num_objects)
        else:
            selected_objects = None

        # Generate 3-5 random literals (IP addresses or networks with prefix)
        num_literals = random.randint(3, 5)
        literals = [_generate_literal() for _ in range(num_literals)]

        network_group = {
            'name': f'network_group_{i}',
        }
        if selected_objects:
            network_group['objects'] = selected_objects
        network_group['literals'] = literals
        network_groups.append(network_group)

        # Add this network group to available objects for future groups (only if reuse is enabled)
        if reuse:
            available_objects.append(f'network_group_{i}')

    return network_groups
