import onnxruntime as ort
import numpy as np
import gc
import cv2
import time
import win32api
import win32con
import pandas as pd
from utils.general import (cv2, non_max_suppression, xyxy2xywh)
import torch
from config import selectedModel, onnxChoice, jitterStrength, showStatus, activationKey, toggleAimbot, showTracers, showBoxes, overlayColor, showFOVCircle, screenShotHeight, screenShotWidth, aaMovementAmp, aaTriggerBotKey, aaMovementAmpHipfire, realtimeOverlay, jitterValueX, jitterValueY, aaPauseKey, useMask, maskHeight, maskWidth, aaQuitKey, confidence, cpsDisplay, visuals, centerOfScreen, fovCircleSize, BodyPart, RandomBodyPart
import gameSelection
import random
import pyMeow as pm

body_part_offsets = {
    "Head": 0.37,
    "Neck": 0.31,
    "Body": 0.2,
    "Pelvis": -0.2
}
def is_key_pressed(key):
    return win32api.GetAsyncKeyState(ord(key)) & 0x8000 != 0

key_code = getattr(win32con, activationKey)

def generate_jitter(scale=jitterStrength):
    jitter_x = random.uniform(-jitterValueX, jitterValueX) * scale
    jitter_y = random.uniform(-jitterValueY, jitterValueY) * scale
    return jitter_x, jitter_y

def is_right_mouse_button_pressed():
    return win32api.GetKeyState(win32con.VK_RBUTTON) < 0

def calculate_offsets(screenShotWidth, screenShotHeight):
    if screenShotWidth == 320 and screenShotHeight == 320:
        return 799.2, 379.1
    elif screenShotWidth == 480 and screenShotHeight == 480:
        return 718.3, 299.5
    else:
        # Linear interpolation
        x1, y1 = 320, 320  # Known dimensions
        x2, y2 = 480, 480  # Known dimensions
        xOffset1, yOffset1 = 799.2, 379.1  # Corresponding offsets
        xOffset2, yOffset2 = 718.3, 299.5  # Corresponding offsets

        xOffset = xOffset1 + (screenShotWidth - x1) * (xOffset2 - xOffset1) / (x2 - x1)
        yOffset = yOffset1 + (screenShotHeight - y1) * (yOffset2 - yOffset1) / (y2 - y1)

        return xOffset, yOffset
    
def hex_to_rgba(hex_code):
    # Remove '#' if it exists in the hex code
    if hex_code.startswith('#'):
        hex_code = hex_code[1:]

    # Parse the hexadecimal code to RGB components
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    # Set alpha value to 255 (fully opaque)
    a = 255

    # Create and return the dictionary
    return {'r': r, 'g': g, 'b': b, 'a': a}
green = hex_to_rgba("#00FF00")
red = hex_to_rgba("#FF0000")

