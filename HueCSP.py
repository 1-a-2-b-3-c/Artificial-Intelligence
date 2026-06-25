import pygame
import copy
import time
from collections import deque
import random 

pygame.init()

WIDTH, HEIGHT = 1100, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bản Đồ Hành Chính Thừa Thiên Huế")

pygame.font.init()

try:
    font_label  = pygame.font.SysFont("Segoe UI", 13, bold=True)
    font_title  = pygame.font.SysFont("Segoe UI", 18, bold=True)
    font_h1     = pygame.font.SysFont("Segoe UI", 28, bold=True)
    font_body   = pygame.font.SysFont("Segoe UI", 14)
    font_small  = pygame.font.SysFont("Segoe UI", 12)
    font_stat   = pygame.font.SysFont("Segoe UI", 22, bold=True)
    font_section= pygame.font.SysFont("Segoe UI", 11)
    font_domain = pygame.font.SysFont("Segoe UI", 11, bold=True)
except:
    font_label  = pygame.font.SysFont(None, 14, bold=True)
    font_title  = pygame.font.SysFont(None, 20, bold=True)
    font_h1     = pygame.font.SysFont(None, 30, bold=True)
    font_body   = pygame.font.SysFont(None, 15)
    font_small  = pygame.font.SysFont(None, 13)
    font_stat   = pygame.font.SysFont(None, 24, bold=True)
    font_section= pygame.font.SysFont(None, 12)
    font_domain = pygame.font.SysFont(None, 13, bold=True)

C = {
    "bg_page":      (240, 244, 248),
    "bg_sidebar":   (255, 255, 255),
    "bg_card":      (246, 248, 250),
    "divider":      (220, 224, 230),
    "border":       (200, 208, 218),
    "text_primary": (28,  36,  50),
    "text_secondary":(100, 112, 128),
    "text_muted":   (150, 162, 178),

    "blue":   ((181, 212, 244), (24,  95, 165), (12,  68, 124)),
    "teal":   ((159, 225, 203), (15, 110,  86), ( 8,  80,  65)),
    "amber":  ((250, 199, 117), (133, 79,  11), ( 99, 56,   6)),
    "coral":  ((245, 196, 179), (153, 60,  29), (113, 43,  19)),
    "purple": ((206, 203, 246), ( 83, 74, 183), ( 60, 52, 137)),
    "green":  ((192, 221, 151), ( 59,109, 17),  ( 39, 80,  10)),
    "pink":   ((244, 192, 209), (153, 53,  86), (114, 36,  62)),

    "btn_blue":   ((230, 241, 251), (133, 183, 235), (12,  68, 124)),
    "btn_green":  ((234, 243, 222), (151, 196,  89), (39,  80,  10)),
    "btn_purple": ((237, 233, 250), (170, 156, 230), (60,  52, 137)),
    "btn_red":    ((252, 235, 235), (240, 149, 149), (121, 31,  31)),

    "badge_running": ((230, 241, 251), (12,  68, 124)),
    "badge_done":    ((234, 243, 222), (39,  80,  10)),
    "badge_idle":    ((246, 248, 250), (100,112, 128)),
    "badge_fail":    ((252, 235, 235), (121, 31,  31)),

    "progress_bg":  (220, 228, 236),
    "progress_fill":( 55,138, 221),
    "white":        (255, 255, 255),
}

COLOR_MAP = {
    "red":    "coral",
    "green":  "teal",
    "blue":   "blue",
    "yellow": "amber",
    "":       None,
}

variables = [
    "Phong Điền","Quảng Điền","A Lưới","Hương Trà",
    "TP Huế","Phú Vang","Hương Thủy","Nam Đông","Phú Lộc"
]

neighbors = {
    "Phong Điền": ["Quảng Điền","Hương Trà","A Lưới"],
    "Quảng Điền": ["Phong Điền","Hương Trà","TP Huế","Phú Vang"],
    "A Lưới":     ["Phong Điền","Hương Trà","Hương Thủy","Nam Đông"],
    "Hương Trà":  ["Phong Điền","Quảng Điền","A Lưới","TP Huế","Phú Vang","Hương Thủy"],
    "TP Huế":     ["Hương Trà","Quảng Điền","Phú Vang","Hương Thủy"],
    "Phú Vang":   ["Quảng Điền","Hương Trà","TP Huế","Hương Thủy","Phú Lộc"],
    "Hương Thủy": ["A Lưới","Hương Trà","TP Huế","Phú Vang","Nam Đông","Phú Lộc"],
    "Nam Đông":   ["A Lưới","Hương Thủy","Phú Lộc"],
    "Phú Lộc":    ["Phú Vang","Hương Thủy","Nam Đông"],
}
COLORS = ["red","green","blue","yellow"]

