import tkinter as tk

class DraggableLabel(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self._drag_data = {"x": 0, "y": 0}
        self.projection = None

    def on_click(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        # Create a projection of the label
        self.projection = tk.Label(self.master, text=self["text"], bg=self["bg"], fg=self["fg"], relief="raised")
        self.projection.place(x=self.winfo_x(), y=self.winfo_y())
        self.projection.lift()

    def on_drag(self, event):
        if self.projection:
            x = self.winfo_x() - self._drag_data["x"] + event.x
            y = self.winfo_y() - self._drag_data["y"] + event.y
            self.projection.place(x=x, y=y)
            self.check_frame(x, y)

    def on_release(self, event):
        if self.projection:
            self.master = self.projection.master
            self.place(x=self.projection.winfo_x(), y=self.projection.winfo_y())
            self.projection.destroy()
            self.projection = None

    def check_frame(self, x, y):
        if self.projection:
            for frame in [self.master.master.frame1, self.master.master.frame2]:
                if frame.winfo_containing(x + frame.winfo_rootx(), y + frame.winfo_rooty()):
                    self.projection.master = frame

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x300")

        self.frame1 = tk.Frame(root, width=250, height=300, bg='lightblue')
        self.frame1.pack(side="left", fill="both", expand=True)

        self.frame2 = tk.Frame(root, width=250, height=300, bg='lightgreen')
        self.frame2.pack(side="right", fill="both", expand=True)

        self.label = DraggableLabel(self.frame1, text="Arrástrame", bg="yellow")
        self.label.place(x=50, y=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
