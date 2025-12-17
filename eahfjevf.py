print("\033c")
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    SETTINGS    ====================================
#=====================================================================================
nama_file = "soccer_ball"
threshold = 15

# Membuat ruang 3D (voxel) dengan ukuran 200x200x200 pixel
# Format: (row, col, depth, channel) dimana channel = RGB (3)
col, row, length = 200, 200, 200
voxel = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)

# Titik pusat bola di tengah ruang 3D
yc = round(0.5*row)    # Pusat Y = 100
xc = round(0.5*col)    # Pusat X = 100
zc = round(0.5*length) # Pusat Z = 100
ball_radius = round(0.20 * row)  # Radius bola = 40 pixel

# Warna untuk bola
warna_putih = [255, 255, 255]  # Warna dasar bola
warna_hitam = [30, 30, 30]     # Warna pentagon

print("Creating soccer ball...")

#============================================================================================
#=======================   CREATE SOCCER BALL WITH PENTAGONS   ==============================
#============================================================================================

#--------------------------------------------------------------------------------------------
# KONSEP GEOMETRI BOLA SEPAK:
# Bola sepak klasik (truncated icosahedron) memiliki:
# - 12 pentagon hitam (segi-5)
# - 20 hexagon putih (segi-6)
# 
# Pentagon ditempatkan pada 12 vertex dari icosahedron.
# Icosahedron memiliki vertex yang posisinya berdasarkan GOLDEN RATIO (phi).
#--------------------------------------------------------------------------------------------

# Golden Ratio (phi) = (1 + sqrt(5)) / 2 ≈ 1.618
# Ini adalah rasio matematika yang muncul di banyak struktur geometri alami
phi = (1 + np.sqrt(5)) / 2

#--------------------------------------------------------------------------------------------
# POSISI 12 PENTAGON:
# Berdasarkan vertex icosahedron dengan koordinat (0, ±1, ±phi), (±1, ±phi, 0), (±phi, 0, ±1)
# Format: (x, y, z, rotation_offset_degrees)
# rotation_offset digunakan untuk memutar pentagon agar sudut-sudutnya tidak saling bertabrakan
#--------------------------------------------------------------------------------------------
pentagon_centers = [
    # Pair 1-2: Pentagon di sumbu Y (atas-bawah)
    (0, phi, 1, 0),       # Atas depan
    (0, -phi, -1, 36),    # Bawah belakang (rotasi 36° agar tidak overlap)
    (0, phi, -1, 0),      # Atas belakang
    (0, -phi, 1, 36),     # Bawah depan
    
    # Pair 3-4: Pentagon di sumbu Z (depan-belakang)
    (1, 0, phi, 36),      # Depan kanan
    (-1, 0, -phi, 0),     # Belakang kiri
    (-1, 0, phi, 0),      # Depan kiri
    (1, 0, -phi, 36),     # Belakang kanan
    
    # Pair 5-6: Pentagon di sumbu X (kiri-kanan)
    (phi, 1, 0, 0),       # Kanan atas
    (-phi, -1, 0, 36),    # Kiri bawah
    (phi, -1, 0, 0),      # Kanan bawah
    (-phi, 1, 0, 36),     # Kiri atas
]

