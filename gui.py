import tkinter as tk
from tkinter import scrolledtext
import threading


# -----------------------------
# Maha GUI
# -----------------------------

class MahaGUI:

    def __init__(self, root, start_assistant):

        self.root = root
        self.start_assistant = start_assistant

        # -----------------------------
        # Window
        # -----------------------------

        self.root.title("MAHA - AI Voice Assistant")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # -----------------------------
        # Title
        # -----------------------------

        self.title_label = tk.Label(
            root,
            text="MAHA",
            font=("Arial", 28, "bold")
        )

        self.title_label.pack(
            pady=(20, 5)
        )

        # -----------------------------
        # Subtitle
        # -----------------------------

        self.subtitle_label = tk.Label(
            root,
            text="AI VOICE ASSISTANT",
            font=("Arial", 12)
        )

        self.subtitle_label.pack()

        # -----------------------------
        # Status
        # -----------------------------

        self.status_label = tk.Label(
            root,
            text="READY",
            font=("Arial", 14, "bold")
        )

        self.status_label.pack(
            pady=15
        )

        # -----------------------------
        # Chat Box
        # -----------------------------

        self.chat_box = scrolledtext.ScrolledText(
            root,
            width=75,
            height=22,
            font=("Arial", 11),
            state="disabled"
        )

        self.chat_box.pack(
            padx=20,
            pady=10
        )

        # -----------------------------
        # Start Button
        # -----------------------------

        self.start_button = tk.Button(
            root,
            text="START MAHA",
            font=("Arial", 13, "bold"),
            width=20,
            height=2,
            command=self.start_listening
        )

        self.start_button.pack(
            pady=15
        )

        # -----------------------------
        # Start Automatically
        # -----------------------------

        self.root.after(
            1000,
            self.start_listening
        )

    # -----------------------------
    # Add Message
    # -----------------------------

    def add_message(self, sender, message):

        self.chat_box.config(
            state="normal"
        )

        self.chat_box.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        self.chat_box.see(
            tk.END
        )

        self.chat_box.config(
            state="disabled"
        )

    # -----------------------------
    # Update Status
    # -----------------------------

    def update_status(self, status):

        self.status_label.config(
            text=status
        )

    # -----------------------------
    # Start Listening
    # -----------------------------

    def start_listening(self):

        # Prevent multiple threads
        if self.start_button["state"] == "disabled":
            return

        self.start_button.config(
            state="disabled",
            text="MAHA IS RUNNING..."
        )

        # Create background thread
        thread = threading.Thread(
            target=self.run_assistant,
            daemon=True
        )

        # Start background thread
        thread.start()

    # -----------------------------
    # Run Assistant
    # -----------------------------

    def run_assistant(self):

        try:

            self.start_assistant(self)

        except Exception as e:

            print("Assistant error:", e)

            self.root.after(
                0,
                lambda error=e: self.add_message(
                    "SYSTEM",
                    f"Error: {error}"
                )
            )

        finally:

            self.root.after(
                0,
                lambda: self.start_button.config(
                    state="normal",
                    text="START MAHA"
                )
            )

            self.root.after(
                0,
                lambda: self.update_status(
                    "READY"
                )
            )


# -----------------------------
# Create GUI
# -----------------------------

def create_gui(start_assistant):

    root = tk.Tk()

    app = MahaGUI(
        root,
        start_assistant
    )

    root.mainloop()

