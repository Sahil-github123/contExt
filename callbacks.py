# -*- coding: utf-8 -*-
import dearpygui.dearpygui as dpg
import numpy as np
import cv2
import enum

class Tabs(enum.Enum):
    __order__ = 'Processing Filtering Thresholding ContourExtraction'
    Processing = 0
    Filtering = 1
    Thresholding = 2
    ContourExtraction = 3

class Blocks(enum.Enum):
    __order__ = 'importImage crop histogramEqualization brightnessAndContrast averageBlur gaussianBlur medianBlur grayscale globalThresholding adaptativeMeanThresholding adaptativeGaussianThresholding otsuBinarization findContour mooreNeighborhood exportSettings'
    importImage = 0
    crop = 1
    histogramEqualization = 2
    brightnessAndContrast = 3
    averageBlur = 4
    gaussianBlur = 5
    medianBlur = 6
    grayscale = 7
    globalThresholding = 8
    adaptativeMeanThresholding = 9
    adaptativeGaussianThresholding = 10
    otsuBinarization = 11
    findContour = 12
    mooreNeighborhood = 13
    exportSettings = 14

class Callbacks:
    def __init__(self) -> None:

        self.filePath = None
        self.fileName = None

        self.blocks = [
            {
                'method': self.importImage,
                'name': self.importImage.__name__,
                'status': True,
                'output': None,
                'tab': 'Processing'
            },
            {
                'method': self.crop,
                'name': self.crop.__name__,
                'status': False,
                'output': None,
                'tab': 'Processing'
            },
            {
                'method': self.histogramEqualization,
                'name': self.histogramEqualization.__name__,
                'status': False,
                'output': None,
                'tab': 'Filtering'
            },
            {
                'method': self.brightnessAndContrast,
                'name': self.brightnessAndContrast.__name__,
                'status': True,
                'output': None,
                'tab': 'Filtering'
            },
            {
                'method': self.averageBlur,
                'name': self.averageBlur.__name__,
                'status': False,
                'output': None,
                'tab': 'Filtering'
            },
            {
                'method': self.gaussianBlur,
                'name': self.gaussianBlur.__name__,
                'status': False,
                'output': None,
                'tab': 'Filtering'
            },
            {
                'method': self.medianBlur,
                'name': self.medianBlur.__name__,
                'status': False,
                'output': None,
                'tab': 'Filtering'
            },
            {
                'method': self.grayscale,
                'name': self.grayscale.__name__,
                'status': False,
                'output': None,
                'tab': 'Thresholding'
            },
            {
                'method': self.globalThresholding,
                'name': self.globalThresholding.__name__,
                'status': False,
                'output': None,
                'tab': 'Thresholding'
            },
            {
                'method': self.adaptativeMeanThresholding,
                'name': self.adaptativeMeanThresholding.__name__,
                'status': False,
                'output': None,
                'tab': 'Thresholding'
            },
            {
                'method': self.adaptativeGaussianThresholding,
                'name': self.adaptativeGaussianThresholding.__name__,
                'status': False,
                'output': None,
                'tab': 'Thresholding'
            },
            {
                'method': self.otsuBinarization,
                'name': self.otsuBinarization.__name__,
                'status': False,
                'output': None,
                'tab': 'Thresholding'
            },
            {
                'method': self.findContour,
                'name': self.findContour.__name__,
                'status': False,
                'output': None,
                'tab': 'ContourExtraction'
            },
            {
                'method': self.mooreNeighborhood,
                'name': self.mooreNeighborhood.__name__,
                'status': False,
                'output': None,
                'tab': 'ContourExtraction'
            },
            {
                'method': self.exportSettings,
                'name': self.exportSettings.__name__,
                'status': False,
                'output': None,
                'tab': 'ContourExtraction'
            },
        ]

        pass


    def executeQuery(self, methodName):
        executeFlag = 0
        for entry in self.blocks:
            if executeFlag == 0 and entry['name'] == methodName:
                executeFlag = 1
            if executeFlag == 1 and entry['status'] is True:
                entry['method']()
        pass

    def executeQueryFromNext(self, methodName):
        executeFlag = 0
        for entry in self.blocks:
            if executeFlag == 0 and entry['name'] == methodName:
                executeFlag = 1
                continue
            if executeFlag == 1 and entry['status'] is True:
                entry['method']()
        pass

    def toggleAndExecuteQuery(self, methodName, sender = None, app_data = None):
        self.toggleEffect(methodName, sender, app_data)
        if dpg.get_value(sender) is True:
            self.executeQuery(methodName)
        else:
            self.retrieveFromLastActive(methodName, sender, app_data)
            self.executeQueryFromNext(methodName)
        pass

    def getIdByMethod(self, methodName):
        id = 0
        for entry in self.blocks:
            if entry['name'] == methodName:
                return id
            id += 1

    def retrieveFromLastActive(self, methodName, sender = None, app_data = None):
        self.blocks[self.getIdByMethod(methodName)]['output'] = self.blocks[self.getLastActiveBeforeMethod(methodName)]['output']
        self.updateTexture(self.blocks[self.getIdByMethod(methodName)]['tab'], self.blocks[self.getIdByMethod(methodName)]['output'])

    def getLastActiveBeforeMethod(self, methodName):
        lastActiveIndex = 0
        lastActive = 0
        for entry in self.blocks:
            if entry['name'] == methodName:
                break
            if entry['status'] is True:
                lastActiveIndex = lastActive 
            lastActive += 1
        return lastActiveIndex

    def openImage(self, filePath):
        stream = open(filePath, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_COLOR)
        return bgrImage

    def openFile(self, sender = None, app_data = None):
        self.filePath = app_data['file_path_name']
        self.fileName = app_data['file_name']
        self.executeQuery('importImage')
        pass

    # TODO: Create Texture
    def createTexture(self, textureTag, textureImage):
        self.deleteTexture(textureTag)
        height = textureImage.shape[0]
        width = textureImage.shape[1]
        textureData = self.textureToData(textureImage)
        dpg.add_dynamic_texture(width=width, height=height, default_value=textureData, tag=textureTag, parent='textureRegistry')
        dpg.add_image(textureTag, parent=textureTag + 'Parent', tag=textureTag + 'Image')
        pass

    # TODO: Delete Texture
    def deleteTexture(self, textureTag):
        try:
            dpg.delete_item(textureTag)
            dpg.delete_item(textureTag + 'Image')
        except:
            pass
        pass

    # TODO: Update Texture
    def updateTexture(self, textureTag, textureImage):
        textureData = self.textureToData(textureImage)
        dpg.set_value(textureTag, textureData)
        pass

    def createAllTextures(self, textureImage):
        for tab in Tabs:
            self.createTexture(tab.name, textureImage)

    # TODO: Delete all textures
    def deleteAllTextures(self):
        for tab in Tabs:
            self.deleteTexture(tab.name)
        pass

    def updateAllTextures(self, textureImage):
        for tab in Tabs:
            self.updateTexture(tab.name, textureImage)
        pass

    # TODO: Convert texture to data
    def textureToData(self, texture):
        auxImg = cv2.cvtColor(texture, cv2.COLOR_RGB2BGRA)
        auxImg = np.asfarray(auxImg, dtype='f')
        auxImg = auxImg.ravel()
        auxImg = np.true_divide(auxImg, 255.0)
        return auxImg

    def toggleEffect(self, methodName, sender = None, app_data = None):
        for entry in self.blocks:
            if entry['name'] == methodName:
                entry['status'] = dpg.get_value(sender)
        pass

    def importImage(self, sender = None, app_data = None):
        # Cria imagem na aba
        dpg.hide_item('import_image')
        self.blocks[Blocks.importImage.value]['output'] = self.openImage(self.filePath)

        self.createAllTextures(self.blocks[Blocks.importImage.value]['output'])

        # Popula os dados na lateral
        dpg.set_value('file_name_text', 'File Name: ' + self.fileName)
        dpg.set_value('file_path_text', 'File Path: ' + self.filePath)

        shape = self.blocks[Blocks.importImage.value]['output'].shape

        dpg.set_value('originalWidth', 'Width: ' + str(shape[1]) + 'px')
        dpg.set_value('originalHeight', 'Height: ' + str(shape[0]) + 'px')
        dpg.set_value('currentWidth', 'Width: ' + str(shape[1]) + 'px')
        dpg.set_value('currentHeight', 'Height: ' + str(shape[0]) + 'px')
        pass

    def resetCrop(self, sender = None, app_data = None):
        self.blocks[Blocks.crop.value]['output'] = self.blocks[Blocks.importImage.value]['output']

        shape = self.blocks[Blocks.crop.value]['output'].shape

        dpg.set_value('currentWidth', 'Width: ' + str(shape[1]) + 'px')
        dpg.set_value('currentHeight', 'Height: ' + str(shape[0]) + 'px')

        self.createAllTextures(self.blocks[Blocks.importImage.value]['output'])

        # TODO: Fazer um método para resetar todas as checkbox e valores depois.

        pass

    def crop(self, sender=None, app_data=None):
        startX = dpg.get_value('startX')
        endX = dpg.get_value('endX')
        startY = dpg.get_value('startY')
        endY = dpg.get_value('endY')
        self.blocks[Blocks.crop.value]['output'] = self.blocks[Blocks.importImage.value]['output'][startX:endX, startY:endY]

        shape = self.blocks[Blocks.crop.value]['output'].shape

        dpg.set_value('currentWidth', 'Width: ' + str(shape[1]) + 'px')
        dpg.set_value('currentHeight', 'Height: ' + str(shape[0]) + 'px')

        self.createAllTextures(self.blocks[Blocks.crop.value]['output'])
        pass

    def histogramEqualization(self, sender=None, app_data=None):

        img_yuv = cv2.cvtColor(self.blocks[self.getLastActiveBeforeMethod('histogramEqualization')]['output'], cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        dst = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        self.blocks[Blocks.histogramEqualization.value]['output'] = dst
        self.updateTexture(self.blocks[Blocks.histogramEqualization.value]['tab'], dst)
        pass

    def brightnessAndContrast(self, sender=None, app_data=None):

        image = self.blocks[self.getLastActiveBeforeMethod('brightnessAndContrast')]['output']
        alpha = dpg.get_value('contrastSlider')
        beta = dpg.get_value('brightnessSlider')
        outputImage = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

        self.blocks[Blocks.brightnessAndContrast.value]['output'] = outputImage
        self.updateTexture(self.blocks[Blocks.brightnessAndContrast.value]['tab'], outputImage)
        pass

    def averageBlur(self, sender=None, app_data=None):
        image = self.blocks[self.getLastActiveBeforeMethod('averageBlur')]['output']

        kernelSize = (2 * dpg.get_value('averageBlurSlider')) - 1
        kernel = np.ones((kernelSize,kernelSize),np.float32)/(kernelSize*kernelSize)
        dst = cv2.filter2D(image,-1,kernel)

        self.blocks[Blocks.averageBlur.value]['output'] = dst
        self.updateTexture(self.blocks[Blocks.averageBlur.value]['tab'], dst)
        pass

    def gaussianBlur(self, sender=None, app_data=None):
        image = self.blocks[self.getLastActiveBeforeMethod('gaussianBlur')]['output']

        kernelSize = (2 * dpg.get_value('gaussianBlurSlider')) - 1
        dst = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

        self.blocks[Blocks.averageBlur.value]['output'] = dst
        self.updateTexture(self.blocks[Blocks.averageBlur.value]['tab'], dst)
        pass

    def medianBlur(self, sender=None, app_data=None):
        image = self.blocks[self.getLastActiveBeforeMethod('medianBlur')]['output']
        kernel = (2 * dpg.get_value('medianBlurSlider')) - 1

        median = cv2.medianBlur(image, kernel)

        self.blocks[Blocks.medianBlur.value]['output'] = median
        self.updateTexture(self.blocks[Blocks.medianBlur.value]['tab'], median)
        pass

    def grayscale(self, sender=None, app_data=None):

        pass

    def globalThresholding(self, sender=None, app_data=None):

        pass

    def adaptativeMeanThresholding(self, sender=None, app_data=None):

        pass

    def adaptativeGaussianThresholding(self, sender=None, app_data=None):

        pass

    def otsuBinarization(self, sender=None, app_data=None):

        pass

    def findContour(self, sender=None, app_data=None):

        pass

    def mooreNeighborhood(self, sender=None, app_data=None):

        pass

    def exportSettings(self, sender=None, app_data=None):

        pass

    def importContour(self, sender=None, app_data=None):

        pass

    def openTxtFile(self, sender = None, app_data = None):
        self.filePath = app_data['file_path_name']
        self.fileName = app_data['file_name']
        self.executeQuery('importContour')
        pass

    def GenerateMesh(self, sender=None, app_data=None):

        pass