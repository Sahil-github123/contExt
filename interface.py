from subprocess import call
import dearpygui.dearpygui as dpg
from math import *

class Interface:
    def __init__(self, callbacks) -> None:
        self.callbacks = callbacks
        self.show()
        pass

    def show(self):
        dpg.create_context()
        dpg.create_viewport(title='ContExt - Image Processing Engine for Differential Calculus', width=900, height=600, min_height=600, min_width=900)
        with dpg.window(tag="Main"):
            self.showTabBar()
            pass
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Main", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
        pass

    def showTabBar(self):
        with dpg.tab_bar():
            self.showTabs()
        pass

    def showTabs(self):
        dpg.add_texture_registry(show=False, tag='textureRegistry')
        with dpg.tab(label='Processing'):
            self.showProcessing()
            pass
        with dpg.tab(label='Filtering'):
            self.showFiltering()
            pass
        with dpg.tab(label='Thresholding'):
            self.showThresholding()
            pass
        with dpg.tab(label='Contour Extraction'):
            self.showContourExtraction()
            pass
        with dpg.tab(label='Mesh Generation'):
            self.showMeshGeneration()
            pass
        with dpg.tab(label='Sparse Mesh Generation'):
            self.showSparseMeshGeneration()
            pass
        pass

    def showProcessing(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):

                with dpg.file_dialog(directory_selector=False, show=False, tag='file_dialog_id', id="file_dialog_id", callback=self.callbacks.openFile):
                    dpg.add_file_extension("", color=(150, 255, 150, 255))
                    dpg.add_file_extension(".png", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".jpeg", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".jpg", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".bmp", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".pgm", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".ppm", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".sr", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".ras", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".jpe", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".jp2", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".tiff", color=(0, 255, 255, 255))
                    dpg.add_file_extension(".tif", color=(0, 255, 255, 255))

                dpg.add_text('Select a image to use.')
                dpg.add_button(tag='import_image', label='Import Image', callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_text('File Name:', tag='file_name_text')
                dpg.add_text('File Path:', tag='file_path_text')
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Cropping')
                    dpg.add_button(label='Reset')
                dpg.add_text('Original Resolution:')
                dpg.add_text('Width:', tag='originalWidth')
                dpg.add_text('Height:', tag='originalHeight')
                dpg.add_text('Current Resolution:')
                dpg.add_text('Width:', tag='currentWidth')
                dpg.add_text('Height:', tag='currentHeight')
                dpg.add_text('New Resolution')
                with dpg.group(horizontal=True):
                    dpg.add_text('Start X')
                    dpg.add_input_int(tag='startX')
                with dpg.group(horizontal=True):
                    dpg.add_text('Start Y')
                    dpg.add_input_int(tag='startY')
                with dpg.group(horizontal=True):
                    dpg.add_text('End X')
                    dpg.add_input_int(tag='endX')
                with dpg.group(horizontal=True):
                    dpg.add_text('End Y')
                    dpg.add_input_int(tag='endY')
                dpg.add_button(label='Apply Changes')
                dpg.add_separator()

                pass
            with dpg.child_window():
                pass

    def showFiltering(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):
                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Histogram Equalization')
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Brightness and Contrast')
                dpg.add_text('Brightness')
                dpg.add_slider_int()
                dpg.add_text('Contrast')
                dpg.add_slider_int()
                dpg.add_separator()
                
                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Average Blur')
                dpg.add_text('Intensity')
                dpg.add_slider_int()
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Gaussian Blur')
                dpg.add_text('Intensity')
                dpg.add_slider_int()
                dpg.add_separator()

                pass
            with dpg.child_window():
                pass

    def showThresholding(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):

                dpg.add_text('Grayscale Conversion')
                dpg.add_checkbox(label='Exclude Blue Channel')
                dpg.add_checkbox(label='Exclude Green Channel')
                dpg.add_checkbox(label='Exclude Red Channel')
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Global Thresholding')
                dpg.add_text('Threshold')
                dpg.add_slider_int()
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Adaptative Mean Thresholding')
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Adaptative Gaussian Thresholding')
                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_checkbox()
                    dpg.add_text('Otsu\'s Binarization')
                dpg.add_text('(Works better after Gaussian Blur)')
                dpg.add_separator()


                pass
            with dpg.child_window():
                pass

    def showContourExtraction(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):

                dpg.add_text('OpenCV2 Find Contour')
                dpg.add_text('Approximation Mode')
                dpg.add_listbox(items=['None', 'Simple', 'TC89_L1', 'TC89_KCOS'])
                dpg.add_text('Interval without approximation')
                dpg.add_input_int()
                dpg.add_button(label='Apply Method')

                dpg.add_separator()
                dpg.add_text('Moore Neighborhood')
                dpg.add_text('Initial Pixel')
                dpg.add_input_int(label='X')
                dpg.add_input_int(label='Y')
                dpg.add_text('Search Direction')
                dpg.add_listbox(items=['Up', 'Right', 'Down', 'Left'])
                dpg.add_text('Interval')
                dpg.add_input_int()
                dpg.add_button(label='Apply Method')
                dpg.add_separator()


                dpg.add_text('Export Settings')
                dpg.add_text('Max Width Mapping')
                dpg.add_input_double()
                dpg.add_text('Max Height Mapping')
                dpg.add_input_double()
                dpg.add_text('X Offset')
                dpg.add_input_double()
                dpg.add_text('Y Offset')
                dpg.add_input_double()
                dpg.add_checkbox(label='Matlab mode')
                dpg.add_checkbox(label='Metadata')
                dpg.add_button(label='Export Contour')
                dpg.add_separator()


                pass
            with dpg.child_window():
                pass

    def showMeshGeneration(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):
                pass
            with dpg.child_window():
                pass

    def showSparseMeshGeneration(self):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=300):
                pass
            with dpg.child_window():
                pass