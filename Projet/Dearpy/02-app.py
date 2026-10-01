import dearpygui.dearpygui as dpg

def greet_user():
    name = dpg.get_value("name_input")
    dpg.set_value("greeting_text", f"Hello {name}")

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("/mnt/c/Windows/Fonts/arial.ttf", 26)

dpg.bind_font(default_font)

with dpg.window(label="Large Input", width=800, height=500):

    dpg.add_spacer(height=40)

    # Label ayrı
    dpg.add_text("Enter your name")

    dpg.add_spacer(height=10)

    # Input artık labelsız
    dpg.add_input_text(
        tag="name_input",
        width=500
    )

    dpg.add_spacer(height=20)

    dpg.add_button(
        label="Greet",
        width=300,
        height=70,
        callback=greet_user
    )

    dpg.add_spacer(height=30)
    dpg.add_text("", tag="greeting_text")

dpg.create_viewport(title="Large Input UI", width=900, height=600)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
    