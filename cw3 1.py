import cv2
import numpy as np
import os

# pip install opencv-python


def uploud(i):
    global files, image
    files = [f for f in os.listdir(r'C:\Users\dawid\OneDrive\Pulpit\MP1')
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')) and os.path.isfile(
            os.path.join(r'C:\Users\dawid\OneDrive\Pulpit\MP1', f))]

    try:
        image_path = os.path.join(r'C:\Users\dawid\OneDrive\Pulpit\MP1', files[i - ord('0')])
        image = cv2.imread(image_path)
        if image is None:
            print(f"Błąd: Nie udało się wczytać obrazu {image_path}")
            return
        norm_size()
    except IndexError:
        print("Błąd: Niepoprawny indeks pliku.")

def resize():
    global image
    h, w = image.shape[:2]
    h = h + int(h*(-0.1))
    w = w + int(w*(-0.1))
    image = cv2.resize(image, (w, h), interpolation= cv2.INTER_LINEAR)
    cv2.imshow('obrazek', image)


def norm_size():
    global image
    h, w = image.shape[:2]
    if h > w:
        if h > 800:
            s = (1 - (800/h)) * (-1)
            w = w + int(w*(s))
            h = h + int(h*(s))
            image = cv2.resize(image, (w, h), interpolation= cv2.INTER_LINEAR)
    else:
        if w > 800:
            s = (1 - (800/w)) * (-1)
            w = w + int(w*(s))
            h = h + int(h*(s))
            image = cv2.resize(image, (w, h), interpolation= cv2.INTER_LINEAR)
    cv2.imshow('obrazek', image)


def hsv_range():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')
    # Convert the HSV colorspace
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only blue color
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])
    mask = cv2.inRange(hsv_frame, lower, upper)
    cv2.imshow('obrazek', mask)


def hsv_bitwais():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])
    mask = cv2.inRange(hsv_frame, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('obrazek', res)


def hsv_median():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')
    ksize = cv2.getTrackbarPos('ksize', 'obrazek')
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])
    mask = cv2.inRange(hsv_frame, lower, upper)
    res = cv2.bitwise_and(image, image, mask=mask)
    res = cv2.medianBlur(res, ksize=ksize)
    cv2.imshow('obrazek', res)


def morphology():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')
    ksize = cv2.getTrackbarPos('ksize', 'obrazek')
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])
    mask = cv2.inRange(hsv_frame, lower, upper)
    kernel = np.ones((ksize, ksize), np.uint8)
    mask_without_noise = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('obrazek', mask_without_noise)


def morphology2():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')
    ksize = cv2.getTrackbarPos('ksize', 'obrazek')
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])
    mask = cv2.inRange(hsv_frame, lower, upper)
    kernel = np.ones((ksize, ksize), np.uint8)
    # mask_without_noise = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('obrazek', mask_closed)


def marker():
    low_color = cv2.getTrackbarPos('low', 'obrazek')
    high_color = cv2.getTrackbarPos('high', 'obrazek')

    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([low_color, 100, 100])
    upper = np.array([high_color, 255, 255])

    mask = cv2.inRange(hsv_frame, lower, upper)
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    M = cv2.moments(contours[0])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    image_marker = image.copy()
    cv2.drawMarker(image_marker, (int(cx), int(cy)), color=(
        0, 255, 0), markerType=cv2.MARKER_CROSS, thickness=2)
    cv2.imshow('obrazek', image_marker)


def change_h(x):
    global fun
    if fun is not None:
        fun()

def mask_ball():
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Przykładowe wartości, dostosuj je do konkretnego koloru piłki
    lower = np.array([20, 50, 50])  # Dolna granica koloru (np. żółty, zmień jeśli potrzebne)
    upper = np.array([40, 255, 255])  # Górna granica koloru

    mask = cv2.inRange(hsv_frame, lower, upper)  # Tworzenie maski
    cv2.imshow('obrazek', mask)  # Wyświetlenie maski

def denoise_image():
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Przykładowe wartości dla usuwania szumu (dostosuj zakres)
    lower = np.array([20, 50, 50])  
    upper = np.array([40, 255, 255])  

    mask = cv2.inRange(hsv_frame, lower, upper)

    kernel = np.ones((5, 5), np.uint8)  # Filtr o rozmiarze 5x5

    # Najpierw otwarcie (usuwa małe plamy szumu)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Następnie zamknięcie (wypełnia dziury w obiektach)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('obrazek', mask)

