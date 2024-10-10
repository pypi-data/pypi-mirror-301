import subprocess
import os
from pathlib import Path
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def test_piper_tts():
    # Find the Piper TTS executable
    project_root = Path(__file__).parent.parent
    piper_dir = project_root / "piper_tts"
    piper_executable = piper_dir / "piper.exe" if os.name == 'nt' else piper_dir / "piper"

    if not piper_executable.exists():
        print(f"Error: Piper executable not found at {piper_executable}")
        return

    # Test text
    test_text = "Hello, this is a test of Piper TTS."

    # Output file
    output_file = project_root / "piper_test_output.wav"

    # Run Piper TTS
    try:
        command = [
            str(piper_executable),
            "--model", str(piper_dir / "en_US-amy-medium.onnx"),
            "--output_file", str(output_file)
        ]
        
        print(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=test_text)

        if process.returncode == 0:
            print(f"Piper TTS test successful. Output saved to {output_file}")
            print("Please check if the audio file was created and play it to verify the output.")
        else:
            print(f"Error running Piper TTS. Return code: {process.returncode}")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
    except Exception as e:
        print(f"An error occurred while testing Piper TTS: {e}")

    # List contents of piper_tts directory
    print("\nContents of piper_tts directory:")
    for item in piper_dir.iterdir():
        print(item.name)

if __name__ == "__main__":
    if not is_admin():
        print("Note: This script is not running with administrator privileges.")
    test_piper_tts()