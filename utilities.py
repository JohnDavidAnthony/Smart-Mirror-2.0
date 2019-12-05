import tkinter as tk


class Marquee(tk.Canvas):
    def __init__(self, parent, text, margin=0, relief='flat', fps=30, textbox_width=200):
        tk.Canvas.__init__(self, parent, relief=relief, highlightthickness=0, bg="black")
        self.fps = fps
        self.og_fps = fps
        self.textbox_width = textbox_width
        self.paused = False
        self.left = True
        self.margin = margin

        self.text_id = self.create_text(self.margin, self.margin, text=text, anchor="w", tags=("text",), fill="white")
        (x0, y0, x1, y1) = self.bbox("text")

        self.height = (y1 - y0) + (2*margin)
        self.configure(width=textbox_width, height=self.height)

        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")

        # if text fits within textbox do nothing
        if x1 < self.textbox_width - 10:
            (x0, y0, x1, y1) = self.bbox("text")
            y0 = int(self.height/2)
            self.coords("text", x0, y0)
            return

        # Otherwise move text back and forth
        # Move left
        if (x1 > self.textbox_width) and self.left and not self.paused:
            self.move("text", -1, 0)

        # Move right
        elif x0 < self.margin*2 and not self.left and not self.paused:
            self.move("text", 1, 0)

        # Stop Moving
        elif not self.paused:
            self.paused = True
            if self.left:
                self.after(4000, self.unpause)
            else:
                self.after(10000, self.unpause)

        # Repeat
        self.after_id = self.after(int(1000 / self.fps), self.animate)

    def unpause(self):
        # start the animation
        (x0, y0, x1, y1) = self.bbox("text")
        y0 = int(self.winfo_height() / 2)
        self.coords("text", x0, y0)

        self.paused = False
        self.left = not self.left

        if self.left:
            self.fps = self.og_fps
        else:
            self.fps = self.og_fps * 3

    def change_text(self, text):
        (x0, y0, x1, y1) = self.bbox("text")
        self.height = (y1 - y0) + (2 * self.margin)
        self.configure(height=self.height)
        if x1 < self.textbox_width - 10:
            self.itemconfig(self.text_id, text=text)
            self.animate()
        self.itemconfig(self.text_id, text=text)


# root = tk.Tk()
# marquee = Marquee(root, text="Nothing's Playing", relief="sunken")
# marquee.pack(side="top", fill="none", pady=20)
# marquee.change_text("adwfsjlihbuiogyftgui87tdrxfyugi8oyigfgchuyio8ygfhchyu")
#
# root.after(1000, root.mainloop())