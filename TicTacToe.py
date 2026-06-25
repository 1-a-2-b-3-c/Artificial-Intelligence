import pygame
import sys
import random

pygame.init()

W, H = 520, 660
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

try:
    FONT_TITLE  = pygame.font.SysFont("segoeui", 30, bold=True)
    FONT_LABEL  = pygame.font.SysFont("segoeui", 18)
    FONT_SMALL  = pygame.font.SysFont("segoeui", 15)
    FONT_CELL   = pygame.font.SysFont("segoeui", 72, bold=True)
    FONT_STATUS = pygame.font.SysFont("segoeui", 20, bold=True)
except:
    FONT_TITLE  = pygame.font.Font(None, 36)
    FONT_LABEL  = pygame.font.Font(None, 24)
    FONT_SMALL  = pygame.font.Font(None, 20)
    FONT_CELL   = pygame.font.Font(None, 90)
    FONT_STATUS = pygame.font.Font(None, 26)

BG         = (245, 244, 240)
WHITE      = (255, 255, 255)
BORDER     = (200, 198, 190)
BORDER_SEL = (55, 138, 221)
TEXT_PRI   = (30, 30, 28)
TEXT_SEC   = (120, 118, 110)
BLUE_BG    = (230, 241, 251)
BLUE_TEXT  = (24, 95, 165)
CORAL      = (216, 90, 48)
BLUE       = (55, 138, 221)
GREEN_BG   = (234, 243, 222)
GREEN_TEXT = (59, 109, 17)
RED_BG     = (252, 235, 235)
RED_TEXT   = (163, 45, 45)
GRAY_BG    = (241, 239, 232)
WIN_BG     = (230, 241, 251)
BTN_HOVER  = (235, 234, 228)
PURPLE_BG  = (243, 237, 255)
PURPLE_BD  = (160, 120, 220)
PURPLE_TX  = (90, 40, 160)

# ═══════════════════════════════════════════════════════
#  THUẬT TOÁN
# ═══════════════════════════════════════════════════════

def check_result(board):
    for row in board:
        if row[0] != " " and row[0] == row[1] == row[2]:
            return row[0]
    for i in range(3):
        if board[0][i] != " " and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[1][1] != " ":
        if (board[0][0] == board[1][1] == board[2][2]) or \
           (board[0][2] == board[1][1] == board[2][0]):
            return board[1][1]
    return " "

def utility(board, ai_sym, pl_sym):
    w = check_result(board)
    if w == ai_sym: return 1
    if w == pl_sym: return -1
    return 0

