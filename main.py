import cv2
import numpy as np
import mss
import ctypes
import keyboard
import time
import os
import timeit

#Fistborn – First Ever Semi-Automatic Roadwork Macro
#Copyright (C) 2026 Valentine

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.


ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "icon.png")

# Detection settings
MATCH_THRESHOLD = 0.65       # threshold
SCALES = np.linspace(0.9, 1.1, 3) # multi scale
ROI_RATIO = 0.4              # KEEP SMALL: 0.4 = 40% of screen. Smaller ROI = Faster FPS.

# Mouse/movement settings
SMOOTH = 6.0                 # higher = smoother but slower
DEADZONE = 5                 # pixels from center to ignore
FPS_LIMIT = 60               # target fps
SEARCH_SPEED = 100.0           # speed for turning right
SEARCH_RANGE = 1000           # maximum pixels to turn right

# Debug window settings
SHOW_DEBUG = True #false if you don't need the debug window
DEBUG_WINDOW_NAME = "Debug View (Press Q to quit)"

# DO NOT TOUCH (Required for mouse movement)
user32 = ctypes.windll.user32
def move_mouse(dx):
    user32.mouse_event(0x0001, int(dx), 0, 0, 0)

def main():
    if not os.path.exists(ICON_PATH):
        print(f"Error: Icon not found at {ICON_PATH}")
        return

    original_icon = cv2.imread(ICON_PATH, cv2.IMREAD_GRAYSCALE)
    if original_icon is None:
        print("Error: Failed to load icon image.")
        return
    

    templates = []
    for scale in SCALES:
        width = int(original_icon.shape[1] * scale)
        height = int(original_icon.shape[0] * scale)
        resized = cv2.resize(original_icon, (width, height))
        templates.append((resized, resized.shape[1], resized.shape[0])) 


    sct = mss.mss()
    primary_monitor = sct.monitors[1] 
    screen_w = primary_monitor['width']
    screen_h = primary_monitor['height']
    center_x = screen_w // 2
    center_y = screen_h // 2

    roi_w = int(screen_w * ROI_RATIO)
    roi_h = int(screen_h * ROI_RATIO)
    roi_monitor = {
        "top": int(primary_monitor["top"] + (screen_h - roi_h) // 2),
        "left": int(primary_monitor["left"] + (screen_w - roi_w) // 2),
        "width": roi_w,
        "height": roi_h,
        "mon": 1
    }

    print(f"=== ACTIVATED ===")
    print(f"Screen: {screen_w}x{screen_h} | ROI: {roi_w}x{roi_h}")
    print("Hold F1 to TRACK | F2 to PAUSE | Q to QUIT script")

    active = False
    
    search_direction = 1  
    search_position = 0    
    frames_without_target = 0  
    
    frame_time = 1.0 / FPS_LIMIT

    while True:
        loop_start = timeit.default_timer()

        if keyboard.is_pressed("F1"):
            active = True
        elif keyboard.is_pressed("F2"):
            active = False
        
        if keyboard.is_pressed("q"):
            print("Exiting...")
            break

        if not active:
            if SHOW_DEBUG and cv2.getWindowProperty(DEBUG_WINDOW_NAME, cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow(DEBUG_WINDOW_NAME)
            time.sleep(0.1)
            continue

        sct_img = np.array(sct.grab(roi_monitor))
        gray_frame = cv2.cvtColor(sct_img, cv2.COLOR_BGRA2GRAY)

        best_val = -1
        best_loc = None
        best_w, best_h = 0, 0

        for template, t_w, t_h in templates:
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_w, best_h = t_w, t_h

        target_x = None
        
        if best_val >= MATCH_THRESHOLD and best_loc is not None:
            top_left = best_loc
            
            obj_center_x = top_left[0] + (best_w // 2)
            
            roi_center_x = roi_w // 2

            diff_x = obj_center_x - roi_center_x

            if abs(diff_x) > DEADZONE:
                move_x = diff_x / SMOOTH
                move_mouse(move_x)
                target_x = obj_center_x
            

            frames_without_target = 0
            search_position = 0
            search_direction = 1
        else:
            frames_without_target += 1
            
            if frames_without_target > 2.5:
                search_movement = SEARCH_SPEED *2
                
                search_position += search_movement
                
                if search_position >= SEARCH_RANGE:
                    search_position = SEARCH_RANGE
                    search_movement = 0  
                
                move_mouse(search_movement)
                target_x = roi_w // 2 + search_position  

        if SHOW_DEBUG:
            debug_frame = sct_img[:, :, :3].copy()
            

            cv2.line(debug_frame, (roi_w//2, 0), (roi_w//2, roi_h), (0, 255, 0), 1)
            cv2.line(debug_frame, (0, roi_h//2), (roi_w, roi_h//2), (0, 255, 0), 1)

            if target_x is not None and best_loc is not None and best_w is not None and best_h is not None:

                cv2.rectangle(debug_frame, 
                              (best_loc[0], best_loc[1]), 
                              (best_loc[0] + best_w, best_loc[1] + best_h), 
                              (0, 0, 255), 2)
                cv2.line(debug_frame, (roi_w//2, roi_h//2), (int(target_x), int(best_loc[1] + best_h//2)), (0, 255, 255), 2)
                
                cv2.putText(debug_frame, f"Conf: {best_val:.2f}", (best_loc[0], best_loc[1] - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            elif target_x is not None and frames_without_target > 5:
                cv2.putText(debug_frame, "SEARCHING...", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                cv2.circle(debug_frame, (int(target_x), roi_h//2), 8, (255, 255, 0), 2)

            cv2.imshow(DEBUG_WINDOW_NAME, debug_frame)
            cv2.waitKey(1) 

        elapsed = timeit.default_timer() - loop_start
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()