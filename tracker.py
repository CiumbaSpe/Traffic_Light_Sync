import traci

class PerformanceTracker:
    """
    Tracks various performance metrics of the simulation.
    """
    def __init__(self):
        self.vehicle_lifetimes = {}
        self.completed_lifetimes = []
        self.stop_time = 0

    def update(self):
        self.update_vehicles()
        self.update_outgoing_vehicles()

    def update_vehicles(self):
        # Get a list of all vehicles currently in the simulation
        for vehicle_id in traci.vehicle.getIDList():
            
            if vehicle_id not in self.vehicle_lifetimes:    # If the vehicle is seen for the first time, record its departure time
                self.vehicle_lifetimes[vehicle_id] = traci.vehicle.getDeparture(vehicle_id)
            
            if traci.vehicle.getSpeed(vehicle_id) < 0.1:    # If the vehicle's speed is close to 0, increment stop_time
                self.stop_time += 1

    def update_outgoing_vehicles(self):
        # Check for vehicles that completed their trips
        arrived_vehicles = traci.simulation.getArrivedIDList()
        for vehicle_id in arrived_vehicles:
            # Calculate the lifetime and store it
            depart_time = self.vehicle_lifetimes.pop(vehicle_id, None)
            if depart_time is not None:
                lifetime = traci.simulation.getTime() - depart_time
                self.completed_lifetimes.append(lifetime)
        