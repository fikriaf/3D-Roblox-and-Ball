print("\033c")
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    SETTINGS    ====================================
#=====================================================================================
nama_file = "roblox_kick"
num_frames = 20
threshold = 15

# Camera angles (fixed)
cam1_angle = 45   # 45° di depan (wajah terlihat)
cam2_angle = 180  # Lurus di belakang (tulisan TEAM 2 terlihat)

# Base values for 200 resolution
BASE_RESOLUTION = 200
BASE_CAM1_DISTANCE = 250
BASE_CAM2_DISTANCE = 350
BASE_FOCAL_LENGTH = 200

#============================================================================================
#=======================   PROJECTION FUNCTION   ============================================
#============================================================================================

def project_with_camera_orbit(voxel, cam_angle_deg, cam_distance, focal):
    """Project 3D voxel using camera orbit system"""
    row, col, length, _ = voxel.shape
    
    # Player center (stationary)
    player_cx = col // 2
    player_cy = row // 2
    player_cz = length // 2
    
    # Camera position (orbits around player)
    angle_rad = np.radians(cam_angle_deg)
    cam_x = player_cx + cam_distance * np.sin(angle_rad)
    cam_z = player_cz + cam_distance * np.cos(angle_rad)
    cam_y = player_cy
    
    # Create screen - BLACK background
    screen = np.zeros((row, col, 3), dtype=np.uint8)
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

# Load first frame to get resolution
first_frame = np.load(f"{nama_file}_frame_000.npy")
voxel_resolution = first_frame.shape[0]
res_scale = voxel_resolution / BASE_RESOLUTION

# Scale camera parameters based on resolution
cam1_distance = round(BASE_CAM1_DISTANCE * res_scale)
cam2_distance = round(BASE_CAM2_DISTANCE * res_scale)
focal_length = round(BASE_FOCAL_LENGTH * res_scale)

print("Rendering kick animation with 2 cameras...")
print(f"Voxel resolution: {voxel_resolution} (scale: {res_scale}x)")
print(f"Camera 1: {cam1_angle}° (front), distance={cam1_distance}, focal={focal_length}")
print(f"Camera 2: {cam2_angle}° (back), distance={cam2_distance}, focal={focal_length}")

for frame in range(num_frames):
    print(f"Frame {frame+1}/{num_frames}")
    
    # Load frame
    voxel_frame = np.load(f"{nama_file}_frame_{frame:03d}.npy")
    
    # Camera 1: 45° front, zoom in
    screen1 = project_with_camera_orbit(voxel_frame, cam1_angle, cam1_distance, focal_length)
    output1 = f"{nama_file}_cam1_{frame:03d}.jpg"
    plt.imsave(output1, screen1)
    
    # Camera 2: 180° back, normal
    screen2 = project_with_camera_orbit(voxel_frame, cam2_angle, cam2_distance, focal_length)
    output2 = f"{nama_file}_cam2_{frame:03d}.jpg"
    plt.imsave(output2, screen2)

print("\n✓ Animation rendered successfully!")
print(f"Created {num_frames} frames for each camera")
print("Camera 1: roblox_kick_cam1_000.jpg to roblox_kick_cam1_019.jpg")
print("Camera 2: roblox_kick_cam2_000.jpg to roblox_kick_cam2_019.jpg")

plt.figure(1)
plt.imshow(screen1)
plt.title('Camera 1: Last Frame')
plt.figure(2)
plt.imshow(screen2)
plt.title('Camera 2: Last Frame')
plt.show()
