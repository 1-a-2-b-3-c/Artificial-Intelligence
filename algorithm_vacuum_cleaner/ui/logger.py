def write_log(text_widget, message):
    text_widget.insert('end', message + '\n')
    text_widget.see('end')