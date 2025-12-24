print("\033c")
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    ANIMATION SETTINGS    ==========================
#=====================================================================================
nama_file = "roblox_kick"
threshold = 15

# Animation frames
num_frames = 20  # Total frames for kick animation
# Frame 0-9: Wind up (kaki kanan ke belakang, tangan kanan ke depan, tangan kiri ke belakang)
# Frame 10-19: Kick (kaki kanan ke depan, tangan kanan ke belakang, tangan kiri ke depan)

#============================================================================================
#=======================   CREATING BASE CHARACTER   ========================================
#============================================================================================
print("Creating base character...")

col, row, length = 800, 800, 800
voxel = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)

# Character parameters
yc = round(0.5*row)
xc = round(0.5*col)
zc = round(0.5*length)

# Colors
warna_kulit = [255, 220, 177]
warna_baju = [255, 255, 255]
warna_celana = [255, 255, 255]
warna_hitam = [50, 50, 50]

# Size parameters
head_size = round(0.18 * row)
leg_width = round(0.14 * row)
leg_gap = max(2, round(4 * row / 200))  # Scale with resolution
body_width = 2 * leg_width + leg_gap
body_height = body_width
body_depth = round(0.15 * row)
arm_width = round(0.12 * row)
arm_length = body_height
arm_depth = round(0.10 * row)
leg_length = round(0.24 * row)
leg_depth = round(0.12 * row)

# Base positions (standing straight)
head_top = round(0.15 * row)
head_bottom = head_top + head_size
body_top = head_bottom
body_bottom = body_top + body_height

#============================================================================================
#=======================   FUNCTION TO CREATE CHARACTER WITH POSE   =========================
#============================================================================================

