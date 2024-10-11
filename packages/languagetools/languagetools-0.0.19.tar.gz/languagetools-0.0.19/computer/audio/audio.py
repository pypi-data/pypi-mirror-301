import os
import subprocess

class Audio:
    def __init__(self, computer):
        self.computer = computer

    def transcribe(self, audio_path, display=True):
        # Define the directory to store the model
        model_dir = os.path.expanduser('~/models')
        os.makedirs(model_dir, exist_ok=True)
        
        # Define the model file path
        model_path = os.path.join(model_dir, 'whisper-tiny.en.llamafile')
        
        # Download the model if it doesn't exist
        if not os.path.exists(model_path):
            subprocess.run(['wget', '-O', model_path, 'https://huggingface.co/Mozilla/whisperfile/resolve/main/whisper-tiny.en.llamafile'], check=True)
        
        # Make the file executable
        subprocess.run(['chmod', '+x', model_path], check=True)

        command = f"{model_path} -f {audio_path} --no-prints"
        
        # Run the transcription
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
            # executable='/bin/bash'  # Specify the shell explicitly
        )
        
        full_output = ""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if display:
                    print(output.strip())
                full_output += output

        return_code = process.poll()
        
        if return_code == 0:
            return full_output
        else:
            error_output = process.stderr.read()
            return f"Transcription failed with return code {return_code}: {error_output}"