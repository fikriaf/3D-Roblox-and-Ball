

print("\033c")       #To close all
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    USER ENTRIES    ================================
#=====================================================================================
nama_file = "roblox_character"
threshold = 15                               #Threshold for checking a non-black voxel

# THE USER DECIDES THE ROTATION ANGLES IN DEGREE
alfa_start = 0; beta_start = 0
delta_alfa = 6; delta_beta = 6
no_of_rotation = int(15)

#============================================================================================
#=======================   CREATING A 3D MODEL USING GEOMETRICAL SCRIPT   ===================
#============================================================================================
print ("Creating a 3D Roblox character...."); print ("")

# THE USER DECIDES THE SIZE OF THE 3D ROOM AND THE 2D SCREEN (MAX 1080 BY 1080)
col, row, length = 200, 200, 200      #Ensure making a cubic 3D space and a square 2D screen.

#Creating The Template Matrix for the 3D Model
voxel  = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)    #Template for the 3D model
buffer = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)    #Template for the 3D buffer
slice = np.zeros(shape=(row, col, 3), dtype=np.uint8)             #Template for the slice cut

# Character parameters (center of space)
yc = round(0.5*row)
xc = round(0.5*col)
zc = round(0.5*length)

# Define colors
warna_kulit = [255, 220, 177]      # Skin color
warna_baju = [255, 255, 255]       # White shirt (Real Madrid)
warna_celana = [255, 255, 255]     # White shorts
warna_hitam = [50, 50, 50]         # Dark gray/black for details

# Size parameters (relative to row) - Made wider and more blocky
head_size = round(0.18 * row)          # Kepala lebih besar
leg_width = round(0.14 * row)          # Kaki lebih tebal
leg_gap = 4                            # Jarak antar kaki
body_width = 2 * leg_width + leg_gap   # Body = lebar 2 kaki + gap
body_height = body_width               # Body kotak dari depan: tinggi = lebar
body_depth = round(0.15 * row)         # Body depth bisa berbeda
arm_width = round(0.12 * row)          # Tangan lebih tebal
arm_length = body_height               # Panjang tangan = tinggi body
arm_depth = round(0.10 * row)          # Tangan punya depth
leg_length = round(0.24 * row)         # Kaki lebih panjang
leg_depth = round(0.12 * row)          # Kaki punya depth

# Position parameters (y-axis: top to bottom)
# Head
head_top = round(0.15 * row)
head_bottom = head_top + head_size
head_left = xc - round(head_size/2)
head_right = xc + round(head_size/2)
head_front = zc - round(head_size/2)
head_back = zc + round(head_size/2)

# Body (torso) - Wide and blocky
body_top = head_bottom  # No gap between head and body
body_bottom = body_top + body_height
body_left = xc - round(body_width/2)
body_right = xc + round(body_width/2)
body_front = zc - round(body_depth/2)
body_back = zc + round(body_depth/2)

# Left Arm - Attached to side of body
left_arm_top = body_top
left_arm_bottom = left_arm_top + arm_length
left_arm_left = body_right  # Starts from body edge
left_arm_right = left_arm_left + arm_width
left_arm_front = zc - round(arm_depth/2)
left_arm_back = zc + round(arm_depth/2)

# Right Arm - Attached to side of body
right_arm_top = body_top
right_arm_bottom = right_arm_top + arm_length
right_arm_right = body_left  # Ends at body edge
right_arm_left = right_arm_right - arm_width
right_arm_front = zc - round(arm_depth/2)
right_arm_back = zc + round(arm_depth/2)

# Left Leg - Attached to bottom of body
left_leg_top = body_bottom
left_leg_bottom = left_leg_top + leg_length
left_leg_left = xc + round(leg_gap/2)  # Small gap between legs
left_leg_right = left_leg_left + leg_width
left_leg_front = zc - round(leg_depth/2)
left_leg_back = zc + round(leg_depth/2)

# Right Leg - Attached to bottom of body
right_leg_top = body_bottom
right_leg_bottom = right_leg_top + leg_length
right_leg_right = xc - round(leg_gap/2)  # Small gap between legs
right_leg_left = right_leg_right - leg_width
right_leg_front = zc - round(leg_depth/2)
right_leg_back = zc + round(leg_depth/2)

