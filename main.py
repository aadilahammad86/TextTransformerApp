import customtkinter as ctk
import tkinter as tk

# Set default appearance mode and color theme
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

class TextTransformerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Text Transformer")
        self.geometry("820x720")
        self.minsize(700, 620)

        # Variables for checkboxes
        # Casing options
        self.case_upper_var = ctk.BooleanVar(value=False)
        self.case_lower_var = ctk.BooleanVar(value=False)
        self.case_title_var = ctk.BooleanVar(value=False)
        self.case_first_only_var = ctk.BooleanVar(value=False)

        # Delimiter replacements
        self.space_to_underscore_var = ctk.BooleanVar(value=False)
        self.space_to_minus_var = ctk.BooleanVar(value=False)
        self.underscore_to_space_var = ctk.BooleanVar(value=False)
        self.minus_to_space_var = ctk.BooleanVar(value=False)
        self.minus_to_underscore_var = ctk.BooleanVar(value=False)
        self.underscore_to_minus_var = ctk.BooleanVar(value=False)

        # Auto-transform toggle
        self.auto_transform_var = ctk.BooleanVar(value=True)

        self._create_layout()

    def _create_layout(self):
        # Configure grid layout weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Input area
        self.grid_rowconfigure(5, weight=1)  # Output area

        # 1. Header Frame
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 8), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame, 
            text="Text Transformer", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Theme Selector
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.grid(row=0, column=1, sticky="e")

        theme_label = ctk.CTkLabel(theme_frame, text="Appearance Theme:", font=ctk.CTkFont(size=13))
        theme_label.pack(side="left", padx=(0, 8))

        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["System", "Light", "Dark"],
            command=self.change_theme,
            width=110
        )
        self.theme_menu.set("System")
        self.theme_menu.pack(side="left")

        # 2. Input Section Header
        input_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_header_frame.grid(row=1, column=0, padx=20, pady=(5, 2), sticky="ew")
        input_header_frame.grid_columnconfigure(0, weight=1)

        input_title = ctk.CTkLabel(
            input_header_frame, 
            text="Input Text:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_title.grid(row=0, column=0, sticky="w")

        btn_paste = ctk.CTkButton(
            input_header_frame, 
            text="📋 Paste", 
            width=75, 
            height=26, 
            command=self.paste_input
        )
        btn_paste.grid(row=0, column=1, padx=(0, 6), sticky="e")

        btn_clear_input = ctk.CTkButton(
            input_header_frame, 
            text="🗑️ Clear", 
            width=75, 
            height=26, 
            fg_color="#c0392b", 
            hover_color="#e74c3c", 
            command=self.clear_input
        )
        btn_clear_input.grid(row=0, column=2, sticky="e")

        # 3. Input Text Box
        self.input_textbox = ctk.CTkTextbox(self, height=120, font=ctk.CTkFont(size=13))
        self.input_textbox.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.input_textbox.bind("<KeyRelease>", lambda event: self.on_input_changed())

        # 4. Checkboxes & Options Section
        options_frame = ctk.CTkFrame(self, corner_radius=10)
        options_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        options_frame.grid_columnconfigure((0, 1), weight=1)

        # Casing Options Sub-Frame
        casing_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        casing_frame.grid(row=0, column=0, padx=15, pady=10, sticky="nw")

        casing_title = ctk.CTkLabel(
            casing_frame, 
            text="Case Conversions:", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        casing_title.pack(anchor="w", pady=(0, 6))

        self.cb_upper = ctk.CTkCheckBox(
            casing_frame, 
            text="ALL CAPS (UPPERCASE)", 
            variable=self.case_upper_var, 
            command=lambda: self.on_case_toggle('upper')
        )
        self.cb_upper.pack(anchor="w", pady=2)

        self.cb_lower = ctk.CTkCheckBox(
            casing_frame, 
            text="all small (lowercase)", 
            variable=self.case_lower_var, 
            command=lambda: self.on_case_toggle('lower')
        )
        self.cb_lower.pack(anchor="w", pady=2)

        self.cb_first_only = ctk.CTkCheckBox(
            casing_frame, 
            text="First letter only caps (Capitalize)", 
            variable=self.case_first_only_var, 
            command=lambda: self.on_case_toggle('first_only')
        )
        self.cb_first_only.pack(anchor="w", pady=2)

        self.cb_title = ctk.CTkCheckBox(
            casing_frame, 
            text="First Letter Of Each Word (Title Case)", 
            variable=self.case_title_var, 
            command=lambda: self.on_case_toggle('title')
        )
        self.cb_title.pack(anchor="w", pady=2)

        # Delimiter Replacements Sub-Frame
        delimiters_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        delimiters_frame.grid(row=0, column=1, padx=15, pady=10, sticky="nw")

        delimiters_title = ctk.CTkLabel(
            delimiters_frame, 
            text="Replace Characters / Delimiters:", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        delimiters_title.pack(anchor="w", pady=(0, 6))

        self.cb_space_under = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace space with underscore ( _ )", 
            variable=self.space_to_underscore_var, 
            command=self.transform_text
        )
        self.cb_space_under.pack(anchor="w", pady=2)

        self.cb_space_minus = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace space with minus ( - )", 
            variable=self.space_to_minus_var, 
            command=self.transform_text
        )
        self.cb_space_minus.pack(anchor="w", pady=2)

        self.cb_under_space = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace underscore with space (   )", 
            variable=self.underscore_to_space_var, 
            command=self.transform_text
        )
        self.cb_under_space.pack(anchor="w", pady=2)

        self.cb_minus_space = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace minus with space (   )", 
            variable=self.minus_to_space_var, 
            command=self.transform_text
        )
        self.cb_minus_space.pack(anchor="w", pady=2)

        self.cb_minus_under = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace minus with underscore ( _ )", 
            variable=self.minus_to_underscore_var, 
            command=self.transform_text
        )
        self.cb_minus_under.pack(anchor="w", pady=2)

        self.cb_under_minus = ctk.CTkCheckBox(
            delimiters_frame, 
            text="Replace underscore with minus ( - )", 
            variable=self.underscore_to_minus_var, 
            command=self.transform_text
        )
        self.cb_under_minus.pack(anchor="w", pady=2)

        # Control Bar below options
        control_bar = ctk.CTkFrame(options_frame, fg_color="transparent")
        control_bar.grid(row=1, column=0, columnspan=2, padx=15, pady=(4, 10), sticky="ew")
        
        self.cb_live = ctk.CTkSwitch(
            control_bar, 
            text="Real-time live conversion", 
            variable=self.auto_transform_var
        )
        self.cb_live.pack(side="left", padx=5)

        btn_reset_checks = ctk.CTkButton(
            control_bar, 
            text="Uncheck All", 
            width=90, 
            height=26, 
            fg_color="gray45", 
            hover_color="gray35", 
            command=self.uncheck_all
        )
        btn_reset_checks.pack(side="right", padx=5)

        btn_convert_now = ctk.CTkButton(
            control_bar, 
            text="⚡ Convert Now", 
            width=120, 
            height=28, 
            font=ctk.CTkFont(weight="bold"), 
            command=self.transform_text
        )
        btn_convert_now.pack(side="right", padx=5)

        # 5. Output Section Header
        output_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        output_header_frame.grid(row=4, column=0, padx=20, pady=(10, 2), sticky="ew")
        output_header_frame.grid_columnconfigure(0, weight=1)

        output_title = ctk.CTkLabel(
            output_header_frame, 
            text="Converted Output:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        output_title.grid(row=0, column=0, sticky="w")

        self.copy_status_label = ctk.CTkLabel(
            output_header_frame, 
            text="", 
            text_color="#2ecc71", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.copy_status_label.grid(row=0, column=1, padx=10, sticky="e")

        btn_use_as_input = ctk.CTkButton(
            output_header_frame, 
            text="⬆️ Use as Input", 
            width=110, 
            height=26, 
            command=self.use_output_as_input
        )
        btn_use_as_input.grid(row=0, column=2, padx=(0, 6), sticky="e")

        btn_copy = ctk.CTkButton(
            output_header_frame, 
            text="📋 Copy Output", 
            width=110, 
            height=26, 
            fg_color="#27ae60", 
            hover_color="#2ecc71", 
            command=self.copy_output
        )
        btn_copy.grid(row=0, column=3, sticky="e")

        # 6. Output Text Box
        self.output_textbox = ctk.CTkTextbox(self, height=120, font=ctk.CTkFont(size=13))
        self.output_textbox.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="nsew")

    def on_case_toggle(self, active_case):
        # Mutual exclusivity among casing options for clean predictable transformation
        if active_case == 'upper' and self.case_upper_var.get():
            self.case_lower_var.set(False)
            self.case_title_var.set(False)
            self.case_first_only_var.set(False)
        elif active_case == 'lower' and self.case_lower_var.get():
            self.case_upper_var.set(False)
            self.case_title_var.set(False)
            self.case_first_only_var.set(False)
        elif active_case == 'title' and self.case_title_var.get():
            self.case_upper_var.set(False)
            self.case_lower_var.set(False)
            self.case_first_only_var.set(False)
        elif active_case == 'first_only' and self.case_first_only_var.get():
            self.case_upper_var.set(False)
            self.case_lower_var.set(False)
            self.case_title_var.set(False)
        
        self.transform_text()

    def on_input_changed(self):
        if self.auto_transform_var.get():
            self.transform_text()

    def transform_text(self):
        input_text = self.input_textbox.get("1.0", "end-1c")
        if not input_text:
            self.output_textbox.delete("1.0", "end")
            return

        result = input_text

        # 1. Delimiter Replacements
        if self.space_to_underscore_var.get():
            result = result.replace(" ", "_")

        if self.space_to_minus_var.get():
            result = result.replace(" ", "-")

        if self.underscore_to_space_var.get():
            result = result.replace("_", " ")

        if self.minus_to_space_var.get():
            result = result.replace("-", " ")

        if self.minus_to_underscore_var.get():
            result = result.replace("-", "_")

        if self.underscore_to_minus_var.get():
            result = result.replace("_", "-")

        # 2. Case Conversions
        if self.case_upper_var.get():
            result = result.upper()
        elif self.case_lower_var.get():
            result = result.lower()
        elif self.case_first_only_var.get():
            lines = result.splitlines(keepends=True)
            capitalized_lines = []
            for line in lines:
                if line:
                    capitalized_lines.append(line[:1].upper() + line[1:].lower())
                else:
                    capitalized_lines.append(line)
            result = "".join(capitalized_lines)
        elif self.case_title_var.get():
            result = result.title()

        # Update output
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", result)
        self.copy_status_label.configure(text="")

    def uncheck_all(self):
        self.case_upper_var.set(False)
        self.case_lower_var.set(False)
        self.case_title_var.set(False)
        self.case_first_only_var.set(False)
        self.space_to_underscore_var.set(False)
        self.space_to_minus_var.set(False)
        self.underscore_to_space_var.set(False)
        self.minus_to_space_var.set(False)
        self.minus_to_underscore_var.set(False)
        self.underscore_to_minus_var.set(False)
        self.transform_text()

    def copy_output(self):
        output_text = self.output_textbox.get("1.0", "end-1c")
        if output_text:
            self.clipboard_clear()
            self.clipboard_append(output_text)
            self.copy_status_label.configure(text="✓ Copied to clipboard!", text_color="#2ecc71")
            self.after(2500, lambda: self.copy_status_label.configure(text=""))
        else:
            self.copy_status_label.configure(text="Nothing to copy!", text_color="#e67e22")
            self.after(2000, lambda: self.copy_status_label.configure(text="", text_color="#2ecc71"))

    def paste_input(self):
        try:
            clipboard_content = self.clipboard_get()
            self.input_textbox.delete("1.0", "end")
            self.input_textbox.insert("1.0", clipboard_content)
            self.transform_text()
        except tk.TclError:
            pass

    def clear_input(self):
        self.input_textbox.delete("1.0", "end")
        self.output_textbox.delete("1.0", "end")
        self.copy_status_label.configure(text="")

    def use_output_as_input(self):
        output_text = self.output_textbox.get("1.0", "end-1c")
        if output_text:
            self.input_textbox.delete("1.0", "end")
            self.input_textbox.insert("1.0", output_text)
            self.transform_text()

    def change_theme(self, new_theme: str):
        ctk.set_appearance_mode(new_theme)


if __name__ == "__main__":
    app = TextTransformerApp()
    app.mainloop()
