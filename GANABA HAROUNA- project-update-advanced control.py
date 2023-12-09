import ezdxf                                                                # import ez
import matplotlib.pyplot as plt                                                   # import plt
import geopandas as gpd                                                           # import geopandas
import tkinter as tk                                                              # import tkinter
from tkinter import filedialog, simpledialog                                      # import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg                   # import FigureCanvasTkAgg
import numpy as np                                                                # import numpy
from shapely.geometry import Point                                                # from shapely.geometry import Point 

class DXFEditorApp(tk.Tk):
    def __init__(self, data = None):
        super().__init__()
        self.title("DXF Editor")                                                  # title
        self.geometry("1200x1000")                                                # width, height of the editor window
        self.data = data if data is not None else np.array([])                             
        self.num_points = tk.IntVar(value=None)                                   # number of points in default for line
        self.num_points_arc = tk.IntVar(value=None)                               # number of points in default for arc shape
        self.simulation_ongoing = False                                           # simulation
        self.x_coords = np.array([])                                              # x_coords coordinates
        self.y_coords = np.array([])                                              # y_coords coordinates
        self.ax = None
        self.ax2 = None                                                           
        self.init_ui()

    def init_ui(self):
        # Create a Figure and Tkinter Canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        # self.ax2 =                        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()
        

        # Create buttons for functionality
        new_button = tk.Button(self, text="New DXF",bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.create_new_dxf)                                         #open a new .dxf file
        open_button = tk.Button(self, text="Open DXF",bg ='light steel blue',font = 'BOLD 12',width = 20, height=1, command=self.open_dxf)                                              #open a .dxf file only
        save_button = tk.Button(self, text="Save Laser Data",bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.save_laser_data)                               #save laser data to desktop
        simulate_button = tk.Button(self, text="Start Simulation", bg ='green', font = 'BOLD 12',width = 20, height=1,  command=self.simulate_laser_movement)                           #start the simulation 
        reset_simulation_button = tk.Button(self, text=" Reset Program", bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.reset_simulation)                  #show the initial menu
        end_simulation_button = tk.Button(self, text=" Exit  Program",bg= 'red', font = 'BOLD 12',width = 20, height=1, command=self.end_simulation)                                    #exit the program
      


        # Buttons to enter the number of points and number of points for arc
        num_points_button = tk.Button(self, text="Enter divided points__lines",bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.enter_num_points)                      #input the number of points in case it is a straight line
        num_points_arc_button = tk.Button(self, text="Enter divided points__arcs",bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.enter_num_points_arc)               #input the number of points in case it is a arc portion
        update_button = tk.Button(self, text="Update Laser Path",bg ='light steel blue', font = 'BOLD 12',width = 20, height=1, command=self.update_laser_path) 
        
        # Create entry fields for num_points and num_points_arc
        num_points_label = tk.Label(self, text="Num Points_lines:", font = 'BOLD 10',width = 20, height=1 )                                            #input the number of points in case it is a straight line
        num_points_label_value = tk.Label(self, textvariable=self.num_points,font = 'BOLD 10',width = 20, height=1 )                                   #store the number of points in case it is a straight line
        num_points_arc_label = tk.Label(self, text="Num Points_Arcs:",  font = 'BOLD 10',width = 20, height=1 )                                        #input the number of points in case it is a arc portion
        num_points_arc_label_value = tk.Label(self , textvariable=self.num_points_arc,font = 'BOLD 10', width = 20, height=1)                          #store the number of points in case it is a arc portion
        
        
        #show the differentspin buttons
        new_button.pack()                                    #show the new_button in the menu bar
        open_button.pack()                                   #show the open_button in the menu bar
        num_points_button.pack()                             #show the num_points_button in the menu bar
        num_points_label_value.pack()                        #show the num_points_label_value in the menu bar
        num_points_arc_button.pack()                         #show the num_points_arc_button in the menu bar
        num_points_arc_label_value.pack()                    #show the num_points_arc_label_value in the menu bar
        update_button.pack()                                 #show the update_button in the menu bar
        save_button.pack()                                   #show the save_button in the menu bar
        simulate_button.pack()                               #show the simulate_button in the menu bar
        reset_simulation_button.pack()                       #show the reset_simulation_button in the menu bar
        end_simulation_button.pack()                         #show the end_simulation_button in the menu bar
        
     #create a new DXF file
    def create_new_dxf(self):
        new_dxf_path = filedialog.asksaveasfilename(defaultextension=".dxf", filetypes=[("DXF files", "*.dxf")])    
        if new_dxf_path:
            doc = ezdxf.new()                 # Create a new DXF document
            msp = doc.modelspace()
            
            # Add a line entities to the modelspace to get a triangle shape(we can adjust to get different shapes with line entities)
            msp.add_line(start=(0, 0), end=(1, 1))  
            msp.add_line(start=(1, 1), end=(1, 0))   
            msp.add_line(start=(1, 0), end=(0, 0)) 
            
            # Add an arc entity to the modelspace to get a circle shape
            center = (1, 1)                                                # Center of the circle containing the arc
            radius = 0.5
            start_angle = 0                                                # Start angle of the arc in degrees
            end_angle =180                                                 # End angle of the arc in degrees(according to the end angle, we can get a circle with 360 degrees)
            msp.add_arc(center=center, radius=radius, start_angle=start_angle, end_angle=end_angle)
              
            # functionality we want to execute                    
            doc.saveas(new_dxf_path)                                       #save the new dxf document
            self.load_and_plot_dxf(new_dxf_path)                           #load and display the new dxf file 


    #open and display the DXF file
    def open_dxf(self):
        file_path = filedialog.askopenfilename(filetypes=[("DXF files", "*.dxf")])
        if file_path:
            self.load_dxf(file_path)
            self.load_and_plot_dxf(file_path)
            

    #load and display the laser path planning platform information
    def load_and_plot_dxf(self, file_path):                            
        dxf_file = gpd.read_file(file_path)                                                   #read and display the dxf file
        dxf_file.plot(ax=self.ax)  
        # dxf_file.plot(ax=self.ax2)
        #plot
        self.ax.set_title('Laser Path Planning Editor')                                       #set title
        self.canvas.draw()                                                                    #draw the plot
        self.ax.set_xlabel('X-direction')                                                     #set the x-direction
        self.ax.set_ylabel('Y-direction')                                                     #set the y-direction
        plt.grid(True)                                                                        #activate grid
        
        
