import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        break  # handle case where frame is not read properly

    # use entire frame to be safe with all sizes
    roi = frame  # change this if cropping is needed later

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.adaptiveThreshold(
        gray_blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 1
    )
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

    result_img = closing.copy()
    # use RETR_EXTERNAL to avoid nested contours
    contours, hierachy = cv2.findContours(result_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    counter = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 5000 or area > 35000:
            continue

        # prevent error from fitEllipse
        if len(cnt) >= 5:
            try:
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(roi, ellipse, (0, 255, 0), 2)
                counter += 1
            except cv2.error:
                # if fitEllipse fails, just skip this contour
                continue

    cv2.putText(roi, str(counter), (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("Show", roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
