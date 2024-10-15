# sumo_simulator/car_controller.py

import traci

def connect_to_sumo(sumo_config_file):
    """Connect to the SUMO simulation."""
    traci.start(["sumo", "-c", sumo_config_file])
    print("Connected to SUMO.")

def disconnect_from_sumo():
    """Disconnect from the SUMO simulation."""
    traci.close()
    print("Disconnected from SUMO.")

def run(car_id, speed):
    """Set the speed of the car to run."""
    try:
        traci.vehicle.setSpeed(car_id, speed)
        print(f"Car {car_id} is running at speed {speed}.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while running the car: {e}")

def stop(car_id):
    """Stop the car by setting its speed to zero."""
    try:
        traci.vehicle.setSpeed(car_id, 0)
        print(f"Car {car_id} has stopped.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while stopping the car: {e}")

def change_lane(car_id, lane_index):
    """Change the lane of the car."""
    try:
        traci.vehicle.changeLane(car_id, lane_index, 10.0)  # 10.0 seconds to change lanes
        print(f"Car {car_id} has changed to lane {lane_index}.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while changing the lane: {e}")

def set_route(car_id, route):
    """Set a predefined route for the car."""
    try:
        traci.vehicle.setRoute(car_id, route)
        print(f"Car {car_id} is now following the route {route}.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while setting the route: {e}")

def set_color(car_id, color):
    """
    Set the color of the car.
    Color should be a tuple of (R, G, B, A), where each component ranges from 0 to 255.
    """
    try:
        traci.vehicle.setColor(car_id, color)
        print(f"Car {car_id} color set to {color}.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while setting the car color: {e}")

def get_speed(car_id):
    """Get the current speed of the car."""
    try:
        speed = traci.vehicle.getSpeed(car_id)
        print(f"Car {car_id} is currently traveling at {speed} m/s.")
        return speed
    except traci.exceptions.TraCIException as e:
        print(f"Error while getting the car speed: {e}")
        return None

def get_position(car_id):
    """Get the current position of the car."""
    try:
        position = traci.vehicle.getPosition(car_id)
        print(f"Car {car_id} is currently at position {position}.")
        return position
    except traci.exceptions.TraCIException as e:
        print(f"Error while getting the car position: {e}")
        return None

def set_max_speed(car_id, max_speed):
    """Set the maximum speed limit for the car."""
    try:
        traci.vehicle.setMaxSpeed(car_id, max_speed)
        print(f"Car {car_id}'s maximum speed is set to {max_speed} m/s.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while setting the maximum speed: {e}")

def change_vehicle_type(car_id, vehicle_type):
    """Change the type of the car (e.g., from passenger car to truck)."""
    try:
        traci.vehicle.setType(car_id, vehicle_type)
        print(f"Car {car_id} type changed to {vehicle_type}.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while changing the vehicle type: {e}")

def slow_down(car_id, speed, duration):
    """Slow down the car to a specified speed over a given duration."""
    try:
        traci.vehicle.slowDown(car_id, speed, duration)
        print(f"Car {car_id} is slowing down to {speed} m/s over {duration} seconds.")
    except traci.exceptions.TraCIException as e:
        print(f"Error while slowing down the car: {e}")
