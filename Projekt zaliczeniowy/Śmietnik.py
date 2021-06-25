import cv2, pytesseract as pt, matplotlib.pyplot as plt
# vidcap = cv2.VideoCapture('Raport.mp4')
# fps = vidcap.get(cv2.CAP_PROP_FPS)
# print(fps)
# img_object = Image.open(r"TestIm.png")
img_object = cv2.imread(r".\SzczytDir\frame0.jpg",cv2.IMREAD_GRAYSCALE)
orig = img_object.copy()
config = ("-l pol --oem 1 --psm 7")
img_text = pt.image_to_string(img_object,config=config)
print(img_text) # TODO Wyciąć nie Ascii charactersy

def sciągnijRamkę(filename,newW,newH):
    image = cv2.imread(filename=filename)
    (origH, origW) = image.shape[:2]
    rW = origW / float(newW)
    rH = origH / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    print(origH, origW)
    print(H, W)
# sciągnijRamkę("TestIm.png", 500,700)
roi = orig[850:980,350:1800]
roi2 = orig[980:1100,330:1700]
img_text2 = pt.image_to_string(roi,config=config)
img_text3 = pt.image_to_string(roi2,config=config)

plt.imshow(img_object)
#plt.imshow(roi)
plt.show()
plt.imshow(roi)
plt.show()
plt.imshow(roi2)
plt.show()
print(img_text2)
print(img_text3)
# success,image = vidcap.read()
# count = 0
# while success:
#   cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
#   success,image = vidcap.read()
#   print('Read a new frame: ', success)
#   count += 1