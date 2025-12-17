# Penjelasan Kode Create_Soccer_Ball.py

## Konsep Dasar

Bola sepak klasik (truncated icosahedron) memiliki:
- 12 pentagon hitam (segi-5)
- 20 hexagon putih (segi-6)

Pentagon ditempatkan pada 12 vertex dari icosahedron, yang posisinya ditentukan oleh Golden Ratio.

---

## 1. Inisialisasi Ruang 3D (Voxel)

```python
col, row, length = 200, 200, 200
voxel = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)
```

Membuat array 4 dimensi:
- `row, col, length` = 200x200x200 pixel (ruang 3D)
- `3` = channel RGB untuk warna
- `dtype=np.uint8` = nilai 0-255 untuk setiap channel

---

## 2. Golden Ratio dan Posisi Pentagon

```python
phi = (1 + np.sqrt(5)) / 2
```

Golden Ratio (phi) ≈ 1.618 adalah rasio matematika yang menentukan posisi vertex icosahedron.

```python
pentagon_centers = [
    (0, phi, 1, 0),
    (0, -phi, -1, 36),
    ...
]
```

Format: `(x, y, z, rotation_offset)`
- `x, y, z` = koordinat pusat pentagon berdasarkan vertex icosahedron
- `rotation_offset` = rotasi pentagon (0° atau 36°) agar sudut tidak bertabrakan

---

## 3. Persamaan Bola

```python
dist_sq = dx**2 + dy**2 + dz**2

if dist_sq <= ball_radius**2:
```

Menggunakan persamaan bola: `x² + y² + z² ≤ r²`

Jika jarak kuadrat dari titik ke pusat lebih kecil dari radius kuadrat, maka titik berada di dalam bola.

---

## 4. Normalisasi (Unit Vector)

```python
nx = dx / dist
ny = dy / dist
nz = dz / dist
```

Mengubah koordinat kartesian menjadi unit vector (panjang = 1).

Unit vector menunjukkan ARAH dari pusat bola ke titik permukaan, terlepas dari jarak.

---

## 5. Dot Product (Kedekatan ke Pentagon)

```python
dot = nx * pcx + ny * pcy + nz * pcz
```

Dot product mengukur kesamaan arah antara dua vector:
- `1` = arah sama persis (sudut 0°)
- `0` = tegak lurus (sudut 90°)
- `-1` = berlawanan (sudut 180°)

Jika `dot > 0.85`, titik cukup dekat dengan pentagon (sudut < ~32°).

---

## 6. Gram-Schmidt Orthogonalization

```python
dot_temp = temp_x*pcx + temp_y*pcy + temp_z*pcz
perp_x = temp_x - dot_temp*pcx
perp_y = temp_y - dot_temp*pcy
perp_z = temp_z - dot_temp*pcz
```

Membuat vector tegak lurus (perpendicular) terhadap pusat pentagon.

Rumus: `perp = temp - (temp·pc) × pc`

Ini diperlukan untuk membuat sistem koordinat lokal 2D pada bidang pentagon.

---

## 7. Cross Product (Vector Tegak Lurus Kedua)

```python
perp2_x = pcy*perp_z - pcz*perp_y
perp2_y = pcz*perp_x - pcx*perp_z
perp2_z = pcx*perp_y - pcy*perp_x
```

Cross product menghasilkan vector yang tegak lurus terhadap kedua input vector.

Rumus: `perp2 = pc × perp`

Sekarang kita punya 3 vector orthogonal: `pc`, `perp`, `perp2` (sistem koordinat lokal).

---

## 8. Proyeksi ke Bidang 2D

```python
proj_x = nx - pcx*dot
proj_y = ny - pcy*dot
proj_z = nz - pcz*dot

local_x = proj_x*perp_x + proj_y*perp_y + proj_z*perp_z
local_y = proj_x*perp2_x + proj_y*perp2_y + proj_z*perp2_z
```

Memproyeksikan titik 3D ke bidang 2D pentagon:
1. `proj` = komponen titik yang sejajar dengan bidang pentagon
2. `local_x, local_y` = koordinat 2D pada bidang pentagon

---

## 9. Membuat Vertex Pentagon

```python
for i in range(5):
    v_angle = np.radians(i * 72 + rotation_offset)
    vx = pentagon_radius * np.cos(v_angle)
    vy = pentagon_radius * np.sin(v_angle)
    vertices.append((vx, vy))
```

Pentagon memiliki 5 sudut dengan jarak 72° (360°/5).

Setiap vertex dihitung dengan:
- `vx = r × cos(θ)`
- `vy = r × sin(θ)`

---

## 10. Point-in-Polygon Test (Cross Product 2D)

```python
edge_x = v2[0] - v1[0]
edge_y = v2[1] - v1[1]

to_point_x = local_x - v1[0]
to_point_y = local_y - v1[1]

cross = edge_x * to_point_y - edge_y * to_point_x

if cross < -0.001:
    inside = False
```

Untuk setiap edge pentagon:
1. Hitung vector edge (v1 → v2)
2. Hitung vector ke titik (v1 → point)
3. Cross product 2D menentukan posisi titik:
   - `cross > 0` = titik di kiri edge (dalam)
   - `cross < 0` = titik di kanan edge (luar)

Jika titik di sisi "dalam" dari SEMUA 5 edge, maka titik berada di dalam pentagon.

---

## 11. Deteksi Hexagon (Opsional)

```python
sum_top3 = sum(p[0] for p in pentagon_dots[:3])

if sum_top3 > 2.22 and sum_top3 < 2.24:
    voxel[y, x, z, :] = [180, 180, 180]
```

Hexagon berada di area yang dekat dengan 3 pentagon sekaligus.

Jika jumlah dot product ke 3 pentagon terdekat berada dalam range tertentu, titik berada di area hexagon.

---

## Ringkasan Alur

```
1. Loop setiap voxel (x, y, z)
2. Cek apakah di dalam bola (persamaan bola)
3. Jika di permukaan:
   a. Normalisasi posisi (unit vector)
   b. Hitung dot product ke setiap pentagon
   c. Jika dekat pentagon (dot > 0.85):
      - Buat sistem koordinat lokal (Gram-Schmidt + Cross Product)
      - Proyeksi ke bidang 2D
      - Cek apakah di dalam pentagon (Point-in-Polygon)
   d. Jika di dalam pentagon → warna hitam
   e. Jika tidak → tetap putih
4. Simpan hasil ke file .npy
```
