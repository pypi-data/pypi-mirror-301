import cv2 as cv

# ตัวแปรเพื่อเก็บตำแหน่งที่คลิก
clicks = []

def mouse_callback(event, x, y, flags, param):
    global clicks
    if event == cv.EVENT_LBUTTONDOWN:
	color = image[y, x]
        clicks.append((x, y))
        print(f"Clicked at: ({x}, {y})")
        cv.circle(image, (x, y), 5, (0, 0, 255), -1)
        cv.imshow('Image', image)

image = cv.imread('image.png')

=cv.imshow('Image', image)

=cv.setMouseCallback('Image', mouse_callback)

# รอให้ผู้ใช้ปิดหน้าต่าง
cv.waitKey(0)
cv.destroyAllWindows()
