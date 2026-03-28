import os
import io

class FileStore:
    """Handles saving heavy artifacts (images, audio) to the local disk."""
    
    def __init__(self, base_dir: str = "./artifacts"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def _get_run_dir(self, run_id: str) -> str:
        run_dir = os.path.join(self.base_dir, run_id)
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

    def save_image(self, run_id: str, name: str, image_array, step: int = None) -> str:
        """Saves a numpy array as a PNG image using PIL."""
        try:
            import numpy as np
            from PIL import Image
        except ImportError:
            raise ImportError("Please install numpy and Pillow to log images: pip install numpy Pillow")
            
        run_dir = self._get_run_dir(run_id)
        img_dir = os.path.join(run_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        
        filename = f"{name}_step_{step}.png" if step is not None else f"{name}.png"
        file_path = os.path.join(img_dir, filename)
        
        # Ensure it's in uint8 format (0-255)
        if hasattr(image_array, 'dtype') and image_array.dtype != np.uint8:
            # If float, assume 0-1 range
            if image_array.max() <= 1.0:
                image_array = (image_array * 255).astype(np.uint8)
            else:
                image_array = image_array.astype(np.uint8)
                
        img = Image.fromarray(image_array)
        img.save(file_path)
        return file_path

    def save_audio(self, run_id: str, name: str, audio_waveform, sample_rate: int, step: int = None) -> str:
        """Saves a numpy array as a WAV file using scipy."""
        try:
            from scipy.io import wavfile
        except ImportError:
            raise ImportError("Please install scipy to log audio: pip install scipy")
            
        run_dir = self._get_run_dir(run_id)
        audio_dir = os.path.join(run_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        filename = f"{name}_step_{step}.wav" if step is not None else f"{name}.wav"
        file_path = os.path.join(audio_dir, filename)
        
        wavfile.write(file_path, sample_rate, audio_waveform)
        return file_path
