print("\033c")
import numpy as np
from matplotlib import pyplot as plt

nama_file = "soccer_ball"
threshold = 15
num_frames = 36
cam_distance = 300

# Load model
print("Loading soccer ball...")
voxel = np.load(nama_file + ".npy")
row, col, length = voxel.shape[0], voxel.shape[1], voxel.shape[2]

ball_cx = col // 2
ball_cy = row // 2
ball_cz = length // 2

print(f"Model: {row}x{col}x{length}, Ball center: ({ball_cx}, {ball_cy}, {ball_cz})")

screen = np.zeros(shape=(row, col, 3), dtype=np.uint8)

for frame in range(num_frames):
    screen[:, :, :] = 0
    
    angle_deg = (frame / num_frames) * 360
    angle_rad = np.radians(angle_deg)
    
    # Camera orbits around ball
    cam_x = ball_cx + cam_distance * np.sin(angle_rad)
    cam_z = ball_cz + cam_distance * np.cos(angle_rad)
    cam_y = ball_cy
    
    print(f"\nFrame {frame+1}/{num_frames}: Angle = {angle_deg:.1f}°")
    
    depth_buffer = np.full((row, col), np.inf)
    
    for i in range(row):
        for j in range(col):
            for k in range(length):
                if voxel[i,j,k,0] + voxel[i,j,k,1] + voxel[i,j,k,2] > threshold:
                    # Vector from voxel to camera
                    dx = j - ball_cx
                    dy = i - ball_cy
                    dz = k - ball_cz
                    
                    # Rotate voxel position to camera's local coordinate system
                    dx_cam = dx * np.cos(-angle_rad) - dz * np.sin(-angle_rad)
                    dz_cam = dx * np.sin(-angle_rad) + dz * np.cos(-angle_rad)
                    dy_cam = dy
                    
                    # Add camera offset (camera is at distance from center)
                    dz_cam = dz_cam + cam_distance
                    
                    # Render if in front of camera
                    if dz_cam > 50:
                        focal = 200
                        scale = focal / dz_cam
                        
                        sx = int(col/2 - dx_cam * scale)
                        sy = int(row/2 + dy_cam * scale)
                        
                        if 0 <= sx < col and 0 <= sy < row:
                            if dz_cam < depth_buffer[sy, sx]:
                                depth_buffer[sy, sx] = dz_cam
                                screen[sy, sx, :] = voxel[i,j,k,:]
    
    output = f"{nama_file}_orbit_{frame:03d}.jpg"
    plt.imsave(output, screen)
    print(f"  Saved: {output}")

print("\n✓ Done!")
plt.imshow(screen)
plt.show()
