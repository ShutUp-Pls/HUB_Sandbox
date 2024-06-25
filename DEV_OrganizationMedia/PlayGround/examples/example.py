import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

PATH_F1 = "C:\\Users\\marqu\\OneDrive\\Pictures\\Screenshots"
PATH_F2 = "C:\\Users\\marqu\\OneDrive\\Pictures\\Jennifer Lawrence"

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.canvas1 = tk.Canvas(root, bg="white", width=300, height=400)
        self.canvas2 = tk.Canvas(root, bg="white", width=300, height=400)
        
        self.canvas1.pack(side="left", fill="both", expand=True)
        self.canvas2.pack(side="right", fill="both", expand=True)

        self.populate_canvas(self.canvas1, PATH_F1)
        self.populate_canvas(self.canvas2, PATH_F2)

        self.drag_data = {"widget": None, "data": None}

    def populate_canvas(self, canvas, folder_path):
        for widget in canvas.winfo_children():
            widget.destroy()

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                label = ttk.Label(canvas, text=filename)
                label.bind("<ButtonPress-1>", self.on_drag_start)
                label.bind("<B1-Motion>", self.on_drag_motion)
                label.bind("<ButtonRelease-1>", self.on_drag_release)
                canvas.create_window(10, 10 + 30 * len(canvas.winfo_children()), anchor="nw", window=label)

    def on_drag_start(self, event):
        widget = event.widget
        self.drag_data["widget"] = widget
        self.drag_data["data"] = widget.cget("text")

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() + event.x
        y = widget.winfo_y() + event.y
        widget.place(x=x, y=y)

    def on_drag_release(self, event):
        widget = event.widget
        x = event.x_root - self.root.winfo_rootx()
        y = event.y_root - self.root.winfo_rooty()

        if self.canvas1.winfo_containing(x, y):
            self.move_file(widget, self.canvas1)
        elif self.canvas2.winfo_containing(x, y):
            self.move_file(widget, self.canvas2)
        
        self.drag_data = {"widget": None, "data": None}

    def move_file(self, widget, target_canvas):
        src_filename = self.drag_data["data"]
        src_path = os.path.join(PATH_F1 if widget.master == self.canvas1 else PATH_F2, src_filename)
        dest_folder = PATH_F1 if target_canvas == self.canvas1 else PATH_F2
        dest_path = os.path.join(dest_folder, src_filename)

        try:
            shutil.move(src_path, dest_path)
            self.populate_canvas(self.canvas1, PATH_F1)
            self.populate_canvas(self.canvas2, PATH_F2)
        except Exception as e:
            print(f"Error moving file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
