"""
components.py

To Be Done.
"""

# ===================================
# Imports

# Standard Library
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from typing import Callable, Optional

#Third-party

# Code Files
from ..utils import constants
# ===================================

def label_constructor(
        frame: ttk.Frame,
        text: str,
        style: str = "TLabel") -> ttk.Label:
    """
    UI helper function for creating ttk.Labels
    
    Parameters:
    ----------
    frame: ttk.Frame
        frame the widget belongs to
    text: str
        the label's text
    style: str = "TLabel"
        style configuration of the label

    Returns:
    --------
    ttk.label
    """

    return ttk.Label(frame, text=text, style=style)

def button_constructor(
        frame: ttk.Frame,
        text: str,
        state: str,
        widget_style: str = "TButton",
        command: Optional[Callable] = None
    ) -> ttk.Button:

    return ttk.Button(frame, text=text, state=state, style=widget_style, command=command)

def entry_constructor(
        frame:ttk.Frame,
        width:int,
        style:str = "TEntry"
    ) -> ttk.Entry:
    return ttk.Entry(frame, width=width, style=style)

def combobox_constructor(
        frame: ttk.Frame,
        input_holder: tk.StringVar,
        values: tuple | list,
        state: str,
        width: int
    ) -> ttk.Combobox:

    return ttk.Combobox(
        frame,
        textvariable=input_holder,
        values=values,
        state=state,
        width=width
    )

class FontStyles:
    @classmethod
    def init_fonts(cls):
        cls.label_font = tkFont.Font(family="Arial", size=12)
        cls.header_page_font = tkFont.Font(family="Arial", size=14)
        cls.title_label = tkFont.Font(family="Montserrat", size=24, weight="bold")

def apply_default_styles():
    FontStyles.init_fonts()
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b"
    )

    style.configure(
        "Treeview.Heading",
        background="#1c1c1c",
        foreground="white"
    )

    style.configure(
        "TButton",
        font=constants.BUTTON_FONT_SIZE,
        foreground=constants.DEFAULT_STYLE["foreground"],
        background=constants.DEFAULT_STYLE["background"],
        width=15,
    )

    style.configure(
        "TLabel",
        font=FontStyles.label_font,
        foreground=constants.DEFAULT_STYLE["foreground"],
        background=constants.DEFAULT_STYLE["background"]
    )

    style.configure(
        "Header.TLabel",
        font=FontStyles.header_page_font
    )

    style.configure(
        "TEntry",
        font=constants.BUTTON_FONT_SIZE,
        foreground=constants.DEFAULT_STYLE["foreground"],
        fieldbackground=constants.DEFAULT_STYLE["background"],
        state=constants.BUTTON_NORMAL_STATE
    )

    style.configure(
        "TSpinbox",
        foreground=constants.DEFAULT_STYLE["foreground"],
        background=constants.DEFAULT_STYLE["background"],
        fieldbackground=constants.DEFAULT_STYLE["background"],
        font=constants.SPINBOX_FONT_SIZE,
        width=15
    )


    style.configure(
        "Disabled.TSpinbox",
        foreground=constants.DISABLED_SPINBOX_STYLE["foreground"],
        fieldbackground=constants.DISABLED_SPINBOX_STYLE["fieldbackground"],
        background=constants.DISABLED_SPINBOX_STYLE["background"],
        font=constants.SPINBOX_FONT_SIZE,
        width=15
    )

    style.configure(
        "TFrame",
        background=constants.DEFAULT_STYLE["background"]
    )

    style.configure(
        "Title.TLabel",
        font=FontStyles.title_label
    )

def apply_default_table_styling():
    style = ttk.Style()
    style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b"
    )

    style.configure(
        "Treeview.Heading",
        background="#1c1c1c",
        foreground="white"
    )

    style.configure("TButton",
        background="#FFFFFF",
        foreground="#000000"
    )

    style.map("TButton",
        background=[("active", "#dbd6cf")],
        foreground=[("active", "#000000")]
    )

def change_theme(bg, fg, root):
    style = ttk.Style()

    # General backgrounds
    root.configure(bg=bg)
    style.configure("TFrame", background=bg)

    # ttk widgets
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=bg, foreground=fg)
    style.configure("TEntry", fieldbackground=bg, foreground=fg)
    style.configure("TSpinbox", fieldbackground=bg, foreground=fg)

    style.configure(
        "Treeview",
        background=bg,
        foreground=fg,
        fieldbackground=bg
    )

    style.configure(
        "Treeview.Heading",
        background=bg,
        foreground=fg
    )

def apply_high_contrast_button():
    style = ttk.Style()
    style.configure("TButton",
        background="#FFFFFF",
        foreground="#000000"
    )

    style.map("TButton",
        background=[("active", "#FFFF00")],
        foreground=[("active", "#000000")]
    )