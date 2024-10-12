import numpy as np
from typing import List, Dict, Tuple, Union, Optional
from shapely.geometry import Polygon as Polygon_Shapely, LineString
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

from .Classes import Line, LineSegment, Polygon
from .generate_line_segments_dynamic_thickness import generate_line_segments_dynamic_thickness

def rot(point, center, rotation_matrix):
    """
    Rotates a point around the center using the given rotation matrix.
    point: numpy array representing the point to rotate
    center: numpy array representing the center of rotation
    rotation_matrix: 2x2 numpy array representing the rotation matrix
    """
    translated_point = point - center
    rotated_point = np.dot(rotation_matrix, translated_point)
    final_point = rotated_point + center

    return final_point

def unit_vector(v):
    """ Returns the unit vector of the vector. """
    return v / np.linalg.norm(v)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'."""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_alignment_mean(line_vector_arr, director):
    """Get the mean alignment."""
    S_all = []
    for item in line_vector_arr:
        line_vector = item['line_vector']
        area = item['area']
        P2 = 0.5*(3*(np.cos(angle_between(line_vector, director)))**2-1)
        S_all.append(P2*area)

    return float(np.mean(S_all))

def compute_alignment_for_angle(angle, segment_thickness_dict, director, box_size):
    """Helper function to compute alignment for a given angle."""
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    center = np.array([box_size / 2, box_size / 2])
    line_vector_arr = []

    # Get all line vectors and areas
    for segment in segment_thickness_dict.values():
        m_pts = np.array([segment.middle_segment.start, segment.middle_segment.end])
        (start_rotated, end_rotated) = rot(m_pts, center, rotation_matrix)
        line_vector = np.array(end_rotated) - np.array(start_rotated)
        line_vector_arr.append({'line_vector': line_vector, 'area': segment.area()})

    # Calculate the alignment for this angle
    alignment = get_alignment_mean(line_vector_arr, director)
    return angle, alignment

def get_max_alignment_angle(segment_thickness_dict, director, box_size, grid_points=360):
    """Get the angle with the maximum alignment."""
    # Define the angles we will test
    angles = np.linspace(0, 2 * np.pi, grid_points)

    with ProcessPoolExecutor() as executor:
        # Submit tasks for each angle in parallel, passing necessary arguments
        results = list(executor.map(
            compute_alignment_for_angle,
            angles,
            [segment_thickness_dict] * len(angles),
            [director] * len(angles),               
            [box_size] * len(angles)                 
        ))

    # Find the angle with the maximum alignment
    max_angle, _ = max(results, key=lambda x: x[1])

    return max_angle

def orientate_network(segment_thickness_dict, config, rotate_angle, box_size):
    # Rotate the orginal network
    rotation_matrix = np.array([[np.cos(rotate_angle), -np.sin(rotate_angle)],[np.sin(rotate_angle), np.cos(rotate_angle)]])
    center = np.array([box_size/2,box_size/2])

    config_angles = [ item['angle'] for item in config]
    orientated_config = []

    # Get all oriented lines
    for i, v in enumerate(segment_thickness_dict.values()):
        angle_rotated = config_angles[i] - rotate_angle
        n_p_0 = rot(np.array(v.middle_segment.start), center, rotation_matrix)
        n_p_1 = rot(np.array(v.middle_segment.end), center, rotation_matrix)

        # Find the intersection between the rotated line and the square
        polygon_box = Polygon_Shapely([(0, 0), (box_size, 0), (box_size, box_size), (0, box_size)])
        line_middle_point = LineString([(n_p_0[0], n_p_0[1]), (n_p_1[0], n_p_1[1])])

        # Calculate the intersection between the box and the line
        intersection = polygon_box.intersection(line_middle_point)

        # Check if the line intersects the polygon
        if intersection.is_empty:
            continue
        else:
            length = intersection.length
            midpoint = intersection.interpolate(length/2)

            x = midpoint.xy[0][0]
            y = midpoint.xy[1][0]

            orientated_config.append({ 'location': (x,y), 'angle': angle_rotated, 'thickness': config[i]['thickness'] })

    return orientated_config 

def generate_line_segments_thickness_orientation(
    size: int, 
    thickness_arr: List[float], 
    orientation: List[int],
    angles: List[float],
    config: List[List[float]] = None, 
    epsilon: float = 0,
    box_size: float = 1,
    grid_points: int = 360
    ) -> List[Tuple[Dict[str, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon], np.ndarray]]:
    """
    Generates a specified number of line segments and updates the polygon and segment thickness dictionaries.

    Args:
        size (int): The number of line segments to generate.
        thickness_arr (List[float]): A list containing the thickness values for each segment to be generated.
        angles (str): The angle distribution method for generating segments. Defaults to 'uniform'.
                List[float]: list of angles in radians.
        orientation (List[int]): the orientation of the model.
        config (List[List[float]]): A list of configurations for the nucleation points and angles.
        epsilon (float): the minimum distance between two line.
        box_size (float): the size of the system.

    Returns:
        - an array of dictionaries for each orientation containing:
        Tuple[Dict[str, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]]:
            - Updated dictionary of line segments.
            - Updated dictionary of polygons.
            - Updated dictionary of segment thicknesses.
            - Array of the nucleation points and angles [x,y,theta].
    """
    # Size of the box
    box_size_0 = box_size*np.sqrt(2)

    # Initial structure
    data_dict = generate_line_segments_dynamic_thickness(size = size,
                                                        thickness_arr =  thickness_arr,
                                                        epsilon= epsilon,
                                                        config = config,
                                                        angles = angles,
                                                        box_size= box_size_0)
    
    segment_thickness_dict = data_dict['segment_thickness_dict']
    generated_config = data_dict['generated_config']

    # Calculate alignment with the y axis
    director = (0,1)
    max_angle = get_max_alignment_angle(segment_thickness_dict, director, box_size, grid_points)
    
    # Regenerate network for each orientation
    output = []
    for o in orientation:
        rotate_angle = o-max_angle
        orientated_config = orientate_network(segment_thickness_dict, generated_config, rotate_angle, box_size)

        data_dict_new = generate_line_segments_dynamic_thickness(size=size,
                                                                thickness_arr=thickness_arr,
                                                                epsilon=epsilon,
                                                                config=orientated_config,
                                                                angles=angles,
                                                                box_size=box_size)

        output.append({'orientation': o, 'data_dict': data_dict_new})
    
    return output