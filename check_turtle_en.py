#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import sys
import os
from ast import literal_eval
from copy import deepcopy
from math import hypot, sin, cos, atan2, acos
sys.stdout, sys.stderr = codecs.getwriter("utf-8")(sys.stdout.detach()), codecs.getwriter("utf-8")(sys.stderr.detach())
OK = 0; PE = 4; WA = 5; CF = 6
EPS = 1e-4
ZERO_EPS = 1e-8
EPS_ABS = 1e-2
def error(*args, sep=' '): sys.stderr.write(args[0].format(*args[1:])+'\n'); sys.exit(WA)
def ok(*args, sep=' '): sys.stdout.write(args[0].format(*args[1:])+'\n'); sys.exit(OK)


DEBUG = False


try:
    test = open(sys.argv[1], encoding='utf-8').read().strip()
    cor_ans = open(sys.argv[3], encoding='utf-8').read().strip()
    pup_ans = open(sys.argv[2], encoding='utf-8').read().strip()
except ZeroDivisionError:
    sys.exit(PE)

# Get the values of variables that set the check parameters
def get_environment(var_name):
    val = os.environ.get(var_name, "").lower()
    return val in ['yes', 'true', 'y', '1']

disable_shift = get_environment('DISABLE_SHIFT')
disable_homothety = get_environment('DISABLE_HOMOTHETY')
disable_rotation = get_environment('DISABLE_ROTATION')


pup_ans = pup_ans.splitlines()
if not all('->' in row for row in pup_ans):
    error('Extra output in stdin')

for i, row in enumerate(pup_ans):
    pup_ans[i] = list(map(lambda x: literal_eval(x.strip()), row.split('->')))

cor_ans = cor_ans.splitlines()
for i, row in enumerate(cor_ans):
    cor_ans[i] = list(map(lambda x: literal_eval(x.strip()), row.split('->')))


if len(cor_ans) == 0 == len(pup_ans):
    ok('Empty -- OK')
elif len(pup_ans) == 0:
    error('Not a single segment drawn!')
elif len(cor_ans) * 50 < len(pup_ans):
    error('The image consists of too many segments for this task')

# OK. We have two lists of segments, we need to check if they are homothetic...

# This function takes a list of segments and normalizes them, modifying the list
# Parallel translation and homothety are also performed
# The function returns three values: x, y, coeff
# (x, y) - coordinates of the center of mass (it was moved to the origin)
# coeff - homothety coefficient
def preprocess_segments(segments):
    # Make sure the minimum segment has length 1
    min_segm = float('inf')
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        min_segm = min(min_segm, hypot(fx-tx, fy-ty))
        if min_segm < 1e-8:
            error('The length of one of the segments is less than 1/10⁸, it is too short: ' + str((i, ((fx, fy), (tx, ty)))))
    coeff1 = 1 / min_segm
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx * coeff1, fy * coeff1], [tx * coeff1, ty * coeff1]]
    # OK, now there are no too short segments

    # Make sure all segments "look" to the right, or at least up.
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        if fx > tx - ZERO_EPS or (abs(fx - tx) < ZERO_EPS and fy > ty - ZERO_EPS):
            segments[i] = [(tx, ty), (fx, fy)]
    # Make it impossible to replace any two segments with one other segment.
    # For now, a naive solution in O(n^2) (and O(n^3) in the worst case)
    i = 0
    while i < len(segments):
        (fx1, fy1), (tx1, ty1) = segments[i]
        dx1, dy1 = tx1 - fx1, ty1 - fy1
        j = i + 1
        while j < len(segments):
            (fx2, fy2), (tx2, ty2) = segments[j]
            dx2, dy2 = tx2 - fx2, ty2 - fy2
            # If two segments lie on the same line and intersect, replace them with one segment
            if abs(dx1 * dy2 - dy1 * dx2) < EPS and abs(dx1 * (ty1 - fy2) - dy1 * (tx1 - fx2)) < EPS:
                # print(f'{i}-th and {j}-th are collinear, {segments[i]}, {segments[j]} ')
                # Two collinear segments intersect if and only if their projections on the X and Y axes intersect
                if max(fx1, tx1) >= min(fx2, tx2) - EPS and max(fx2, tx2) >= min(fx1, tx1) - EPS and \
                        max(fy1, ty1) >= min(fy2, ty2) - EPS and max(fy2, ty2) >= min(fy1, ty1) - EPS:
                    mnx, mxx = min((fx1, tx1, fx2, tx2)), max((fx1, tx1, fx2, tx2))
                    mny, mxy = min((fy1, ty1, fy2, ty2)), max((fy1, ty1, fy2, ty2))
                    if abs(dx1 * (mxy-mny) - dy1 * (mxx-mnx)) < EPS:
                        segments[i] = [(mnx, mny), (mxx, mxy)]
                    elif abs(dx1 * (-mxy+mny) - dy1 * (mxx-mnx)) < EPS:
                        segments[i] = [(mnx, mxy), (mxx, mny)]
                    else:
                        continue
                        # raise ValueError('Error in check pgm')
                    # print(f'{i}-th and {j}-th intersect. Replacing with {segments[i]}')
                    segments.pop(j)
                    break
            j += 1
        else:
            i += 1
    if DEBUG:
        print('After gluing before scaling:')
        for i, ((fx, fy), (tx, ty)) in enumerate(segments):
            print('({:+05.2f},{:+05.2f}) -> ({:+05.2f},{:+05.2f})'.format(fx, fy, tx, ty))
        print('Number of segments obtained:', len(segments))
    # Adjust all points so that the center of mass is at (0,0),
    # and the furthest point is at a distance of 1000
    corr_x = sum(ans[0][0] + ans[1][0] for ans in segments) / 2 / len(segments)
    corr_y = sum(ans[0][1] + ans[1][1] for ans in segments) / 2 / len(segments)
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx - corr_x, fy - corr_y], [tx - corr_x, ty - corr_y]]
    max_dist = max(max(hypot(fx, fy), hypot(tx, ty)) for (fx, fy), (tx, ty) in segments)
    if max_dist == 0:
        error('There is only one point in the answer...')
    coeff2 = 1000 / max_dist
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx * coeff2, fy * coeff2], [tx * coeff2, ty * coeff2]]
    return corr_x / coeff1, corr_y / coeff1, coeff1 * coeff2


