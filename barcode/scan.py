import cv2
from pyzbar.pyzbar import decode

# Open camera
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    barcodes = decode(frame)

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"Scanned Barcode: {barcode_data}")

    cv2.imshow("Barcode Scanner", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
