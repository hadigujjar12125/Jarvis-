"""GUI interface for JARVIS Pro."""

import logging
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime
import threading

logger = logging.getLogger(__name__)


class JARVISGui:
    """Modern GUI interface for JARVIS Pro."""

    def __init__(self, on_submit=None):
        """Initialize GUI."""
        self.on_submit = on_submit
        self.root = tk.Tk()
        self.root.title("JARVIS Pro - AI Assistant")
        self.root.geometry("900x700")
        
        # Set dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#0078d4"
        self.secondary_bg = "#2d2d2d"
        
        self.root.configure(bg=self.bg_color)
        
        self._setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_ui(self):
        """Setup user interface."""
        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="🤖 JARVIS Pro - AI Assistant",
            font=("Arial", 18, "bold"),
            bg=self.accent_color,
            fg=self.fg_color
        )
        header_label.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display
        chat_label = tk.Label(
            main_frame,
            text="Chat History",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        chat_label.pack(anchor="w", pady=(0, 5))
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            height=20,
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=("Arial", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#4fc3f7")
        self.chat_display.tag_config("assistant", foreground="#81c784")
        self.chat_display.tag_config("error", foreground="#ff6b6b")
        self.chat_display.tag_config("timestamp", foreground="#999999")
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_label = tk.Label(
            input_frame,
            text="Your Message",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        input_label.pack(anchor="w", pady=(0, 5))
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg=self.secondary_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.input_field.pack(fill=tk.X, pady=(0, 8))
        self.input_field.bind("<Return>", lambda e: self._send_message())
        
        # Buttons frame
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 5))
        
        send_btn = tk.Button(
            button_frame,
            text="📤 Send",
            command=self._send_message,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self._clear_chat,
            bg=self.secondary_bg,
            fg=self.fg_color,
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            activebackground="#404040"
        )
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=self.secondary_bg,
            fg="#999999",
            font=("Arial", 9),
            relief=tk.SUNKEN,
            anchor="w"
        )
        status_bar.pack(fill=tk.X, padx=0, pady=0)

    def _send_message(self):
        """Send user message and get response."""
        message = self.input_field.get().strip()
        
        if not message:
            messagebox.showwarning("Empty Message", "Please type something!")
            return
        
        # Display user message
        self._display_message("You", message, "user")
        self.input_field.delete(0, tk.END)
        self.status_var.set("Processing...")
        
        # Process message in separate thread
        thread = threading.Thread(target=self._process_message, args=(message,))
        thread.daemon = True
        thread.start()

    def _process_message(self, message):
        """Process message and get response."""
        try:
            if self.on_submit:
                response = self.on_submit(message)
                self._display_message("JARVIS", response, "assistant")
                self.status_var.set("Ready")
            else:
                self._display_message("JARVIS", "No handler connected!", "error")
                self.status_var.set("Error")
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            self._display_message("JARVIS", f"Error: {str(e)}", "error")
            self.status_var.set("Error")

    def _display_message(self, sender, message, tag="assistant"):
        """Display message in chat."""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _clear_chat(self):
        """Clear chat history."""
        if messagebox.askyesno("Clear Chat", "Clear all messages?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.status_var.set("Chat cleared")

    def _on_closing(self):
        """Handle window closing."""
        if messagebox.askokcancel("Quit", "Exit JARVIS Pro?"):
            self.root.destroy()

    def run(self):
        """Start GUI."""
        logger.info("Starting GUI")
        self.root.mainloop()