regions = {
    "Phong Điền": [(211, 109), (216, 112), (219, 114), (222, 118), (228, 122), (236, 130), (234, 136), (232, 141), (231, 145), (232, 155), (234, 159), (233, 164), (231, 173), (229, 180), (224, 187), (217, 191), (209, 192), (201, 194), (194, 201), (189, 212), (184, 215), (178, 219), (170, 224), (163, 229), (155, 227), (146, 226), (134, 228), (122, 233), (120, 228), (118, 224), (117, 213), (109, 216), (102, 219), (95, 222), (87, 225), (81, 228), (73, 231), (65, 235), (67, 226), (72, 215), (75, 205), (78, 198), (84, 189), (90, 178), (99, 164), (111, 152), (124, 144), (141, 136), (159, 130), (178, 122), (196, 116)],
    "Quảng Điền": [(211, 109), (222, 106), (233, 102), (242, 99), (256, 95), (270, 87), (281, 84), (294, 80), (300, 84), (307, 90), (316, 96), (325, 102), (332, 105), (337, 108), (339, 116), (342, 127), (346, 139), (348, 150), (351, 161), (353, 172), (342, 174), (330, 176), (318, 178), (307, 179), (293, 170), (279, 159), (268, 153), (256, 145), (246, 138), (236, 130), (228, 122), (222, 118), (216, 112)],
    "Hương Trà": [(236, 130), (246, 138), (256, 145), (268, 153), (279, 159), (293, 170), (307, 179), (303, 188), (300, 196), (296, 205), (293, 215), (302, 222), (312, 228), (324, 236), (337, 245), (348, 246), (358, 247), (368, 247), (379, 248), (380, 256), (381, 265), (381, 274), (381, 282), (370, 285), (358, 288), (348, 298), (339, 307), (330, 316), (322, 327), (309, 321), (296, 314), (284, 309), (275, 302), (268, 296), (263, 289), (247, 275), (231, 261), (220, 253), (210, 247), (212, 240), (215, 233), (223, 227), (231, 219), (230, 200), (229, 180), (231, 173), (233, 164), (232, 141)],
    "TP Huế": [(379, 248), (384, 247), (390, 246), (396, 245), (402, 245), (405, 253), (408, 261), (413, 272), (419, 285), (415, 292), (410, 299), (407, 306), (404, 311), (397, 307), (390, 302), (382, 296), (373, 290), (377, 286), (381, 282), (381, 274), (381, 265), (380, 256)],
    "Phú Vang": [(337, 108), (343, 114), (348, 122), (357, 143), (366, 164), (372, 168), (379, 173), (385, 178), (392, 184), (396, 196), (401, 210), (407, 226), (412, 240), (421, 253), (432, 265), (445, 281), (460, 297), (466, 305), (471, 311), (474, 319), (478, 327), (464, 320), (450, 311), (442, 305), (434, 298), (427, 291), (419, 285), (413, 272), (408, 261), (405, 253), (402, 245), (396, 245), (390, 246), (384, 247), (379, 248), (368, 247), (358, 247), (348, 246), (337, 245), (324, 236), (312, 228), (302, 222), (293, 215), (296, 205), (300, 196), (303, 188), (307, 179), (318, 178), (330, 176), (342, 174), (353, 172), (351, 161), (348, 150), (342, 127)],
    "A Lưới": [(65, 235), (73, 231), (81, 228), (87, 225), (95, 222), (102, 219), (109, 216), (117, 213), (118, 224), (120, 228), (122, 233), (134, 228), (146, 226), (155, 227), (163, 229), (170, 224), (178, 219), (184, 215), (189, 212), (194, 201), (201, 194), (217, 191), (224, 187), (229, 180), (230, 200), (231, 219), (223, 227), (215, 233), (212, 240), (210, 247), (220, 253), (231, 261), (247, 275), (263, 289), (268, 296), (275, 302), (284, 309), (296, 314), (309, 321), (322, 327), (320, 345), (316, 362), (313, 381), (312, 398), (290, 406), (270, 413), (247, 419), (224, 427), (204, 433), (184, 439), (167, 423), (150, 408), (134, 390), (118, 371), (97, 360), (76, 348), (60, 336), (45, 324), (49, 304), (53, 284), (55, 270), (58, 256)],
    "Hương Thủy": [(322, 327), (330, 316), (339, 307), (348, 298), (358, 288), (370, 285), (381, 282), (377, 286), (373, 290), (382, 296), (390, 302), (397, 307), (404, 311), (407, 306), (410, 299), (415, 292), (419, 285), (427, 291), (434, 298), (442, 305), (450, 311), (464, 320), (478, 327), (484, 328), (491, 330), (499, 332), (506, 334), (496, 353), (487, 371), (475, 390), (464, 408), (450, 431), (436, 455), (410, 462), (385, 468), (367, 472), (348, 476), (339, 478), (331, 481), (325, 461), (318, 441), (314, 419), (312, 398), (313, 381), (316, 362), (320, 345)],
    "Nam Đông": [(331, 481), (339, 478), (348, 476), (367, 472), (385, 468), (410, 462), (436, 455), (450, 459), (464, 464), (478, 466), (491, 468), (503, 471), (514, 474), (511, 494), (508, 514), (503, 540), (499, 566), (473, 573), (445, 582), (422, 587), (399, 593), (384, 596), (370, 600), (358, 587), (346, 574), (338, 560), (331, 548), (327, 531), (324, 514), (327, 498)],
    "Phú Lộc": [(478, 327), (487, 337), (496, 348), (508, 356), (520, 363), (531, 365), (542, 367), (550, 370), (558, 373), (573, 383), (588, 394), (610, 406), (632, 418), (651, 425), (671, 431), (693, 435), (713, 438), (724, 431), (735, 426), (729, 430), (722, 436), (710, 443), (699, 450), (687, 458), (676, 466), (664, 463), (653, 459), (642, 454), (632, 450), (608, 454), (584, 459), (561, 464), (538, 469), (526, 471), (514, 474), (503, 471), (491, 468), (478, 466), (464, 464), (450, 459), (436, 455), (450, 431), (464, 408), (475, 390), (487, 371), (496, 353), (506, 334), (499, 332), (491, 330), (484, 328)],
}

