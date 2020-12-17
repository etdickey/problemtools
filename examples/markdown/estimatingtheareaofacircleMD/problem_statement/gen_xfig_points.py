#!/usr/bin/python
 """Generate 75 points inside and 25 points outside the circle"""
 import random
 
 boundary_x = (3300, 7700)
 boundary_y = (3000, 7400)
 radius_2 = 2250 ** 2
 center_x = 5490
 center_y = 5220
 
 point_radius = 45
 
 count = 0
 while count < 75:
     cx = random.randint(*boundary_x)
     cy = random.randint(*boundary_y)
 
     if (cx - center_x) ** 2 + (cy - center_y) ** 2 < radius_2:
         sx = cx - (point_radius - 1) / 2
         sy = cy - (point_radius - 1) / 2
         ex = cx + (point_radius - 1) / 2
         ey = cy + (point_radius - 1) / 2
 
         print '1 4 0 1 0 0 50 -1 20 0.000 1 0.0000 {cx} {cy} {point_radius} {point_radius} {sx} {sy} {ex} {ey}'.format(**locals())
         count += 1
 
 
 count = 0
 while count < 25:
     cx = random.randint(*boundary_x)
     cy = random.randint(*boundary_y)
 
     if (cx - center_x) ** 2 + (cy - center_y) ** 2 >= radius_2:
         sx = cx - (point_radius - 1) / 2
         sy = cy - (point_radius - 1) / 2
         ex = cx + (point_radius - 1) / 2
         ey = cy + (point_radius - 1) / 2
 
         print '1 4 0 1 0 0 50 -1 20 0.000 1 0.0000 {cx} {cy} {point_radius} {point_radius} {sx} {sy} {ex} {ey}'.format(**locals())
         count += 1
 
