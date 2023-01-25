from dataclasses import dataclass
from enum import Enum
from typing import Tuple

@dataclass
class Configuration:
    # Path Drones
    circle_path: bool
    demo_path: bool
    path_from_JSON: bool
    JSON_path_prefix: str
    random_steps: list
    random_start_point: bool

    # Drawing
    # plot_simulation: bool
    wait_simulation_step: float
    skip_simulation_step: float
    draw_size: int
    show_dir_vec: bool

    # Simulation
    simulation_name: str
    time_step_duration: float
    simulation_length: int
    seed: int
    n_drones: int
    env_width: int
    env_height: int
    plot_options: object
    # show_plot: bool
    debug: bool
    experiments_dir: str
    save_plot: bool
    save_plot_dir: bool
    enable_proabilities: bool

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
    routing_algorithm: object
    communication_error_type: str
    communication_success_probabilities: float
    gaussian_scale: float
    packets_max_ttl: int
    retransmission_delay: int
    hello_delay: int
    reception_granted: float
    lil_delta: float
    old_hello_packet: int
    root_evaluation_delta: str
    nn_model_path: str

class Plot_Options(Enum):
    PLOT = 1
    PLOT_AND_SAVE = 2
    NOTHING = 3