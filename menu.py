import customtkinter
import os
from PIL import Image
import subprocess
from pyMeow import get_display_resolution

displayResolution = get_display_resolution()

def get_engine_files():
    return [f for f in os.listdir() if f.endswith('.engine')]

def create_model_selector(parent, row, column, engine_files, default_model):
    customtkinter.CTkLabel(parent, text="Select Model").grid(row=row, column=column, pady=(10, 0), padx=(10, 0), sticky="w")
    model_selector = customtkinter.CTkComboBox(parent, values=engine_files)
    model_selector.set(default_model)
    model_selector.grid(row=row, column=column + 1, pady=(10, 0), padx=(10, 10), sticky="w")
    return model_selector

def set_initial_values(entry_widget, config_value):
    entry_widget.insert(0, str(config_value))

def set_switch(switch, value):
    if hasattr(switch, 'get'):
        current_value = switch.get()
        if current_value != value:  
            if value:
                switch.select()
            else:
                switch.deselect()

class App(customtkinter.CTk):
    def __init__(app):
        super().__init__()
        import config

        def run():
            print("Started Running 'main_tensorrt.py'")
            selected_model = model_selector.get()
            subprocess.Popen(['python', 'main_tensorrt.py', selected_model])
            exit()


        # self explanatory save settings
        def save_settings():
            selected_model = model_selector.get()
            use_mask_value = use_mask_switch.get() == 1
            auto_game_detection_value = auto_game_detection_switch.get() == 1
            cps_display_value = cps_display_switch.get() == 1
            visuals_value = visuals_switch.get() == 1
            realtime_overlay_value = realtime_overlay_switch.get() == 1
            center_of_screen_value = center_of_screen_switch.get() == 1
            arduino_leonardo_value = arduino_leonardo_switch.get() == 1
            random_body_part_value = random_body_part_switch.get() == 1
            triggerBot_value = triggerBot_switch.get() == 1
            showTriggerBot_value = showTriggerBot_switch.get() == 1
            showFOVCircle_value = showFOVCircle_switch.get() == 1

            # save to config.py
            with open('config.py', 'w') as config_file:
                config_file.write(f"screenShotHeight = {screen_shot_height_entry.get()}\n")
                config_file.write(f"screenShotWidth = {screen_shot_width_entry.get()}\n")
                config_file.write(f"jitterValue = {jitter_value_box.get()}\n")
                config_file.write(f"useMask = {use_mask_value}\n")
                config_file.write(f"maskWidth = {mask_width_entry.get()}\n")
                config_file.write(f"maskHeight = {mask_height_entry.get()}\n")
                config_file.write(f"autoGameDetection = {auto_game_detection_value}\n")
                config_file.write(f"gameName = '{game_name_entry.get()}'\n")
                config_file.write(f"aaMovementAmp = {float(aa_movement_amp_entry.get())}\n")
                config_file.write(f"aaMovementAmpHipfire = {float(aa_movement_amp_hipfire_entry.get())}\n")
                config_file.write(f"confidence = {float(confidence_entry.get())}\n")
                config_file.write(f"fovCircleSize = {fov_circle_size_entry.get()}\n")
                config_file.write(f"aaQuitKey = '{aa_quit_key_entry.get()}'\n")
                config_file.write(f"aaTriggerBotKey = '{aa_trigger_bot_key_entry.get()}'\n")
                config_file.write(f"aaPauseKey = '{aa_pause_key_entry.get()}'\n")
                config_file.write(f"cpsDisplay = {cps_display_value}\n")
                config_file.write(f"visuals = {visuals_value}\n")
                config_file.write(f"realtimeOverlay = {realtime_overlay_value}\n")
                config_file.write(f"centerOfScreen = {center_of_screen_value}\n")
                config_file.write(f"onnxChoice = {int(onnx_choice_entry.get())}\n")
                config_file.write(f"ArduinoLeonardo = {arduino_leonardo_value}\n")
                config_file.write(f"arduinoPort = '{arduino_port_entry.get()}'\n")
                config_file.write(f"selectedModel = '{selected_model}'\n") 
                config_file.write(f"BodyPart = '{body_part_selector.get()}'\n")
                config_file.write(f"RandomBodyPart = {random_body_part_value}\n")
                config_file.write(f"triggerBot = {triggerBot_value}\n")
                config_file.write(f"triggerbot_actdistance = {triggerbot_actdistance_entry.get()}\n")
                config_file.write(f"showTriggerBotRadius = {showTriggerBot_value}\n")
                config_file.write(f"showFOVCircle = {showFOVCircle_value}\n")
                config_file.write(f"overlayColor = '{overlayColor_entry.get()}'\n")
            app.after(500, save_settings)

        def create_setting_widget(parent, label, row, column, widget_type=customtkinter.CTkEntry, **options):
            customtkinter.CTkLabel(parent, text=label).grid(row=row, column=column, pady=(10, 0), padx=(10, 0), sticky="w")
            if widget_type == customtkinter.CTkCheckBox and 'text' not in options:
                options['text'] = ""
            widget = widget_type(parent, **options)
            widget.grid(row=row, column=column + 1, pady=(10, 0), padx=(10, 10), sticky="w")
            return widget

        themes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "themes")
        customtkinter.set_default_color_theme(os.path.join(themes_path, "red.json"))

        app.title("Res Softaim Menu")
        app.iconbitmap("icon.ico")
        app.geometry("700x440")
        app.resizable(False, False)

        # set grid layout 1x2
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=1)

        # load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        app.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon-removebg-preview.png")), size=(84, 84))
        app.screen_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "screen.png")), size=(20, 20))
        app.mask_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "mask.png")), size=(20, 20))
        app.gameaim_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "gameaim.png")), size=(20, 20))
        app.advanced_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "advanced.png")), size=(20, 20))
        app.hardware_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "hardware.png")), size=(20, 20))

        # create navigation frame
        app.navigation_frame = customtkinter.CTkFrame(app, corner_radius=0)
        app.navigation_frame.grid(row=0, column=0, sticky="nsew")
        app.navigation_frame.grid_rowconfigure(8, weight=1)

        app.navigation_frame_label = customtkinter.CTkLabel(app.navigation_frame, text = "", image=app.logo_image)
        app.navigation_frame_label.grid(row=6, column=0, padx=20, pady=20)
        app.run_button = create_setting_widget(app.navigation_frame, "", 7, 0, widget_type=customtkinter.CTkButton, text="Run Softaim", command=run)
        app.run_button.grid(row=7, column=0)
        app.display = create_setting_widget(app.navigation_frame, "", 8, 0, widget_type=customtkinter.CTkLabel, text=str(displayResolution[0]) + " x " + str(displayResolution[1]))
        app.display.grid(row=8, column=0)

        app.screen_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Screen",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=app.screen_image, anchor="w", command=app.screen_button_event)
        app.screen_button.grid(row=1, column=0, sticky="ew")

        app.frame_2_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Mask",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=app.mask_image, anchor="w", command=app.frame_2_button_event)
        app.frame_2_button.grid(row=2, column=0, sticky="ew")

        app.frame_3_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Game & Aim",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=app.gameaim_image, anchor="w", command=app.frame_3_button_event)
        app.frame_3_button.grid(row=3, column=0, sticky="ew")

        app.frame_4_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Advanced",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=app.advanced_image, anchor="w", command=app.frame_4_button_event)
        app.frame_4_button.grid(row=4, column=0, sticky="ew")

        app.frame_5_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Hardware",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=app.hardware_image, anchor="w", command=app.frame_5_button_event)
        app.frame_5_button.grid(row=5, column=0, sticky="ew")



        # create screen frame
        app.screen_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.screen_frame.grid_columnconfigure(0, weight=1)

        screen_shot_height_entry = create_setting_widget(app.screen_frame, "Screen Shot Height", 0, 0)
        screen_shot_width_entry = create_setting_widget(app.screen_frame, "Screen Shot Width", 1, 0)

        # create mask frame
        app.second_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.second_frame.grid_columnconfigure(0, weight=1)

        use_mask_switch = create_setting_widget(app.second_frame, "Use Mask", 0, 0, widget_type=customtkinter.CTkSwitch, text="")
        mask_width_entry = create_setting_widget(app.second_frame, "Mask Width", 1, 0)
        mask_height_entry = create_setting_widget(app.second_frame, "Mask Height", 2, 0)

        # create game & aim frame
        app.third_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.third_frame.grid_columnconfigure(3, weight=1)

        game_name_entry = create_setting_widget(app.third_frame, "Game Name", 1, 0)
        aa_movement_amp_entry = create_setting_widget(app.third_frame, "Softaim ADS Sensitivity", 2, 0, widget_type=customtkinter.CTkEntry)
        aa_movement_amp_hipfire_entry = create_setting_widget(app.third_frame, "Softaim Hipfire Sensitivity", 3, 0, widget_type=customtkinter.CTkEntry)
        confidence_entry = create_setting_widget(app.third_frame, "Aim Confidence", 4, 0)
        jitter_value_box = create_setting_widget(app.third_frame, "Jitter Amount", 5, 0)
        fov_circle_size_entry = create_setting_widget(app.third_frame, "FOV Circle Size", 6, 0)
        body_part_selector = create_setting_widget(app.third_frame, "Body Part Selector", 7, 0, widget_type=customtkinter.CTkComboBox, values=["Head", "Neck", "Body", "Pelvis"])
        body_part_selector.set(config.BodyPart)
        auto_game_detection_switch = create_setting_widget(app.third_frame, "Automatic Game Detection", 1, 2, widget_type=customtkinter.CTkSwitch, text="")
        random_body_part_switch = create_setting_widget(app.third_frame, "Randomized Body Part", 2, 2, widget_type=customtkinter.CTkSwitch, text="")
        triggerBot_switch = create_setting_widget(app.third_frame, "Trigger Bot", 3, 2, widget_type=customtkinter.CTkSwitch, text="")
        triggerbot_actdistance_entry = create_setting_widget(app.third_frame, "Activation Distance", 4, 2, widget_type=customtkinter.CTkEntry)
        realtime_overlay_switch = create_setting_widget(app.third_frame, "Realtime Overlay", 5, 2, widget_type=customtkinter.CTkSwitch, text="")
        showTriggerBot_switch = create_setting_widget(app.third_frame, "Trigger Bot FOV Overlay", 6, 2, widget_type=customtkinter.CTkSwitch, text="")
        showFOVCircle_switch = create_setting_widget(app.third_frame, "FOV Circle Overlay", 7, 2, widget_type=customtkinter.CTkSwitch, text="")
        center_of_screen_switch = create_setting_widget(app.third_frame, "Center of Screen Selection", 8, 2, widget_type=customtkinter.CTkSwitch, text="")

        # create advanced frame
        app.fourth_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.fourth_frame.grid_columnconfigure(0, weight=1)

        cps_display_switch = create_setting_widget(app.fourth_frame, "Display CPS", 1, 0, widget_type=customtkinter.CTkSwitch, text="")
        visuals_switch = create_setting_widget(app.fourth_frame, "Enable Softaim View", 2, 0, widget_type=customtkinter.CTkSwitch, text="")
        aa_quit_key_entry = create_setting_widget(app.fourth_frame, "Softaim Quit Key", 3, 0)
        aa_pause_key_entry = create_setting_widget(app.fourth_frame, "Softaim Pause Key", 4, 0)
        aa_trigger_bot_key_entry = create_setting_widget(app.fourth_frame, "Trigger Bot Key", 5, 0)
        overlayColor_entry = create_setting_widget(app.fourth_frame, "Choose Overlay Color (HEX Format)", 6, 0, widget_type=customtkinter.CTkEntry)
        engine_files = get_engine_files()
        model_selector = create_model_selector(app.fourth_frame, 7, 0, engine_files, config.selectedModel)

        # create hardware frame
        app.fifth_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.fifth_frame.grid_columnconfigure(0, weight=1)

        arduino_leonardo_switch = create_setting_widget(app.fifth_frame, "Use Arduino Leonardo", 1, 0, widget_type=customtkinter.CTkSwitch, text="")
        arduino_port_entry = create_setting_widget(app.fifth_frame, "Arduino Port", 2, 0)
        onnx_choice_entry = create_setting_widget(app.fifth_frame, "ONNX Choice (1-CPU, 2-AMD, 3-NVIDIA)", 3, 0)

        set_initial_values(screen_shot_height_entry, config.screenShotHeight)
        set_initial_values(screen_shot_width_entry, config.screenShotWidth)
        set_initial_values(mask_width_entry, config.maskWidth)
        set_initial_values(mask_height_entry, config.maskHeight)
        set_initial_values(game_name_entry, config.gameName)
        set_initial_values(aa_movement_amp_entry, config.aaMovementAmp)
        set_initial_values(aa_movement_amp_hipfire_entry, config.aaMovementAmpHipfire)
        set_initial_values(confidence_entry, config.confidence)
        set_initial_values(fov_circle_size_entry, config.fovCircleSize)
        set_initial_values(aa_quit_key_entry, config.aaQuitKey)
        set_initial_values(aa_trigger_bot_key_entry, config.aaTriggerBotKey)
        set_initial_values(aa_pause_key_entry, config.aaPauseKey)
        set_initial_values(onnx_choice_entry, config.onnxChoice)
        set_initial_values(arduino_port_entry, config.arduinoPort)
        set_initial_values(jitter_value_box, config.jitterValue)
        set_initial_values(triggerbot_actdistance_entry, config.triggerbot_actdistance)
        set_initial_values(overlayColor_entry, config.overlayColor)


        set_switch(use_mask_switch, config.useMask)
        set_switch(auto_game_detection_switch, config.autoGameDetection)
        set_switch(cps_display_switch, config.cpsDisplay)
        set_switch(visuals_switch, config.visuals)
        set_switch(center_of_screen_switch, config.centerOfScreen)
        set_switch(arduino_leonardo_switch, config.ArduinoLeonardo)
        set_switch(random_body_part_switch, config.RandomBodyPart) 
        set_switch(triggerBot_switch, config.triggerBot) 
        set_switch(realtime_overlay_switch, config.realtimeOverlay)
        set_switch(showTriggerBot_switch, config.showTriggerBotRadius)
        set_switch(showFOVCircle_switch, config.showFOVCircle)

        save_settings()

        # select default frame
        app.select_frame_by_name("frame_3")

    def select_frame_by_name(app, name):
        # set button color for selected button
        app.screen_button.configure(fg_color=("gray75", "gray25") if name == "screen" else "transparent")
        app.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        app.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        app.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        app.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")

        # show selected frame
        if name == "screen":
            app.screen_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.screen_frame.grid_forget()
            
        if name == "frame_2":
            app.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.second_frame.grid_forget()

        if name == "frame_3":
            app.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.third_frame.grid_forget()

        if name == "frame_4":
            app.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.fourth_frame.grid_forget()

        if name == "frame_5":
            app.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.fifth_frame.grid_forget()


    def screen_button_event(app):
        app.select_frame_by_name("screen")

    def frame_2_button_event(app):
        app.select_frame_by_name("frame_2")

    def frame_3_button_event(app):
        app.select_frame_by_name("frame_3")
    
    def frame_4_button_event(app):
        app.select_frame_by_name("frame_4")

    def frame_5_button_event(app):
        app.select_frame_by_name("frame_5")

if __name__ == "__main__":
    app = App()
    app.mainloop()