from dataclasses import dataclass
from typing import Tuple


@dataclass
class Configuration:
    # Simulation
    simulation_name: str
    time_step_duration: float
    simulation_length: int
    seed: int
    n_drones: int
    env_width: int
    env_height: int
    show_plot: bool
    prob_size_cell_r: float

    # Drones
    drone_com_range: int
    drone_sen_range: int
    drone_speed: int
    drone_max_buffer_size: int
    drone_max_energy: int
    drone_retransmission_delta: int
    drone_communication_success: int

    # Depot
    depot_com_range: int
    depot_coordinates: Tuple[int, int]

    # Event
    event_duration: int
    event_generation_prob: float
    event_generation_delay: int

    # Routing
    packets_max_ttl: int
    routing_algorithm: str
    communication_error_type: str
