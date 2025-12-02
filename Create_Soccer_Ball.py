print("\033c")
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    SETTINGS    ====================================
#=====================================================================================
nama_file = "soccer_ball"
threshold = 15

col, row, length = 200, 200, 200
voxel = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)

# Ball parameters
yc = round(0.5*row)
xc = round(0.5*col)
zc = round(0.5*length)
ball_radius = round(0.20 * row)  # Radius bola

# Colors
warna_putih = [255, 255, 255]
warna_hitam = [30, 30, 30]

print("Creating soccer ball...")

#============================================================================================
#=======================   CREATE SOCCER BALL WITH PENTAGONS   ==============================
#============================================================================================

# Pentagon positions with rotation offsets
# Based on icosahedron vertices - classic soccer ball pattern
phi = (1 + np.sqrt(5)) / 2  # Golden ratio
# Format: (x, y, z, rotation_offset_degrees)
pentagon_centers = [
    # Pair 1: Top-Bottom (Y-axis) - rotasi berbeda untuk yang berhadapan
    (0, phi, 1, 0),       # Atas depan - 0°
    (0, -phi, -1, 36),    # Bawah belakang - 36° (berhadapan dengan atas depan)
    
    # Pair 2: Top-Bottom (Y-axis, rotated) - rotasi berbeda untuk yang berhadapan
    (0, phi, -1, 0),      # Atas belakang - 0°
    (0, -phi, 1, 36),     # Bawah depan - 36° (berhadapan dengan atas belakang)
    
    # Pair 3: Front-Back (Z-axis) - JANGAN UBAH (sudah benar)
    (1, 0, phi, 36),      # Depan kanan
    (-1, 0, -phi, 0),     # Belakang kiri
    
    # Pair 4: Front-Back (Z-axis, rotated) - JANGAN UBAH (sudah benar)
    (-1, 0, phi, 0),      # Depan kiri
    (1, 0, -phi, 36),     # Belakang kanan
    
    # Pair 5: Left-Right (X-axis) - rotasi berbeda untuk yang berhadapan
    (phi, 1, 0, 0),       # Kanan atas - 0°
    (-phi, -1, 0, 36),    # Kiri bawah - 36° (berhadapan dengan kanan atas)
    
    # Pair 6: Left-Right (X-axis, rotated) - rotasi berbeda untuk yang berhadapan
    (phi, -1, 0, 0),      # Kanan bawah - 0°
    (-phi, 1, 0, 36),     # Kiri atas - 36° (berhadapan dengan kanan bawah)
]