print("Creating Roblox character parts...")

# HEAD (rounded box - kotak dengan sudut sedikit rounded)
head_half = round(head_size / 2)
corner_radius = 4  # Radius untuk sudut rounded (kecil)

for i in range(head_top, head_bottom):
    for j in range(xc - head_half, xc + head_half):
        for k in range(zc - head_half, zc + head_half):
            # Hitung jarak dari tepi kotak
            dx = max(0, abs(j - xc) - (head_half - corner_radius))
            dy = max(0, abs(i - (head_top + head_half)) - (head_half - corner_radius))
            dz = max(0, abs(k - zc) - (head_half - corner_radius))
            
            # Jika dalam radius corner, gambar
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            if distance <= corner_radius:
                voxel[i, j, k, :] = warna_kulit[:]

# BODY (white shirt - rounded box)
body_corner_radius = 2
body_half_width = round(body_width / 2)
body_half_height = round(body_height / 2)
body_half_depth = round(body_depth / 2)
body_center_y = body_top + body_half_height

for i in range(body_top, body_bottom):
    for j in range(body_left, body_right):
        for k in range(body_front, body_back):
            dx = max(0, abs(j - xc) - (body_half_width - body_corner_radius))
            dy = max(0, abs(i - body_center_y) - (body_half_height - body_corner_radius))
            dz = max(0, abs(k - zc) - (body_half_depth - body_corner_radius))
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            if distance <= body_corner_radius:
                voxel[i, j, k, :] = warna_baju[:]

# LEFT ARM (40% white sleeve with black edge, 60% skin - rounded box)
sleeve_length = round(arm_length * 0.40)
black_edge_length = round(sleeve_length * 0.20)
white_sleeve_length = sleeve_length - black_edge_length
arm_corner_radius = 2
arm_half_width = round(arm_width / 2)
arm_half_depth = round(arm_depth / 2)
left_arm_center_x = left_arm_left + arm_half_width
left_arm_center_z = (left_arm_front + left_arm_back) // 2

for i in range(left_arm_top, left_arm_bottom):
    for j in range(left_arm_left, left_arm_right):
        for k in range(left_arm_front, left_arm_back):
            dx = max(0, abs(j - left_arm_center_x) - (arm_half_width - arm_corner_radius))
            dz = max(0, abs(k - left_arm_center_z) - (arm_half_depth - arm_corner_radius))
            distance = np.sqrt(dx**2 + dz**2)
            if distance <= arm_corner_radius:
                if i < left_arm_top + white_sleeve_length:
                    voxel[i, j, k, :] = warna_baju[:]
                elif i < left_arm_top + sleeve_length:
                    voxel[i, j, k, :] = warna_hitam[:]
                else:
                    voxel[i, j, k, :] = warna_kulit[:]

# RIGHT ARM (40% white sleeve with black edge, 60% skin - rounded box)
right_arm_center_x = right_arm_left + arm_half_width
right_arm_center_z = (right_arm_front + right_arm_back) // 2

for i in range(right_arm_top, right_arm_bottom):
    for j in range(right_arm_left, right_arm_right):
        for k in range(right_arm_front, right_arm_back):
            dx = max(0, abs(j - right_arm_center_x) - (arm_half_width - arm_corner_radius))
            dz = max(0, abs(k - right_arm_center_z) - (arm_half_depth - arm_corner_radius))
            distance = np.sqrt(dx**2 + dz**2)
            if distance <= arm_corner_radius:
                if i < right_arm_top + white_sleeve_length:
                    voxel[i, j, k, :] = warna_baju[:]
                elif i < right_arm_top + sleeve_length:
                    voxel[i, j, k, :] = warna_hitam[:]
                else:
                    voxel[i, j, k, :] = warna_kulit[:]

# LEFT LEG (white shorts - rounded box)
leg_corner_radius = 2
leg_half_width = round(leg_width / 2)
leg_half_depth = round(leg_depth / 2)
left_leg_center_x = left_leg_left + leg_half_width
left_leg_center_z = (left_leg_front + left_leg_back) // 2

