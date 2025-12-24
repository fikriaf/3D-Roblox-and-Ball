print("\033c")
import numpy as np
from matplotlib import pyplot as plt

nama_file = "roblox_character"
nama_file_latar = "Lapangan_edit-with-ball"
threshold = 15
num_frames = 36

# Base values for 200 resolution
BASE_RESOLUTION = 200
BASE_CAM_DISTANCE = 350
BASE_FOCAL = 200

# Load model
print("Loading model...")
voxel = np.load(nama_file + "_0_0_.npy")
row, col, length = voxel.shape[0], voxel.shape[1], voxel.shape[2]

# Scale camera parameters based on resolution
scale = row / BASE_RESOLUTION
cam_distance = round(BASE_CAM_DISTANCE * scale)
focal = round(BASE_FOCAL * scale)

print(f"Resolution: {row} (scale: {scale}x)")
print(f"Camera distance: {cam_distance}, Focal: {focal}")

# Load background image
print("Loading background...")
from PIL import Image
latar_pil = Image.open(nama_file_latar + ".png")
latar_pil = latar_pil.convert("RGB")  # Ensure RGB format
latar_pil = latar_pil.resize((col, row), Image.LANCZOS)
latar_gambar = np.array(latar_pil, dtype=np.uint8)

print(f"Background size: {latar_gambar.shape}")

player_cx = col // 2
player_cy = row // 2
player_cz = length // 2

print(f"Model: {row}x{col}x{length}, Player center: ({player_cx}, {player_cy}, {player_cz})")

for frame in range(num_frames):
    # Start with background image
    screen = latar_gambar.copy()
    
    angle_deg = (frame / num_frames) * 360
    angle_rad = np.radians(angle_deg)
    
    # Camera orbits around player
    cam_x = player_cx + cam_distance * np.sin(angle_rad)
    cam_z = player_cz + cam_distance * np.cos(angle_rad)
    cam_y = player_cy
    
    print(f"\nFrame {frame+1}/{num_frames}: Angle = {angle_deg:.1f}°")
    
    depth_buffer = np.full((row, col), np.inf)
    
    for i in range(row):
        for j in range(col):
            for k in range(length):
                if voxel[i,j,k,0] + voxel[i,j,k,1] + voxel[i,j,k,2] > threshold:
                    # Vector from voxel to camera
                    dx = j - player_cx
                    dy = i - player_cy
                    dz = k - player_cz
                    
                    # Rotate voxel position to camera's local coordinate system
                    dx_cam = dx * np.cos(-angle_rad) - dz * np.sin(-angle_rad)
                    dz_cam = dx * np.sin(-angle_rad) + dz * np.cos(-angle_rad)
                    dy_cam = dy
                    
                    # Add camera offset
                    dz_cam = dz_cam + cam_distance
                    
                    # Render if in front of camera
                    if dz_cam > 50:
                        proj_scale = focal / dz_cam
                        
                        sx = int(col/2 - dx_cam * proj_scale)
                        sy = int(row/2 + dy_cam * proj_scale)
                        
                        if 0 <= sx < col and 0 <= sy < row:
                            if dz_cam < depth_buffer[sy, sx]:
                                depth_buffer[sy, sx] = dz_cam
                                screen[sy, sx, :] = voxel[i,j,k,:]
    
    output = f"{nama_file}_Lapangan_edit-with-ball_orbit_{frame:03d}.jpg"
    plt.imsave(output, screen)
    print(f"  Saved: {output}")

print("\nDone!")
plt.imshow(screen)
plt.show()
