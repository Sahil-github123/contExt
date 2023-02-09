import dearpygui.dearpygui as dpg

def showMeshGeneration(callbacks):
    with dpg.group(horizontal=True):
        with dpg.child_window(width=300, tag="meshGeneration"):
                
            with dpg.file_dialog(directory_selector=False, show=False, min_size=[400,300], tag='txt_file_dialog_id', id="txt_file_dialog_id", callback=callbacks.meshGeneration.openContourFile):
                dpg.add_file_extension("", color=(150, 255, 150, 255))
                dpg.add_file_extension(".txt", color=(0, 255, 255, 255))
                dpg.add_file_extension(".dat", color=(0, 255, 255, 255))


            dpg.add_text('Select a contour file to use.')
            dpg.add_button(tag='import_contour', label='Import Contour', callback=lambda: dpg.show_item("txt_file_dialog_id"))

            dpg.add_text('File Name:', tag='contour_file_name_text')
            dpg.add_text('File Path:', tag='contour_file_path_text')
                
            with dpg.window(label='Error', modal=True, show=False, tag="txtFileErrorPopup"):
                dpg.add_text("File doesn't contain a valid contour")
                dpg.add_button(label="Ok", callback=lambda: dpg.configure_item("txtFileErrorPopup", show=False))

            dpg.add_separator()

            dpg.add_text('Contour Ordering')
            dpg.add_button(tag='contour_ordering2', enabled=False, label='Anticlockwise', callback=callbacks.meshGeneration.toggleOrdering)
            with dpg.tooltip("contour_ordering2"):
                dpg.add_text("Click to change contour ordering. If the ordering is incorrect the mesh generation may have some errors")

            dpg.add_separator()

            dpg.add_text("Mesh Grid")
            dpg.add_button(label ='Plot Mesh Grid', tag='plotGrid', callback=callbacks.meshGeneration.toggleGrid, enabled=False)
            with dpg.tooltip("plotGrid"):
                dpg.add_text("Click to draw mesh grid and count the number of internal node. Might take a while.")
                
            dpg.add_separator()

            dpg.add_text('Mesh Generation Options')
            dpg.add_text('Original Nodes Number:', tag="nodeNumber")
            with dpg.tooltip("nodeNumber", tag="nodeNumberTooltip", show=False):
                dpg.add_text("Doesn't account submesh nodes number.")
            dpg.add_text('nx: --', tag='original_nx')
            dpg.add_text('ny: --', tag='original_ny')
            dpg.add_text('Nodes Number:')
            dpg.add_text('nx: --', tag='nx')
            dpg.add_text('ny: --', tag='ny')

            dpg.add_text('Original Node Size:')
            dpg.add_text('dx: --', tag='original_dx')
            dpg.add_text('dy: --', tag='original_dy')
            dpg.add_text('Node Size')
            with dpg.group(horizontal=True):
                dpg.add_text('dx:')
                dpg.add_input_float(tag='dx', default_value=1, min_value=1, min_clamped=True)
            with dpg.group(horizontal=True):
                dpg.add_text('dy:')
                dpg.add_input_float(tag='dy', default_value=1, min_value=1, min_clamped=True)

            dpg.add_text('Original Mesh Start:')
            dpg.add_text('x: --', tag='original_xi')
            dpg.add_text('y: --', tag='original_yi')
            dpg.add_text('Mesh Start')
            with dpg.group(horizontal=True):
                dpg.add_text('x:')
                dpg.add_input_float(tag='xi')
            with dpg.group(horizontal=True):
                dpg.add_text('y:')
                dpg.add_input_float(tag='yi')
            dpg.add_button(label='Apply Changes', callback= callbacks.meshGeneration.updateMesh)
            dpg.add_separator()
                
            with dpg.group(tag="sparseGroup"):
                dpg.add_text('Sparse and Adataptive Mesh')
                dpg.add_button(label='Add Mesh Zoom Region', enabled=False, tag="sparseButton", callback=lambda: dpg.configure_item("sparsePopup", show=True))
                dpg.add_button(label ='Reset Mesh', tag='resetMesh', callback=callbacks.meshGeneration.resetMesh, show=False)
                with dpg.tooltip("resetMesh"):
                    dpg.add_text("Click to remove all zoom regions.")

            dpg.add_separator()
                
            dpg.add_text("Save Mesh")
            dpg.add_button(tag='exportMesh', enabled=False, label='Export Mesh', callback=lambda: dpg.configure_item("exportMeshFile", show=True))
            with dpg.tooltip("exportMesh"):
                dpg.add_text("Click to save mesh data in text files.")
                
            with dpg.window(label='Add Mesh Zoom Region', modal=True, show=False, tag="sparsePopup", min_size=[400,420]):
                dpg.add_text('Type of Mesh Zoom')
                dpg.add_button(tag='meshZoomType', enabled=True, label='Sparse', callback=callbacks.meshGeneration.toggleZoom)
                with dpg.tooltip("meshZoomType"):
                    dpg.add_text("Click to change the mesh zoom type.", tag="meshZoomTypeTooltip")
                    
                dpg.add_separator()
                dpg.add_text('Zoom Region Name')
                dpg.add_input_text(tag="zoomRegionName", default_value="Zoom region 1")

                dpg.add_separator()
                dpg.add_text('Zoom Node Size')
                dpg.add_listbox(tag='dxListbox', items=['Divided by 2', 'Divided by 4', 'Divided by 8', 'Divided by 16'])
                    
                dpg.add_separator()
                dpg.add_text('Zoom Bottom')
                with dpg.group(horizontal=True):
                    dpg.add_text('Bottom x:')
                    dpg.add_input_float(tag='xi_zoom')
                with dpg.group(horizontal=True):
                    dpg.add_text('Bottom y:')
                    dpg.add_input_float(tag='yi_zoom')

                dpg.add_separator()
                dpg.add_text('Zoom Top')
                with dpg.group(horizontal=True):
                    dpg.add_text('Top x:')
                    dpg.add_input_float(tag='xf_zoom')
                with dpg.group(horizontal=True):
                    dpg.add_text('Top y:')
                    dpg.add_input_float(tag='yf_zoom')
                    
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Add Zoom", width=100, callback=callbacks.meshGeneration.addZoomRegion)
                    dpg.add_button(label="Cancel", width=100, callback=lambda: dpg.configure_item("sparsePopup", show=False))
                dpg.add_text("Invalid range due to overlap", tag="addZoomError", show=False)

            with dpg.window(label="Save File", modal=False, show=False, tag="exportMeshFile", no_title_bar=False, min_size=[600,255]):
                dpg.add_text("Name your file")
                dpg.add_input_text(tag='inputMeshNameText')
                dpg.add_separator()
                dpg.add_text("You MUST enter a File Name to select a directory")
                dpg.add_button(label='Select the directory', callback= callbacks.meshGeneration.openMeshDirectorySelector)
                dpg.add_file_dialog(directory_selector=True, min_size=[400,300], show=False, tag='meshDirectorySelectorFileDialog', id="meshDirectorySelectorFileDialog", callback=callbacks.meshGeneration.selectMeshFileFolder)
                dpg.add_separator()
                dpg.add_text('File Name: ', tag='exportMeshFileName')
                dpg.add_text('Complete Path Name: ', tag='exportMeshPathName')
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Save', callback=lambda: callbacks.meshGeneration.exportMesh())
                    dpg.add_button(label='Cancel', callback=lambda: dpg.configure_item('exportMeshWindow', show=False))
                dpg.add_text("Missing file name or directory.", tag="exportMeshError", show=False)

            dpg.add_separator()

        with dpg.child_window(tag='MeshGenerationParent'):
            with dpg.theme(tag="grid_plot_theme"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (100, 100, 100), category=dpg.mvThemeCat_Plots)
            with dpg.plot(tag="meshPlotParent", label="Mesh Plot", height=650, width=650):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

            with dpg.group(horizontal=True):
                dpg.add_text('Original Area: --', tag='original_area')
                dpg.add_text('Current Area: --', tag='current_area')
                dpg.add_text('Difference: --', tag='difference')
            with dpg.group(horizontal=True):
                dpg.add_text('Contour Nodes Number: --', tag='contour_nodes_number')
                dpg.add_text('Internal Nodes Number: --', tag='current_nodes_number', show=False)   
            pass