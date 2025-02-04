import traci
import os

def simulation_run(gui=False, random=True):

        sumoBinary = 'sumo-gui' if gui else 'sumo'
        sumoBinary = os.popen(f'which {sumoBinary}').read().strip()

        sumoCmd = [sumoBinary, "-c", "test.sumocfg"]
        if random:
            sumoCmd.append("--random")
        traci.start(sumoCmd)

        vehicles = []
        step = 0 
        vehicle_lifetimes = {}


        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

            # Get a list of all vehicles currently in the simulation
            for vehicle_id in traci.vehicle.getIDList():

                # Check if the vehicle is on Edge 1
                if traci.vehicle.getRoadID(vehicle_id) == 'E1':
                    if vehicle_id not in vehicle_lifetimes:
                        vehicle_lifetimes[vehicle_id] = traci.simulation.getTime()

                if traci.vehicle.getRoadID(vehicle_id) == 'E3':
                    depart_time = vehicle_lifetimes.pop(vehicle_id, None)
                    if depart_time is not None:
                        lifetime = traci.simulation.getTime() - depart_time
                        vehicles.append(lifetime)
            
            step += 1

        # traci.close() # close the connection to SUMO but keep the simulation running
        traci.close(False) # close the connection to SUMO
        return vehicles





def main():
    v = simulation_run(gui = True, random = True)
    print(sum(v)/len(v))


if __name__ == '__main__':
    main()
