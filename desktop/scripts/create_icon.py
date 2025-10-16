#!/usr/bin/env python3
"""
Script to create macOS .icns file from PNG logo
"""

import os
import subprocess
from PIL import Image

def create_icon_set():
    """Create icon set for macOS"""
    
    # Get paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_dir = os.path.dirname(current_dir)
    assets_dir = os.path.join(desktop_dir, 'assets')
    logo_path = os.path.join(assets_dir, 'app_logo.png')
    
    # Create iconset directory
    iconset_dir = os.path.join(assets_dir, 'app_logo.iconset')
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Required icon sizes for macOS
    icon_sizes = [
        (16, 'icon_16x16.png'),
        (32, 'icon_16x16@2x.png'),
        (32, 'icon_32x32.png'),
        (64, 'icon_32x32@2x.png'),
        (128, 'icon_128x128.png'),
        (256, 'icon_128x128@2x.png'),
        (256, 'icon_256x256.png'),
        (512, 'icon_256x256@2x.png'),
        (512, 'icon_512x512.png'),
        (1024, 'icon_512x512@2x.png')
    ]
    
    try:
        # Load original image
        image = Image.open(logo_path)
        
        # Create all required icon sizes
        for size, filename in icon_sizes:
            # Resize image maintaining aspect ratio
            resized = image.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save to iconset directory
            output_path = os.path.join(iconset_dir, filename)
            resized.save(output_path, 'PNG')
            print(f"Created {filename} ({size}x{size})")
        
        # Create .icns file using iconutil (macOS built-in tool)
        icns_path = os.path.join(assets_dir, 'app_logo.icns')
        
        try:
            subprocess.run([
                'iconutil', '-c', 'icns', iconset_dir, '-o', icns_path
            ], check=True)
            print(f"Created {icns_path}")
            
            # Clean up iconset directory
            import shutil
            shutil.rmtree(iconset_dir)
            print("Cleaned up iconset directory")
            
        except subprocess.CalledProcessError as e:
            print(f"Error creating .icns file: {e}")
            print("You may need to install Xcode command line tools")
            
    except Exception as e:
        print(f"Error creating icon set: {e}")

if __name__ == "__main__":
    create_icon_set()
