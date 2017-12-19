#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import sys
from ast import literal_eval
from copy import deepcopy
from math import hypot, sin, cos, atan2, acos
sys.stdout, sys.stderr = codecs.getwriter("utf-8")(sys.stdout.detach()), codecs.getwriter("utf-8")(sys.stderr.detach())
OK = 0; PE = 4; WA = 5; CF = 6
EPS = 1e-4
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

# cor_ans = """\
# (-350.0,-233.33333333333334)->(0.0,-233.33333333333334)
# (0.0,-233.33333333333334)->(-174.99999999999991,69.77555799122021)
# (-174.99999999999991,69.77555799122021)->(-350.00000000000006,-233.33333333333323)
# (-350.00000000000006,-233.33333333333323)->(-5.684341886080802e-14,-233.33333333333323)
# (-5.684341886080802e-14,-233.33333333333323)->(349.99999999999994,-233.33333333333323)
# (349.99999999999994,-233.33333333333323)->(175.00000000000003,69.77555799122032)
# (175.00000000000003,69.77555799122032)->(-1.1368683772161603e-13,-233.33333333333312)
# (-1.1368683772161603e-13,-233.33333333333312)->(-175.00000000000003,69.77555799122044)
# (-175.00000000000003,69.77555799122044)->(174.99999999999997,69.77555799122044)
# (174.99999999999997,69.77555799122044)->(5.684341886080802e-14,372.88444931577396)
# (5.684341886080802e-14,372.88444931577396)->(-175.00000000000009,69.77555799122052)
# (-175.00000000000009,69.77555799122052)->(-350.0000000000002,-233.33333333333292)
# """
#
# pup_ans = """\
# (-400.0,-300.0)->(-50.0,-300.0)
# (-50.0,-300.0)->(-224.99999999999991,3.1088913245535537)
# (-224.99999999999991,3.1088913245535537)->(-400.00000000000006,-299.9999999999999)
# (-400.00000000000006,-299.9999999999999)->(-50.00000000000006,-300.0)
# (-50.00000000000006,-300.0)->(299.99999999999994,-300.0000000000001)
# (299.99999999999994,-300.0000000000001)->(125.00000000000023,3.1088913245536105)
# (125.00000000000023,3.1088913245536105)->(-50.00000000000023,-299.9999999999996)
# (-50.00000000000023,-299.9999999999996)->(-224.99999999999994,3.108891324554122)
# (-224.99999999999994,3.108891324554122)->(125.00000000000006,3.1088913245540364)
# (125.00000000000006,3.1088913245540364)->(-49.99999999999966,306.21778264910773)
# (-49.99999999999966,306.21778264910773)->(-225.0000000000001,3.10889132455452)
# (-225.0000000000001,3.10889132455452)->(-400.00000000000057,-299.9999999999987)
# """

pup_ans = pup_ans.splitlines()
if not all('->' in row for row in pup_ans):
    error('Лишний вывод в stdin')

for i, row in enumerate(pup_ans):
    pup_ans[i] = list(map(lambda x: literal_eval(x.strip()), row.split('->')))

cor_ans = cor_ans.splitlines()
for i, row in enumerate(cor_ans):
    cor_ans[i] = list(map(lambda x: literal_eval(x.strip()), row.split('->')))


if len(cor_ans) == 0 == len(pup_ans):
    ok('Пусто -- ок')
elif len(pup_ans) == 0:
    error('Не нарисовано ни одного отрезка!')

# Ок. У нас есть два списка отрезков, нужно проверить, что они гомотетичны...

# segments = [[(0.0, 0.0), (100.0, 0.0)], [(100.0, 0.0), (0.0, -0.0)], [(0.0, -0.0), (100.0, 0.0)], [(100.0, 0.0), (50.0, -86.6)], [(50.0, -86.6), (-0.0, -0.0)], [(-0.0, -0.0), (100.0, 0.0)], [(100.0, 0.0), (100.0, -100.0)], [(100.0, -100.0), (0.0, -100.0)], [(0.0, -100.0), (-0.0, -0.0)], [(-0.0, -0.0), (100.0, -0.0)], [(100.0, -0.0), (130.9, -95.11)], [(130.9, -95.11), (50.0, -153.88)], [(50.0, -153.88), (-30.9, -95.11)], [(-30.9, -95.11), (-0.0, -0.0)], [(-0.0, -0.0), (100.0, -0.0)], [(100.0, -0.0), (150.0, -86.6)], [(150.0, -86.6), (100.0, -173.21)], [(100.0, -173.21), (0.0, -173.21)], [(0.0, -173.21), (-50.0, -86.6)], [(-50.0, -86.6), (-0.0, -0.0)], [(-0.0, -0.0), (100.0, 0.0)], [(100.0, 0.0), (162.35, -78.18)], [(162.35, -78.18), (140.1, -175.68)], [(140.1, -175.68), (50.0, -219.06)], [(50.0, -219.06), (-40.1, -175.68)], [(-40.1, -175.68), (-62.35, -78.18)], [(-62.35, -78.18), (-0.0, -0.0)]]
# segments = [[(0.0, 0.0), (100.0, 0.0)], [(100.0, 0.0), (200.0, -0.0)], [(50.0, -0.0), (150.0, 0.0)]]

