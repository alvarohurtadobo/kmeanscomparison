import cv2

class ObjectCenters():
    """
    This class make use of backround substraction to detect objects in a video
    """
    def __init__(self):
        # We initialize the object with an image
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

    def getForeground(self,imagenActual):
        imagenActualEnGris = cv2.cvtColor(imagenActual, cv2.COLOR_BGR2GRAY)
        imagenActualEnGris = cv2.GaussianBlur(imagenActualEnGris,(5,5),0)
        imagenActualEnGris = cv2.threshold(imagenActualEnGris, 70, 255, cv2.THRESH_BINARY)[1]
        fgmask = self.fgbg.apply(imagenActualEnGris)
        _, contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangulos = [cv2.boundingRect(contour) for contour in contours]		
        rectangulosFiltrados = []
        for (index, contour) in enumerate(contours):
            #contour = cv2.convexHull(contour)			
            cv2.drawContours(imagenActual, contour, -1, (255-25*index,25*index,0), 3)
        for rec in rectangulos:
            (x,y,w,h) = rec
            if (h>8)&(w>6):
                rectangulosFiltrados.append((x+w//2,y+h//2))
        return rectangulosFiltrados