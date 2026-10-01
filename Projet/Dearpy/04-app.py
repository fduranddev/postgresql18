import psycopg2
import dearpygui.dearpygui as dpg

def get_connection():
    return psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port="5437"
    )

def insert_user():
    name = dpg.get_value("name_input")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()

    dpg.set_value("status_text", "Insertion utilisateur OK!")
    dpg.set_value("name_input", "")

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("/mnt/c/Windows/Fonts/arial.ttf", 26)

dpg.bind_font(default_font)

with dpg.window(label="Insertion Utilisateur", width=900, height=600):

    dpg.add_spacer(height=50)

    dpg.add_text("Nom utilisateur")

    dpg.add_spacer(height=10)

    dpg.add_input_text(
        tag="name_input",
        width=600
    )

    dpg.add_spacer(height=30)

    dpg.add_button(
        label="Sauvegardez dans la Base de données",
        width=410,
        height=80,
        callback=insert_user
    )

    dpg.add_spacer(height=40)
    dpg.add_text("", tag="status_text")

dpg.create_viewport(title="Insertion", width=1000, height=700)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()