import numpy as np
import sys
#from src.conversions import min2decimal I couldn't get this to work so I just copied the function in

#for running the script just to test, these are the file locations
#true_file = "/mnt/c/Users/Caleb/Documents/MRover/mrover-workspace/onboard/filter/tools/tuning_test.csv"
#filtered_file = "/mnt/c/Users/Caleb/Documents/MRover/mrover-workspace/onboard/filter/tools/tuning_test2.csv"

SIMP_DTYPES = ['lat','long','speed','bearing'] #apparently I didn't end up actually using this, but it's how true_path and filtered_path are ordered

def min2decimal(deg, min): #this was in the src.conversions but I was getting errors importing that so I just copied it here
    '''
    Converts integer degrees and decimal minutes to decimal degrees

    @param int deg:  integer degrees
    @param float min: decimal minutes
    @return float: decimal degrees
    '''
    return deg + min / 60

def csv_to_inputs(csv_file):
    '''
    gets numpy arrays from csv paths

    @param path csv_file: path to csv of simulated rovers path (true or filtered) in [lat_deg, lat_min, long_deg, long_min, bearing, speed]
    @return ndarray path: simulator's true path in numpy array format, no dtype. follows SIMP_DTYPE though
    '''
    
    old_dtypes = ['lat_min', 'lat_deg', 'long_min', 'long_deg', 'speed', 'bearing']
    path_data = np.genfromtxt(csv_file, delimiter = ',', names = old_dtypes, skip_header = 1)

    # restructure to merge minutes and degrees
    #I had trouble doing anything to the array once I added in the dtypes so I didn't on these ones. They follow SIMP_DTYPES though.
    path = np.array([min2decimal(path_data['lat_min'], path_data['lat_deg']),min2decimal(path_data['long_min'], path_data['long_deg']),
                     path_data['speed'], path_data['bearing']])
    return path

def evaluate_fit(true_path, filtered_path):
    '''
    assign a number to how good the KF did

    @param true_path: numpy array of the SIMP_DTYPES generaged by the simulater
    @param filtered_path: numpy array of the SIMP_DTYPES from the simulated rovers KF 
    @return float: the assesment, which should range from [0,1]
    '''

    lat_range = max(true_path[0])- min(true_path[0])
    long_range = max(true_path[1]) - min(true_path[1])
    speed_range = 10 #THIS IS JUST A GUESS
    bearing_range = 360 #assuming degrees
    range_scale = [lat_range, long_range, speed_range, bearing_range]

    diff = abs(true_path - filtered_path)
    scaled_diff = np.divide(diff, np.reshape(range_scale, (4,1)))
    
    return np.average(scaled_diff)

#print(evaluate_fit(csv_to_inputs(true_file), csv_to_inputs(filtered_file)))


if __name__ == "__main__":
    # Get arguments
    if len(sys.argv) != 3:
        print('Error: Usage from onboard/filter is python3 -m tools.tuning <data_type>')
        sys.exit()

    # Evaluate
    print(evaluate_fit(csv_to_inputs(sys.argv[1]), csv_to_inputs(sys.argv[2])))
    