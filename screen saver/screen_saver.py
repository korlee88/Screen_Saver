import pyautogui
import time
import sys
import threading
from PIL import Image, ImageDraw
import pystray

INTERVAL = 9 * 60 + 50  # 9분 50초

def create_icon():
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(0, 200, 100))
    draw.text((20, 20), "S", fill=(255, 255, 255))
    return img

def keep_awake(stop_event):
    while not stop_event.is_set():
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        stop_event.wait(INTERVAL)

def quit_app(icon, stop_event):
    stop_event.set()
    icon.stop()

def main():
    pyautogui.FAILSAFE = True

    stop_event = threading.Event()

    thread = threading.Thread(target=keep_awake, args=(stop_event,), daemon=True)
    thread.start()

    icon = pystray.Icon(
        "screen_saver",
        create_icon(),
        f"화면보호기 방지 중 ({INTERVAL}초 간격)",
        menu=pystray.Menu(
            pystray.MenuItem("화면보호기 방지 실행 중", lambda: None, enabled=False),
            pystray.MenuItem("종료", lambda icon, item: quit_app(icon, stop_event)),
        ),
    )
    icon.run()

if __name__ == "__main__":
    main()
