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


def generate_network_groups(network_groups_number, available_objects, reuse=False, max_nesting_depth=5):
    """
    Generate network group objects with sequential names, random object references,
    and random literal values.
    Each network group contains 3-5 objects (if available) and 3-5 literals.

    When reuse is enabled, nested network groups are constrained to max_nesting_depth
    levels: a group containing only non-group objects has depth 1; including a group
    of depth N yields depth N+1, capped at max_nesting_depth.

    Args:
        network_groups_number: Number of network groups to generate
        available_objects: List of object names that can be referenced (hosts, networks, ranges, network_groups)
        reuse: If True, previously generated network groups can be referenced as objects by subsequent ones
        max_nesting_depth: Maximum nesting depth for network groups
    """
    network_groups = []
    # Depth of each generated network group; non-group objects implicitly have depth 0.
    group_depths = {}

    for i in range(1, network_groups_number + 1):
        name = f'network_group_{i}'

        # Exclude groups already at the max depth — including one would push the parent over the limit.
        eligible_objects = [
            obj for obj in available_objects
            if group_depths.get(obj, 0) < max_nesting_depth
        ]

        if eligible_objects:
            num_objects = random.randint(3, 5)
            if len(eligible_objects) < num_objects:
                selected_objects = eligible_objects.copy()
            else:
                selected_objects = random.sample(eligible_objects, num_objects)
        else:
            selected_objects = None

        # Generate 3-5 random literals (IP addresses or networks with prefix)
        num_literals = random.randint(3, 5)
        literals = [_generate_literal() for _ in range(num_literals)]

        network_group = {
            'name': name,
        }
        if selected_objects:
            network_group['objects'] = selected_objects
        network_group['literals'] = literals
        network_groups.append(network_group)

        max_child_depth = max(
            (group_depths.get(obj, 0) for obj in (selected_objects or [])),
            default=0,
        )
        group_depths[name] = max_child_depth + 1

        # Add this network group to available objects for future groups (only if reuse is enabled)
        if reuse:
            available_objects.append(name)

    return network_groups