for i in range(left_leg_top, left_leg_bottom):
    for j in range(left_leg_left, left_leg_right):
        for k in range(left_leg_front, left_leg_back):
            dx = max(0, abs(j - left_leg_center_x) - (leg_half_width - leg_corner_radius))
            dz = max(0, abs(k - left_leg_center_z) - (leg_half_depth - leg_corner_radius))
            distance = np.sqrt(dx**2 + dz**2)
            if distance <= leg_corner_radius:
                voxel[i, j, k, :] = warna_celana[:]

# RIGHT LEG (white shorts - rounded box)
right_leg_center_x = right_leg_left + leg_half_width
right_leg_center_z = (right_leg_front + right_leg_back) // 2

for i in range(right_leg_top, right_leg_bottom):
    for j in range(right_leg_left, right_leg_right):
        for k in range(right_leg_front, right_leg_back):
            dx = max(0, abs(j - right_leg_center_x) - (leg_half_width - leg_corner_radius))
            dz = max(0, abs(k - right_leg_center_z) - (leg_half_depth - leg_corner_radius))
            distance = np.sqrt(dx**2 + dz**2)
            if distance <= leg_corner_radius:
                voxel[i, j, k, :] = warna_celana[:]

# Add text "Team 2" on back of body
back_z = body_back - 2  # Position on back of body

# Simple pixel art for "TEAM" - centered horizontally
team_y_start = body_top + round(body_height * 0.10)  # Lebih ke atas
team_total_width = 21  # Total width of TEAM text
team_x_start = xc - round(team_total_width / 2)

# Letter T
voxel[team_y_start:team_y_start+1, team_x_start:team_x_start+5, back_z:back_z+2, :] = warna_hitam[:]  # Top bar
voxel[team_y_start:team_y_start+7, team_x_start+2:team_x_start+3, back_z:back_z+2, :] = warna_hitam[:]  # Vertical

# Letter E
voxel[team_y_start:team_y_start+7, team_x_start+6:team_x_start+7, back_z:back_z+2, :] = warna_hitam[:]  # Vertical
voxel[team_y_start:team_y_start+1, team_x_start+6:team_x_start+10, back_z:back_z+2, :] = warna_hitam[:]  # Top
voxel[team_y_start+3:team_y_start+4, team_x_start+6:team_x_start+9, back_z:back_z+2, :] = warna_hitam[:]  # Middle
voxel[team_y_start+6:team_y_start+7, team_x_start+6:team_x_start+10, back_z:back_z+2, :] = warna_hitam[:]  # Bottom

# Letter A
voxel[team_y_start+1:team_y_start+7, team_x_start+11:team_x_start+12, back_z:back_z+2, :] = warna_hitam[:]  # Left
voxel[team_y_start+1:team_y_start+7, team_x_start+14:team_x_start+15, back_z:back_z+2, :] = warna_hitam[:]  # Right
voxel[team_y_start:team_y_start+1, team_x_start+12:team_x_start+14, back_z:back_z+2, :] = warna_hitam[:]  # Top
voxel[team_y_start+3:team_y_start+4, team_x_start+11:team_x_start+15, back_z:back_z+2, :] = warna_hitam[:]  # Middle

# Letter M
voxel[team_y_start:team_y_start+7, team_x_start+16:team_x_start+17, back_z:back_z+2, :] = warna_hitam[:]  # Left
voxel[team_y_start:team_y_start+7, team_x_start+20:team_x_start+21, back_z:back_z+2, :] = warna_hitam[:]  # Right
voxel[team_y_start+1:team_y_start+4, team_x_start+18:team_x_start+19, back_z:back_z+2, :] = warna_hitam[:]  # Middle

# Number "2" at center of body - much bigger and centered
num_height = 16
num_y_start = body_top + round(body_height / 2) - round(num_height / 2)  # Center vertically
num_width = 14  # Much bigger width
num_x_start = xc - round(num_width / 2)
stroke_width = 3  # Thicker strokes