def find_best_dist(segments):
    dists = []
    for (fx, fy), (tx, ty) in segments:
        h1 = hypot(fx, fy)
        if h1 > EPS:
            dists.append(h1)
        h2 = hypot(tx, ty)
        if h2 > EPS:
            dists.append(h2)
    # Find the radius that has the minimum number of points in its EPS-neighborhood
    # If there are several such, take the maximum radius value
    if dists:
        return min(dists, key=lambda d1: (sum(abs(d1 - d2) < EPS for d2 in dists), -d1))
    else:
        return 0


def find_rad_points(segments, rad):
    rad_points = []
    for (fx, fy), (tx, ty) in segments:
        if abs(hypot(fx, fy) - rad) < EPS:
            rad_points.append((fx, fy))
        if abs(hypot(tx, ty) - rad) < EPS:
            rad_points.append((tx, ty))
    # Now we need to remove duplicates from rad_points (distance between which is less than EPS)
    i = 0
    while i < len(rad_points):
        j = i + 1
        cx1, cy1 = rad_points[i]
        while j < len(rad_points):
            cx2, cy2 = rad_points[j]
            if hypot(cx2 - cx1, cy2 - cy1) < EPS:
                rad_points.pop(j)
                break
            j += 1
        else:
            i += 1
    return rad_points


def calc_test_angles(pts1, pts2):
    # Add a rotation angle of 0 at the beginning to check if the answer works without rotation
    angles = [0]
    fx, fy = pts1[0]
    for sx, sy in pts2:
        angles.append(atan2(sx * fy - sy * fx, sx * fx + sy * fy))
    return angles


def rotate_everything(segments, angle):
    ca, sa = cos(angle), sin(angle)
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx * ca + fy * (-sa), fx * sa + fy * ca], [tx * ca + ty * (-sa), tx * sa + ty * ca]]


def two_segmset_eq(segm1, segm2):
    segm1 = deepcopy(segm1)
    segm2 = deepcopy(segm2)
    i = 0
    while i < len(segm1):
        (fx1, fy1), (tx1, ty1) = segm1[i]
        j = 0
        while j < len(segm2):
            (fx2, fy2), (tx2, ty2) = segm2[j]
            if (abs(fx1 - fx2) < EPS_ABS and abs(fy1 - fy2) < EPS_ABS and abs(tx1 - tx2) < EPS_ABS and abs(ty1 - ty2) < EPS_ABS) or \
                    (abs(fx1 - tx2) < EPS_ABS and abs(fy1 - ty2) < EPS_ABS and abs(tx1 - fx2) < EPS_ABS and abs(ty1 - fy2) < EPS_ABS):
                segm1.pop(i)
                segm2.pop(j)
                break
            j += 1
        else:
            i += 1
    return len(segm1) == len(segm2) == 0

if DEBUG: print("Processing the correct answer")
cor_x, cor_y, cor_coeff = preprocess_segments(cor_ans)
if DEBUG:
    print(f"Center of mass: ({cor_x}, {cor_y})")
    print(f"Scaling coefficient: {cor_coeff}")
    print('After scaling:', cor_ans, sep='\n')

if DEBUG: print("\nProcessing the student's answer")
pup_x, pup_y, pup_coeff = preprocess_segments(pup_ans)
if DEBUG:
    print(f"Center of mass: ({pup_x}, {pup_y})")
    print(f"Scaling coefficient: {pup_coeff}")
    print('After scaling:', pup_ans, sep='\n')

if len(cor_ans) != len(pup_ans):
    error('The number of non-intersecting segments in the answer {} does not match the correct one {}', len(pup_ans), len(cor_ans))

best_rad = find_best_dist(cor_ans)
cor_rad_points = find_rad_points(cor_ans, best_rad)
pup_rad_points = find_rad_points(pup_ans, best_rad)
if DEBUG: print(best_rad, cor_rad_points, pup_rad_points, sep='\n*\n')

if len(cor_rad_points) != len(pup_rad_points):
    error('The image in the answer cannot be transformed into the correct one by a similarity transformation, '
          'points at the required distance from the center of mass were not found')

test_angles = calc_test_angles(cor_rad_points, pup_rad_points)
for angle in test_angles:
    pup_ans_cp = deepcopy(pup_ans)
    rotate_everything(pup_ans_cp, angle)
    if two_segmset_eq(cor_ans, pup_ans_cp):
        # Found a suitable rotation angle...
        if disable_homothety and abs(cor_coeff - pup_coeff) >= EPS:
            error('The image in the answer is similar to the correct one, but the image size does not match.\nIt is required that the image size matches the correct answer')
        if disable_rotation and angle != 0: # Here we can use exact equality, because the first angle value in the list is 0
            error('The image in the answer is correct, but rotated.\nIt is required that the image matches the correct answer without rotation')
        if disable_shift and (abs(cor_x - pup_x) >= EPS or abs(cor_y - pup_y) >= EPS):
            error('The image in the answer differs from the correct one by a shift.\nIt is required that the image position matches the correct answer.')
        ok('Everything is correct!')

error('The image in the answer cannot be transformed into the correct one by a similarity transformation')