# Create ball with pentagons in one pass
for y in range(row):
    for x in range(col):
        for z in range(length):
            dx = x - xc
            dy = y - yc
            dz = z - zc
            dist_sq = dx**2 + dy**2 + dz**2
            
            # Check if inside sphere
            if dist_sq <= ball_radius**2:
                # Default: white
                voxel[y, x, z, :] = warna_putih[:]
                
                # Check if near any pentagon (only if on surface)
                dist = np.sqrt(dist_sq)
                if dist > ball_radius * 0.85:  # Only check outer surface
                    # Normalize position
                    if dist > 0:
                        nx = dx / dist
                        ny = dy / dist
                        nz = dz / dist
                        
                        # Track distances to all pentagons for hexagon detection
                        pentagon_dots = []
                        
                        # Check proximity to pentagon centers
                        for pc in pentagon_centers:
                            # Extract position and rotation offset
                            pcx_raw, pcy_raw, pcz_raw, rotation_offset = pc[0], pc[1], pc[2], pc[3]
                            
                            # Normalize pentagon center
                            pc_len = np.sqrt(pcx_raw**2 + pcy_raw**2 + pcz_raw**2)
                            if pc_len > 0:
                                pcx = pcx_raw / pc_len
                                pcy = pcy_raw / pc_len
                                pcz = pcz_raw / pc_len
                                
                                # Dot product (cosine similarity)
                                dot = nx * pcx + ny * pcy + nz * pcz
                                pentagon_dots.append((dot, pcx, pcy, pcz, rotation_offset))
                                
                                # If close to pentagon center (threshold lebih ketat untuk sudut lancip)
                                if dot > 0.85:
                                    # Create local coordinate system to check pentagon shape
                                    # Find perpendicular vector
                                    if abs(pcx) < 0.9:
                                        temp_x, temp_y, temp_z = 1, 0, 0
                                    else:
                                        temp_x, temp_y, temp_z = 0, 1, 0
                                    
                                    # Make it perpendicular: temp = temp - (temp·pc)*pc
                                    dot_temp = temp_x*pcx + temp_y*pcy + temp_z*pcz
                                    perp_x = temp_x - dot_temp*pcx
                                    perp_y = temp_y - dot_temp*pcy
                                    perp_z = temp_z - dot_temp*pcz
                                    
                                    # Normalize
                                    perp_len = np.sqrt(perp_x**2 + perp_y**2 + perp_z**2)
                                    if perp_len > 0:
                                        perp_x /= perp_len
                                        perp_y /= perp_len
                                        perp_z /= perp_len
                                        
                                        # Second perpendicular (cross product: pc × perp)
                                        perp2_x = pcy*perp_z - pcz*perp_y
                                        perp2_y = pcz*perp_x - pcx*perp_z
                                        perp2_z = pcx*perp_y - pcy*perp_x
                                        
                                        # Project point to local plane
                                        proj_x = nx - pcx*dot
                                        proj_y = ny - pcy*dot
                                        proj_z = nz - pcz*dot
                                        
                                        # Get 2D local coordinates
                                        local_x = proj_x*perp_x + proj_y*perp_y + proj_z*perp_z
                                        local_y = proj_x*perp2_x + proj_y*perp2_y + proj_z*perp2_z
                                        
                                        # Calculate angle with rotation offset
                                        angle_rad = np.arctan2(local_y, local_x)
                                        angle_deg = (np.degrees(angle_rad) + rotation_offset) % 360
                                        
                                        # Pentagon: check if inside pentagon with STRAIGHT sides
                                        # Create 5 vertices of pentagon (radius diperbesar)
                                        pentagon_radius = 0.40
                                        vertices = []
                                        for i in range(5):
                                            v_angle = np.radians(i * 72 + rotation_offset)
                                            vx = pentagon_radius * np.cos(v_angle)
                                            vy = pentagon_radius * np.sin(v_angle)
                                            vertices.append((vx, vy))
                                        
                                        # Check if point (local_x, local_y) is inside pentagon
                                        # Using strict edge detection for sharp corners
                                        inside = True
                                        min_distance_to_edge = float('inf')
                                        
                                        for i in range(5):
                                            v1 = vertices[i]
                                            v2 = vertices[(i + 1) % 5]
                                            
                                            # Vector from v1 to v2 (edge)
                                            edge_x = v2[0] - v1[0]
                                            edge_y = v2[1] - v1[1]
                                            
                                            # Vector from v1 to point
                                            to_point_x = local_x - v1[0]
                                            to_point_y = local_y - v1[1]
                                            
                                            # Cross product (perpendicular distance to line)
                                            cross = edge_x * to_point_y - edge_y * to_point_x
                                            
                                            # Hitung jarak ke edge untuk memastikan sudut lancip
                                            edge_length = np.sqrt(edge_x**2 + edge_y**2)
                                            if edge_length > 0:
                                                distance_to_edge = abs(cross) / edge_length
                                                min_distance_to_edge = min(min_distance_to_edge, distance_to_edge)
                                            
                                            # Point harus di sisi dalam dari semua edge
                                            if cross < -0.001:  # Toleransi sangat kecil untuk sudut tajam
                                                inside = False
                                                break
                                        
                                        if inside:
                                            voxel[y, x, z, :] = warna_hitam[:]
                                            break
                        
                        # Check if in hexagon area (close to 3 pentagons)
                        if voxel[y, x, z, 0] == 255:  # Still white
                            # Sort by distance (closest first)
                            pentagon_dots.sort(key=lambda x: x[0], reverse=True)
                            
                            # Hexagon: area that's moderately close to 3 pentagons
                            if len(pentagon_dots) >= 3:
                                # Sum of 3 closest - hexagon is where 3 pentagons are equidistant
                                sum_top3 = sum(p[0] for p in pentagon_dots[:3])
                                
                                # Hexagon area: sum is high but not too high (not at pentagon)
                                if sum_top3 > 2.22 and sum_top3 < 2.24:
                                    voxel[y, x, z, :] = [180, 180, 180]  # Abu-abu untuk hexagon

print("Soccer ball created!")

#============================================================================================
#=======================   VISUALIZE   ======================================================
#============================================================================================

# Show different views
plt.figure(1)
plt.title('Front View (Z slice)')
plt.imshow(voxel[:, :, zc, :])

plt.figure(2)
plt.title('Side View (X slice)')
plt.imshow(voxel[:, xc, :, :])

plt.figure(3)
plt.title('Top View (Y slice)')
plt.imshow(voxel[yc, :, :, :])

plt.show()

# Save
np.save(f"{nama_file}.npy", voxel)
print(f"Saved: {nama_file}.npy")
