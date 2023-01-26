from src.simulation.configurator import Configurator
config = Configurator().configuration
def path_manager_tests():
    from src.mission.mission_manager import MissionManager
    mission_manager = MissionManager()

    #block_2(mission_manager)



def block_1(mission_manager):
    assert type(mission_manager.mission) is dict
    #________________________

    # testing set_drone_path
    feasible_path = [(0,0), (100,0), (100,100), (0, 100)]
    # drone id in range, well formatted path -> OK
    mission_manager.set_drone_path(0, feasible_path)

    # MUST END in AssertionError
    # drone id not in range, well formatted path
    # mission_manager.set_drone_path(-1, feasible_path) -> OK
    # mission_manager.set_drone_path(config.n_drones +1, feasible_path) -> OK

    # drone id in range, wrong format for path
    unfeasible_path = [0,0, (100, 0)] #-> OK
    # unfeasible_path = [(-1,0)] -> OK
    # unfeasible_path = [(100, config.env_height + 1)] -> OK
    # unfeasible_path = [(config.env_width + 1, 100)] -> OK
    # mission_manager.set_drone_path(0, unfeasible_path)
    #________________________

    # testing get_drone_path
    assert mission_manager.get_drone_path(0) == feasible_path # -> OK
    feasible_path2 = [(0, 0), (100, 0), (100, 100), (0, 0)]
    mission_manager.set_drone_path(0, feasible_path2)
    assert mission_manager.get_drone_path(0) != feasible_path  # -> OK
    # ________________________

    # testing mission_to_json
    json_file_out = config.JSON_path_prefix.format("TEST")
    print(f"writing {json_file_out}")
    mission_manager.mission_to_json(json_file_out)
    mission = mission_manager.mission
    # ________________________

    # testing json_to_mission
    print(f"reading from {json_file_out}")
    mission_manager.json_to_mission(json_file_out)
    assert mission == mission_manager.mission # -> OK
    # ________________________

    # testing set_mission
    mission_manager.set_mission(mission) # -> OK
    # MUST END in AssertionError
    #mission[0] = unfeasible_path
    #print(mission)
    #mission_manager.set_mission(mission) # -> OK
    #mission[-1] = feasible_path
    #print(mission)
    #mission_manager.set_mission(mission)  # -> OK
    # ________________________

def block_2(mission_manager):
    # converting RANDOM_mission0.json to RANDOM_mission0NEW.json
    json_file_in = config.JSON_path_prefix.format(0)
    json_file_out = config.JSON_path_prefix.format("0NEW")
    #mission_manager.old_mission_format_to_new_format(json_file_in, json_file_out)
    # ________________________

    # testing RANDOM_mission0NEW.json
    mission_from_old = mission_manager.json_to_mission_old(json_file_in, True)
    mission_manager.json_to_mission(json_file_out, True)
    mission_from_new = mission_manager.mission
    assert mission_from_new == mission_from_old




