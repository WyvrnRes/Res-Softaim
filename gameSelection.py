import pygetwindow
import time
import bettercam
from config import screenShotHeight, screenShotWidth, autoGameDetection, gameName

def gameSelection() -> (bettercam.BetterCam, int, int | None):
    # Selecting the correct game window
    try:
        videoGameWindows = pygetwindow.getAllWindows()

        if autoGameDetection:
            # Filter windows by the specified game name
            filteredWindows = [window for window in videoGameWindows if gameName.lower() in window.title.lower()]

            if not filteredWindows:
                print(f"No windows found for the game '{gameName}'. Exiting.")
                return None

            videoGameWindow = filteredWindows[0] if len(filteredWindows) == 1 else None
            if videoGameWindow is None:
                print("Multiple or no matching game windows found. Exiting.")
                return None
        else:
            # Manual selection process with output to the user
            print("=== All Windows ===")
            for index, window in enumerate(videoGameWindows):
                if window.title != "":
                    print(f"[{index}]: {window.title}")

            try:
                userInput = int(input("Please enter the number corresponding to the window you'd like to select: "))
                videoGameWindow = videoGameWindows[userInput]
            except ValueError:
                print("You didn't enter a valid number. Please try again.")
                return None
            except IndexError:
                print("Invalid selection. Please try again.")
                return None

    except Exception as e:
        print(f"Failed to select game window: {e}")
        return None

    # Activate the selected Window
    activationRetries = 30
    while activationRetries > 0:
        try:
            videoGameWindow.activate()
            break
        except pygetwindow.PyGetWindowException:
            activationRetries -= 1
            time.sleep(1.0)
            continue
        except Exception as e:
            print(f"Failed to activate game window: {e}")
            return None

    if activationRetries == 0:
        print("Failed to activate the game window after multiple attempts. Exiting.")
        return None

    # Starting screenshoting engine
    left = ((videoGameWindow.left + videoGameWindow.right) // 2) - (screenShotWidth // 2)
    top = videoGameWindow.top + (videoGameWindow.height - screenShotHeight) // 2
    right, bottom = left + screenShotWidth, top + screenShotHeight
    region: tuple = (left, top, right, bottom)

    # Calculating the center Autoaim box
    cWidth: int = screenShotWidth // 2
    cHeight: int = screenShotHeight // 2

    camera = bettercam.create(region=region, output_color="BGRA", max_buffer_len=512)
    if camera is None:
        print("Your Camera Failed! Ask for help in the support channel.")
        return None
    camera.start(target_fps=135, video_mode=True)

    return camera, cWidth, cHeight