#--------------------------------------------------------------------------------------------
# ALGORITMA UTAMA: Iterasi setiap voxel dalam ruang 3D
# Untuk setiap titik (x, y, z), tentukan apakah:
# 1. Berada di dalam bola (jarak dari pusat <= radius)
# 2. Jika di permukaan, apakah masuk area pentagon hitam atau tetap putih
#--------------------------------------------------------------------------------------------
for y in range(row):
    for x in range(col):
        for z in range(length):
            # Hitung jarak dari titik (x,y,z) ke pusat bola (xc,yc,zc)
            dx = x - xc
            dy = y - yc
            dz = z - zc
            dist_sq = dx**2 + dy**2 + dz**2  # Jarak kuadrat (lebih efisien tanpa sqrt)
            
            #--------------------------------------------------------------------------------
            # CEK 1: Apakah titik berada di dalam bola?
            # Menggunakan persamaan bola: x² + y² + z² <= r²
            #--------------------------------------------------------------------------------
            if dist_sq <= ball_radius**2:
                # Default: warnai putih
                voxel[y, x, z, :] = warna_putih[:]
                
                # Hanya cek pentagon untuk titik di permukaan bola (85% radius ke luar)
                # Ini menghemat komputasi karena bagian dalam bola tidak perlu dicek
                dist = np.sqrt(dist_sq)
                if dist > ball_radius * 0.85:
                    
                    #------------------------------------------------------------------------
                    # NORMALISASI POSISI:
                    # Ubah koordinat kartesian (dx,dy,dz) menjadi unit vector (nx,ny,nz)
                    # Unit vector menunjukkan ARAH dari pusat bola ke titik permukaan
                    #------------------------------------------------------------------------
                    if dist > 0:
                        nx = dx / dist
                        ny = dy / dist
                        nz = dz / dist
                        
                        # Simpan dot product ke semua pentagon untuk deteksi hexagon nanti
                        pentagon_dots = []
                        
                        #--------------------------------------------------------------------
                        # CEK KEDEKATAN KE SETIAP PENTAGON:
                        # Gunakan DOT PRODUCT untuk mengukur kesamaan arah
                        # Dot product = cos(sudut) antara dua vector
                        # Nilai 1 = arah sama persis, 0 = tegak lurus, -1 = berlawanan
                        #--------------------------------------------------------------------
                        for pc in pentagon_centers:
                            pcx_raw, pcy_raw, pcz_raw, rotation_offset = pc[0], pc[1], pc[2], pc[3]
                            
                            # Normalisasi posisi pusat pentagon menjadi unit vector
                            pc_len = np.sqrt(pcx_raw**2 + pcy_raw**2 + pcz_raw**2)
                            if pc_len > 0:
                                pcx = pcx_raw / pc_len
                                pcy = pcy_raw / pc_len
                                pcz = pcz_raw / pc_len
                                
                                # DOT PRODUCT: mengukur seberapa dekat titik ke pentagon
                                # dot > 0.85 berarti sudut < ~32° (cukup dekat)
                                dot = nx * pcx + ny * pcy + nz * pcz
                                pentagon_dots.append((dot, pcx, pcy, pcz, rotation_offset))
                                
                                #------------------------------------------------------------
                                # JIKA DEKAT DENGAN PENTAGON (dot > 0.85):
                                # Lakukan pengecekan lebih detail apakah titik berada
                                # DI DALAM bentuk pentagon (bukan hanya dekat pusatnya)
                                #------------------------------------------------------------
                                if dot > 0.85:
                                    #--------------------------------------------------------
                                    # BUAT SISTEM KOORDINAT LOKAL:
                                    # Untuk mengecek bentuk pentagon, kita perlu proyeksi 2D
                                    # Buat 2 vector tegak lurus (perp dan perp2) pada bidang pentagon
                                    #--------------------------------------------------------
                                    
                                    # Pilih vector temporary yang tidak sejajar dengan pentagon center
                                    if abs(pcx) < 0.9:
                                        temp_x, temp_y, temp_z = 1, 0, 0
                                    else:
                                        temp_x, temp_y, temp_z = 0, 1, 0
                                    
                                    # GRAM-SCHMIDT: Buat vector tegak lurus pertama (perp)
                                    # perp = temp - (temp·pc)*pc
                                    dot_temp = temp_x*pcx + temp_y*pcy + temp_z*pcz
                                    perp_x = temp_x - dot_temp*pcx
                                    perp_y = temp_y - dot_temp*pcy
                                    perp_z = temp_z - dot_temp*pcz
                                    
                                    # Normalisasi perp
                                    perp_len = np.sqrt(perp_x**2 + perp_y**2 + perp_z**2)
                                    if perp_len > 0:
                                        perp_x /= perp_len
                                        perp_y /= perp_len
                                        perp_z /= perp_len
                                        
                                        # CROSS PRODUCT: Buat vector tegak lurus kedua (perp2)
                                        # perp2 = pc × perp
                                        perp2_x = pcy*perp_z - pcz*perp_y
                                        perp2_y = pcz*perp_x - pcx*perp_z
                                        perp2_z = pcx*perp_y - pcy*perp_x
                                        
                                        #----------------------------------------------------
                                        # PROYEKSI KE BIDANG LOKAL:
                                        # Proyeksikan titik ke bidang 2D pentagon
                                        #----------------------------------------------------
                                        proj_x = nx - pcx*dot
                                        proj_y = ny - pcy*dot
                                        proj_z = nz - pcz*dot
                                        
                                        # Koordinat 2D lokal pada bidang pentagon
                                        local_x = proj_x*perp_x + proj_y*perp_y + proj_z*perp_z
                                        local_y = proj_x*perp2_x + proj_y*perp2_y + proj_z*perp2_z
                                        
                                        #----------------------------------------------------
                                        # BUAT VERTEX PENTAGON:
                                        # Pentagon memiliki 5 sudut dengan jarak 72° (360°/5)
                                        #----------------------------------------------------
                                        pentagon_radius = 0.40
                                        vertices = []
                                        for i in range(5):
                                            v_angle = np.radians(i * 72 + rotation_offset)
                                            vx = pentagon_radius * np.cos(v_angle)
                                            vy = pentagon_radius * np.sin(v_angle)
                                            vertices.append((vx, vy))
                                        
                                        #----------------------------------------------------
                                        # CEK APAKAH TITIK DI DALAM PENTAGON:
                                        # Gunakan metode CROSS PRODUCT untuk setiap edge
                                        # Jika titik di sisi "dalam" dari SEMUA edge, maka di dalam pentagon
                                        #----------------------------------------------------
                                        inside = True
                                        
                                        for i in range(5):
                                            v1 = vertices[i]
                                            v2 = vertices[(i + 1) % 5]
                                            
                                            # Vector edge (dari v1 ke v2)
                                            edge_x = v2[0] - v1[0]
                                            edge_y = v2[1] - v1[1]
                                            
                                            # Vector dari v1 ke titik yang dicek
                                            to_point_x = local_x - v1[0]
                                            to_point_y = local_y - v1[1]
                                            
                                            # CROSS PRODUCT 2D: edge × to_point
                                            # Positif = titik di kiri edge (dalam)
                                            # Negatif = titik di kanan edge (luar)
                                            cross = edge_x * to_point_y - edge_y * to_point_x
                                            
                                            # Jika cross < 0, titik di luar pentagon
                                            if cross < -0.001:
                                                inside = False
                                                break
                                        
                                        # Jika di dalam pentagon, warnai hitam
                                        if inside:
                                            voxel[y, x, z, :] = warna_hitam[:]
                                            break
                        
                        #--------------------------------------------------------------------
                        # DETEKSI HEXAGON (opsional - untuk visualisasi):
                        # Hexagon berada di area yang dekat dengan 3 pentagon sekaligus
                        # Ini adalah area "di antara" pentagon-pentagon
                        #--------------------------------------------------------------------
                        if voxel[y, x, z, 0] == 255:  # Masih putih
                            pentagon_dots.sort(key=lambda x: x[0], reverse=True)
                            
                            if len(pentagon_dots) >= 3:
                                # Jumlah dot product 3 pentagon terdekat
                                sum_top3 = sum(p[0] for p in pentagon_dots[:3])
                                
                                # Hexagon: area dimana 3 pentagon hampir sama jaraknya
                                if sum_top3 > 2.22 and sum_top3 < 2.24:
                                    voxel[y, x, z, :] = [180, 180, 180]  # Abu-abu

print("Soccer ball created!")

#============================================================================================
#=======================   VISUALIZE   ======================================================
#============================================================================================

# Tampilkan 3 view berbeda dengan slicing voxel
plt.figure(1)
plt.title('Front View (Z slice)')
plt.imshow(voxel[:, :, zc, :])  # Slice di tengah sumbu Z

plt.figure(2)
plt.title('Side View (X slice)')
plt.imshow(voxel[:, xc, :, :])  # Slice di tengah sumbu X

plt.figure(3)
plt.title('Top View (Y slice)')
plt.imshow(voxel[yc, :, :, :])  # Slice di tengah sumbu Y

plt.show()

# Simpan voxel ke file .npy untuk digunakan script lain
np.save(f"{nama_file}.npy", voxel)
print(f"Saved: {nama_file}.npy")
