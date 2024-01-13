import cv2
import numpy as np

# Hough Dönüşümü için parametreler
min_radius = 10
max_radius = 50
accumulator_threshold = 15

# Watershed Algoritması için parametreler
marker_threshold = 150
max_value = 255

def find_coins(image_path):
    # Görüntüyü yükle
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Hough Dönüşümü ile daireleri bul
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=min_radius, maxRadius=max_radius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        num_coins = len(circles[0])

        # Bozuk paraların konumlarını ve değerlerini saklamak için listeler
        coin_positions = []
        total_tl = 0
        total_euro = 0

        # Her bir daireyi işle
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]

            # Bozuk paraların değerini ve konumunu belirle
            if radius < 20:
                value = 1  # TL
                total_tl += 1
            else:
                value = 2  # Euro
                total_euro += 1

            coin_positions.append((center, value))

            # Daireyi çiz
            cv2.circle(img, center, radius, (0, 255, 0), 2)

        # Toplam TL ve Euro miktarını köşeye yazdır
        text_position = (10, 30)
        cv2.putText(img, f"TL: {total_tl}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f"Euro: {total_euro}", (text_position[0], text_position[1] + 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        # Görüntüyü kaydet
        cv2.imwrite(f"result_{image_path}", img)

        return num_coins, coin_positions, total_tl, total_euro
    else:
        return 0, [], 0, 0

# Görüntülerin yolları
image_paths = ["C:/Users/Çağlar/Desktop/KS2/img1.jpg","C:/Users/Çağlar/Desktop/KS2/img2.jpg", "C:/Users/Çağlar/Desktop/KS2/img3.jpg"]

for image_path in image_paths:
    num_coins, coin_positions, total_tl, total_euro = find_coins(image_path)

    # Sonuçları ekrana yazdır
    print(f"{image_path}:")
    print("Yöntem: Hough Dönüşümü ve Watershed Algoritması")
    print("Bulunan Para Sayısı:", num_coins)
    print("Toplam TL:", total_tl)
    print("Toplam Euro:", total_euro)
    print("")