def create_character_with_pose(right_leg_angle, left_leg_angle, right_arm_angle, left_arm_angle):
    """
    Create character with specific limb angles
    Angles in degrees: positive = forward, negative = backward
    """
    voxel_pose = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)
    
    # HEAD (rounded box)
    head_half = round(head_size / 2)
    corner_radius = max(2, round(4 * row / 200))  # Scale with resolution
    for i in range(head_top, head_bottom):
        for j in range(xc - head_half, xc + head_half):
            for k in range(zc - head_half, zc + head_half):
                dx = max(0, abs(j - xc) - (head_half - corner_radius))
                dy = max(0, abs(i - (head_top + head_half)) - (head_half - corner_radius))
                dz = max(0, abs(k - zc) - (head_half - corner_radius))
                distance = np.sqrt(dx**2 + dy**2 + dz**2)
                if distance <= corner_radius:
                    voxel_pose[i, j, k, :] = warna_kulit[:]
    
    # BODY (rounded box)
    body_corner_radius = max(1, round(2 * row / 200))  # Scale with resolution
    body_half_width = round(body_width / 2)
    body_half_height = round(body_height / 2)
    body_half_depth = round(body_depth / 2)
    body_center_y = body_top + body_half_height
    
    for i in range(body_top, body_bottom):
        for j in range(xc - body_half_width, xc + body_half_width):
            for k in range(zc - body_half_depth, zc + body_half_depth):
                dx = max(0, abs(j - xc) - (body_half_width - body_corner_radius))
                dy = max(0, abs(i - body_center_y) - (body_half_height - body_corner_radius))
                dz = max(0, abs(k - zc) - (body_half_depth - body_corner_radius))
                distance = np.sqrt(dx**2 + dy**2 + dz**2)
                if distance <= body_corner_radius:
                    voxel_pose[i, j, k, :] = warna_baju[:]
    
    # ARMS and LEGS with rotation
    # (Simplified - create as boxes and rotate)
    
    # Right Leg - rotated with proper orientation (KANAN dari sudut pandang Roblox)
    right_leg_rad = np.radians(right_leg_angle)
    leg_pivot_y = body_bottom
    leg_pivot_x = xc + leg_width//2 + leg_gap//2  # KANAN (positive X)
    leg_pivot_z = zc
    
    cos_leg = np.cos(right_leg_rad)
    sin_leg = np.sin(right_leg_rad)
    
    for dx in range(-leg_width//2, leg_width//2):
        for dy in range(leg_length):
            for dz in range(-leg_depth//2, leg_depth//2):
                # Rotate the entire leg segment (BALIK ARAH: positive angle = ke belakang)
                y_rot = dy * cos_leg + dz * sin_leg
                z_rot = -dy * sin_leg + dz * cos_leg
                
                y_pos = leg_pivot_y + int(y_rot)
                z_pos = leg_pivot_z + int(z_rot)
                x_pos = leg_pivot_x + dx
                
                if 0 <= y_pos < row and 0 <= z_pos < length and 0 <= x_pos < col:
                    voxel_pose[y_pos, x_pos, z_pos, :] = warna_celana[:]
    
    # Left Leg - rotated with proper orientation (KIRI dari sudut pandang Roblox)
    left_leg_rad = np.radians(left_leg_angle)
    leg_pivot_x = xc - leg_width//2 - leg_gap//2  # KIRI (negative X)
    
    cos_leg = np.cos(left_leg_rad)
    sin_leg = np.sin(left_leg_rad)
    
    for dx in range(-leg_width//2, leg_width//2):
        for dy in range(leg_length):
            for dz in range(-leg_depth//2, leg_depth//2):
                # Rotate the entire leg segment (BALIK ARAH: positive angle = ke belakang)
                y_rot = dy * cos_leg + dz * sin_leg
                z_rot = -dy * sin_leg + dz * cos_leg
                
                y_pos = leg_pivot_y + int(y_rot)
                z_pos = leg_pivot_z + int(z_rot)
                x_pos = leg_pivot_x + dx
                
                if 0 <= y_pos < row and 0 <= z_pos < length and 0 <= x_pos < col:
                    voxel_pose[y_pos, x_pos, z_pos, :] = warna_celana[:]
    
    # Right Arm - rotated with proper orientation (kembalikan ke posisi asli)
    right_arm_rad = np.radians(right_arm_angle)
    arm_pivot_y = body_top
    arm_pivot_x = xc - body_width//2 - arm_width//2  # Posisi asli
    arm_pivot_z = zc
    
    sleeve_len = round(arm_length * 0.40)
    black_len = round(sleeve_len * 0.20)
    
    cos_arm = np.cos(right_arm_rad)
    sin_arm = np.sin(right_arm_rad)
    
    for dx in range(-arm_width//2, arm_width//2):
        for dy in range(arm_length):
            for dz in range(-arm_depth//2, arm_depth//2):
                # Rotate the entire arm segment
                y_rot = dy * cos_arm - dz * sin_arm
                z_rot = dy * sin_arm + dz * cos_arm
                
                y_pos = arm_pivot_y + int(y_rot)
                z_pos = arm_pivot_z + int(z_rot)
                x_pos = arm_pivot_x + dx
                
                if 0 <= y_pos < row and 0 <= z_pos < length and 0 <= x_pos < col:
                    if dy < sleeve_len - black_len:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_baju[:]
                    elif dy < sleeve_len:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_hitam[:]
                    else:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_kulit[:]
    
    # Left Arm - rotated with proper orientation (kembalikan ke posisi asli)
    left_arm_rad = np.radians(left_arm_angle)
    arm_pivot_x = xc + body_width//2 + arm_width//2  # Posisi asli
    
    cos_arm = np.cos(left_arm_rad)
    sin_arm = np.sin(left_arm_rad)
    
    for dx in range(-arm_width//2, arm_width//2):
        for dy in range(arm_length):
            for dz in range(-arm_depth//2, arm_depth//2):
                # Rotate the entire arm segment
                y_rot = dy * cos_arm - dz * sin_arm
                z_rot = dy * sin_arm + dz * cos_arm
                
                y_pos = arm_pivot_y + int(y_rot)
                z_pos = arm_pivot_z + int(z_rot)
                x_pos = arm_pivot_x + dx
                
                if 0 <= y_pos < row and 0 <= z_pos < length and 0 <= x_pos < col:
                    if dy < sleeve_len - black_len:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_baju[:]
                    elif dy < sleeve_len:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_hitam[:]
                    else:
                        voxel_pose[y_pos, x_pos, z_pos, :] = warna_kulit[:]
    
    # Scale factor for text/face (relative to 200 resolution)
    scale = row / 200
    text_depth = max(2, round(row / 100))
    
    # ADD FACE (eyes and smile) on FRONT of head
    face_z_start = zc - head_half
    face_z_end = face_z_start + text_depth
    
    # Eyes - SCALED (bigger eyes)
    eye_width = max(3, round(6 * scale))
    eye_height = max(5, round(10 * scale))
    eye_spacing = round(head_size * 0.20)
    eye_y_start = head_top + round(head_size * 0.28)
    eye_y_end = eye_y_start + eye_height
    
    # Left eye
    left_eye_x_start = xc - eye_spacing - eye_width//2
    left_eye_x_end = xc - eye_spacing + eye_width//2
    voxel_pose[eye_y_start:eye_y_end, left_eye_x_start:left_eye_x_end, face_z_start:face_z_end, :] = warna_hitam[:]
    
    # Right eye
    right_eye_x_start = xc + eye_spacing - eye_width//2
    right_eye_x_end = xc + eye_spacing + eye_width//2
    voxel_pose[eye_y_start:eye_y_end, right_eye_x_start:right_eye_x_end, face_z_start:face_z_end, :] = warna_hitam[:]
    
    # Smile - SCALED (shorter width)
    smile_y_start = head_top + round(head_size * 0.65)
    smile_width = round(head_size * 0.25)  # Reduced from 0.40 to 0.25
    smile_thickness = max(2, round(3 * scale))
    smile_curve = max(2, round(4 * scale))
    
    for j in range(xc - smile_width, xc + smile_width + 1):
        x_norm = (j - xc) / smile_width
        if abs(x_norm) <= 1:
            y_offset = int(smile_curve * (1 - x_norm**2))
            smile_y = smile_y_start + y_offset
            if smile_y < head_bottom - 2:
                voxel_pose[smile_y:smile_y+smile_thickness, j, face_z_start:face_z_end, :] = warna_hitam[:]
    
    # ADD TEXT "TEAM 2" on BACK of body
    body_half_depth = round(body_depth / 2)
    back_z = zc + body_half_depth - 2
    
    # "TEAM" text - SCALED
    team_y_start = body_top + round(body_height * 0.10)
    letter_height = round(7 * scale)
    letter_stroke = max(1, round(1 * scale))
    team_total_width = round(21 * scale)
    team_x_start = xc - round(team_total_width / 2)
    
    # Letter T
    t_width = round(5 * scale)
    voxel_pose[team_y_start:team_y_start+letter_stroke, team_x_start:team_x_start+t_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start:team_y_start+letter_height, team_x_start+round(2*scale):team_x_start+round(3*scale), back_z:back_z+text_depth, :] = warna_hitam[:]
    
    # Letter E
    e_start = team_x_start + round(6 * scale)
    e_width = round(4 * scale)
    voxel_pose[team_y_start:team_y_start+letter_height, e_start:e_start+letter_stroke, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start:team_y_start+letter_stroke, e_start:e_start+e_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start+round(3*scale):team_y_start+round(4*scale), e_start:e_start+round(3*scale), back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start+letter_height-letter_stroke:team_y_start+letter_height, e_start:e_start+e_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    
    # Letter A
    a_start = team_x_start + round(11 * scale)
    a_width = round(4 * scale)
    voxel_pose[team_y_start+letter_stroke:team_y_start+letter_height, a_start:a_start+letter_stroke, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start+letter_stroke:team_y_start+letter_height, a_start+a_width-letter_stroke:a_start+a_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start:team_y_start+letter_stroke, a_start+letter_stroke:a_start+a_width-letter_stroke, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start+round(3*scale):team_y_start+round(4*scale), a_start:a_start+a_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    
    # Letter M
    m_start = team_x_start + round(16 * scale)
    m_width = round(5 * scale)
    voxel_pose[team_y_start:team_y_start+letter_height, m_start:m_start+letter_stroke, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start:team_y_start+letter_height, m_start+m_width-letter_stroke:m_start+m_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[team_y_start+letter_stroke:team_y_start+round(4*scale), m_start+round(2*scale):m_start+round(3*scale), back_z:back_z+text_depth, :] = warna_hitam[:]
    
    # Big "2" at center back - SCALED
    num_height = round(16 * scale)
    num_width = round(14 * scale)
    num_y_start = body_top + round(body_height / 2) - round(num_height / 2)
    num_x_start = xc - round(num_width / 2)
    stroke_width = max(2, round(3 * scale))
    
    voxel_pose[num_y_start:num_y_start+stroke_width, num_x_start:num_x_start+num_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[num_y_start:num_y_start+round(7*scale), num_x_start+num_width-stroke_width:num_x_start+num_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[num_y_start+round(6*scale):num_y_start+round(9*scale), num_x_start:num_x_start+num_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[num_y_start+round(8*scale):num_y_start+num_height, num_x_start:num_x_start+stroke_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    voxel_pose[num_y_start+num_height-stroke_width:num_y_start+num_height, num_x_start:num_x_start+num_width, back_z:back_z+text_depth, :] = warna_hitam[:]
    
    # Small "2" on FRONT right - SCALED (MIRRORED for correct projection view)
    front_z = zc - body_half_depth
    small_num_height = round(7 * scale)
    small_num_width = round(5 * scale)
    small_num_y_start = body_top + round(body_height * 0.15)
    small_num_x_start = xc - round(body_width/2) + round(8 * scale)  # Mirrored position (left side)
    stroke = max(1, round(1 * scale))
    small_mid = round(3 * scale)
    
    # Mirrored "2": left stroke at top-right, right stroke at bottom-left
    voxel_pose[small_num_y_start:small_num_y_start+stroke, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+text_depth, :] = warna_hitam[:]  # Top
    voxel_pose[small_num_y_start:small_num_y_start+small_mid, small_num_x_start:small_num_x_start+stroke, front_z:front_z+text_depth, :] = warna_hitam[:]  # Left top (mirrored)
    voxel_pose[small_num_y_start+small_mid:small_num_y_start+small_mid+stroke, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+text_depth, :] = warna_hitam[:]  # Middle
    voxel_pose[small_num_y_start+small_mid:small_num_y_start+small_num_height, small_num_x_start+small_num_width-stroke:small_num_x_start+small_num_width, front_z:front_z+text_depth, :] = warna_hitam[:]  # Right bottom (mirrored)
    voxel_pose[small_num_y_start+small_num_height-stroke:small_num_y_start+small_num_height, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+text_depth, :] = warna_hitam[:]  # Bottom
    
    return voxel_pose

#============================================================================================
#=======================   CREATE ANIMATION FRAMES   ========================================
#============================================================================================

print("Creating kick animation frames...")

for frame in range(num_frames):
    print(f"Creating frame {frame+1}/{num_frames}")
    
    if frame < 10:
        # Wind up phase
        t = frame / 9  # 0 to 1
        right_leg_angle = -50 * t  # Kaki kanan ke belakang (negative)
        left_leg_angle = 0
        right_arm_angle = 45 * t  # Tangan kanan ke depan (positive)
        left_arm_angle = -45 * t  # Tangan kiri ke belakang (negative)
    else:
        # Kick phase
        t = (frame - 10) / 9  # 0 to 1
        right_leg_angle = -50 + 100 * t  # Kaki kanan dari belakang ke depan
        left_leg_angle = 0
        right_arm_angle = 45 - 90 * t  # Tangan kanan dari depan ke belakang
        left_arm_angle = -45 + 90 * t  # Tangan kiri dari belakang ke depan
    
    # Create character with this pose
    voxel_frame = create_character_with_pose(right_leg_angle, left_leg_angle, right_arm_angle, left_arm_angle)
    
    # Save frame
    np.save(f"{nama_file}_frame_{frame:03d}.npy", voxel_frame)
    
    # Visualize
    if frame % 5 == 0:
        slice_img = voxel_frame[:, :, zc, :]
        plt.figure(frame//5 + 1)
        plt.title(f'Frame {frame}: RL={right_leg_angle:.0f}° RA={right_arm_angle:.0f}°')
        plt.imshow(slice_img)

plt.show()
print(f"\n✓ Created {num_frames} animation frames!")
print("Next: Run projection script to render these frames")
