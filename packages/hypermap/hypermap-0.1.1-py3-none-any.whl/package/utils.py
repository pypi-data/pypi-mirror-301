import pandas as pd
import numpy as np


def is_point_in_circle(x, y, center, radius):
    return (x - center[0])**2 + (y - center[1])**2 <= radius**2

def generate_reticle_info(name, wafer_radius, reticle_width, reticle_height, num_reticles_x, num_reticles_y, 
                                 center_reticle_x, center_reticle_y, xoffset, yoffset):
    # reticle_width = 20.5  
    # reticle_height = 21.88  
    # num_reticles_x = 8  
    # num_reticles_y = 7  
    # center_reticle_x = 5 
    # center_reticle_y = 4
    # xoffset, yoffset = 8.938, -7.58  
    
    reticle = {}
    reticle['name'] = name 
    reticle['reticle_width'] = reticle_width
    reticle['reticle_height'] = reticle_height
    reticle['num_reticles_x'] = num_reticles_x
    reticle['num_reticles_y'] = num_reticles_y
    reticle['center_reticle_x'] = center_reticle_x
    reticle['center_reticle_y'] = center_reticle_y
    reticle['xoffset'] = xoffset
    reticle['yoffset'] = yoffset

    coordinates = {}
    # Calculate the bottom-left corner reticle on the grid (1, 1)  
    x0 = xoffset - reticle_width / 2 - (center_reticle_x - 1) * reticle_width
    y0 = yoffset - reticle_height / 2 - (center_reticle_y - 1) * reticle_height
    # Draw the grid of reticles
    for i in range(num_reticles_x):
        for j in range(num_reticles_y):
            # Calculate the bottom-left corner of each reticle, applying the offset
            x = x0 + i * reticle_width
            y = y0 + j * reticle_height
            
            # reticle_x, reticle_y design the coordinates of the reticle in the wafer (see reticle_map)
            reticle_x, reticle_y = i + 1, j + 1
           
            # Calculate the four corners of the reticle
            corners = [
                (x, y),  # Bottom-left
                (x + reticle_width, y),  # Bottom-right
                (x, y + reticle_height),  # Top-left
                (x + reticle_width, y + reticle_height)  # Top-right
            ]
            

            # Check how many corners are inside the circle
            num_corners_in_circle = sum(is_point_in_circle(xc, yc, (0, 0), wafer_radius) for xc, yc in corners)

            # Save the rectangle only if more than 1 corner is inside the circle 
            if num_corners_in_circle >= 1:
                coordinates[(reticle_x, reticle_y)] = corners
    
    reticle['coordinates'] = coordinates

    return reticle

def load_and_parse_S1_thickness(filename):
    LN_thick = pd.read_csv(f'{filename}.csv')
    LN1dict = dict()
    locxy = []
    for i in range(len(LN_thick)):
        LN1t = float(LN_thick.loc[i,'L1厚度 (nm)'])
        loc = LN_thick.loc[i,'样品编号'].split('(')[1].split(')')[0]
        xt, yt = float(loc.split(',')[0]), float(loc.split(',')[1])
        locxy.append((xt, yt))
        LN1dict[(xt, yt)] = LN1t

    locxy = sorted(locxy)
    LN = []
    locx = []
    locy = []
    for x, y in locxy:
        LN.append(LN1dict[(x,y)])
        locx.append(x)
        locy.append(y)

    data = pd.DataFrame()
    data['x (mm)'] = locx
    data['y (mm)'] = locy
    data['LN (nm)'] = LN
    return data


if __name__ == "__main__":
    # Example usage:
    pass