def mark_ball_center():
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Zakres kolorów dla jasnoczerwonej piłki
    lower_red1 = np.array([0, 100, 100])  # Dolny zakres (początek czerwieni)
    upper_red1 = np.array([10, 255, 255])  # Górny zakres (jasnoczerwony)

    lower_red2 = np.array([170, 100, 100])  # Drugi zakres czerwieni (na końcu spektrum)
    upper_red2 = np.array([180, 255, 255])  # Górny zakres (czerwony)

    # Tworzenie masek dla dwóch zakresów czerwieni
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

    # Łączenie obu masek
    mask = cv2.bitwise_or(mask1, mask2)

    # Usuwanie szumu za pomocą operacji morfologicznych
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Otwarcie (usuwa szum)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Zamknięcie (wypełnia dziury)

    # Znalezienie konturów
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Wybierz największy kontur, który będzie piłką
        largest_contour = max(contours, key=cv2.contourArea)

        # Oblicz momenty
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dodanie markera na środek piłki
            image_marker = image.copy()
            cv2.drawMarker(image_marker, (cx, cy), (0, 255, 0), cv2.MARKER_CROSS, thickness=2)

            cv2.imshow('obrazek', image_marker)
        else:
            print("Nie można obliczyć środka obiektu.")

image = None
fun = None
files = None

def main():
    global image, fun, files
    files = os.listdir('C:\\Users\\dawid\\OneDrive\\Pulpit\\MP1')
    uploud(ord('0'))
    nimg = image.copy()
    cv2.createTrackbar('low', 'obrazek', 0, 255, change_h)
    cv2.createTrackbar('high', 'obrazek', 0, 255, change_h)
    cv2.createTrackbar('ksize', 'obrazek', 5, 50, change_h)

    while True:
        key = cv2.waitKey()
    # -----------wybor obrazka----------------
        if key >= ord('0') and key <= ord('9'):
            uploud(key)
            nimg = image.copy()
    # ----------------zmiana rozmiaru---------------
        elif key == ord('-'):
            resize()
            nimg = image.copy()
            cv2.imshow('obrazek', image)
        elif key == ord('='):
            cv2.imshow('obrazek', image)
            nimg = image.copy()
    # ----------------kolory------------------------
        elif key == ord('q'):
            cv2.imshow('obrazek', cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
        elif key == ord('w'):
            nimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            cv2.imshow('obrazek', nimg)
        elif key == ord('e'):
            hsv_range()
            fun = hsv_range
        elif key == ord('r'):
            hsv_bitwais()
            fun = hsv_bitwais
        elif key == ord('t'):
            hsv_median()
            fun = hsv_median
        elif key == ord('z'):
            # h = barwa
            cv2.imshow('obrazek', nimg[:, :, 0])
        elif key == ord('x'):
            # s = nasycene
            cv2.imshow('obrazek', nimg[:, :, 1])
        elif key == ord('c'):
            # v = wartość
            cv2.imshow('obrazek', nimg[:, :, 2])
    # ----------------filtry
        elif key == ord('a'):
            cv2.imshow('obrazek', cv2.Canny(image, 55.0, 30.0))
        elif key == ord('s'):
            cv2.imshow('obrazek', cv2.blur(image, (7, 7)))
        elif key == ord('d'):
            b = cv2.blur(image, (7, 7))
            cv2.imshow('obrazek', cv2.Canny(b, 55.0, 30.0))
        elif key == ord('f'):
            morphology()
            fun = morphology
        elif key == ord('g'):
            morphology2()
            fun = morphology2
        elif key == ord('h'):
            marker()
            fun = marker
        elif key == 27:
            cv2.destroyAllWindows()
            break
        elif key == ord('b'):
            mask_ball()
            fun = mask_ball
        elif key == ord('n'):
            denoise_image()
            fun = denoise_image
        elif key == ord('m'):
            mark_ball_center()
            fun = mark_ball_center

if __name__ == '__main__':
    main()