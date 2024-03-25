# Res-Softaim Features (Default Activation Key is Left-alt!)
![image](https://github.com/justaseal82/Res-Softaim/assets/62959173/afcfffd5-34f5-4772-be5e-85be0cf41fc8)
![image](https://github.com/justaseal82/Res-Softaim/assets/62959173/194acfe4-e53e-45c8-9681-dd367fe70773)
![image](https://github.com/justaseal82/Res-Softaim/assets/62959173/c419b051-58e1-4b1a-878b-10bd97a1b2ba)
![image](https://github.com/justaseal82/Res-Softaim/assets/62959173/ffb2e5a4-013f-4f7d-bfe0-4d4dd7dd0c45)
![image](https://github.com/justaseal82/Res-Softaim/assets/62959173/e91a943d-b5c6-4194-bef7-f0c45c27fe9f)

Demo Video: https://youtu.be/yk4MmO7PUzM

Use Rootkit's Setup guide for initial Pre-Requisites
## 🧰 Requirements
- Nvidia RTX 980 🆙, higher or equivalent
- And one of the following:
  - Nvidia CUDA Toolkit 11.8 [DOWNLOAD HERE](https://developer.nvidia.com/cuda-11-8-0-download-archive)

## 🚀 Pre-setup Steps
1. Download and Unzip the AI Aimbot and stash the folder somewhere handy 🗂️.
2. Ensure you've got Python installed (like a pet python 🐍) – grab version 3.11 [HERE](https://www.python.org/downloads/release/python-3116/).
   - 🛑 Facing a `python is not recognized...` error? [WATCH THIS!](https://youtu.be/E2HvWhhAW0g)
   - 🛑 Is it a `pip is not recognized...` error? [WATCH THIS!](https://youtu.be/zWYvRS7DtOg)
3. Fire up `PowerShell` or `Command Prompt` on Windows 🔍.
4. To install `PyTorch`, select the appropriate command based on your GPU.
    - Nvidia `pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118`
    - AMD or CPU `pip install torch torchvision torchaudio`
5. 📦 Run the file below to install all the libraries
```
Install Requirements.bat
```
## 🔌 How to Run (Faster 🏃‍♂️💨 Version)
Follow these steps **after** Python and all packages have been installed:

1. Tweak the `onnxChoice` variable in the menu to correspond with your hardware specs:
    - `onnxChoice = 1` # CPU ONLY 🖥
    - `onnxChoice = 2` # AMD/NVIDIA ONLY 🎮
    - `onnxChoice = 3` # NVIDIA ONLY 🏎️
2. IF you have an NVIDIA set up, run the following
    ```
    pip install onnxruntime-gpu
    pip install cupy-cuda11x
    ```
2. Follow the same steps as for the Fast 🏃‍♂️ Version above except for step 4, you will run `python main_onnx.py` instead.


## 🔌 How to Run (Fastest 🚀 Version)
Follow these sparkly steps to get your TensorRT ready for action! 🛠️✨

1. **Introduction** 🎬
   Watch the TensorRT section of the setup [video 🎥](https://www.youtube.com/watch?v=uniL5yR7y0M&ab_channel=RootKit) before you begin. It's loaded with useful tips!

2. **Oops! Don't Forget the Environment** 🌱
   We forgot to mention adding environmental variable paths in the video. Make sure to do this part!

3. **Get Support If You're Stumped** 🤔
   If you ever feel lost, you can always `@Wonder` your questions in our [Discord 💬](https://discord.gg/rootkitorg). Wonder is here to help!

4. **Install Cupy**
    Run the following `pip install cupy-cuda11x`

5. **CUDNN Installation** 🧩
   Click to install [CUDNN 📥](https://developer.nvidia.com/downloads/compute/cudnn/secure/8.9.6/local_installers/11.x/cudnn-windows-x86_64-8.9.6.50_cuda11-archive.zip/). You'll need a Nvidia account to proceed. Don't worry it's free.

6. **Unzip and Relocate** 📁➡️
   Open the .zip CuDNN file and move all the folders/files to where the CUDA Toolkit is on your machine, usually at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`.

7. **Get TensorRT 8.6 GA** 🔽
   Fetch [`TensorRT 8.6 GA 🛒`](https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/secure/8.6.1/zip/TensorRT-8.6.1.6.Windows10.x86_64.cuda-11.8.zip).

8. **Unzip and Relocate** 📁➡️
   Open the .zip TensorRT file and move all the folders/files to where the CUDA Toolkit is on your machine, usually at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`.

9. **Python TensorRT Installation** 🎡
   Once you have all the files copied over, you should have a folder at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\python`. If you do, good, then run the following command to install TensorRT in python.
   ```
   pip install "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\python\tensorrt-8.6.1-cp311-none-win_amd64.whl"
   ```
    🚨 If the following steps didn't work, don't stress out! 😅 The labeling of the files corresponds with the Python version you have installed on your machine. We're not looking for the 'lean' or 'dispatch' versions. 🔍 Just locate the correct file and replace the path with your new one. 🔄 You've got this! 💪

10. **Set Your Environmental Variables** 🌎
   Add these paths to your environment:
   - `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\lib`
   - `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp`
   - `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin`

11. **Download Pre-trained Models** 🤖
   You can use one of the .engine models we supply. But if it doesn't work, then you will need to re-export it. Grab the `.pt` file here for the model you want. We recommend `yolov5s.py` or `yolov5m.py` [HERE 🔗](https://github.com/ultralytics/yolov5/releases/tag/v7.0).

12. **Run the Export Script** 🏃‍♂️💻
   Time to execute `export.py` with the following command. Patience is key; it might look frozen, but it's just concentrating hard! Can take up to 20 mintues.
   
   ```
   python .\export.py --weights ./FortniteTaipei.pt --include engine --half --imgsz 320 320 --device 0
   ```
   
   Note: You can pick a different YOLOv5 model size. TensorRT's power allows for larger models if desired!

If you've followed these steps, you should be all set with TensorRT! ⚙️🚀