label_pos = {
    "Phong Điền": (160, 183),
    "Quảng Điền": (290, 126),
    "Hương Trà":  (292, 236),
    "TP Huế":     (394, 276),
    "Phú Vang":   (381, 226),
    "A Lưới":     (181, 284),
    "Hương Thủy": (398, 354),
    "Nam Đông":   (413, 518),
    "Phú Lộc":    (572, 415),
}

assignment   = {v: "" for v in variables}
steps        = []
node_count   = 0
elapsed      = 0.0
algorithm_name = "Chưa chọn"
current_step = 0
animating    = False
anim_speed   = 150   

ac3_domains  = None      
ac3_result   = None     

def reset():
    global assignment, steps, node_count, elapsed, algorithm_name, current_step, animating
    global ac3_domains, ac3_result
    assignment     = {v: "" for v in variables}
    steps          = []
    node_count     = 0
    elapsed        = 0.0
    algorithm_name = "Chưa chọn"
    current_step   = 0
    animating      = False
    ac3_domains    = None
    ac3_result     = None

def is_consistent(region, color, assign):
    return all(assign[nb] != color for nb in neighbors[region])

def count_conflicts(region, color, assign):
    conflicts = 0

    for nb in neighbors[region]:
        if assign[nb] == color:
            conflicts += 1

    return conflicts

def first_unassigned(assign):
    for v in variables:
        if assign[v] == "": return v
    return None

def backtracking(assign):
    global node_count, steps
    node_count += 1
    if all(assign[v] != "" for v in variables): return True
    var = first_unassigned(assign)
    for color in COLORS:
        if is_consistent(var, color, assign):
            assign[var] = color
            steps.append(copy.deepcopy(assign))
            if backtracking(assign): return True
            assign[var] = ""
            steps.append(copy.deepcopy(assign))
    return False