voxel[num_y_start:num_y_start+stroke_width, num_x_start:num_x_start+num_width, back_z:back_z+2, :] = warna_hitam[:]  # Top
voxel[num_y_start:num_y_start+7, num_x_start+num_width-stroke_width:num_x_start+num_width, back_z:back_z+2, :] = warna_hitam[:]  # Right top
voxel[num_y_start+6:num_y_start+9, num_x_start:num_x_start+num_width, back_z:back_z+2, :] = warna_hitam[:]  # Middle
voxel[num_y_start+8:num_y_start+num_height, num_x_start:num_x_start+stroke_width, back_z:back_z+2, :] = warna_hitam[:]  # Left bottom
voxel[num_y_start+num_height-stroke_width:num_y_start+num_height, num_x_start:num_x_start+num_width, back_z:back_z+2, :] = warna_hitam[:]  # Bottom

# Add small "2" on front right of body
front_z = body_front  # Position on front of body (at surface)
small_num_height = 7
small_num_width = 5
small_num_y_start = body_top + round(body_height * 0.15)  # Top right area
small_num_x_start = body_right - small_num_width - 8  # Right side with more margin
stroke = 1  # Thin stroke

voxel[small_num_y_start:small_num_y_start+stroke, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+2, :] = warna_hitam[:]  # Top
voxel[small_num_y_start:small_num_y_start+3, small_num_x_start+small_num_width-stroke:small_num_x_start+small_num_width, front_z:front_z+2, :] = warna_hitam[:]  # Right top
voxel[small_num_y_start+3:small_num_y_start+4, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+2, :] = warna_hitam[:]  # Middle
voxel[small_num_y_start+3:small_num_y_start+small_num_height, small_num_x_start:small_num_x_start+stroke, front_z:front_z+2, :] = warna_hitam[:]  # Left bottom
voxel[small_num_y_start+small_num_height-stroke:small_num_y_start+small_num_height, small_num_x_start:small_num_x_start+small_num_width, front_z:front_z+2, :] = warna_hitam[:]  # Bottom

# Add Roblox-style face (2 oval eyes and curved smile)
# Face positioned at the FRONT of the head
face_z_start = head_front
face_z_end = head_front + 3

# Eyes - simple rectangles (easier to see)
eye_width = 4
eye_height = 8
eye_spacing = round(head_size * 0.20)
eye_y_start = head_top + round(head_size * 0.30)
eye_y_end = eye_y_start + eye_height

# Left eye
left_eye_x_start = xc - eye_spacing - eye_width//2
left_eye_x_end = xc - eye_spacing + eye_width//2
voxel[eye_y_start:eye_y_end, left_eye_x_start:left_eye_x_end, face_z_start:face_z_end, :] = warna_hitam[:]

# Right eye
right_eye_x_start = xc + eye_spacing - eye_width//2
right_eye_x_end = xc + eye_spacing + eye_width//2
voxel[eye_y_start:eye_y_end, right_eye_x_start:right_eye_x_end, face_z_start:face_z_end, :] = warna_hitam[:]

# Smile - simple curved line
smile_y_start = head_top + round(head_size * 0.65)
smile_width = round(head_size * 0.40)
smile_thickness = 3

# Draw smile as a simple arc
for j in range(xc - smile_width, xc + smile_width + 1):
    # Parabolic curve for smile
    x_norm = (j - xc) / smile_width
    if abs(x_norm) <= 1:
        y_offset = int(5 * (1 - x_norm**2))  # Curve upward
        smile_y = smile_y_start + y_offset
        if smile_y < head_bottom - 2:
            voxel[smile_y:smile_y+smile_thickness, j, face_z_start:face_z_end, :] = warna_hitam[:]

half_length = round(0.5*row)
quarter_length = round(0.25*row)
three_quarter_length = round(0.75*row)

# Figure 1: Top view (horizontal slice at head level)
slice[:, :, :] = voxel[head_top + 10, :, : :]
plt.figure(1); plt.title('Top View (Head Level)')
plt.imshow(slice)

# Figure 2: Full body front view (vertical slice at center z)
slice[:, :, :] = voxel[:, :, zc, :]
plt.figure(2); plt.title('Full Body Front View')
plt.imshow(slice)

# Figure 3: Face close-up (vertical slice at front of head)
slice[:, :, :] = voxel[:, :, head_front + 1, :]
plt.figure(3); plt.title('Face View')
plt.imshow(slice)

