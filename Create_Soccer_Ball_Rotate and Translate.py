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
ball_radius = round(0.20 * row)

# Colors
warna_putih = [255, 255, 255]
warna_hitam = [30, 30, 30]

print("Creating soccer ball...")

#============================================================================================
#=======================   CREATE SOCCER BALL WITH PENTAGONS   ==============================
#============================================================================================

phi = (1 + np.sqrt(5)) / 2

pentagon_centers = [
    (0, phi, 1, 0),
    (0, -phi, -1, 36),
    (0, phi, -1, 0),
    (0, -phi, 1, 36),
    (1, 0, phi, 36),
    (-1, 0, -phi, 0),
    (-1, 0, phi, 0),
    (1, 0, -phi, 36),
    (phi, 1, 0, 0),
    (-phi, -1, 0, 36),
    (phi, -1, 0, 0),
    (-phi, 1, 0, 36),
]

for y in range(row):
    for x in range(col):
        for z in range(length):
            dx = x - xc
            dy = y - yc
            dz = z - zc
            dist_sq = dx**2 + dy**2 + dz**2
            
            if dist_sq <= ball_radius**2:
                voxel[y, x, z, :] = warna_putih[:]
                
                dist = np.sqrt(dist_sq)
                if dist > ball_radius * 0.85:
                    if dist > 0:
                        nx = dx / dist
                        ny = dy / dist
                        nz = dz / dist
                        
                        pentagon_dots = []
                        
                        for pc in pentagon_centers:
                            pcx_raw, pcy_raw, pcz_raw, rotation_offset = pc[0], pc[1], pc[2], pc[3]
                            
                            pc_len = np.sqrt(pcx_raw**2 + pcy_raw**2 + pcz_raw**2)
                            if pc_len > 0:
                                pcx = pcx_raw / pc_len
                                pcy = pcy_raw / pc_len
                                pcz = pcz_raw / pc_len
                                
                                dot = nx * pcx + ny * pcy + nz * pcz
                                pentagon_dots.append((dot, pcx, pcy, pcz, rotation_offset))
                                
                                if dot > 0.85:
                                    if abs(pcx) < 0.9:
                                        temp_x, temp_y, temp_z = 1, 0, 0
                                    else:
                                        temp_x, temp_y, temp_z = 0, 1, 0
                                    
                                    dot_temp = temp_x*pcx + temp_y*pcy + temp_z*pcz
                                    perp_x = temp_x - dot_temp*pcx
                                    perp_y = temp_y - dot_temp*pcy
                                    perp_z = temp_z - dot_temp*pcz
                                    
                                    perp_len = np.sqrt(perp_x**2 + perp_y**2 + perp_z**2)
                                    if perp_len > 0:
                                        perp_x /= perp_len
                                        perp_y /= perp_len
                                        perp_z /= perp_len
                                        
                                        perp2_x = pcy*perp_z - pcz*perp_y
                                        perp2_y = pcz*perp_x - pcx*perp_z
                                        perp2_z = pcx*perp_y - pcy*perp_x
                                        
                                        proj_x = nx - pcx*dot
                                        proj_y = ny - pcy*dot
                                        proj_z = nz - pcz*dot
                                        
                                        local_x = proj_x*perp_x + proj_y*perp_y + proj_z*perp_z
                                        local_y = proj_x*perp2_x + proj_y*perp2_y + proj_z*perp2_z
                                        
                                        pentagon_radius = 0.40
                                        vertices = []
                                        for i in range(5):
                                            v_angle = np.radians(i * 72 + rotation_offset)
                                            vx = pentagon_radius * np.cos(v_angle)
                                            vy = pentagon_radius * np.sin(v_angle)
                                            vertices.append((vx, vy))
                                        
                                        inside = True
                                        
                                        for i in range(5):
                                            v1 = vertices[i]
                                            v2 = vertices[(i + 1) % 5]
                                            
                                            edge_x = v2[0] - v1[0]
                                            edge_y = v2[1] - v1[1]
                                            
                                            to_point_x = local_x - v1[0]
                                            to_point_y = local_y - v1[1]
                                            
                                            cross = edge_x * to_point_y - edge_y * to_point_x
                                            
                                            if cross < -0.001:
                                                inside = False
                                                break
                                        
                                        if inside:
                                            voxel[y, x, z, :] = warna_hitam[:]
                                            break
                        
                        if voxel[y, x, z, 0] == 255:
                            pentagon_dots.sort(key=lambda x: x[0], reverse=True)
                            
                            if len(pentagon_dots) >= 3:
                                sum_top3 = sum(p[0] for p in pentagon_dots[:3])
                                
                                if sum_top3 > 2.22 and sum_top3 < 2.24:
                                    voxel[y, x, z, :] = [180, 180, 180]

print("Soccer ball created!")

#============================================================================================
#=======================   VISUALIZE   ======================================================
#============================================================================================

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

np.save(f"{nama_file}.npy", voxel)
print(f"Saved: {nama_file}.npy")
