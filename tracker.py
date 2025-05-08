import traci
import traci.constants as tc

NETWORK_JUNCTION = ["J1", "J2", "J3", "J4"]
DIRECTIONS = ["tang", "tras"]

class ManageTrackers:
    """
        Manages the update of trackers placed at junctions.
    """
    def __init__(self):
        self.T = 0

        self.trackers = [JointTracker(DIRECTIONS[0]), FirstJoint()]
        # self.trackers = [FirstJoint()]
        for sub in self.trackers:
            sub.get_roads_from_junction()
        
        self.name = "Network"
        self.subscribed_vehicles = set()  # Keep track of subscribed vehicles

    def update(self):
        self.T += 1
        
        # Get current vehicles in simulation
        current_vehicles = set(traci.vehicle.getIDList())
        
        # Subscribe to new vehicles
        for vehicle_id in current_vehicles:
            if vehicle_id not in self.subscribed_vehicles:
                traci.vehicle.subscribe(vehicle_id, [tc.VAR_ROAD_ID, tc.VAR_SPEED])
                self.subscribed_vehicles.add(vehicle_id)
        
        # Get all vehicle data at once
        vehicle_data = traci.vehicle.getAllSubscriptionResults()
        
        # Process each vehicle
        for vehicle_id, data in vehicle_data.items():
            current_edge = data[tc.VAR_ROAD_ID]
            vehicle_speed = data[tc.VAR_SPEED]
            
            for tracker in self.trackers:
                tracker.T = self.T
                tracker.process_vehicle(vehicle_id, current_edge, vehicle_speed)
        
        # Clean up subscriptions for vehicles that left the simulation
        departed_vehicles = self.subscribed_vehicles - current_vehicles
        for vehicle_id in departed_vehicles:
            self.subscribed_vehicles.remove(vehicle_id)
            # TraCI automatically unsubscribes departed vehicles, so no explicit unsubscribe needed
        
    def simulation_end(self):
        for tracker in self.trackers:
            tracker.simulation_end()        

class JointTracker():
    def __init__(self, direction: str):
        self.system = {}    # keep track of vehicles id in the system
        self.metrics_for_stats: dict[str, float | int | list[float]] = {
            'completed_lifetimes': [],
        }
        self.T = 0          # simulation step
        self.arrivals = 0   # number of vehicles that arrived in the system
        self.completed = 0  # number of vehicles that completed their trip

        self.incoming_routes = set()
        self.outgoing_routes = set()
        self.incoming_junctions = set()

        self.completed_at_time = [] # store the simulation step in which a vehicle completed its trip

        self.direction = direction
        self.name = f"Network_{direction}"

    def get_roads_from_junction(self):
        for junction in NETWORK_JUNCTION:

            self.outgoing_routes.update(
                e for e in traci.junction.getOutgoingEdges(junction) 
                if not e.startswith(":") and e.endswith(self.direction)
            )
            
            self.incoming_routes.update(
                e for e in traci.junction.getIncomingEdges(junction) 
                if not e.startswith(":") and e.endswith(self.direction)
            )
            
            self.incoming_junctions.update(
                e for e in traci.junction.getIncomingEdges(junction) 
                if e.startswith(":") and e.endswith(self.direction)
            )

    def process_vehicle(self, vehicle_id, current_edge, vehicle_speed):
        """Process vehicle data from subscription in a single pass"""
        # Handle incoming vehicles
        is_relevant_edge = (vehicle_id not in self.system) and (
            (current_edge in self.incoming_junctions) or 
            (current_edge in self.incoming_routes and vehicle_speed < 0.1)
        )
        
        if is_relevant_edge:
            self.arrivals += 1
            self.system[vehicle_id] = self.T
            
        # Handle outgoing vehicles
        if current_edge in self.outgoing_routes:
            depart_time = self.system.pop(vehicle_id, None)
            if depart_time is not None:
                self.completed += 1
                lifetime = self.T - depart_time
                self.metrics_for_stats['completed_lifetimes'].append(lifetime)
                self.completed_at_time.append(self.T)


    def simulation_end(self):
        # Adding safety checks to avoid division by zero
        self.metrics_for_stats['arrival_rate'] = self.arrivals / self.T if self.T > 0 else 0
        self.metrics_for_stats['throughput'] = self.completed / self.T if self.T > 0 else 0
        self.metrics_for_stats['completed'] = self.completed


class FirstJoint(JointTracker):
    def __init__(self):
        super().__init__("tang")
        self.name = f"first_servant"

        # to manage the request time
        self.track_step = self.T
        self.rq_time = 0

    def process_vehicle(self, vehicle_id, current_edge, vehicle_speed):
        super().process_vehicle(vehicle_id, current_edge, vehicle_speed)

        if len(self.system) > 0 and self.track_step < self.T:
            self.rq_time += 1
            self.track_step = self.T

    def simulation_end(self):
        super().simulation_end()
        self.metrics_for_stats['utilization'] = self.rq_time / self.T if self.T > 0 else 0
        self.metrics_for_stats['average_time_service'] = self.rq_time / self.completed if self.completed > 0 else 0


    def get_roads_from_junction(self):
        self.outgoing_routes = {"E2"}
        self.incoming_routes = {"E0.66_tang"}