#load dxf file and print their coordinates
    def load_dxf(self, dxf1_path):
        try:
            doc = ezdxf.readfile(dxf1_path)
            print(f"Successfully loaded DXF file: {dxf1_path}")
            modelspace = doc.modelspace()
            for entity in modelspace.query('*'):
                print(f"Entity Type: {entity.dxftype()}, Data: {entity.dxfattribs()}")
        except ezdxf.DXFError as e:
            print(f"Error reading DXF file: {e}")
            
    #save laser data
    def save_laser_data(self):
        default_filename = "output.txt"
        laser_data_path = filedialog.asksaveasfilename(
            defaultextension = ".txt",
            filetypes=[("Text files", "*.txt")],
            # initialfile = default_filename
        )
        print(laser_data_path)
        
        if laser_data_path:
            with open(laser_data_path, 'w') as file:
                for coordinates in self.data:
                    line = ' '.join(map(str, coordinates))
                    file.write(line + '\n')
            print(f"Laser data has been saved to {laser_data_path}")
    
    #update laser path
    def update_laser_path(self):
        num_points = self.num_points.get()
        num_points_arc = self.num_points_arc.get()
        print(f"you divided the lines' trajectories into {num_points} points at equal sampling intervals,\nyou divided the arcs' trajectories into {num_points_arc} points at equal sampling intervals")
        
        #different points information
        x_coords =[]
        y_coords =[]
        #movement around first pattern characteristics
        start_point11 = ( 0, 0 )
        end_point11 = ( -70.4494512781, 0)
        start_point12 =  ( -70.4494512781, 0)
        end_point12 = ( -157.9542443419, 21.0454553492 )
        start_point13 = ( -157.9542443419, 21.0454553492 )
        end_point13 = ( -117.1014503458, 64.9891605038 )
        start_point14 = ( -117.1014503458, 64.9891605038 )
        end_point14 = ( -70.4494512781, 0)
        
        #movement around second pattern characteristics
        start_point21 = ( -70.4494512781, 0)
        end_point21 = ( 0, 32.1487603306 )
        start_point22 = ( 0, 32.1487603306 )
        end_point22 = ( -30, 62.1487603306 )
        
        # interpolate with an arc path to complete the second pattern
        def interpolate_arc ( radius, start_position, end_angle, num_points_arc ) :  
            
        # Calculate the start angle based on the start position
            start_angle = 0
            
        # Interpolate angles
            angles = np.linspace ( start_angle,end_angle, num_points_arc )

        # Parametric equations for a circle
            x23 = radius * np.cos (np.radians ( angles ) )
            y23 = radius * np.sin ( np.radians ( angles ) ) + 62.1487603306
            return -x23, y23
        
        # existing parameters:
        start_position = ( -30, 62.1487603306 )
        radius = 30
        end_angle = 270
        x23, y23 = interpolate_arc ( radius, start_position, end_angle, num_points)
        
        
        start_point31 = ( 0, 32.1487603306 )
        end_point31 = ( 80.6050340467, 0 )
        start_point32 = ( 80.6050340467, 0 )
        end_point32 = ( 98.443093928, 35.802285118)
        start_point33 = ( 98.443093928, 35.802285118)
        end_point33 = ( 158.8330899801,-16.667214373 )
        start_point34 = ( 158.8330899801,-16.667214373 )
        end_point34 = ( 133.9645023171, -45.3074734)
        start_point35 = ( 133.9645023171, -45.3074734)
        end_point35 = ( 80.6050340467, 0 )

        #movement around fourth pattern characteristics
        start_point41 =   ( 80.6050340467, 0 )
        end_point41 =( 31.4013355186, -55.1979521956 )
        start_point42 =  ( 31.4013355186, -55.1979521956 )
        end_point42 = ( 68.0096007714, -129.6764137166 )
        start_point43 =  ( 68.0096007714, -129.6764137166 )
        end_point43 = ( 18.7300807634, -192.6964812173 )
        start_point44 =  ( 18.7300807634, -192.6964812173 )
        end_point44 = ( -56.4337742475,-165.3031444382 )
        start_point45 =   ( -56.4337742475,-165.3031444382 )
        end_point45 = ( -53.6080713618, -85.3530637428 )
        start_point46 =   ( -53.6080713618, -85.3530637428 )
        end_point46 = ( 31.4013355186, -55.1979521956 )
        
        #the interpolation of the pattern 1
        x11 = np.linspace ( start_point11[0], end_point11[0], num_points )
        y11 = np.linspace ( start_point11[1], end_point11[1], num_points )
        x12 = np.linspace ( start_point12[0], end_point12[0], num_points )
        y12 = np.linspace ( start_point12[1], end_point12[1], num_points )
        x13 = np.linspace ( start_point13[0], end_point13[0], num_points )
        y13 = np.linspace ( start_point13[1], end_point13[1], num_points )
        x14 = np.linspace ( start_point14[0], end_point14[0], num_points )
        y14 = np.linspace ( start_point14[1], end_point14[1], num_points )

        # interpolation of the pattern 2
        x21 = np.linspace ( start_point21[0], end_point21[0], num_points )
        y21 = np.linspace ( start_point21[1], end_point21[1], num_points )
        x22 = np.linspace ( start_point22[0], end_point22[0], num_points )
        y22 = np.linspace ( start_point22[1], end_point22[1], num_points )

         # interpolation of the pattern 3
        x31 = np.linspace ( start_point31[0], end_point31[0], num_points )
        y31 = np.linspace ( start_point31[1], end_point31[1], num_points )
        x32 = np.linspace ( start_point32[0], end_point32[0], num_points )
        y32 = np.linspace ( start_point32[1], end_point32[1], num_points )
        x33 = np.linspace ( start_point33[0], end_point33[0], num_points )
        y33 = np.linspace ( start_point33[1], end_point33[1], num_points )
        x34 = np.linspace ( start_point34[0], end_point34[0], num_points )
        y34 = np.linspace ( start_point34[1], end_point34[1], num_points )
        x35 = np.linspace ( start_point35[0], end_point35[0], num_points )
        y35 = np.linspace ( start_point35[1], end_point35[1], num_points )

        # interpolation of the pattern 4
        x41 = np.linspace ( start_point41[0], end_point41[0], num_points)
        y41 = np.linspace ( start_point41[1], end_point41[1], num_points )
        x42 = np.linspace ( start_point42[0], end_point42[0], num_points )
        y42 = np.linspace ( start_point42[1], end_point42[1], num_points )
        x43 = np.linspace ( start_point43[0], end_point43[0], num_points )
        y43 = np.linspace ( start_point43[1], end_point43[1], num_points )
        x44 = np.linspace ( start_point44[0], end_point44[0], num_points )
        y44 = np.linspace ( start_point44[1], end_point44[1], num_points )
        x45 = np.linspace ( start_point45[0], end_point45[0], num_points )
        y45 = np.linspace ( start_point45[1], end_point45[1], num_points )
        x46 = np.linspace ( start_point46[0], end_point46[0], num_points )
        y46 = np.linspace ( start_point46[1], end_point46[1], num_points )

        ##store the data to generate in a laser machine
        self.x_coords = np.concatenate( ( x11, x12, x13, x14, x21, x22, x23, x31, x32, x33, x34, x35, x41, x42, x43, x44, x45, x46) )   # the definition of the path along x axis
        self.y_coords = np.concatenate( ( y11, y12, y13, y14, y21, y22, y23, y31, y32, y33, y34, y35, y41, y42, y43, y44, y45, y46) )   # the definition of the path along y axis
        path_coordinates = list ( zip ( self.x_coords, self.y_coords ) )
        
        #save path coordinates to a text file
        # point_txt = "output.txt"
        # with open(point_txt, 'w') as file:
        #     for coordinates in path_coordinates:
        #         line = ' '.join( map(str, coordinates ) )
        #         file.write( line + '\n' )
        # print(f"A laser data has been written to { point_txt } " )
        self.data = path_coordinates
        
    def plot_dxf(self, file_path):
        if file_path:
            dxf_file = gpd.read_file(file_path)
            dxf_file.plot(ax=self.ax)
            # dxf_file.plot(ax=self.ax2)
            self.ax.set_title('Laser Path Planning Editor')
            self.dxf_file.plot(ax=self.ax)
            self.ax.set_xlabel('X-direction')
            self.ax.set_ylabel('Y-direction')
            #plt.show()
            plt.grid(True)
        
    #update the trajectories of the laser path 
    def update_trajectories(self, index):
        self.ax.plot(self.x_coords[:index + 1], self.y_coords[:index + 1], 'r-')     # Draw the trajectory up to the current point
        x =self.x_coords [ index ]
        y = self.y_coords [ index ]
        point, = self.ax.plot( x, y, 'bo' ) 
        self.ax.set_xlabel('X-direction')
        self.ax.set_ylabel('Y-direction')
        self.ax.set_title('Laser Path Planning Editor') 
        plt.axis('equal')
        plt.grid(True)
        
        # Update the canvas
        self.canvas.draw ()
        point.remove()
        
    #simulate the laser movement    
    def simulate_laser_movement(self, index = 0) :
        if index < len ( self.x_coords )  :
            self.update_trajectories ( index )
            self.after(100, lambda idx=index + 1: self.simulate_laser_movement(idx))
            
             
    #reset the simulation       
    def reset_simulation(self):
        self.simulation_ongoing = False
        print(f"Simulation has ended")                     #show the end of simulation
        self.ax.clear()                                    # Clear the trajectories
        self.x_coords = np.array([])                       # Reset the y_coords array
        self.y_coords = np.array([])                       # Reset the y_coords array
        self.canvas.draw() 
        
    #exit the program
    def end_simulation(self):
        self.destroy()
        
    #set the division of each trajectory in number of points for a line case
    def enter_num_points(self):
        value = simpledialog.askinteger("Enter Num Points for straight lines", "Enter the number of points for straight lines:")
        if value is not None:
            self.num_points.set(value)

#set the division of each trajectory in number of points for an arc case
    def enter_num_points_arc(self):
        value = simpledialog.askinteger("Enter Num Points for Arcs", "Enter the number of points for arcs:")
        if value is not None:
           self.num_points_arc.set(value)

#exceute the program
if __name__ == '__main__':
    # file_name = "output.txt"
    # data = np.loadtxt(file_name)
    execute = DXFEditorApp()
    execute.protocol("WM_DELETE_WINDOW", execute.end_simulation)               # Set the close event to end_simulation
    execute.mainloop()

