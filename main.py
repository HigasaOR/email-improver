#!/usr/bin/env python3
"""Email & Text Improver — refine your writing with Claude AI."""

import json
import threading
from pathlib import Path

import anthropic
import customtkinter as ctk

# ── Configuration ────────────────────────────────────────────────────────────

CONFIG_PATH = Path.home() / ".email-improver.json"

TONES = {
    "Professional":      "professional and polished, ideal for business contexts",
    "Friendly & Polite": "warm, approachable, and considerate while staying respectful",
    "Concise & Direct":  "brief and to the point, cutting any unnecessary words",
    "Formal":            "highly formal, structured, and appropriate for official correspondence",
    "Casual":            "relaxed, natural, and conversational",
}

MODE_SYSTEM = {
    "Email": (
        "You are an expert email editor. Refine the given email while preserving "
        "its structure (greeting, body, sign-off) and the sender's original intent. "
        "Output only the refined email — no explanations or commentary."
    ),
    "Text Message": (
        "You are an expert at writing text messages. Refine the given message while "
        "keeping it appropriately brief and preserving the sender's original intent. "
        "Output only the refined message — no explanations or commentary."
    ),
}

MODEL = "claude-sonnet-4-6"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


# ── App ───────────────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.mode_var = ctk.StringVar(value="Email")
        self.tone_var = ctk.StringVar(value="Professional")
        self._mode_state: dict[str, dict[str, str]] = {
            "Email":        {"input": "", "output": ""},
            "Text Message": {"input": "", "output": ""},
        }
        self._build_ui()
        self.title("Email & Text Improver")
        self.geometry("980x660")
        self.minsize(740, 500)

    # ── UI ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_toolbar()
        self._build_content()
        self._build_bottom()

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self, height=54, corner_radius=0)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_columnconfigure(1, weight=1)

        # Mode toggle
        mode_frame = ctk.CTkFrame(bar, fg_color="transparent")
        mode_frame.grid(row=0, column=0, padx=18, pady=10, sticky="w")
        ctk.CTkLabel(mode_frame, text="Mode:", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(0, 8))
        for mode in ("Email", "Text Message"):
            ctk.CTkRadioButton(
                mode_frame, text=mode, variable=self.mode_var, value=mode,
                font=ctk.CTkFont(size=13), command=self._on_mode_change,
            ).pack(side="left", padx=6)

        # Tone selector (centered)
        tone_frame = ctk.CTkFrame(bar, fg_color="transparent")
        tone_frame.grid(row=0, column=1, pady=10)
        ctk.CTkLabel(tone_frame, text="Tone:", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(0, 8))
        ctk.CTkOptionMenu(
            tone_frame, variable=self.tone_var,
            values=list(TONES.keys()),
            width=200, font=ctk.CTkFont(size=13),
        ).pack(side="left")

        # API key button
        ctk.CTkButton(
            bar, text="⚙  API Key", width=110,
            fg_color="transparent", border_width=1,
            font=ctk.CTkFont(size=13),
            command=self._open_settings,
        ).grid(row=0, column=2, padx=18, pady=10)

    def _build_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

        # Column headers
        ctk.CTkLabel(content, text="Your Draft", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 6))
        ctk.CTkLabel(content, text="Refined", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=2, sticky="w", pady=(0, 6))

        # Input box
        self.input_box = ctk.CTkTextbox(content, wrap="word", font=ctk.CTkFont(size=14))
        self.input_box.grid(row=1, column=0, sticky="nsew")

        # Middle column: Refine button centered vertically
        mid = ctk.CTkFrame(content, fg_color="transparent", width=90)
        mid.grid(row=0, column=1, rowspan=2, padx=10, sticky="ns")
        mid.grid_propagate(False)
        mid.grid_rowconfigure(0, weight=1)
        self.refine_btn = ctk.CTkButton(
            mid, text="Refine\n→",
            width=80, height=56,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._refine,
        )
        self.refine_btn.grid(row=0, column=0, pady=0)

        # Output box
        self.output_box = ctk.CTkTextbox(content, wrap="word", font=ctk.CTkFont(size=14))
        self.output_box.grid(row=1, column=2, sticky="nsew")

    def _build_bottom(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=2, column=0, sticky="ew", padx=16, pady=(4, 10))
        bar.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            bar, text="Enter your text and click Refine.",
            text_color="gray", font=ctk.CTkFont(size=12),
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(bar, fg_color="transparent")
        btn_frame.grid(row=0, column=1)

        ctk.CTkButton(
            btn_frame, text="Clear", width=80,
            fg_color="transparent", border_width=1,
            font=ctk.CTkFont(size=13),
            command=self._clear,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame, text="Copy Result", width=110,
            font=ctk.CTkFont(size=13),
            command=self._copy_output,
        ).pack(side="left")

    # ── Actions ───────────────────────────────────────────────────────────

    def _on_mode_change(self):
        # Save current mode's content before switching
        prev = "Email" if self.mode_var.get() == "Text Message" else "Text Message"
        self._mode_state[prev]["input"]  = self.input_box.get("1.0", "end-1c")
        self._mode_state[prev]["output"] = self.output_box.get("1.0", "end-1c")

        # Restore the new mode's content
        new = self.mode_var.get()
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", self._mode_state[new]["input"])
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", self._mode_state[new]["output"])
        self._set_status("Enter your text and click Refine.")

    def _clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self._set_status("Cleared.")

    def _refine(self):
        api_key = self.cfg.get("api_key", "").strip()
        if not api_key:
            self._open_settings(prompt="Please enter your Anthropic API key first.")
            return

        text = self.input_box.get("1.0", "end").strip()
        if not text:
            self._set_status("Please enter some text to refine.", error=True)
            return

        self.refine_btn.configure(state="disabled", text="…")
        self.output_box.delete("1.0", "end")
        self._set_status("Refining with Claude…")

        threading.Thread(
            target=self._call_claude, args=(api_key, text), daemon=True
        ).start()

    def _call_claude(self, api_key: str, text: str):
        try:
            client = anthropic.Anthropic(api_key=api_key)
            mode = self.mode_var.get()
            tone_desc = TONES[self.tone_var.get()]

            with client.messages.stream(
                model=MODEL,
                max_tokens=2048,
                system=MODE_SYSTEM[mode],
                messages=[{
                    "role": "user",
                    "content": (
                        f"Refine the following in a {tone_desc} tone:\n\n{text}"
                    ),
                }],
            ) as stream:
                for chunk in stream.text_stream:
                    self.after(0, self._append_output, chunk)

            self.after(0, self._on_done)
        except anthropic.AuthenticationError:
            self.after(0, self._on_error,
                       "Invalid API key. Open ⚙ API Key to update it.")
        except anthropic.RateLimitError:
            self.after(0, self._on_error, "Rate limit reached. Try again in a moment.")
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _append_output(self, chunk: str):
        self.output_box.insert("end", chunk)
        self.output_box.see("end")

    def _on_done(self):
        self.refine_btn.configure(state="normal", text="Refine\n→")
        self._set_status("Done. Click 'Copy Result' to copy.")

    def _on_error(self, msg: str):
        self.refine_btn.configure(state="normal", text="Refine\n→")
        self._set_status(f"Error: {msg}", error=True)

    def _copy_output(self):
        text = self.output_box.get("1.0", "end").strip()
        if not text:
            self._set_status("Nothing to copy yet.", error=True)
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self._set_status("Copied to clipboard!")

    def _set_status(self, msg: str, error: bool = False):
        self.status_label.configure(
            text=msg, text_color="red" if error else "gray")

    # ── Settings dialog ───────────────────────────────────────────────────

    def _open_settings(self, prompt: str = ""):
        win = ctk.CTkToplevel(self)
        win.title("API Key Settings")
        win.geometry("460x230")
        win.resizable(False, False)
        win.grab_set()
        win.focus()

        pad = {"padx": 24}

        if prompt:
            ctk.CTkLabel(
                win, text=prompt,
                text_color=("orange", "#FFA500"),
                font=ctk.CTkFont(size=13),
            ).pack(pady=(18, 0), **pad, anchor="w")

        ctk.CTkLabel(
            win,
            text="Get your key at console.anthropic.com → API Keys",
            text_color="gray", font=ctk.CTkFont(size=12),
        ).pack(pady=(18 if not prompt else 10, 4), **pad, anchor="w")

        key_var = ctk.StringVar(value=self.cfg.get("api_key", ""))
        key_entry = ctk.CTkEntry(
            win, textvariable=key_var, show="•",
            width=410, font=ctk.CTkFont(size=13),
        )
        key_entry.pack(**pad)

        show_var = ctk.BooleanVar(value=False)
        def toggle_show():
            key_entry.configure(show="" if show_var.get() else "•")
        ctk.CTkCheckBox(
            win, text="Show key", variable=show_var, command=toggle_show,
            font=ctk.CTkFont(size=12),
        ).pack(pady=(8, 0), **pad, anchor="w")

        def save():
            self.cfg["api_key"] = key_var.get().strip()
            save_config(self.cfg)
            self._set_status("API key saved.")
            win.destroy()

        ctk.CTkButton(
            win, text="Save", width=120,
            font=ctk.CTkFont(size=13), command=save,
        ).pack(pady=16)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
