print("\033c")
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

#=====================================================================================
#=================================    SETTINGS    ====================================
#=====================================================================================
nama_file_karakter = "roblox_kick"
nama_file_bola = "soccer_ball"
nama_file_latar = "bg2"
num_frames = 20
threshold = 15

# Camera settings
cam_distance = 350
cam_angle = 45  # 45° dari depan
focal_length = 200

# Ball position offset (relative to character center)
# Bola di depan karakter (Z negatif = depan)
ball_offset_x = 0      # Tengah
ball_offset_y = 30     # Sedikit di bawah (dekat kaki)
ball_offset_z = -50    # Di depan karakter

#============================================================================================
#=======================   LOAD ASSETS   ====================================================
#============================================================================================
print("Loading assets...")

# Load background
latar_pil = Image.open(nama_file_latar + ".png")
latar_pil = latar_pil.convert("RGB")

# Load soccer ball
bola = np.load(nama_file_bola + ".npy")
print(f"Ball shape: {bola.shape}")

#============================================================================================
#=======================   COMBINE VOXELS FUNCTION   ========================================
#============================================================================================

def combine_character_and_ball(voxel_karakter, voxel_bola, offset_x, offset_y, offset_z):
    """
    Gabungkan voxel karakter dan bola dalam 1 array.
    Bola akan di-translasi sesuai offset.
    """
    row, col, length, ch = voxel_karakter.shape
    combined = voxel_karakter.copy()
    
    bola_row, bola_col, bola_len, _ = voxel_bola.shape
    
    # Center of character (pivot point)
    char_cx = col // 2
    char_cy = row // 2
    char_cz = length // 2
    
    # Center of ball in its own voxel
    ball_cx = bola_col // 2
    ball_cy = bola_row // 2
    ball_cz = bola_len // 2
    
    # Target position for ball center
    target_x = char_cx + offset_x
    target_y = char_cy + offset_y
    target_z = char_cz + offset_z
    
    # Copy ball voxels to combined array with translation
    for i in range(bola_row):
        for j in range(bola_col):
            for k in range(bola_len):
                if voxel_bola[i, j, k, 0] + voxel_bola[i, j, k, 1] + voxel_bola[i, j, k, 2] > threshold:
                    # Calculate new position
                    new_y = i - ball_cy + target_y
                    new_x = j - ball_cx + target_x
                    new_z = k - ball_cz + target_z
                    
                    # Check bounds
                    if 0 <= new_y < row and 0 <= new_x < col and 0 <= new_z < length:
                        # Only overwrite if destination is empty (no collision)
                        if combined[new_y, new_x, new_z, 0] + combined[new_y, new_x, new_z, 1] + combined[new_y, new_x, new_z, 2] <= threshold:
                            combined[new_y, new_x, new_z, :] = voxel_bola[i, j, k, :]
    
    return combined

#============================================================================================
#=======================   PROJECTION FUNCTION   ============================================
#============================================================================================

def project_with_camera(voxel, cam_angle_deg, cam_distance, focal, background):
    """Project 3D voxel with background"""
    row, col, length, _ = voxel.shape
    
    # Resize background
    bg_resized = background.resize((col, row), Image.LANCZOS)
    screen = np.array(bg_resized, dtype=np.uint8)
    
    # Center
    cx = col // 2
    cy = row // 2
    cz = length // 2
    
    angle_rad = np.radians(cam_angle_deg)
    depth_buffer = np.full((row, col), np.inf)
    
    for i in range(row):
        for j in range(col):
            for k in range(length):
                if voxel[i,j,k,0] + voxel[i,j,k,1] + voxel[i,j,k,2] > threshold:
                    dx = j - cx
                    dy = i - cy
                    dz = k - cz
                    
                    # Rotate to camera coordinate
                    dx_cam = dx * np.cos(-angle_rad) - dz * np.sin(-angle_rad)
                    dz_cam = dx * np.sin(-angle_rad) + dz * np.cos(-angle_rad)
                    dy_cam = dy
                    
                    dz_cam = dz_cam + cam_distance
                    
                    if dz_cam > 50:
                        scale = focal / dz_cam
                        sx = int(col/2 - dx_cam * scale)
                        sy = int(row/2 + dy_cam * scale)
                        
                        if 0 <= sx < col and 0 <= sy < row:
                            if dz_cam < depth_buffer[sy, sx]:
                                depth_buffer[sy, sx] = dz_cam
                                screen[sy, sx, :] = voxel[i,j,k,:]
    
    return screen

#============================================================================================
#=======================   RENDER ANIMATION   ===============================================
#============================================================================================

print(f"\nRendering kick animation with ball...")
print(f"Ball offset: X={ball_offset_x}, Y={ball_offset_y}, Z={ball_offset_z}")
print(f"Camera: {cam_angle}°, distance={cam_distance}")

for frame in range(num_frames):
    print(f"Frame {frame+1}/{num_frames}")
    
    # Load character frame
    voxel_karakter = np.load(f"{nama_file_karakter}_frame_{frame:03d}.npy")
    
    # Combine character and ball
    voxel_combined = combine_character_and_ball(voxel_karakter, bola, 
                                                 ball_offset_x, ball_offset_y, ball_offset_z)
    
    # Project
    screen = project_with_camera(voxel_combined, cam_angle, cam_distance, focal_length, latar_pil)
    
    # Save
    output = f"kick_with_ball_{frame:03d}.jpg"
    plt.imsave(output, screen)

print("\nDone!")
print("Output: kick_with_ball_000.jpg to kick_with_ball_019.jpg")

# Show last frame
plt.figure(1)
plt.imshow(screen)
plt.title('Kick Animation with Ball')
plt.show()