def main():
    from config import triggerBot, triggerbot_actdistance

    aimbot = False # Starting aimbot off by default

    if triggerBot == False:
        disableTriggerBot = True
    else:
        disableTriggerBot = False


    running = True
    last_mid_coord = None

    # External func for running the game selection menu 
    game_selection_result = gameSelection.gameSelection()

    camera, cWidth, cHeight = game_selection_result

    # Used for forcing garbage collection
    count = 0
    sTime = time.time()

    # Choosing the correct ONNX Provider based on config.py
    onnxProvider = ""
    if onnxChoice == 1:
        onnxProvider = "CPUExecutionProvider"
    elif onnxChoice == 2:
        onnxProvider = "DmlExecutionProvider"
    elif onnxChoice == 3:
        import cupy as cp
        onnxProvider = "CUDAExecutionProvider"

    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    ort_sess = ort.InferenceSession(selectedModel, sess_options=so, providers=[
                                    onnxProvider])

    # Used for colors drawn on bounding boxes
    COLORS = np.random.uniform(0, 255, size=(1500, 3))

    # Set the cooldown time in seconds
    cooldown_time = 1  # Adjust the cooldown time as needed

    # Initialize variables
    last_pause_time = time.time()
    running = True

    if realtimeOverlay == True:
        pm.overlay_init()
        innerRadius = fovCircleSize
        outerRadius = innerRadius + 2
        width, height = pm.get_screen_width(), pm.get_screen_height()
        centerX, centerY = width // 2, height // 2
        overlay_color = hex_to_rgba(overlayColor)
        xOffset, yOffset = calculate_offsets(screenShotWidth, screenShotHeight)

    with torch.no_grad():

        while win32api.GetAsyncKeyState(ord(aaQuitKey)) == 0:

            if realtimeOverlay == True:
                pm.overlay_loop()
                pm.begin_drawing()
                if showFOVCircle == True:
                    pm.draw_ring(centerX, centerY, 1, innerRadius, outerRadius, 0, 360, overlay_color)
                if showStatus == True:
                    if aimbot:
                        softaim_overlay_color = green
                    else:
                        softaim_overlay_color = red
                    if triggerBot:
                        text_overlay_color = green
                    else:
                        text_overlay_color = red
                    pm.draw_text(f"Softaim: {aimbot}", centerX - 40, centerY + 300, 10, softaim_overlay_color)
                    pm.draw_text(f"TriggerBot: {triggerBot}", centerX - 40, centerY + 310, 10, text_overlay_color)
                pm.end_drawing()

            current_time = time.time()

            if is_key_pressed(aaPauseKey) and (current_time - last_pause_time) > cooldown_time:
             running = not running
             last_pause_time = current_time
             print("Paused" if not running else "Resumed")

            if not running:
             time.sleep(0.1)  # Sleep to reduce CPU usage when paused
             continue

            # Getting Frame
            npImg = np.array(camera.get_latest_frame())

            if useMask:
                npImg[-maskHeight:, -maskWidth:, :] = 0

            # If Nvidia, do this
            if onnxChoice == 3:
                # Normalizing Data
                im = torch.from_numpy(npImg).to('cuda')
                if im.shape[2] == 4:
                    # If the image has an alpha channel, remove it
                    im = im[:, :, :3,]

                im = torch.movedim(im, 2, 0)
                im = im.half()
                im /= 255
                if len(im.shape) == 3:
                    im = im[None]
            # If AMD or CPU, do this
            else:
                # Normalizing Data
                im = np.array([npImg])
                if im.shape[3] == 4:
                    # If the image has an alpha channel, remove it
                    im = im[:, :, :, :3]
                im = im / 255
                im = im.astype(np.half)
                im = np.moveaxis(im, 3, 1)

            # If Nvidia, do this
            if onnxChoice == 3:
                outputs = ort_sess.run(None, {'images': cp.asnumpy(im)})
            # If AMD or CPU, do this
            else:
                outputs = ort_sess.run(None, {'images': np.array(im)})

            im = torch.from_numpy(outputs[0]).to('cpu')

            pred = non_max_suppression(
                im, confidence, confidence, 0, False, max_det=10)

            targets = []
            for i, det in enumerate(pred):
                s = ""
                gn = torch.tensor(im.shape)[[0, 0, 0, 0]]
                if len(det):
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {int(c)}, "  # add to string

                    for *xyxy, conf, cls in reversed(det):
                        targets.append((xyxy2xywh(torch.tensor(xyxy).view(
                            1, 4)) / gn).view(-1).tolist() + [float(conf)])  # normalized xywh

            targets = pd.DataFrame(
                targets, columns=['current_mid_x', 'current_mid_y', 'width', "height", "confidence"])

            center_screen = [cWidth, cHeight]

            # Triggerbot Toggle
            if is_key_pressed(aaTriggerBotKey) and disableTriggerBot == False:
                triggerBot = not triggerBot
                print(f"TriggerBot toggled: {triggerBot}")
                time.sleep(0.25)

            # aimbot toggle
            if win32api.GetKeyState(key_code) < 0 and toggleAimbot == True:
                aimbot = not aimbot
                print(f"Aimbot toggled: {aimbot}")
                time.sleep(0.25)


            # If there are people in the center bounding box
            if len(targets) > 0:
                if (centerOfScreen):
                    # Compute the distance from the center
                    targets["dist_from_center"] = np.sqrt((targets.current_mid_x - center_screen[0])**2 + (targets.current_mid_y - center_screen[1])**2)

                    # Sort the data frame by distance from center
                    targets = targets.sort_values("dist_from_center")


                # get last person coordinate if exist
                if last_mid_coord:
                    targets['last_mid_x'] = last_mid_coord[0]
                    targets['last_mid_y'] = last_mid_coord[1]
                    targets['dist'] = np.linalg.norm(
                        targets.iloc[:, [0, 1]].values - targets.iloc[:, [4, 5]], axis=1)
                    targets.sort_values(by="dist", ascending=False)

                xMid = targets.iloc[0].current_mid_x
                yMid = targets.iloc[0].current_mid_y

                selected_body_part = BodyPart
                random_body_part = RandomBodyPart
                if random_body_part:
                    selected_body_part = random.choice(list(body_part_offsets.keys()))

                body_part_offset = body_part_offsets.get(selected_body_part, 0.30)

                box_height = targets.iloc[0].height
                offset = box_height * body_part_offset

                mouseMove = [xMid - cWidth, (yMid - offset) - cHeight]

                # Calculate distance from the center of the screen
                dist_from_center = np.sqrt(mouseMove[0]**2 + mouseMove[1]**2)

                # Triggerbot
                if triggerBot == True and abs(mouseMove[0]) <= triggerbot_actdistance and abs(mouseMove[1]) <= triggerbot_actdistance:
                    # Press the mouse button
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


                # Check if the target is within the FOV circle
                if dist_from_center <= fovCircleSize:
                 
                    if aimbot == True or win32api.GetKeyState(key_code) < 0 and toggleAimbot == False:

                        jitter_x, jitter_y = generate_jitter()
                        mouseMove[0] = int(mouseMove[0] + jitter_x)
                        mouseMove[1] = int(mouseMove[1] + jitter_y)

                        # Move mouse
                        if is_right_mouse_button_pressed():
                            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,
                            int(mouseMove[0] * aaMovementAmp),
                            int(mouseMove[1] * aaMovementAmp), 0, 0)
                        else:
                            # If hipfire then hipfire modifier
                            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,
                            int(mouseMove[0] * aaMovementAmpHipfire),
                            int(mouseMove[1] * aaMovementAmpHipfire), 0, 0)
                         
                    

            else:
                last_mid_coord = None

            # See visuals
            if visuals:
                npImg = cp.asnumpy(npImg[0])


                # Loops over every item identified and draws a bounding box
                for i in range(0, len(targets)):
                    halfW = round(targets["width"][i] / 2)
                    halfH = round(targets["height"][i] / 2)
                    midX = targets['current_mid_x'][i]
                    midY = targets['current_mid_y'][i]
                    (startX, startY, endX, endY) = int(
                        midX + halfW), int(midY + halfH), int(midX - halfW), int(midY - halfH)

                    idx = 0
                    # draw the bounding box and label on the frame
                    label = "{}: {:.2f}%".format(
                        "Enemy", targets["confidence"][i] * 100)
                    cv2.rectangle(npImg, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(npImg, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)\
                                
                    # Draw a red line from the center of the screen to the bounding box
                    centerXline, centerYline = npImg.shape[1] // 2, npImg.shape[0] // 2
                    cv2.line(npImg, (centerXline, centerYline), (int(midX), int(midY)), (0, 0, 255), 1)

                    # Apply offset to live overlay
                    fixedX, fixedY = midX + xOffset, midY + yOffset

                    # Overlay
                    if realtimeOverlay == True:
                        if showTracers == True:
                            pm.draw_line(centerX, centerY, fixedX, fixedY, overlay_color, 1)
                        if showBoxes == True:
                            pm.draw_rectangle_lines(fixedX - halfW, fixedY - halfH, round(targets["width"][i]), round(targets["height"][i]), overlay_color, 1)

            if realtimeOverlay == True and visuals == False:

                for i in range(0, len(targets)):
                    halfW = round(targets["width"][i] / 2)
                    halfH = round(targets["height"][i] / 2)
                    midX = targets['current_mid_x'][i]
                    midY = targets['current_mid_y'][i]
                    (startX, startY, endX, endY) = int(
                        midX + halfW), int(midY + halfH), int(midX - halfW), int(midY - halfH)
                    
                    fixedX, fixedY = midX + xOffset, midY + yOffset

                    if showTracers == True:
                        pm.draw_line(centerX, centerY, fixedX, fixedY, overlay_color, 1)
                    if showBoxes == True:
                        pm.draw_rectangle_lines(fixedX - halfW, fixedY - halfH, round(targets["width"][i]), round(targets["height"][i]), overlay_color, 1)



            # Forced garbage cleanup every second
            count += 1
            if (time.time() - sTime) > 1:
                if cpsDisplay:
                    print("CPS: {}".format(count))
                count = 0
                sTime = time.time()

            # Uncomment if memory issues
            # gc.collect(generation=0)

            # See visually what the Aimbot sees
            if visuals:
                cv2.imshow('Live Feed', npImg)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    exit()

    camera.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print(str(e))
        print("")
        input()