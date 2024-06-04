import cv2

# Set camera
cap = cv2.VideoCapture(0)

# Pre-settings
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
area_threshold = 5000

def human_detector():
    ret, frame = cap.read()
    if not ret:
        print('read camera error')
        return False
    
    human_detected = False

    rects, _ = hog.detectMultiScale(frame, winStride=(8,8) ,scale=1.1, useMeanshiftGrouping=False)

    for x,y,w,h in rects:   # If detected
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 2)
        human_detected = True

    cv2.imshow('Frame', frame)
    cv2.waitKey(33)
    return human_detected


def fall_detector():
    ret, frame = cap.read()
    if not ret:
        print('read camera error')
        return False

    fall_detected = False

    # Background subtractor
    fgmask = fgbg.apply(frame)
    
    # Reduce noise
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < area_threshold:
            continue

        # Turn the contour into a rectangle
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Check if fall
        if aspect_ratio > 1.5:
            cv2.putText(frame, 'Fall Detected!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            fall_detected = True

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.waitKey(33)
    return fall_detected
