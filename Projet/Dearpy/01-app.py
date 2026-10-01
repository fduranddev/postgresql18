import dearpygui.dearpygui as dpg

dpg.create_context()

# ----- FONT SETUP -----
with dpg.font_registry():
    default_font = dpg.add_font("/mnt/c/Windows/Fonts/arial.ttf", 28)

dpg.bind_font(default_font)

# ----- WINDOW -----
with dpg.window(label="Hello World Window", width=800, height=500):
    dpg.add_spacer(height=40)
    dpg.add_text("Hello World!")
    dpg.add_spacer(height=20)
    dpg.add_button(label="Click Me", width=250, height=60)

dpg.create_viewport(title="Step 1 - Large Hello World", width=900, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()