def preprocess_segments(segments):
    # Делаем так, чтобы все отрезки «смотрели» направо, или хотя бы наверх.
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        if fx > tx - EPS or (abs(fx - tx) < EPS and fy > ty - EPS):
            segments[i] = [(tx, ty), (fx, fy)]
    # Сделаем так, чтобы никакие два отрезка нельзя было заменить одним другим отрезком.
    # Пока наивное решение за n**2 (и n**3 в худшем случае)
    i = 0
    while i < len(segments):
        (fx1, fy1), (tx1, ty1) = segments[i]
        dx1, dy1 = tx1 - fx1, ty1 - fy1
        j = i + 1
        while j < len(segments):
            (fx2, fy2), (tx2, ty2) = segments[j]
            dx2, dy2 = tx2 - fx2, ty2 - fy2
            # Если два отрезка лежат на одной прямой и пересекаются, то заменяем их на один отрезок
            if abs(dx1 * dy2 - dy1 * dx2) < EPS and abs(dx1 * (ty1 - fy2) - dy1 * (tx1 - fx2)) < EPS:
                # print(f'{i}-й и {j}-й коллинеарны, {segments[i]}, {segments[j]} ')
                # Два коллиниарных отрезка пересекаются тогда и только тогда,
                # когда пересекаются их проекции на оси Х и Y
                if max(fx1, tx1) >= min(fx2, tx2) - EPS and max(fx2, tx2) >= min(fx1, tx1) - EPS and \
                        max(fy1, ty1) >= min(fy2, ty2) - EPS and max(fy2, ty2) >= min(fy1, ty1) - EPS:
                    nfx, nfy = min([(fx2, fy2), (tx2, ty2), (fx1, fy1), (tx1, ty1)])
                    ntx, nty = max([(fx2, fy2), (tx2, ty2), (fx1, fy1), (tx1, ty1)])
                    segments[i] = [(nfx, nfy), (ntx, nty)]
                    # print(f'{i}-й и {j}-й пересекаются. Заменяем на {segments[i]}')
                    segments.pop(j)
                    break
            j += 1
        else:
            i += 1
    if DEBUG:
        print('После склеивания до масштабирования:')
        for i, ((fx, fy), (tx, ty)) in enumerate(segments):
            print('({:+05.2f},{:+05.2f}) -> ({:+05.2f},{:+05.2f})'.format(fx, fy, tx, ty))
        print('Получилось отрезков:', len(segments))
    # Подправим все точки так, чтобы центр масс был в (0,0),
    # а наиболее удалённая точка была на расстоянии 1000
    corr_x = sum(ans[0][0] + ans[1][0] for ans in segments) / 2 / len(segments)
    corr_y = sum(ans[0][1] + ans[1][1] for ans in segments) / 2 / len(segments)
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx - corr_x, fy - corr_y], [tx - corr_x, ty - corr_y]]
    max_dist = max(max(hypot(fx, fy), hypot(tx, ty)) for (fx, fy), (tx, ty) in segments)
    if max_dist == 0:
        error('В ответе только одна точка...')
    coeff = 1000 / max_dist
    for i, ((fx, fy), (tx, ty)) in enumerate(segments):
        segments[i] = [[fx * coeff, fy * coeff], [tx * coeff, ty * coeff]]


def find_best_dist(segments):
    dists = []
    for (fx, fy), (tx, ty) in segments:
        dists.append(hypot(fx, fy))
        dists.append(hypot(tx, ty))
    # Ищем радиус, у которого в EPS-окрестности минимальное кол-во точек
    best_rad = min(dists, key=lambda d1: sum(abs(d1 - d2) < EPS for d2 in dists))
    return best_rad


def find_rad_points(segments, rad):
    rad_points = []
    for (fx, fy), (tx, ty) in segments:
        if abs(hypot(fx, fy) - rad) < EPS:
            rad_points.append((fx, fy))
        if abs(hypot(tx, ty) - rad) < EPS:
            rad_points.append((tx, ty))
    # Теперь нужно удалить из rad_points дубликаты (расстояние между которыми меньше EPS)
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
    angles = []
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


for segments in (cor_ans, pup_ans):
    preprocess_segments(segments)
    if DEBUG: print('После масштабирования:', segments, sep='\n')


if len(cor_ans) != len(pup_ans):
    error('Количество непересекающихся отрезков в ответе {} не соответствует правильному {}', len(cor_ans), len(pup_ans))

best_rad = find_best_dist(cor_ans)
cor_rad_points = find_rad_points(cor_ans, best_rad)
pup_rad_points = find_rad_points(pup_ans, best_rad)
if DEBUG: print(best_rad, cor_rad_points, pup_rad_points, sep='\n*\n')

if len(cor_rad_points) != len(pup_rad_points):
    error('Картинку из ответа не удаётся перевести в правильную преобразованием подобия, '
          'не найдены точки на нужном расстоянии от центра масс')

test_angles = calc_test_angles(cor_rad_points, pup_rad_points)
for angle in test_angles:
    pup_ans_cp = deepcopy(pup_ans)
    rotate_everything(pup_ans_cp, angle)
    if two_segmset_eq(cor_ans, pup_ans_cp):
        ok('Всё верно!')

error('Картинку из ответа не удаётся перевести в правильную преобразованием подобия')