def forward_checking(assign, domains):
    global node_count, steps
    node_count += 1
    if all(assign[v] != "" for v in variables): return True
    var = first_unassigned(assign)
    for color in domains[var][:]:
        if is_consistent(var, color, assign):
            saved = copy.deepcopy(domains)
            assign[var] = color
            steps.append(copy.deepcopy(assign))
            fail = any(
                assign[nb] == "" and color in domains[nb] and len([c for c in domains[nb] if c != color]) == 0
                for nb in neighbors[var]
            )
            if not fail:
                for nb in neighbors[var]:
                    if assign[nb] == "" and color in domains[nb]:
                        domains[nb].remove(color)
                if forward_checking(assign, domains): return True
            assign[var] = ""
            steps.append(copy.deepcopy(assign))
            domains = saved
    return False

def ac3(domains):
    """
    AC-3 algorithm (theo mã giả AIMA).
    domains: dict {var: [colors...]}  -- sẽ bị sửa tại chỗ (in-place).
    Trả về True nếu mọi domain vẫn còn giá trị (consistent / arc-consistent),
    False nếu có domain bị rỗng (CSP chắc chắn vô nghiệm).
    """
    queue = deque()
    for xi in variables:
        for xj in neighbors[xi]:
            queue.append((xi, xj))

    def rm_inconsistent_values(xi, xj):
        removed = False
        for x in domains[xi][:]:
            if not any(x != y for y in domains[xj]):
                domains[xi].remove(x)
                removed = True
        return removed

    while queue:
        xi, xj = queue.popleft()           
        if rm_inconsistent_values(xi, xj):
            if len(domains[xi]) == 0:
                return False                
            for xk in neighbors[xi]:
                queue.append((xk, xi))      

    return True

def min_conflicts(max_steps=1000):
    global node_count, steps

    node_count = 0
    steps = []

    current = {v: random.choice(COLORS) for v in variables}
    steps.append(copy.deepcopy(current))

    for _ in range(max_steps):
        node_count += 1

        conflicted = []

        for var in variables:
            if count_conflicts(var, current[var], current) > 0:
                conflicted.append(var)

        if not conflicted:
            assignment.update(current)
            return True

        var = random.choice(conflicted)

        min_conflict = float("inf")
        best_colors = []

        for color in COLORS:
            conflicts = count_conflicts(var, color, current)

            if conflicts < min_conflict:
                min_conflict = conflicts
                best_colors = [color]

            elif conflicts == min_conflict:
                best_colors.append(color)

        current[var] = random.choice(best_colors)

        steps.append(copy.deepcopy(current))

    return False

SIDEBAR_X  = 770
SIDEBAR_W  = 330

def draw_rounded_rect(surf, color, rect, radius=8, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, width=border, border_radius=radius)

def draw_text(surf, text, font, color, x, y, align="left", max_width=None):
    surf2 = font.render(text, True, color)
    if align == "center":
        x -= surf2.get_width() // 2
    elif align == "right":
        x -= surf2.get_width()
    surf.blit(surf2, (x, y))
    return surf2.get_width()

def draw_section_label(surf, text, y):
    t = font_section.render(text.upper(), True, C["text_muted"])
    surf.blit(t, (SIDEBAR_X + 20, y))
    return y + t.get_height() + 6

