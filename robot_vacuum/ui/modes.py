# modes.py
from ui.buttons import update_buttons_for_mode

def switch_to_full(single_matrix_frame, partial_container, current_mode_ref):
    partial_container.pack_forget()
    single_matrix_frame.pack(expand=True)
    current_mode_ref[0] = "FULL"
    update_buttons_for_mode("FULL")

def switch_to_partial(single_matrix_frame, partial_container, current_mode_ref):
    single_matrix_frame.pack_forget()
    partial_container.pack(fill="both", expand=True)
    current_mode_ref[0] = "PARTIAL"
    update_buttons_for_mode("PARTIAL")

def switch_to_complex(single_matrix_frame, partial_container, current_mode_ref):
    partial_container.pack_forget()
    single_matrix_frame.pack(expand=True)
    current_mode_ref[0] = "COMPLEX"
    update_buttons_for_mode("COMPLEX")