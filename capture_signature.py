import time
import csv
from pynput import mouse, keyboard

LOG_FILE = '/Volumes/KIOXIA/clippeaks/biometric_signature.csv'

with open(LOG_FILE, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Event_Type', 'Action', 'X_or_Key', 'Y_or_Dwell_Flight'])

last_key_time = time.time()
key_press_times = {}

def on_move(x, y):
    with open(LOG_FILE, mode='a', newline='') as f:
        csv.writer(f).writerow([time.time(), 'Mouse', 'Move', x, y])

def on_click(x, y, button, pressed):
    action = 'Pressed' if pressed else 'Released'
    with open(LOG_FILE, mode='a', newline='') as f:
        csv.writer(f).writerow([time.time(), 'Mouse', action, x, y])

def on_press(key):
    global last_key_time
    current_time = time.time()
    flight_time = current_time - last_key_time
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    if k not in key_press_times:
        key_press_times[k] = current_time
    with open(LOG_FILE, mode='a', newline='') as f:
        csv.writer(f).writerow([current_time, 'Keyboard', 'Press (Flight: {:.4f}s)'.format(flight_time), k, ''])

def on_release(key):
    global last_key_time
    current_time = time.time()
    last_key_time = current_time
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    dwell_time = 0.0
    if k in key_press_times:
        dwell_time = current_time - key_press_times.pop(k)
    with open(LOG_FILE, mode='a', newline='') as f:
        csv.writer(f).writerow([current_time, 'Keyboard', 'Release (Dwell: {:.4f}s)'.format(dwell_time), k, ''])
    if key == keyboard.Key.esc:
        return False

print("🚨 [生体ラーニング・モード起動] 🚨")
print("マウスとキーボードの微細な挙動の記録を開始しました。")
print("普段通りブラウジングを行い、終了時は『ESCキー』を押してください。")

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()
keyboard_listener.join()
mouse_listener.stop()

print(f"✅ 記録完了。生体データは {LOG_FILE} に保存されました。")
