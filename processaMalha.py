class ProcessaMalha:


    """
    Retorna a coordenada do nó da malha onde o ponto informado está 
    """

    def getNode(xpoint, ypoint, xmin, ymin, dx, dy):
       point = []
       point.append((xpoint - xmin)//dx * dx + xmin)
       point.append((ypoint - ymin)//dy * dy + ymin)
       return point


    """
    Percore x e y, obtendo os nós da malha para cada ponto com a função getNode, 
    e removendo nós irrelevantes
    """

    def getMesh(x, y, xmin, ymin, dx, dy):
        xResult = []
        yResult = []
        xmax = max(x)
        ymax = max(y)
        prevpoint = ProcessaMalha.getNode(x[0], y[0], xmin, ymin, dx, dy) 
        xResult.append(prevpoint[0])
        yResult.append(prevpoint[1])
        flagx = 0
        flagy = 0
        dirx = prevpoint[0] > x[-2]
        diry = prevpoint[1] > y[-2]
        tam = len(x)
        for i in range(1,tam):
            point = ProcessaMalha.getNode(x[i], y[i], xmin, ymin, dx, dy)
            if point[0] != prevpoint[0] or point[1] != prevpoint[1]:
                if flagx and point[1] == prevpoint[1] and ((point[0] > prevpoint[0]) != diry):
                    xResult[-1] = point[0]
                    yResult[-1] = point[1]
                elif flagy and point[0] == prevpoint[0] and ((point[1] > prevpoint[1]) == dirx):
                    xResult[-1] = point[0]
                    yResult[-1] = point[1]
                elif flagy and point[1] == prevpoint[1] and ((point[0] > prevpoint[0]) != dirx):
                    xResult[-1] = point[0]
                    yResult[-1] = point[1]
                elif flagx and point[0] == prevpoint[0] and ((point[1] > prevpoint[1]) != diry):
                    xResult[-1] = point[0]
                    yResult[-1] = point[1]
                else:
                    xResult.append(point[0])
                    yResult.append(point[1])
                flagx = 0
                flagy = 0
                if point[0] == xResult[-2]:
                    flagx = 1
                elif point[1] == yResult[-2]:
                    flagy = 1
                dirx = point[0] > xResult[-2]
                diry = point[1] > yResult[-2]
                prevpoint = point
        point = [xResult[0], yResult[0]]
        if point[0] != prevpoint[0] or point[1] != prevpoint[1]:
            xResult.append(point[0])
            yResult.append(point[1])
        
        aux = max(xResult)
        if aux != xmax:
            xmax = aux
        nx = int((xmax - xmin)/dx) + 1
        aux = max(yResult)
        if aux != ymax:
            ymax = aux
        ny = int((ymax - ymin)/dy) + 1
        xResult = [nx, xmin, xmax, dx] + xResult
        yResult = [ny, ymin, ymax, dy] + yResult
        print(xResult[:8])
        return xResult, yResult
        
    

    """
    Essa função é utilizada para converter o array das coordenadas em uma string para ser impressa no arquivo de texto. Retorna a string.
    """

    def converte_pointArray_to_string(array):
        content = ''
        i = 0
        while i < len(array):
            element = array[i]
            content = content + str(element[0]) + " " + str(element[1]) + "\n"
            i += 1
        return content


    """
    Função responsável por exportar as coordenadas dos nós da malha em um arquivo path
    """

    def exporta_coords_malha(path, mesh, nx, ny, xmin, ymin, xmax, ymax, dx, dy):
        content = ''
        content = content + str(nx) + " " + str(ny) + "\n"
        content = content + str(xmin) + " " + str(ymin) + "\n"
        content = content + str(xmax) + " " + str(ymax) + "\n"
        content = content + str(dx) + " " + str(dy) + "\n"
        try:
            with open(path, "w") as dataFile:
                content += ProcessaMalha.converte_pointArray_to_string(
                    mesh)
                dataFile.write(content)
        except:
            print('Path does not exist for mesh export')
            return


    """
    Utiliza um método descrito por Gauss para o cálculo da área de um poligono irregular convexo
    Utiliza como base: https://www.thecivilengineer.org/education/calculation-examples/item/1319-calculation-example-three-point-resection
    Para esse algoritmo funcionar ele precisa de uma lista ordenada de pontos. No caso, a própria lista de pontos que foi adquirida a partir da extração de contorno
    """

    def calcula_area(mesh):
        area = 0
        i = 0
        j = 0
        for index in range(0, (len(mesh)) - 1):
            auxI = mesh[index]
            auxJ = mesh[index + 1]
            area += auxI[1] * auxJ[0] - auxI[0] * auxJ[1]
        auxI = mesh[len(mesh) - 1]
        auxJ = mesh[0]
        area += auxI[1] * auxJ[0] - auxI[0] * auxJ[1]
        area = area / 2
        return area
    

    