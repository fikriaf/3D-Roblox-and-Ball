print("\033c")
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

#=====================================================================================
#=================================    SETTINGS    ====================================
#=====================================================================================
nama_file = "roblox_kick"
nama_file_latar = "Lapangan_edit"
num_frames = 20
threshold = 15

# Camera 1: 45° di depan (wajah terlihat), zoom in
cam1_distance = 250
cam1_angle = 45

# Camera 2: Lurus di belakang (tulisan TEAM 2 terlihat), normal
cam2_distance = 350
cam2_angle = 180

focal_length = 200

#============================================================================================
#=======================   LOAD BACKGROUND   ================================================
#============================================================================================
print("Loading background...")
latar_pil = Image.open(nama_file_latar + ".png")
latar_pil = latar_pil.convert("RGB")

#============================================================================================
#=======================   PROJECTION FUNCTION   ============================================
#============================================================================================

def project_with_camera_orbit(voxel, cam_angle_deg, cam_distance, focal, background):
    """Project 3D voxel using camera orbit system with background"""
    row, col, length, _ = voxel.shape
    
    # Resize background to match screen size
    bg_resized = background.resize((col, row), Image.LANCZOS)
    screen = np.array(bg_resized, dtype=np.uint8)
    
    # Player center (stationary)
    player_cx = col // 2
    player_cy = row // 2
    player_cz = length // 2
    
    # Camera position (orbits around player)
    angle_rad = np.radians(cam_angle_deg)
    
    depth_buffer = np.full((row, col), np.inf)
    
    # Render each voxel
    for i in range(row):
        for j in range(col):
            for k in range(length):
                if voxel[i,j,k,0] + voxel[i,j,k,1] + voxel[i,j,k,2] > threshold:
                    # Vector from player center to voxel
                    dx = j - player_cx
                    dy = i - player_cy
                    dz = k - player_cz
                    
                    # Rotate to camera's coordinate system
                    dx_cam = dx * np.cos(-angle_rad) - dz * np.sin(-angle_rad)
                    dz_cam = dx * np.sin(-angle_rad) + dz * np.cos(-angle_rad)
                    dy_cam = dy
                    
                    # Add camera offset
                    dz_cam = dz_cam + cam_distance
                    
                    # Project if in front of camera
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
#=======================   RENDER ALL FRAMES WITH 2 CAMERAS   ===============================
#============================================================================================

print("Rendering kick animation with 2 cameras + background...")
print(f"Background: {nama_file_latar}.png")
print(f"Camera 1: {cam1_angle}° (front), distance={cam1_distance}")
print(f"Camera 2: {cam2_angle}° (back), distance={cam2_distance}")

for frame in range(num_frames):
    print(f"Frame {frame+1}/{num_frames}")
    
    # Load frame
    voxel_frame = np.load(f"{nama_file}_frame_{frame:03d}.npy")
    
    # Camera 1: 45° front
    screen1 = project_with_camera_orbit(voxel_frame, cam1_angle, cam1_distance, focal_length, latar_pil)
    output1 = f"{nama_file}Lapangan_edit_cam1_{frame:03d}.jpg"
    plt.imsave(output1, screen1)
    
    # Camera 2: 180° back
    screen2 = project_with_camera_orbit(voxel_frame, cam2_angle, cam2_distance, focal_length, latar_pil)
    output2 = f"{nama_file}Lapangan_edit_cam2_{frame:03d}.jpg"
    plt.imsave(output2, screen2)

print("\nDone!")
print(f"Output: {nama_file}Lapangan_edit_cam1_000.jpg to {nama_file}_bg_cam1_019.jpg")
print(f"Output: {nama_file}Lapangan_edit_cam2_000.jpg to {nama_file}_bg_cam2_019.jpg")

plt.figure(1)
plt.imshow(screen1)
plt.title('Camera 1 + Background')
plt.figure(2)
plt.imshow(screen2)
plt.title('Camera 2 + Background')
plt.show()
