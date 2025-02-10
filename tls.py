import setting 
import traci
from traci._trafficlight import Logic

# This functino manage traffic light logic

class TrafficLightSystem: 
    def __init__(self, tls : tuple, config : int = 0):
        self.cycle_time = setting.TLS_TOTAL_TIME
        self.traffic_lights = tls
        self.configuration = config
        # self.set_cycle() # set the cycle of the traffic light
        self.set_phase()

    def set_cycle(self):
        for tl_id in self.traffic_lights:
            
            # Get initial traffic light program
            initial_program = traci.trafficlight.getAllProgramLogics(tl_id)

            # Create a new program with modified phase durations
            new_program: Logic = initial_program[0]

            # Modify phase durations
            new_phases = [
                traci.trafficlight.Phase(self.cycle_time//2-2, "rGGrGG"),  # New green phase
                traci.trafficlight.Phase(2, "ryyryy"),   # New yellow phase
                traci.trafficlight.Phase(self.cycle_time//2-2, "GrrGrr"),  # Opposite direction green
                traci.trafficlight.Phase(2, "yrryrr"),   # Opposite direction yellow
            ]

            # Apply new phases
            new_program.phases = new_phases
            traci.trafficlight.setProgramLogic(tl_id, new_program)

    def set_phase(self):
        # Get a list of all traffic light IDs 
        traffic_light_ids = traci.trafficlight.getIDList()
        
        # Set the offset for each traffic light
        for tl_id in traffic_light_ids: 
            traci.trafficlight.setPhase(tl_id, 0)
            for _ in range(self.configuration):
                traci.simulationStep()

    def print_logic(self):
        for tl_id in self.traffic_lights:
            program_id = traci.trafficlight.getProgram(tl_id)
            program_details = traci.trafficlight.getAllProgramLogics(tl_id)
            print("\nTraffic Light ID:", tl_id)
            print("Program ID:", program_id)
            print("Program Details:", program_details)
