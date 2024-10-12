import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import matplotlib.patches as patches
import matplotlib.colors as colors

class HyperMap:
    """ wafermap represents a circular wafer layout, with edge exclusion, optional reticle"""
    def __init__(self, wafer_radius, *args, **kwargs):
        self.wafer_radius = wafer_radius
        self.title = kwargs.get('title', 'WaferMap')
        self.measurements = kwargs.get('measurements', {})
        self.reticle = kwargs.get('reticle', {})
        self.measurements_per_reticle = kwargs.get('measurements_per_reticle', {})
        
    def __str__(self):
        return f"drawing a wafermap with {self.wafer_radius}"      
    
    def draw_wafer_edge(self, ax):
        # Plot the circular part of the wafer edge, plot wafer edge with a flat edge at bottom
        theta_circle = np.linspace(0, 2 * np.pi, 1000)
        circle_x = self.wafer_radius * np.cos(theta_circle)
        circle_y = self.wafer_radius * np.sin(theta_circle)
        # Mask out the part of the circle that is below the flat line at y = _flat_y
        self._flat_y = -69.27
        circular_mask = circle_y >= self._flat_y
        ax.plot(circle_x[circular_mask], circle_y[circular_mask], color='black', linewidth=1)
        # Plot the flat edge at y = _flat_y
        flat_x = np.linspace(-np.sqrt(self.wafer_radius**2 - self._flat_y**2), np.sqrt(self.wafer_radius**2 - self._flat_y**2), 100)
        ax.plot(flat_x, [self._flat_y] * len(flat_x), color='black', linewidth=1)
        ax.plot(0, 0, marker='+', markersize=5, color='black')
        return 


    def draw_measurements(self, ax):
        """
        Plot the measurement data on the wafer.
        """
        if self.measurements:
            x, y = zip(*self.measurements.keys())
            self.x, self.y = list(x), list(y)
            self.values = list(self.measurements.values()) 
            
            
            # calculate edge exclusion based on measurements
            self.edge_exclusion = self.wafer_radius - max([np.sqrt(xi**2 + yi**2) for (xi, yi) in zip(self.x, self.y)])
            
            # calculate the flat_y (this method only works when the flat side is at the bottom)
            # step 1: find the flat side coordinates.
            self.flat_y = min (self.y)
            # step 2: add edge exclusion to the flat side coordinates
            self.flat_y -= self.edge_exclusion

            # Scatter plot to represent measurement data
            ax.scatter(self.x, self.y, color='black', s=1, zorder=5, label='Actual Points')
            # Annotate the actual values next to the black dots
            font_size = 3 if len(self.values) > 300 else 5
            decimal_places = 1 if len(self.values) > 300 else 2
            for i in range(len(self.x)):
                plt.text(self.x[i], self.y[i], f'{self.values[i]:.{decimal_places}f}', color='black', fontsize=font_size, ha='right', va='bottom')
            
            # calculate stats and label on the plot
            min_val = np.min(self.values)
            max_val = np.max(self.values)
            mean_val = np.mean(self.values)
            std_dev = np.std(self.values)
            range_val = max_val - min_val
            uniformity = 100 * (range_val / (2 * mean_val))
            # uniformity = 100 * (range_val / (max_val + min_val))
            stats_text = (f'Min: {min_val:.{decimal_places}f} \n'
                        f'Max: {max_val:.{decimal_places}f} \n'
                        f'Mean: {mean_val:.{decimal_places}f} \n'
                        f'Std Dev: {std_dev:.{decimal_places}f} \n'
                        f'Range: {range_val:.{decimal_places}f} \n'
                        f'Uniformity: {uniformity:.1f} %')
            plt.text(self.wafer_radius * 0.7, -self.wafer_radius * 1.0, stats_text, fontsize=5)
        return 

    def draw_contour_map(self, ax, interpolation_method='rbf', vmin=None, vmax=None, defined_grid=None):
        """
        Fit the measurement data into a grid and draw a contour map.
        """
        if self.measurements:
            # Generate a circular grid to fit the measurements inside the circle
            num_points = 300  # Number of points in the circular grid
            r = np.linspace(0, self.wafer_radius, num_points)
            theta = np.linspace(0, 2 * np.pi, num_points)
            r_grid, theta_grid = np.meshgrid(r, theta)
            # Convert polar coordinates to Cartesian coordinates (x, y)
            grid_x = r_grid * np.cos(theta_grid)
            grid_y = r_grid * np.sin(theta_grid)

            if interpolation_method == 'rbf':
                # Create RBF interpolator for extrapolation
                rbf = Rbf(self.x, self.y, self.values, function='multiquadric')
                # Interpolate/extrapolate the thickness values across the grid
                grid_values = rbf(grid_x, grid_y)
                
                # Overwrite the interpolated values at actual (x, y) points with actual thickness values
                # Find the closest grid points to each (x, y) and replace with actual values
                for i in range(len(self.x)):
                    # Find the closest grid point to the actual (x, y)
                    distance = np.sqrt((grid_x - self.x[i])**2 + (grid_y - self.y[i])**2)
                    closest_idx = np.unravel_index(np.argmin(distance), grid_x.shape)
                    # Overwrite the interpolated value with the actual thickness
                    # print(f'interpolcated value at meas_loc : {grid_values[closest_idx]}')
                    # print(f'actual value at meas_loc : {self.values[i]}')
                    
                    grid_values[closest_idx] = self.values[i]
                
                # mask out points outside the wafer
                mask = grid_y < self._flat_y
                grid_values[mask] = np.nan 

                # contour plot of wafermap.
                if not vmin or not vmax:
                    vmin, vmax = np.nanmin(grid_values), np.nanmax(grid_values)
                contour = ax.contourf(grid_x, grid_y, grid_values, cmap='coolwarm', levels=np.linspace(vmin, vmax, 100), extend='both')
                cbar = plt.colorbar(contour, ax=ax, shrink=0.5, extend='both')
                cbar.set_ticks(np.linspace(vmin, vmax, 10))

                if defined_grid:
                    defined_grid_x, defined_grid_y = zip(*defined_grid)
                    defined_grid_values = rbf(list(defined_grid_x), list(defined_grid_y))
                    
                    return defined_grid_values
                

            # elif interpolation_method == 'kriging':
            #     # Flatten the grid arrays for input into kriging
            #     grid_x_flat = grid_x.ravel()
            #     grid_y_flat = grid_y.ravel()
            #     # Choose the variogram model: 'linear', 'power', 'gaussian', 'spherical', 'exponential'
            #     variogram_model = 'spherical'
            #     # Create an Ordinary Kriging object
            #     OK = OrdinaryKriging(
            #         self.x, self.y, self.values,
            #         variogram_model=variogram_model,
            #         verbose=False,
            #         enable_plotting=False
            #     )

            #     # Perform the kriging interpolation
            #     # Since we have a flattened grid, we'll use the 'points' mode
            #     z_predicted, ss = OK.execute('points', grid_x_flat, grid_y_flat)

            #     # Reshape the predicted values back to the grid shape
            #     grid_values = z_predicted.reshape(grid_x.shape)

            #     mask = grid_y < self.flat_y
            #     grid_values[mask] = np.nan

            #     contour = ax.contourf(grid_x, grid_y, grid_values, cmap='coolwarm', levels=100)
            #     cbar = plt.colorbar(contour, shrink=0.5) 
        return 
    
    
    
    def draw_reticles(self, ax):
        """
        Plot the reticle locations on the wafer.
        reticle is a dictionary of reticle locations, where each key is a reticle site (x, y) 
        and each value is left-bottom coordinates of the reticle.
        """
        if self.reticle:
            reticle_width = self.reticle['reticle_width']
            reticle_height = self.reticle['reticle_height']
            for (x, y), _, _, _ in self.reticle['coordinates'].values():
                rect = patches.Rectangle((x, y), reticle_width, reticle_height, 
                                         linewidth=0.5, edgecolor='black', 
                                         facecolor='none')
                ax.add_patch(rect)
        return

    def draw_measurements_per_reticle(self, ax):
        """
        Plot the measurement data per reticle.
        """
        if self.measurements_per_reticle:
            reticle_width = self.reticle['reticle_width']
            reticle_height = self.reticle['reticle_height']
            # Define a colormap and normalize the values
            cmap = plt.colormaps.get_cmap('viridis')  
            norm = colors.Normalize(vmin=min(self.measurements_per_reticle.values()), 
                                    vmax=max(self.measurements_per_reticle.values()))
            for (reticle_x, reticle_y) in self.measurements_per_reticle.keys():
                color = cmap(norm(self.measurements_per_reticle[(reticle_x, reticle_y)]))
                rect = patches.Rectangle(self.reticle['coordinates'][(reticle_x, reticle_y)][0], 
                                         reticle_width, reticle_height, 
                                         linewidth=0.5, edgecolor='black', 
                                         facecolor=color, alpha=1)
                ax.add_patch(rect)

            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, orientation='vertical', location='left', shrink=0.4, pad=0.13)
            cbar.set_label('reticle level measurements')

        return
    
    def draw_edge_exclusions(self, ax):
        # Plot the circular part of the wafer edge, plot wafer edge with a flat edge at bottom
        theta_circle = np.linspace(0, 2 * np.pi, 1000)
        circle_x = (self.wafer_radius - 10) * np.cos(theta_circle)
        circle_y = (self.wafer_radius - 10)* np.sin(theta_circle)
        ax.plot(circle_x, circle_y, color='red', linewidth=0.5)
        
        theta_circle = np.linspace(0, 2 * np.pi, 1000)
        circle_x = (self.wafer_radius - 20) * np.cos(theta_circle)
        circle_y = (self.wafer_radius - 20)* np.sin(theta_circle)
        ax.plot(circle_x, circle_y, color='red', linewidth=0.5)
        return 

    def draw_wafer_map(self, vmin=None, vmax=None, defined_grid=None):
        """
        Draw the entire wafer map with optional components: wafer edge, measurements, contour map, reticle locations, and measurements per reticle.
        """
        _, ax = plt.subplots(figsize=(6, 6))
        # Set up the plot limits to match the wafer radius
        ax.set_xlim(-self.wafer_radius*1.3, self.wafer_radius*1.3)
        ax.set_ylim(-self.wafer_radius*1.3, self.wafer_radius*1.3)
        
        # Draw the wafer edge
        self.draw_wafer_edge(ax)
    
        if self.measurements:
            # plot wafer-level measurement data
            self.draw_measurements(ax)
            output = self.draw_contour_map(ax, vmin=vmin, vmax=vmax, defined_grid=defined_grid)
        
        # Conditionally plot reticle
        if self.reticle:
            self.draw_reticles(ax)
        
        # Conditionally plot measurements per reticle
        if self.measurements_per_reticle:
            self.draw_measurements_per_reticle(ax)

        # self.draw_edge_exclusions(ax)

        ax.set_aspect('equal')
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_title(self.title)
        plt.tight_layout()
        # plt.show()
        return output

if __name__ == '__main__':

   pass