def actions(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

# ── Minimax ──────────────────────────────────────────

def max_value(board, ai_sym, pl_sym):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    if not actions(board): return 0
    v = float("-inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        v = max(v, min_value(board, ai_sym, pl_sym))
        board[r][c] = " "
    return v

def min_value(board, ai_sym, pl_sym):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    if not actions(board): return 0
    v = float("inf")
    for r, c in actions(board):
        board[r][c] = pl_sym
        v = min(v, max_value(board, ai_sym, pl_sym))
        board[r][c] = " "
    return v

def minimax(board, ai_sym, pl_sym):
    best_move, best_val = None, float("-inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        val = min_value(board, ai_sym, pl_sym)
        board[r][c] = " "
        if val > best_val:
            best_val = val
            best_move = (r, c)
    return best_move

# ── Alpha-Beta ───────────────────────────────────────

def max_value_ab(board, ai_sym, pl_sym, alpha, beta):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    if not actions(board): return 0
    v = float("-inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        v = max(v, min_value_ab(board, ai_sym, pl_sym, alpha, beta))
        board[r][c] = " "
        alpha = max(alpha, v)
        if alpha >= beta: break
    return v

def min_value_ab(board, ai_sym, pl_sym, alpha, beta):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    if not actions(board): return 0
    v = float("inf")
    for r, c in actions(board):
        board[r][c] = pl_sym
        v = min(v, max_value_ab(board, ai_sym, pl_sym, alpha, beta))
        board[r][c] = " "
        beta = min(beta, v)
        if alpha >= beta: break
    return v

def minimax_ab(board, ai_sym, pl_sym):
    best_move, best_val = None, float("-inf")
    alpha, beta = float("-inf"), float("inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        val = min_value_ab(board, ai_sym, pl_sym, alpha, beta)
        board[r][c] = " "
        if val > best_val:
            best_val = val
            best_move = (r, c)
        alpha = max(alpha, best_val)
    return best_move

# ── Expectimax ───────────────────────────────────────

def max_value_ex(board, ai_sym, pl_sym):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    if not actions(board): return 0
    v = float("-inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        v = max(v, chance_node(board, ai_sym, pl_sym))
        board[r][c] = " "
    return v

def chance_node(board, ai_sym, pl_sym):
    if check_result(board) != " ": return utility(board, ai_sym, pl_sym)
    available = actions(board)
    if not available: return 0
    total = 0
    for r, c in available:
        board[r][c] = pl_sym
        total += max_value_ex(board, ai_sym, pl_sym)
        board[r][c] = " "
    return total / len(available)

def expectimax(board, ai_sym, pl_sym):
    best_move, best_val = None, float("-inf")
    for r, c in actions(board):
        board[r][c] = ai_sym
        val = chance_node(board, ai_sym, pl_sym)
        board[r][c] = " "
        if val > best_val:
            best_val = val
            best_move = (r, c)
    return best_move

# ═══════════════════════════════════════════════════════
#  HELPERS VẼ
# ═══════════════════════════════════════════════════════

def draw_rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_text_center(surf, text, font, color, cx, cy):
    s = font.render(text, True, color)
    surf.blit(s, (cx - s.get_width()//2, cy - s.get_height()//2))

def draw_text_left(surf, text, font, color, x, y):
    surf.blit(font.render(text, True, color), (x, y))

# ═══════════════════════════════════════════════════════
#  TRẠNG THÁI
# ═══════════════════════════════════════════════════════

STATE_SETUP = "setup"
STATE_GAME  = "game"
state = STATE_SETUP

selected_algo  = "minimax"   # "minimax" | "alphabeta" | "expectimax"
selected_first = "player"    # "player"  | "ai"

game_board    = None
current_turn  = "X"
game_over     = False
winner_symbol = None
p_symbol      = "X"
a_symbol      = "O"
ai_goes_first = False
pending_ai    = False

PAD        = 28
BADGE_TOP  = 10
STATUS_TOP = 70
BOARD_TOP  = 116
CELL_SIZE  = 148

def cell_rect(r, c):
    board_left = (W - CELL_SIZE * 3) // 2
    return pygame.Rect(board_left + c * CELL_SIZE,
                       BOARD_TOP  + r * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)

def get_winner_cells(b):
    lines = [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
    ]
    for line in lines:
        syms = [b[r][c] for r, c in line]
        if syms[0] != " " and syms[0] == syms[1] == syms[2]:
            return line
    return []

def reset_board():
    global game_board, current_turn, game_over, winner_symbol, pending_ai
    game_board    = [[" "]*3 for _ in range(3)]
    current_turn  = "X"
    game_over     = False
    winner_symbol = None
    pending_ai    = False

def do_place(sym, r, c):
    global game_over, winner_symbol, current_turn
    game_board[r][c] = sym
    w = check_result(game_board)
    if w != " ":
        game_over = True; winner_symbol = w; return True
    if not actions(game_board):
        game_over = True; return True
    current_turn = "O" if sym == "X" else "X"
    return False

def do_ai_move():
    global pending_ai
    pending_ai = False
    if game_over: return
    if selected_algo == "alphabeta":
        move = minimax_ab(game_board, a_symbol, p_symbol)
    elif selected_algo == "expectimax":
        move = expectimax(game_board, a_symbol, p_symbol)
    else:
        move = minimax(game_board, a_symbol, p_symbol)
    if move:
        do_place(a_symbol, move[0], move[1])

def do_random_move():
    """Người chơi đi ngẫu nhiên (dùng cho Expectimax)."""
    global pending_ai
    available = actions(game_board)
    if available and not game_over:
        r, c = random.choice(available)
        ended = do_place(p_symbol, r, c)
        if not ended:
            pending_ai = True

def start_game():
    global state, p_symbol, a_symbol, ai_goes_first
    ai_goes_first = (selected_first == "ai")
    if ai_goes_first:
        a_symbol = "X"; p_symbol = "O"
    else:
        p_symbol = "X"; a_symbol = "O"
    reset_board()
    state = STATE_GAME
    if ai_goes_first:
        global pending_ai
        pending_ai = True

# ═══════════════════════════════════════════════════════
#  NÚT BẤM
# ═══════════════════════════════════════════════════════

class Button:
    def __init__(self, rect, label, value):
        self.rect  = pygame.Rect(rect)
        self.label = label
        self.value = value

    def draw(self, surf, selected):
        active = (selected == self.value)
        bg = BLUE_BG    if active else WHITE
        tc = BLUE_TEXT  if active else TEXT_PRI
        bc = BORDER_SEL if active else BORDER
        draw_rounded_rect(surf, bg, self.rect, radius=8,
                          border=2 if active else 1, border_color=bc)
        draw_text_center(surf, self.label, FONT_LABEL, tc,
                         self.rect.centerx, self.rect.centery)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

# Setup — 3 thuật toán, mỗi nút rộng hơn
_aw = (W - PAD*2 - 16) // 3
algo_buttons = [
    Button((PAD,              130, _aw, 42), "Minimax",     "minimax"),
    Button((PAD + _aw + 8,    130, _aw, 42), "Alpha-Beta",  "alphabeta"),
    Button((PAD + (_aw+8)*2,  130, _aw, 42), "Expectimax",  "expectimax"),
]
first_buttons = [
    Button((PAD,       240, 220, 42), "Người chơi (X)", "player"),
    Button((PAD+228,   240, 220, 42), "AI (X)",          "ai"),
]

# Game — nút dưới bàn cờ
_btn_top  = BOARD_TOP + CELL_SIZE * 3 + 10
_btn_w    = (W - PAD*2 - 10) // 2
reset_btn  = pygame.Rect(PAD,              _btn_top, _btn_w, 42)
back_btn   = pygame.Rect(PAD + _btn_w + 10, _btn_top, _btn_w, 42)

# Nút random (chỉ hiện khi Expectimax + lượt người)
_rand_top = _btn_top + 52
random_btn = pygame.Rect(PAD, _rand_top, W - PAD*2, 40)

# ═══════════════════════════════════════════════════════
#  VẼ MÀN HÌNH
# ═══════════════════════════════════════════════════════

def draw_setup(mx, my):
    screen.fill(BG)
    draw_text_center(screen, "Tic-Tac-Toe", FONT_TITLE, TEXT_PRI, W//2, 50)
    draw_text_left(screen, "Thuật toán AI", FONT_LABEL, TEXT_SEC, PAD, 104)
    for btn in algo_buttons:
        btn.draw(screen, selected_algo)
    draw_text_left(screen, "Ai đi trước?", FONT_LABEL, TEXT_SEC, PAD, 214)
    for btn in first_buttons:
        btn.draw(screen, selected_first)
    sr = pygame.Rect(PAD, 310, W-PAD*2, 46)
    bg = BTN_HOVER if sr.collidepoint(mx, my) else WHITE
    draw_rounded_rect(screen, bg, sr, radius=8, border=1, border_color=BORDER)
    draw_text_center(screen, "▶  Bắt đầu", FONT_STATUS, TEXT_PRI, sr.centerx, sr.centery)
    return sr

def draw_game(mx, my):
    screen.fill(BG)

    # Badges
    algo_name = {"minimax": "Minimax", "alphabeta": "Alpha-Beta",
                 "expectimax": "Expectimax"}[selected_algo]
    badges = [(algo_name, "Thuật toán"),
              ("AI" if ai_goes_first else "Người", "Đi trước"),
              (p_symbol, "Ký hiệu bạn")]
    bw = (W - PAD*2 - 16) // 3
    for i, (val, lbl) in enumerate(badges):
        bx = PAD + i * (bw + 8)
        draw_rounded_rect(screen, GRAY_BG, pygame.Rect(bx, BADGE_TOP, bw, 50), radius=8)
        draw_text_center(screen, val, FONT_LABEL, TEXT_PRI, bx+bw//2, BADGE_TOP+15)
        draw_text_center(screen, lbl, FONT_SMALL, TEXT_SEC, bx+bw//2, BADGE_TOP+37)

    # Status bar
    if game_over:
        if winner_symbol:
            is_win = (winner_symbol == p_symbol)
            sbg = GREEN_BG if is_win else RED_BG
            stc = GREEN_TEXT if is_win else RED_TEXT
            msg = "Bạn thắng! 🎉" if is_win else "AI thắng!"
        else:
            sbg, stc, msg = GRAY_BG, TEXT_SEC, "Hòa! Không ai thắng."
    else:
        sbg, stc = BLUE_BG, BLUE_TEXT
        if current_turn == p_symbol:
            msg = f"Lượt của bạn ({p_symbol})"
        else:
            msg = "AI đang suy nghĩ..."

    draw_rounded_rect(screen, sbg, pygame.Rect(PAD, STATUS_TOP, W-PAD*2, 38), radius=8)
    draw_text_center(screen, msg, FONT_STATUS, stc, W//2, STATUS_TOP+19)

    # Bàn cờ
    win_cells = get_winner_cells(game_board) if (game_over and winner_symbol) else []
    for r in range(3):
        for c in range(3):
            rect = cell_rect(r, c)
            is_win = (r, c) in win_cells
            draw_rounded_rect(screen, WIN_BG if is_win else WHITE, rect, radius=10,
                              border=2 if is_win else 1,
                              border_color=BORDER_SEL if is_win else BORDER)
            sym = game_board[r][c]
            if sym != " ":
                draw_text_center(screen, sym, FONT_CELL,
                                 BLUE if sym == "X" else CORAL,
                                 rect.centerx, rect.centery)

    # Nút Reset & Back
    for btn_rect, label in [(back_btn, "← Cài đặt"), (reset_btn, "↺  Chơi lại")]:
        bg = BTN_HOVER if btn_rect.collidepoint(mx, my) else WHITE
        draw_rounded_rect(screen, bg, btn_rect, radius=8, border=1, border_color=BORDER)
        draw_text_center(screen, label, FONT_LABEL, TEXT_SEC,
                         btn_rect.centerx, btn_rect.centery)

    # Nút Random — chỉ hiện khi Expectimax + lượt người + chưa kết thúc
    if selected_algo == "expectimax" and not game_over and current_turn == p_symbol:
        is_hov = random_btn.collidepoint(mx, my)
        rbg = PURPLE_BG
        draw_rounded_rect(screen, rbg, random_btn, radius=8,
                          border=2, border_color=PURPLE_BD)
        draw_text_center(screen, "🎲  Đi ngẫu nhiên", FONT_LABEL, PURPLE_TX,
                         random_btn.centerx, random_btn.centery)

# ═══════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════

while True:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if state == STATE_SETUP:
                for btn in algo_buttons:
                    if btn.hit(event.pos):
                        selected_algo = btn.value
                for btn in first_buttons:
                    if btn.hit(event.pos):
                        selected_first = btn.value
                if pygame.Rect(PAD, 310, W-PAD*2, 46).collidepoint(event.pos):
                    start_game()

            elif state == STATE_GAME:
                if back_btn.collidepoint(event.pos):
                    state = STATE_SETUP

                elif reset_btn.collidepoint(event.pos):
                    reset_board()
                    if ai_goes_first:
                        pending_ai = True

                # Nút random (Expectimax)
                elif (selected_algo == "expectimax"
                      and not game_over
                      and current_turn == p_symbol
                      and random_btn.collidepoint(event.pos)):
                    do_random_move()

                elif not game_over and current_turn == p_symbol:
                    for r in range(3):
                        for c in range(3):
                            if cell_rect(r, c).collidepoint(event.pos) \
                               and game_board[r][c] == " ":
                                ended = do_place(current_turn, r, c)
                                if not ended:
                                    pending_ai = True

    # AI đi
    if pending_ai and state == STATE_GAME and not game_over:
        do_ai_move()

    if state == STATE_SETUP:
        draw_setup(mx, my)
    else:
        draw_game(mx, my)

    pygame.display.flip()
    clock.tick(60)