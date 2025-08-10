import cv2
import time
from playsound import playsound

FILENAME = "registered_codes.txt"
success_sound = "success.wav"
fail_sound = "fail.mp3"
cooldown = 3  # 連続で同じQRに反応しない秒数

# 登録コードを読み込む関数
def load_registered_codes():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

registered_codes = load_registered_codes()
last_scanned = {}

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

print("QRコードをかざしてください。[q]で終了")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    data, points, _ = detector.detectAndDecode(frame)
    if data:
        now = time.time()
        # 連続検出防止
        if data in last_scanned and now - last_scanned[data] < cooldown:
            pass
        else:
            last_scanned[data] = now
            print("読み取った内容:", data)

            if data in registered_codes:
                print("✅ 登録済みコード！")
                playsound(success_sound)
            else:
                print("❌ 未登録コード！")
                playsound(fail_sound)

        # QRコードの枠を表示
        if points is not None:
            points = points.astype(int)
            n = len(points)
            for i in range(n):
                pt1 = tuple(points[i][0])
                pt2 = tuple(points[(i + 1) % n][0])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

    cv2.imshow("QRCode Reader", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
