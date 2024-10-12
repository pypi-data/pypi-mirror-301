import cv2 as cv





image = cv.imread('image.png')
cv.imshow('Image', image)


##################################################
def mouse_callback(event, x, y, flags, param):
	return x,y
cv.setMouseCallback('Image', mouse_callback)




cv.putText(image, text, position, font, font_scale, color, thickness) ##color: RGB
cv.putText('example', text, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)








cv.waitKey(0)
cv.destroyAllWindows()








