import snake
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox


class MainMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # Set window configuration
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("SnakeAI")
        self.parent.resizable(False, False)

        # Frame
        self.frame = tk.LabelFrame(self.parent, text="Menu", padx=10, pady=10)
        self.frame.pack(padx=5, pady=5, fill="both", expand="yes")

        # Labels
        self.rows_label = tk.Label(self.frame, text="Rows")
        self.columns_label = tk.Label(self.frame, text="Columns")

        # Entries
        self.rows_entry = tk.Entry(self.frame, width=5)
        self.rows_entry.insert(0, 12)
        self.columns_entry = tk.Entry(self.frame, width=5)
        self.columns_entry.insert(0, 12)

        # Positions
        self.rows_label.grid(row=0, column=0, padx=5)
        self.rows_entry.grid(row=0, column=1, padx=(0, 5))
        self.columns_label.grid(row=0, column=2, padx=5)
        self.columns_entry.grid(row=0, column=3, padx=(0, 5))

        # Grid frame
        self.grid_frame = tk.Frame(self.frame)
        self.grid_frame.grid(row=2, columnspan=4)

        # Buttons
        self.load_button = tk.Button(self.grid_frame, text="Play", padx=20, command=self.play)
        self.edit_button = tk.Button(self.grid_frame, text="Run AI", padx=15, command=self.run_AI)

        # Grid Positions
        self.load_button.grid(row=2, column=1, padx=(20, 5), pady=(10, 10))
        self.edit_button.grid(row=2, column=2, padx=(20, 5), pady=(10, 10))

        # Get screen dimensions
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = self.parent.winfo_reqwidth()
        window_height = self.parent.winfo_reqheight()
        self.parent.geometry(f"+{(screen_width - window_width) // 2 - 50}+{(screen_height - window_height) // 2 - 50}")

    def play(self):
        num_rows = int(self.rows_entry.get())
        num_cols = int(self.columns_entry.get())
        try:
            window = snake.GameWindow(rows=num_rows, columns=num_cols)
            window.run(mode="Play")
            messagebox.showinfo("You win!", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.SnakeCollisionError:
            messagebox.showinfo("You lose!", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.GameExitedError:
            messagebox.showinfo("Exit", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.WindowDimensionError:
            messagebox.showerror("Error!", f"Rows and columns must be larger than 2!", parent=self)

    def run_AI(self):
        num_rows = int(self.rows_entry.get())
        num_cols = int(self.columns_entry.get())
        try:
            window = snake.GameWindow(rows=num_rows, columns=num_cols)
            window.run(mode="AI")
            messagebox.showinfo("You win!", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.SnakeCollisionError:
            messagebox.showinfo("You lose!", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.NoPathError:
            messagebox.showinfo("You lose!", f"Snake got trapped!", parent=self)
            window.close()
        except snake.GameExitedError:
            messagebox.showinfo("Exit", f"Your total score is {window.score}!", parent=self)
            window.close()
        except snake.WindowDimensionError:
            messagebox.showerror("Error!", f"Rows and columns must be larger than 2!", parent=self)


if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