# Figure 4: Full body side view (vertical slice through left leg)
slice[:, :, :] = voxel[:, left_leg_left + 5, :, :]
plt.figure(4); plt.title('Full Body Side View')
plt.imshow(slice)

# Figure 5: Back view with "Team 2" text (vertical slice at back of body)
slice[:, :, :] = voxel[:, :, body_back - 2, :]
plt.figure(5); plt.title('Back View - Team 2')
plt.imshow(slice)

# Figure 6: Front body view with small "2" (vertical slice at front of body)
slice[:, :, :] = voxel[:, :, body_front + 1, :]
plt.figure(6); plt.title('Front Body View - Small 2')
plt.imshow(slice)

plt.ion()
plt.show()
plt.pause(1)

np.save(nama_file + "_0_0_.npy", voxel)

#================================================================================================
#=================    DEFINING FUNCTION FOR DEGREE CONVERSION AND ROTATION    ===================
#================================================================================================
# Converting degree unit of alfa and beta to radiant unit
def degree_to_rad (alfa, beta):
    alfa_rad = (alfa / 180) * np.pi  # Converting degree to rad
    beta_rad = (beta / 180) * np.pi  # Converting dgreee to rad
    return alfa_rad, beta_rad

#FUNCTION TO ROTATE A VOXEL (yi, xi, zi) ABOUT A CENTER AS MUCH AS ALFA RAD THEN BETA RAD
def putar_titik(y_pusat, x_pusat, z_pusat, yi, xi, zi, alfa_rad, beta_rad):
    #Putar titik dengan as berupa sumbu z, sejauh alfa_rad
    xr1 = round(np.cos(alfa_rad)*(xi-x_pusat) - np.sin(alfa_rad)*(yi-y_pusat)) + x_pusat
    yr1 = round(np.sin(alfa_rad)*(xi-x_pusat) + np.cos(alfa_rad)*(yi-y_pusat)) + y_pusat
    zr1 = zi                                                                         #zi tetap.
    #Putar titik dengan as berupa sumbu y, sejauh beta_rad
    xr2 = round(np.cos(beta_rad)*(xr1-x_pusat) - np.sin(beta_rad)*(zr1-z_pusat)) + x_pusat
    zr2 = round(np.sin(beta_rad)*(xr1-x_pusat) + np.cos(beta_rad)*(zr1-z_pusat)) + z_pusat
    yr2 = yr1                                                                       #yi tetap.
    return yr2, xr2, zr2

#============================================================================================
#==========================   MAIN PROGRAM TO ROTATE THE 3D OBJECT   ========================
#============================================================================================
#The object is rotated with the same angle over and over again acc. to number of rotations.
xc = round(col/2); yc = round(row/2); zc = round(length/2)      #Center of 3D object rotation

alfa = alfa_start
beta = beta_start
for r in range (1, no_of_rotation+1):
    alfa = alfa + delta_alfa
    beta = beta + delta_beta
    alfa_rad, beta_rad = degree_to_rad(alfa, beta)                #Convert degree to rad.
    voxel = np.load(nama_file + "_0_0_.npy")                #Always reads original model.

    for i in range (0, row):                              #Rotating te whole voxel[:,:,:]
        print('alfa =', alfa, ', beta =', beta,', now rotating voxels in row', i, '.')
        for j in range (0, col):
            for k in range (0, length):
                cek1 = int(voxel[i,j,k,0])
                cek2 = int(voxel[i,j,k,1])
                cek3 = int(voxel[i,j,k,2])
                if  (cek1 + cek2 + cek3) > threshold:
                    yr, xr, zr = putar_titik(yc,xc,zc,i,j,k,alfa_rad,beta_rad) #Rotate every voxel
                    i, j, k, yr, xr, zr = int(i), int(j), int(k), int(yr), int(xr), int(zr)
                    buffer[yr,xr,zr,:] = voxel[i,j,k,:]
                    voxel[i,j,k,:] = 0                         #Must be put back to black.
    #Result of one time rotation of the object is ready for next rotation
    np.save(nama_file + "_" + str(alfa) + "_" + str(beta) + "_" + ".npy", buffer)
    voxel[:, :, :] = 0                                      #Must be put back to black.
    buffer[:, :, :] = 0                                     #Must be put back to black.

plt.show()