def draw_button(surf, rect, label, scheme, hovered):
    fill, border, text_c = scheme
    bg = tuple(max(0, c - 15) for c in fill) if hovered else fill
    draw_rounded_rect(surf, bg, rect, radius=8, border=1, border_color=border)
    draw_text(surf, label, font_body, text_c,
              rect.centerx, rect.centery - font_body.get_height()//2, align="center")

def draw_stat_card(surf, rect, label, value):
    draw_rounded_rect(surf, C["bg_card"], rect, radius=8)
    draw_text(surf, label, font_small, C["text_secondary"], rect.x + 10, rect.y + 8)
    draw_text(surf, value, font_stat, C["text_primary"], rect.x + 10, rect.y + 26)

def draw_badge(surf, text, x, y, scheme):
    bg, fg = scheme
    t = font_small.render(text, True, fg)
    pad_x, pad_y = 10, 4
    r = pygame.Rect(x, y, t.get_width() + pad_x*2, t.get_height() + pad_y*2)
    draw_rounded_rect(surf, bg, r, radius=r.height//2)
    surf.blit(t, (x + pad_x, y + pad_y))
    return r.width

def get_region_fill(color_name):
    key = COLOR_MAP.get(color_name)
    if key is None:
        return C["white"], C["border"]
    fill, border, _ = C[key]
    return fill, border

def get_label_color(color_name):
    key = COLOR_MAP.get(color_name)
    if key is None:
        return C["text_primary"]
    _, _, lbl = C[key]
    return lbl

btn_bt    = pygame.Rect(SIDEBAR_X + 16, 100, SIDEBAR_W - 32, 40)
btn_fc    = pygame.Rect(SIDEBAR_X + 16, 148, SIDEBAR_W - 32, 40)
btn_ac3   = pygame.Rect(SIDEBAR_X + 16, 196, SIDEBAR_W - 32, 40)
btn_mc    = pygame.Rect(SIDEBAR_X + 16, 244, SIDEBAR_W - 32, 40)
btn_reset = pygame.Rect(SIDEBAR_X + 16, 292, SIDEBAR_W - 32, 40)

slider_rect      = pygame.Rect(SIDEBAR_X + 16, 318, SIDEBAR_W - 32, 14)
slider_drag      = False
slider_hit_rect  = slider_rect.inflate(0, 20)   
track_rect       = pygame.Rect(SIDEBAR_X + 16, 318, SIDEBAR_W - 32, 6)  
SPEED_MIN, SPEED_MAX = 30, 600   

def speed_to_x(spd):
    ratio = (spd - SPEED_MIN) / (SPEED_MAX - SPEED_MIN)
    return track_rect.x + int(ratio * track_rect.width)

def x_to_speed(x):
    ratio = (x - track_rect.x) / track_rect.width
    ratio = max(0.0, min(1.0, ratio))
    return int(SPEED_MIN + ratio * (SPEED_MAX - SPEED_MIN))

LEGEND = [
    ("Màu 1", "blue"),
    ("Màu 2", "teal"),
    ("Màu 3", "amber"),
    ("Màu 4", "coral"),
]

clock        = pygame.time.Clock()
last_update  = pygame.time.get_ticks()
running      = True

while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_bt.collidepoint(event.pos):
                reset()
                start = time.perf_counter()
                backtracking(assignment)
                elapsed = time.perf_counter() - start
                algorithm_name = "Backtracking"
                animating    = True
                current_step = 0
                last_update  = pygame.time.get_ticks()

            elif btn_fc.collidepoint(event.pos):
                reset()
                domains = {v: list(COLORS) for v in variables}
                start = time.perf_counter()
                forward_checking(assignment, domains)
                elapsed = time.perf_counter() - start
                algorithm_name = "Forward Checking"
                animating    = True
                current_step = 0
                last_update  = pygame.time.get_ticks()

            elif btn_ac3.collidepoint(event.pos):
                reset()
                domains = {v: list(COLORS) for v in variables}
                start = time.perf_counter()
                ok = ac3(domains)
                elapsed = time.perf_counter() - start
                algorithm_name = "AC-3"
                ac3_domains = domains
                ac3_result  = ok
                
                for v in variables:
                    if len(domains[v]) == 1:
                        assignment[v] = domains[v][0]
                node_count   = len(variables)  
                                                
                steps        = [copy.deepcopy(assignment)]
                animating    = False
                current_step = 1

            elif btn_mc.collidepoint(event.pos):
                reset()

                start = time.perf_counter()
                min_conflicts(max_steps=1000)
                elapsed = time.perf_counter() - start

                algorithm_name = "Min-Conflicts"

                animating = True
                current_step = 0
                last_update = pygame.time.get_ticks()

            elif btn_reset.collidepoint(event.pos):
                reset()

            if slider_hit_rect.collidepoint(event.pos):
                slider_drag = True
                anim_speed  = max(SPEED_MIN, min(SPEED_MAX, x_to_speed(mx)))

        if event.type == pygame.MOUSEBUTTONUP:
            slider_drag = False

        if event.type == pygame.MOUSEMOTION and slider_drag:
            anim_speed = max(SPEED_MIN, min(SPEED_MAX, x_to_speed(mx)))

    display_assign = assignment
    if animating and steps:
        display_assign = steps[min(current_step, len(steps) - 1)]
        if pygame.time.get_ticks() - last_update > anim_speed:
            current_step += 1
            last_update = pygame.time.get_ticks()
        if current_step >= len(steps):
            animating = False

    screen.fill(C["bg_page"])

    for region, pts in regions.items():
        fill, border = get_region_fill(display_assign[region])

        shadow = [(x + 3, y + 3) for x, y in pts]
        pygame.draw.polygon(screen, (210, 216, 226), shadow)
        pygame.draw.polygon(screen, fill,   pts)
        pygame.draw.polygon(screen, border, pts, 2)

    for region, (lx, ly) in label_pos.items():
        lc = get_label_color(display_assign[region])
        t  = font_label.render(region, True, lc)

        domain_suffix = None
        if ac3_domains is not None and display_assign[region] == "":
            dsize = len(ac3_domains[region])
            domain_suffix = f"({dsize})"

        if domain_suffix:
            t_suffix = font_domain.render(domain_suffix, True, C["text_secondary"])
            total_w = t.get_width() + 4 + t_suffix.get_width()
        else:
            total_w = t.get_width()

        bg = pygame.Rect(lx - total_w//2 - 5, ly - 3, total_w + 10, t.get_height() + 6)
        pygame.draw.rect(screen, (255, 255, 255, 180), bg, border_radius=4)
        pygame.draw.rect(screen, C["divider"], bg, width=1, border_radius=4)

        tx = lx - total_w//2
        screen.blit(t, (tx, ly))
        if domain_suffix:
            screen.blit(t_suffix, (tx + t.get_width() + 4, ly + 1))

    title_bg = pygame.Rect(24, 20, 320, 58)
    draw_rounded_rect(screen, C["white"], title_bg, radius=10, border=1, border_color=C["divider"])
    draw_text(screen, "THỪA THIÊN HUẾ", font_h1, (200, 40, 40), 32, 26)
    draw_text(screen, "Bản đồ hành chính  ·  Tô màu CSP", font_small, C["text_secondary"], 32, 56)

    sidebar_bg = pygame.Rect(SIDEBAR_X, 0, SIDEBAR_W, HEIGHT)
    pygame.draw.rect(screen, C["bg_sidebar"], sidebar_bg)
    pygame.draw.line(screen, C["divider"], (SIDEBAR_X, 0), (SIDEBAR_X, HEIGHT), 1)

    sy = 20

    draw_text(screen, "Điều khiển", font_title, C["text_primary"], SIDEBAR_X + 20, sy)
    sy += 36

    sy = draw_section_label(screen, "Thuật toán", sy)
    draw_button(screen, btn_bt,    "Chạy Backtracking",   C["btn_blue"],   btn_bt.collidepoint(mx, my))
    draw_button(screen, btn_fc,    "Forward Checking",    C["btn_green"],  btn_fc.collidepoint(mx, my))
    draw_button(screen, btn_ac3,   "Chạy AC-3",           C["btn_purple"], btn_ac3.collidepoint(mx, my))
    draw_button(screen, btn_mc,    "Min-Conflicts",       C["btn_purple"], btn_mc.collidepoint(mx, my))
    draw_button(screen, btn_reset, "Đặt lại bản đồ",      C["btn_red"],    btn_reset.collidepoint(mx, my))
    sy = btn_reset.bottom + 16

    pygame.draw.line(screen, C["divider"], (SIDEBAR_X + 16, sy), (SIDEBAR_X + SIDEBAR_W - 16, sy), 1)
    sy += 10

    sy = draw_section_label(screen, "Tốc độ mô phỏng", sy)
    draw_text(screen, "Nhanh", font_small, C["text_muted"], SIDEBAR_X + 16, sy)
    draw_text(screen, "Chậm",  font_small, C["text_muted"], SIDEBAR_X + SIDEBAR_W - 16, sy, align="right")
    sy += 16

    track_rect = pygame.Rect(SIDEBAR_X + 16, sy + 3, SIDEBAR_W - 32, 6)
    slider_hit_rect = track_rect.inflate(0, 20)
    pygame.draw.rect(screen, C["progress_bg"], track_rect, border_radius=3)

    knob_x = speed_to_x(anim_speed)
    fill_w2 = knob_x - track_rect.x
    if fill_w2 > 0:
        pygame.draw.rect(screen, C["progress_fill"],
                         (track_rect.x, sy + 3, fill_w2, 6), border_radius=3)

    pygame.draw.circle(screen, C["white"], (knob_x, sy + 6), 9)
    pygame.draw.circle(screen, C["progress_fill"], (knob_x, sy + 6), 9, 2)
    sy += 24

    pygame.draw.line(screen, C["divider"], (SIDEBAR_X + 16, sy), (SIDEBAR_X + SIDEBAR_W - 16, sy), 1)
    sy += 10

    sy = draw_section_label(screen, "Thống kê", sy)

    card_w  = (SIDEBAR_W - 48) // 2
    card_h  = 54
    card_y  = sy
    draw_stat_card(screen, pygame.Rect(SIDEBAR_X + 16, card_y, card_w, card_h),
                   "Số nút duyệt", str(node_count))
    draw_stat_card(screen, pygame.Rect(SIDEBAR_X + 16 + card_w + 16, card_y, card_w, card_h),
                   "Số bước", str(len(steps)))
    sy = card_y + card_h + 8
    wide_rect = pygame.Rect(SIDEBAR_X + 16, sy, SIDEBAR_W - 32, card_h)
    draw_stat_card(screen, wide_rect, "Thời gian",
                   f"{elapsed:.6f} s" if elapsed else "—")
    sy = wide_rect.bottom + 8

    draw_text(screen, "Thuật toán:", font_small, C["text_secondary"], SIDEBAR_X + 16, sy + 2)
    t2 = font_body.render(algorithm_name, True, C["text_primary"])
    screen.blit(t2, (SIDEBAR_X + 16 + 90, sy))
    sy += 20

    if ac3_result is not None:
        draw_text(screen, "Kết quả AC-3:", font_small, C["text_secondary"], SIDEBAR_X + 16, sy + 2)
        result_text = "Arc-consistent" if ac3_result else "Vô nghiệm (domain rỗng)"
        result_scheme = C["badge_done"] if ac3_result else C["badge_fail"]
        draw_badge(screen, result_text, SIDEBAR_X + 16 + 90, sy - 3, result_scheme)
        sy += 24

    pygame.draw.line(screen, C["divider"], (SIDEBAR_X + 16, sy), (SIDEBAR_X + SIDEBAR_W - 16, sy), 1)
    sy += 10

    sy = draw_section_label(screen, "Tiến độ", sy)

    total = len(steps)
    prog  = current_step / total if total > 0 else 0.0
    step_label = f"{min(current_step, total)} / {total}" if total else "—"

    if animating:
        badge_scheme = C["badge_running"]
        badge_text   = "Đang chạy"
    elif total > 0:
        badge_scheme = C["badge_done"]
        badge_text   = "Hoàn thành"
    else:
        badge_scheme = C["badge_idle"]
        badge_text   = "Chờ"

    draw_badge(screen, badge_text, SIDEBAR_X + 16, sy, badge_scheme)
    draw_text(screen, step_label, font_small, C["text_secondary"],
              SIDEBAR_X + SIDEBAR_W - 16, sy + 4, align="right")
    sy += 24

    bar_rect = pygame.Rect(SIDEBAR_X + 16, sy, SIDEBAR_W - 32, 6)
    pygame.draw.rect(screen, C["progress_bg"], bar_rect, border_radius=3)
    fw = int(bar_rect.width * prog)
    if fw > 0:
        pygame.draw.rect(screen, C["progress_fill"],
                         (bar_rect.x, sy, fw, 6), border_radius=3)
    sy = bar_rect.bottom + 12

    pygame.draw.line(screen, C["divider"], (SIDEBAR_X + 16, sy), (SIDEBAR_X + SIDEBAR_W - 16, sy), 1)
    sy += 10

    sy = draw_section_label(screen, "Chú thích màu", sy)
    per_row = 2
    item_w  = (SIDEBAR_W - 32) // per_row
    for i, (lbl, key) in enumerate(LEGEND):
        col = i % per_row
        row = i // per_row
        ix = SIDEBAR_X + 16 + col * item_w
        iy = sy + row * 22
        fill, border, text_c = C[key]
        pygame.draw.rect(screen, fill,   (ix, iy + 2, 14, 14), border_radius=3)
        pygame.draw.rect(screen, border, (ix, iy + 2, 14, 14), width=1, border_radius=3)
        draw_text(screen, lbl, font_small, C["text_secondary"], ix + 20, iy + 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()