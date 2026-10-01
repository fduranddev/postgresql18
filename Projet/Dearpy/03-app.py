import psycopg2
import dearpygui.dearpygui as dpg

def test_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="HR",
            user="postgres",
            password="admin",
            port="5436"
        )
        conn.close()
        dpg.set_value("status_text", "Connected successfully!")
    except Exception as e:
        dpg.set_value("status_text", f"Connection error: {e}")

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("/mnt/c/Windows/Fonts/arial.ttf", 26)

dpg.bind_font(default_font)

with dpg.window(label="Database Connection", width=900, height=600):
    dpg.add_spacer(height=60)

    dpg.add_button(
        label="Test Database Connection",
        width=400,
        height=80,
        callback=test_connection
    )

    dpg.add_spacer(height=40)
    dpg.add_text("", tag="status_text")

dpg.create_viewport(title="DB Connection", width=1000, height=700)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()