import dearpygui.dearpygui as dpg
import os.path
from ._mesh import Mesh
from ._sparseMesh import SparseMesh

class MeshGeneration:
    
    def __init__(self) -> None:

        self.filePath = None
        self.txtFilePath = None
        self.txtFileName = None
        self.toggleOrderingFlag = True
        self.toggleZoomFlag = True
        self.toggleGridFlag = False
        self.sparseMeshHandler = None
        self.countGrid = 0
        self.originalX = []
        self.originalY = []
        self.currentX = []
        self.currentY = []
        self.exportFilePath = None
        self.exportFileName = None

    def openContourFile(self, sender = None, app_data = None):
        self.txtFilePath = app_data['file_path_name']
        self.txtFileName = app_data['file_name']
        
        dpg.set_value('contour_file_name_text', 'File Name: ' + self.txtFileName)
        dpg.set_value('contour_file_path_text', 'File Path: ' + self.txtFilePath)

        self.originalX = []
        self.originalY = []
        f = open(self.txtFilePath,'r')
        for line in f.readlines():
            aux = line.split()
            if(len(aux) != 2):
                print("File doesn't contain a valid contour")
                dpg.configure_item("txtFileErrorPopup", show=True)
                return
            try:
                self.originalX.append(float(aux[0]))
                self.originalY.append(float(aux[1]))
            except:
                print("File doesn't contain a valid contour")
                dpg.configure_item("txtFileErrorPopup", show=True)
                return
        if not self.toggleOrderingFlag:
            self.originalX = self.originalX[:4] + self.originalX[4::-1]
            self.originalY = self.originalY[:4] + self.originalY[4::-1]
        f.close()
        self.importContour()
        
    def importContour(self, sender = None, app_data = None):
        if self.toggleGridFlag:
            self.removeGrid()
        dpg.delete_item("meshPlot")
        dpg.delete_item("originalMeshPlot")
        dpg.configure_item('contour_ordering2', enabled=True)
        dpg.configure_item('sparseButton', enabled=True)
        dpg.configure_item('plotGrid', enabled=True)

        if self.currentX == [] and self.currentY == []:
            dpg.configure_item("exportMesh", show=True)
            dpg.configure_item("exportMeshText", show=True)
            dpg.configure_item("exportMeshTooltip", show=True)
            dpg.add_separator(parent="meshGeneration")

        self.currentX = self.originalX
        self.currentY = self.originalY
        self.originalX = self.originalX[4:]
        self.originalY = self.originalY[4:]

        nx = self.currentX[0]
        ny = self.currentY[0]
        xmin = self.currentX[1]
        ymin = self.currentY[1]
        xmax = self.currentX[2]
        ymax = self.currentY[2]
        dx = self.currentX[3]
        dy = self.currentY[3]

        dpg.set_value("original_xi", 'x: ' + str(xmin))
        dpg.set_value("original_yi", 'y: ' + str(ymin))
        dpg.set_value("original_dx", 'dx: ' + str(dx))
        dpg.set_value("original_dy", 'dy: ' + str(dy))
        dpg.set_value("original_nx", 'nx: ' + str(int(nx)))
        dpg.set_value("original_ny", 'ny: ' + str(int(ny)))
        dpg.set_value("nx", 'nx: ' + str(int(nx)))
        dpg.set_value("ny", 'ny: ' + str(int(ny)))
        dpg.configure_item("dx", default_value = dx)
        dpg.configure_item("dy", default_value = dy)
        dpg.configure_item("xi", default_value = xmin)
        dpg.configure_item("yi", default_value = ymin)
        dpg.configure_item("xi_zoom", default_value = xmin)
        dpg.configure_item("yi_zoom", default_value = ymin)
        dpg.configure_item("xf_zoom", default_value = xmin + dx, min_value = xmin + dx)
        dpg.configure_item("yf_zoom", default_value = ymin + dy, min_value = ymin + dy)

        dpg.set_value('current_area', 'Current Area: --')
        dpg.set_value('difference', 'Difference: --')

        self.currentX = self.currentX[4:]
        self.currentY = self.currentY[4:]
        dpg.set_value("original_area", "Original Area: " + str(Mesh.get_area(self.currentX, self.currentY)))
        dpg.add_line_series(self.currentX, self.currentY, label="Original Mesh", tag="originalMeshPlot", parent='y_axis')
        dpg.fit_axis_data("x_axis")
        dpg.fit_axis_data("y_axis")     

    def cancelImportContour(self, sender = None, app_data = None):
        dpg.hide_item("txt_file_dialog_id")
        pass

    def toggleOrdering(self, sender = None, app_data = None):
        self.toggleOrderingFlag = not self.toggleOrderingFlag
        if self.toggleOrderingFlag:
            dpg.configure_item('contour_ordering', label="Anticlockwise")
            dpg.configure_item('contour_ordering2', label="Anticlockwise")
        else:
            dpg.configure_item('contour_ordering', label="Clockwise")
            dpg.configure_item('contour_ordering2', label="Clockwise")
        pass

    def toggleZoom(self, sender = None, app_data = None):
        self.toggleZoomFlag = not self.toggleZoomFlag
        if self.toggleZoomFlag:
            dpg.configure_item('meshZoomType', label="Sparse")
        else:
            dpg.configure_item('meshZoomType', label="Adaptive")
        pass

    def addZoomRegion(self, sender = None, app_data = None):
        listBoxValue = dpg.get_value("dxListbox")
        n = int(listBoxValue[11:])
        name = dpg.get_value("zoomRegionName")
        dx = dpg.get_value("dx")
        dy = dpg.get_value("dy")
        xmin = dpg.get_value("xi_zoom")
        ymin = dpg.get_value("yi_zoom")
        xmax = dpg.get_value("xf_zoom")
        ymax = dpg.get_value("yf_zoom")

        if self.sparseMeshHandler == None:
            self.sparseMeshHandler = SparseMesh()
            self.sparseMeshHandler.addRange(dpg.get_value("xi"), dpg.get_value("yi"), max(self.originalX), max(self.originalY), dx, dy)
        if not self.sparseMeshHandler.addRange(xmin, ymin, xmax, ymax, n, n):
            dpg.configure_item("addZoomError", show=True)
            return

        dpg.configure_item("addZoomError", show=False)
        nZoom = len(self.sparseMeshHandler.ranges) - 1
        dpg.add_separator(tag="separatorZoomStart" + str(nZoom), parent="sparseGroup")
        dpg.add_text(name, tag="zoomTxt" + str(nZoom), parent="sparseGroup")
        dpg.add_text("Node Size: " + listBoxValue, tag="listBoxZoom" + str(nZoom), parent="sparseGroup")
        dpg.add_text("Bottom x: " + str(xmin), tag="xminZoom" + str(nZoom), parent="sparseGroup")
        dpg.add_text("Bottom y: " + str(xmin), tag="yminZoom" + str(nZoom), parent="sparseGroup")
        dpg.add_text("Top x: " + str(xmin), tag="xmaxZoom" + str(nZoom), parent="sparseGroup")
        dpg.add_text("Top x: " + str(xmin), tag="ymaxZoom" + str(nZoom), parent="sparseGroup")
        dpg.add_button(tag="removeZoom" + str(nZoom), label="Remove Zoom Region", parent="sparseGroup", callback=self.removeZoomRegion)

        if nZoom == 2:
            dpg.configure_item("resetMesh", show=True)
        dpg.configure_item("sparsePopup", show=False)
        dpg.configure_item("meshZoomType", enabled=False)
        dpg.set_value("meshZoomTypeTooltip", "You cannot add diferent types of zoom on the same mesh.")
        self.updateMesh()
        dpg.configure_item("zoomRegionName", default_value="Zoom region " + str(nZoom + 1))


    def removeZoomRegion(self, sender, app_data=None):
        nZoom = len(self.sparseMeshHandler.ranges)
        nRegion = int(sender[10:])
        self.removeGrid()
        aux = self.sparseMeshHandler.ranges.pop(nRegion)

        if nZoom < 4:
            dpg.configure_item("resetMesh", show=False)
        if nZoom == 2:
            self.sparseMeshHandler = None
            dpg.configure_item("meshZoomType", enabled=True)
            dpg.set_value("meshZoomTypeTooltip", "Click to change the mesh zoom type.")
        else:
            for i in range(nRegion, nZoom):
                name = dpg.get_value("zoomTxt" + str(i + 1))
                nodeSize = dpg.get_value("listBoxZoom" + str(i + 1))
                dpg.set_value("zoomTxt" + str(i), name)
                dpg.set_value("listBoxZoom" + str(i), nodeSize)
            pass
        dpg.delete_item("separatorZoomStart" + str(nZoom - 1))
        dpg.delete_item("zoomTxt" + str(nZoom - 1))
        dpg.delete_item("listBoxZoom" + str(nZoom - 1))
        dpg.delete_item("xminZoom" + str(nZoom - 1))
        dpg.delete_item("yminZoom" + str(nZoom - 1))
        dpg.delete_item("xmaxZoom" + str(nZoom - 1))
        dpg.delete_item("ymaxZoom" + str(nZoom - 1))
        dpg.delete_item("removeZoom" + str(nZoom - 1))
        dpg.delete_item("plotRec" +  str(nZoom - 1))
        self.updateMesh()

    def updateMesh(self, sender=None, app_data=None):
        dx = dpg.get_value("dx")
        dy = dpg.get_value("dy")
        xmin = dpg.get_value("xi")
        ymin = dpg.get_value("yi")
        self.removeGrid()

        if self.sparseMeshHandler == None:
            self.currentX, self.currentY = Mesh.getMesh(self.originalX, self.originalY, xmin, ymin, dx, dy)
            nx = self.currentX[0]
            ny = self.currentY[0]
            xmin = self.currentX[1]
            ymin = self.currentY[1]
            dx = self.currentX[3]
            dy = self.currentY[3]

            self.currentX = self.currentX[4:]
            self.currentY = self.currentY[4:]
            dpg.set_value("nx", 'nx: ' + str(int(nx)))
            dpg.set_value("ny", 'ny: ' + str(int(ny)))
            self.plotGrid()
        else:
            self.sparseMeshHandler.updateRanges(dx, dy, xmin, ymin)

            if self.toggleZoomFlag == True:
                self.currentX, self.currentY = self.sparseMeshHandler.get_sparse_mesh(self.originalX, self.originalY)
                nx = self.sparseMeshHandler.ranges[0]["nx"]
                ny = self.sparseMeshHandler.ranges[0]["ny"]
                dpg.configure_item("nodeNumber", show=True)
            else:
                self.currentX, self.currentY = self.sparseMeshHandler.get_adaptative_mesh(self.originalX, self.originalY)
                nx = len(self.sparseMeshHandler.dx)
                ny = len(self.sparseMeshHandler.dy)
            
            dpg.set_value("nx", 'nx: ' + str(int(nx)))
            dpg.set_value("ny", 'ny: ' + str(int(ny)))
            self.plotGrid()
            for i in range(1,len(self.sparseMeshHandler.ranges)):
                dpg.delete_item("plotRec" +  str(i))
                r = self.sparseMeshHandler.ranges[i]
                dpg.set_value("xminZoom" + str(i), "Bottom x: " + str(r['xi']))
                dpg.set_value("yminZoom" + str(i), "Bottom y: " + str(r['yi']))
                dpg.set_value("xmaxZoom" + str(i), "Top x: " + str(r['xf']))
                dpg.set_value("ymaxZoom" + str(i), "Top y: " + str(r['yf']))
                dpg.delete_item("plotRec" +  str(i))
                dpg.add_line_series([r['xi'],r['xi'],r['xf'],r['xf'],r['xi']], [r['yi'],r['yf'],r['yf'],r['yi'],r['yi']], tag="plotRec" +  str(i), label=dpg.get_value("zoomTxt" + str(i)), parent="y_axis")

            aux = self.sparseMeshHandler.ranges[0]
            xmin = aux["xi"]
            ymin = aux["yi"]
            dx = aux["dx"]
            dy = aux["dy"]

        dpg.configure_item("dx", default_value = dx)
        dpg.configure_item("dy", default_value = dy)
        dpg.configure_item("xi", default_value = xmin)
        dpg.configure_item("yi", default_value = ymin)

        area = Mesh.get_area(self.currentX, self.currentY)
        dpg.set_value("current_area", "Currente Area: " + str(area))
        aux = dpg.get_value("original_area")
        originalArea = float(aux[15:])
        dif = abs(originalArea - area)
        dpg.set_value("difference", "Difference: " + str(dif) + " ({:.2f}%)".format(abs(100*dif/originalArea)))
        dpg.set_value("contour_nodes_number", "Contour Nodes Number: " + str(len(self.currentX)))

        dpg.delete_item("meshPlot")
        dpg.add_line_series(self.currentX, self.currentY, label="Current Mesh", tag="meshPlot", parent='y_axis')
        dpg.fit_axis_data("x_axis")
        dpg.fit_axis_data("y_axis")

    def plotGrid(self, sender=None, app_data=None):
        if self.toggleGridFlag:
            dpg.configure_item("current_nodes_number", show=True)
            nInternalNodes = self.drawGrid()
            dpg.set_value("current_nodes_number","Internal Nodes Number: " + str(nInternalNodes))
        else:
            dpg.configure_item("current_nodes_number", show=False)

    def drawGrid(self, sender=None, app_data=None):
        dpg.configure_item('plotGrid', enabled=False)
        nInternalNodes = 0       
        meshTypeFlag = 0
        if self.sparseMeshHandler != None:
            if self.toggleZoomFlag:
                meshTypeFlag = 1
            else:
                meshTypeFlag = 2

        if meshTypeFlag == 2:
            dx = self.sparseMeshHandler.dx
            dy = self.sparseMeshHandler.dy
        else:
            dx = dpg.get_value("dx")
            dy = dpg.get_value("dy")
        xmin = dpg.get_value("xi")
        ymin = dpg.get_value("yi")
        nx = int(dpg.get_value("nx")[4:])
        ny = int(dpg.get_value("ny")[4:])


        for i in range(ny):
            flag = True
            xGrid = []
            yGrid = []
            for j in range(nx):
                if meshTypeFlag == 2:
                    auxX = dx[j]
                    auxY = dy[i]
                else:
                    auxX = xmin + j * dx
                    auxY = ymin + i * dy

                if Mesh.insidePolygon(self.currentX, self.currentY, auxX, auxY):
                    if flag:
                        flag = False
                        xGrid.append(auxX)
                        yGrid.append(auxY)
                        xGrid.append(auxX)
                        yGrid.append(auxY)
                    else:
                        xGrid[-1] = auxX
                        yGrid[-1] = auxY
                    nInternalNodes += 1
                else:
                    flag = True
            tam = len(xGrid)
            count = 0
            while count < tam:
                dpg.add_line_series(xGrid[count:count + 2], yGrid[count:count + 2], tag="meshGridPlotY0/" + str(i) + "/" + str(count), parent='y_axis')
                dpg.bind_item_theme("meshGridPlotY0/" + str(i) + "/"  + str(count), "grid_plot_theme")
                count += 2
            if count > self.countGrid:
                self.countGrid = count 

        for j in range(nx):
            flag = True
            xGrid = []
            yGrid = []
            for i in range(ny):
                if meshTypeFlag == 2:
                    auxX = dx[j]
                    auxY = dy[i]
                else:
                    auxX = xmin + j * dx
                    auxY = ymin + i * dy

                if Mesh.insidePolygon(self.currentX, self.currentY, auxX, auxY):
                    if flag:
                        flag = False
                        xGrid.append(auxX)
                        yGrid.append(auxY)
                        xGrid.append(auxX)
                        yGrid.append(auxY)
                    else:
                        xGrid[-1] = auxX
                        yGrid[-1] = auxY
                else:
                    flag = True

            tam = len(xGrid)
            count = 0
            while count < tam:
                dpg.add_line_series(xGrid[count:count + 2], yGrid[count:count + 2], tag="meshGridPlotX0/" + str(j) + "/" + str(count), parent='y_axis')
                dpg.bind_item_theme("meshGridPlotX0/" + str(j) + "/"  + str(count), "grid_plot_theme")
                count += 2
            if count > self.countGrid:
                self.countGrid = count 
        
        if meshTypeFlag == 1:
            nAux = 0
            for z in range(1, len(self.sparseMeshHandler.ranges)):
                r = self.sparseMeshHandler.ranges[z]
                for i in range(r["ny"]):
                    flag = True
                    xGrid = []
                    yGrid = []
                    for j in range(r["nx"]):
                        auxX = r["xi"] + j * r["dx"]
                        auxY = r["yi"] + i * r["dy"]
                        if Mesh.insidePolygon(self.currentX, self.currentY, auxX, auxY):
                            if flag:
                                flag = False
                                xGrid.append(auxX)
                                yGrid.append(auxY)
                                xGrid.append(auxX)
                                yGrid.append(auxY)
                            else:
                                xGrid[-1] = auxX
                                yGrid[-1] = auxY
                            nAux += 1
                        else:
                            flag = True
                    tam = len(xGrid)
                    count = 0
                    while count < tam:
                        dpg.add_line_series(xGrid[count:count + 2], yGrid[count:count + 2], tag="meshGridPlotY" + str(z) + "/" + str(i) + "/" + str(count), parent='y_axis')
                        dpg.bind_item_theme("meshGridPlotY" + str(z) + "/" + str(i) + "/" + str(count), "grid_plot_theme")
                        count += 2
                    if count > self.countGrid:
                        self.countGrid = count 

                for j in range(r["nx"]):
                    flag = True
                    xGrid = []
                    yGrid = []
                    for i in range(r["ny"]):
                        auxX = r["xi"] + j * r["dx"]
                        auxY = r["yi"] + i * r["dy"]
                        if Mesh.insidePolygon(self.currentX, self.currentY, auxX, auxY):
                            if flag:
                                flag = False
                                xGrid.append(auxX)
                                yGrid.append(auxY)
                                xGrid.append(auxX)
                                yGrid.append(auxY)
                            else:
                                xGrid[-1] = auxX
                                yGrid[-1] = auxY
                        else:
                            flag = True
                    tam = len(xGrid)
                    count = 0
                    while count < tam:
                        dpg.add_line_series(xGrid[count:count + 2], yGrid[count:count + 2], tag="meshGridPlotX" + str(z) + "/" + str(j) + "/" + str(count), parent='y_axis')
                        dpg.bind_item_theme("meshGridPlotX" + str(z) + "/" + str(j) + "/" + str(count), "grid_plot_theme")
                        count += 2
                    if count > self.countGrid:
                        self.countGrid = count 
                
                #nAux -= (1 + (r["xf"] - r["xi"])//dx) * (1 + (r["yf"] - r["yi"])//dy)    
            nInternalNodes += nAux - nAux//4
        dpg.configure_item('plotGrid', enabled=True)
        return nInternalNodes

    def removeGrid(self, sender=None, app_data=None):
        if self.sparseMeshHandler == None or not self.toggleZoomFlag:
            n = 1
            nx = [int(dpg.get_value("nx")[4:])]
            ny = [int(dpg.get_value("ny")[4:])]
        else:
            aux = self.sparseMeshHandler.ranges
            n = len(aux)
            nx = []
            ny = []
            for r in aux:
                nx.append(r["nx"])
                ny.append(r["ny"])
        for k in range(0,self.countGrid,2):
            for z in range(n):
                for i in range(ny[z]):
                        dpg.delete_item("meshGridPlotY" + str(z) + "/" + str(i) + "/" + str(k))
                for j in range(nx[z]):
                        dpg.delete_item("meshGridPlotX" + str(z) + "/" + str(j) + "/" + str(k))
        self.countGrid = 0

    def toggleGrid(self, sender=None, app_data=None):
        self.toggleGridFlag = not self.toggleGridFlag
        if self.toggleGridFlag:
            dpg.configure_item("plotGrid", label="Remove Plot Mesh Grid")
            self.updateMesh()
        else:
            dpg.configure_item("plotGrid", label="Plot Mesh Grid")
            self.removeGrid()

    def resetMesh(self, sender=None, app_data=None):
        for i in range(1,len(self.sparseMeshHandler.ranges)):
            dpg.delete_item("separatorZoomStart" + str(i))
            dpg.delete_item("zoomTxt" + str(i))
            dpg.delete_item("listBoxZoom" + str(i))
            dpg.delete_item("xminZoom" + str(i))
            dpg.delete_item("yminZoom" + str(i))
            dpg.delete_item("xmaxZoom" + str(i))
            dpg.delete_item("ymaxZoom" + str(i))
            dpg.delete_item("removeZoom" + str(i))
            dpg.delete_item("plotRec" +  str(i))

        dpg.configure_item("meshZoomType", enabled=True)
        dpg.set_value("meshZoomTypeTooltip", "Click to change the mesh zoom type.")
        dpg.configure_item("resetMesh", show=False)
        self.sparseMeshHandler = None
        self.updateMesh()

    def openMeshDirectorySelector(self, sender=None, app_data=None):
        if dpg.get_value('inputMeshNameText') != '':
            dpg.configure_item('meshDirectorySelectorFileDialog', show=True)

    def selectMeshFileFolder(self, sender=None, app_data=None):

        self.exportFilePath = app_data['file_path_name']

        self.exportFileName = dpg.get_value('inputMeshNameText') + '.txt'
        filePath = os.path.join(self.exportFilePath, self.exportFileName)

        dpg.set_value('exportMeshFileName', 'File Name: ' + self.exportFileName)
        dpg.set_value('exportMeshPathName', 'Complete Path Name: ' + filePath)

        pass

    def exportMesh(self, sender=None, app_data=None):
        if self.exportFilePath is None:
            dpg.configure_item("exportMeshError", show=True)
            return

        dpg.configure_item("exportMeshError", show=False)
        filePath = os.path.join(self.exportFilePath, self.exportFileName)
        if self.sparseMeshHandler != None:
            if self.toggleZoomFlag:
                SparseMesh.export_coords_mesh(filePath, self.currentX, self.currentY, self.toggleOrderingFlag)
                filePathRanges = filePath[:-4] + "_ranges.txt"
                self.sparseMeshHandler.export_ranges(filePathRanges)
            else:
                SparseMesh.export_coords_mesh(filePath, self.currentX, self.currentY, self.toggleOrderingFlag)
                filePathDx = filePath[:-4] + "_dx.txt"
                filePathDy = filePath[:-4] + "_dy.txt"
                self.sparseMeshHandler.export_node_size_mesh(filePathDx, filePathDy)
        else:
            nx = int(dpg.get_value("nx")[4:])
            ny = int(dpg.get_value("ny")[4:])
            xmin = min(self.currentX)
            ymin = min(self.currentY)
            xmax = max(self.currentX)
            ymax = max(self.currentY)
            dx = (xmax - xmin)/(nx - 1)
            dy = (ymax - ymin)/(ny - 1)
            Mesh.export_coords_mesh(filePath, self.currentX, self.currentY, nx, ny, xmin, ymin, xmax, ymax, dx, dy, self.toggleOrderingFlag)
        self.exportFilePath = None
        self.exportFileName = None
        dpg.configure_item("exportMeshFile", show=False)

    def exportContourOnMesh(self, xarray, yarray, path):
        if self.sparseMeshHandler == None:
            dx = dpg.get_value("dx")
            dy = dpg.get_value("dy")
            xmin = dpg.get_value("xi")
            ymin = dpg.get_value("yi")
            xarray, yarray = Mesh.getMesh(xarray, yarray, xmin, ymin, dx, dy)
            xmax = max(xarray)
            ymax = max(yarray)
            nx = (xmax - xmin)// dx + 1
            ny = (ymax - ymin)// dy + 1
            Mesh.export_coords_mesh(path, self.currentX, self.currentY, nx, ny, xmin, ymin, xmax, ymax, dx, dy, self.toggleOrderingFlag)
        else:
            if self.toggleZoomFlag == True:
                xarray, yarray = self.sparseMeshHandler.get_sparse_mesh(xarray, yarray)
            else:
                xarray, yarray = self.sparseMeshHandler.get_adaptative_mesh(xarray, yarray)
            self.sparseMeshHandler.export_coords_mesh(path, self.currentX, self.currentY, self.toggleOrderingFlag)