import copy
from ui.log import write_log
from core.belief import belief_goal
from ui.constants import DIRECTION_LABEL


def animate_full_path(i, result, matrix, log_panel, on_done=None):
    if i >= len(result):
        write_log(log_panel, "[HOÀN THÀNH] Robot đã dọn sạch!")
        write_log(log_panel, "=" * 23)

        matrix.is_running = False

        matrix.is_running = False
        matrix.after_id = None

        if on_done:          
            on_done()        
        return
        
    matrix.node = copy.deepcopy(result[i])
    matrix.show_state_have_robot()

    if result[i].direction is not None:
        huong = DIRECTION_LABEL.get(result[i].direction, result[i].direction)

        write_log(log_panel, f"Bước {i:>2}: {huong} → ô ({result[i].x}, {result[i].y})")
        if result[i-1].state[result[i].x][result[i].y] == 1:  
            write_log(log_panel, f"         🧹 Dọn bụi tại ({result[i].x}, {result[i].y})")
        
    matrix.after_id = matrix.parent.after(500, animate_full_path, i + 1, result, matrix, log_panel)

def animate_full_path_partial(i, result, matrix_1, matrix_2, log_panel):
    # Kiểm tra cả 2 đã xong chưa
    m1_done = i >= len(result) or matrix_1.is_running == False
    m2_done = i >= len(result) or matrix_2.is_running == False

    if i >= len(result):
        if not m1_done:
            write_log(log_panel, "[HOÀN THÀNH] Belief 1 đã dọn sạch!")
        if not m2_done:
            write_log(log_panel, "[HOÀN THÀNH] Belief 2 đã dọn sạch!")
        write_log(log_panel, "=" * 23)
        matrix_1.is_running = False
        matrix_2.is_running = False
        matrix_1.after_id = None
        matrix_2.after_id = None
        return

    # Animate matrix_1 nếu chưa đạt đích
    if matrix_1.is_running:
        current_node_1 = result[i][0]  # node của belief 1
        matrix_1.node = copy.deepcopy(current_node_1)
        matrix_1.show_state_have_robot()

        if current_node_1.direction is not None:
            huong = DIRECTION_LABEL.get(current_node_1.direction, current_node_1.direction)
            write_log(log_panel, f"[B1] Bước {i:>2}: {huong} → ô ({current_node_1.x}, {current_node_1.y})")
            if result[i-1][0].state[current_node_1.x][current_node_1.y] == 1:
                write_log(log_panel, f"         🧹 Dọn bụi tại ({current_node_1.x}, {current_node_1.y})")

        # Kiểm tra belief 1 đạt đích ở bước này không
        if belief_goal([current_node_1]):
            write_log(log_panel, f"[HOÀN THÀNH] Belief 1 đã dọn sạch ở bước {i}!")
            matrix_1.is_running = False
            matrix_1.after_id = None

    # Animate matrix_2 nếu chưa đạt đích
    if matrix_2.is_running:
        current_node_2 = result[i][1]  # node của belief 2
        matrix_2.node = copy.deepcopy(current_node_2)
        matrix_2.show_state_have_robot()

        if current_node_2.direction is not None:
            huong = DIRECTION_LABEL.get(current_node_2.direction, current_node_2.direction)
            write_log(log_panel, f"[B2] Bước {i:>2}: {huong} → ô ({current_node_2.x}, {current_node_2.y})")
            if result[i-1][1].state[current_node_2.x][current_node_2.y] == 1:
                write_log(log_panel, f"         🧹 Dọn bụi tại ({current_node_2.x}, {current_node_2.y})")

        # Kiểm tra belief 2 đạt đích ở bước này không
        if belief_goal([current_node_2]):
            write_log(log_panel, f"[HOÀN THÀNH] Belief 2 đã dọn sạch ở bước {i}!")
            matrix_2.is_running = False
            matrix_2.after_id = None

    # Nếu cả 2 đều đã dừng thì kết thúc
    if not matrix_1.is_running and not matrix_2.is_running:
        write_log(log_panel, "=" * 23)
        return

    # Tiếp tục animate bước tiếp theo
    after_id = matrix_1.parent.after(
        500, animate_full_path_partial, i + 1, result, matrix_1, matrix_2, log_panel
    )
    matrix_1.after_id = after_id
    matrix_2.after_id = after_id

def animate_realtime(gen, prev_node, matrix, log_panel, step):
    try:
        node = next(gen)
    except StopIteration:
        write_log(log_panel, "[DỪNG] Không cải thiện được thêm!")
        write_log(log_panel, "=" * 23)
        matrix.is_running = False
        matrix.after_id   = None
        return

    matrix.node = copy.deepcopy(node)
    matrix.show_state_have_robot()

    if node.direction is not None and prev_node is not None:
        huong   = DIRECTION_LABEL.get(node.direction, node.direction)

        if prev_node.state[node.x][node.y] == 1:   
            bui_don = [(node.x, node.y)]
        else:
            bui_don = []

        write_log(log_panel, f"Bước {step:>2}: {huong} → ô ({node.x}, {node.y})")
        for (r, c) in bui_don:
            write_log(log_panel, f"         🧹 Dọn bụi tại ({r}, {c})")

    matrix.after_id = matrix.parent.after(
        500, animate_realtime, gen, node, matrix, log_panel, step + 1)
