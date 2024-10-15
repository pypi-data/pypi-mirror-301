import traci
import os

# Define the SUMO-related functions

def connect_to_sumo(sumo_config_file):
    """
    Connect to the SUMO simulation using the provided configuration file.
    """
    print(f"Connecting to SUMO using configuration: {sumo_config_file}")
    traci.start(["sumo-gui", "-c", sumo_config_file])  # Start SUMO with GUI

def disconnect_from_sumo():
    """
    Disconnect from the SUMO simulation.
    """
    print("Disconnecting from SUMO.")
    traci.close()

def run(vehicle_id, speed):
    """
    Run the specified vehicle at the given speed.
    """
    print(f"Running vehicle {vehicle_id} at speed {speed}.")
    traci.vehicle.setSpeed(vehicle_id, speed)

def stop(vehicle_id):
    """
    Stop the specified vehicle.
    """
    print(f"Stopping vehicle {vehicle_id}.")
    traci.vehicle.setSpeed(vehicle_id, 0)

def change_lane(vehicle_id, lane_id):
    """
    Change the lane of the specified vehicle.
    """
    print(f"Changing lane of vehicle {vehicle_id} to lane {lane_id}.")
    traci.vehicle.changeLane(vehicle_id, lane_id, 10)  # Change lane with a duration

def set_route(vehicle_id, route):
    """
    Set the route for the specified vehicle.
    """
    print(f"Setting route for vehicle {vehicle_id} to {route}.")
    traci.vehicle.setRoute(vehicle_id, route)

def set_color(vehicle_id, color):
    """
    Set the color of the specified vehicle.
    """
    print(f"Setting color of vehicle {vehicle_id} to {color}.")
    # This function may not directly set color in SUMO but can be used in visualization scripts

def get_speed(vehicle_id):
    """
    Get the speed of the specified vehicle.
    """
    speed = traci.vehicle.getSpeed(vehicle_id)
    print(f"Speed of vehicle {vehicle_id}: {speed}")
    return speed

def get_position(vehicle_id):
    """
    Get the position of the specified vehicle.
    """
    position = traci.vehicle.getPosition(vehicle_id)
    print(f"Position of vehicle {vehicle_id}: {position}")
    return position

def set_max_speed(vehicle_id, max_speed):
    """
    Set the maximum speed for the specified vehicle.
    """
    print(f"Setting maximum speed of vehicle {vehicle_id} to {max_speed}.")
    traci.vehicle.setMaxSpeed(vehicle_id, max_speed)

def change_vehicle_type(vehicle_id, vehicle_type):
    """
    Change the type of the specified vehicle.
    """
    print(f"Changing type of vehicle {vehicle_id} to {vehicle_type}.")
    traci.vehicle.changeVehicleClass(vehicle_id, vehicle_type)

def slow_down(vehicle_id, decrement):
    """
    Slow down the specified vehicle by a given decrement.
    """
    current_speed = get_speed(vehicle_id)
    new_speed = max(0, current_speed - decrement)
    print(f"Slowing down vehicle {vehicle_id} to speed {new_speed}.")
    set_speed(vehicle_id, new_speed)

def create_route_file(route_file):
    """
    Create a route file for the SUMO simulation.
    """
    print(f"Creating route file: {route_file}")
    
    # Example content for the route file
    route_content = """<routes>
    <vType id="car" vClass="passenger" accel="2.6" decel="4.5" sigma="0.5" />
    <route id="route_0" edges="edge1 edge2 edge3" />
    <vehicle id="car_1" type="car" route="route_0" depart="0" />
</routes>"""

    # Write to the specified route file
    with open(route_file, 'w') as f:
        f.write(route_content)

    print(f"Route file {route_file} created successfully.")
