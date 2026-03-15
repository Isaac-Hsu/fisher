# To use in another file: from ui import get_selection
# items = get_selection()
## ui for fish selction + prio, returns list in order of prio

import tkinter as tk
from tkinter import ttk

# Colours
BG        = "#1e1e1e"   # window / frame background
BG2       = "#252526"   # listbox / canvas background
BG3       = "#2d2d2d"   # slightly raised surfaces
FG        = "#d4d4d4"   # default text
FG_DIM    = "#6a6a6a"   # subdued text
SEL_BG    = "#094771"   # listbox selection
SEL_FG    = "#ffffff"
BTN_BG    = "#3a3a3a"
BTN_ACT   = "#4a4a4a"

# Data
LOCATIONS = {
    "Camp Guillermo": {
        "Normal":   ["Bass", "Minnow", "Bluegill", "Crappie", "Goldfish", "Guppy", "Bullfrog", "Snapping Turtle", "Weather Loach", "Yellow Perch", "White Perch"],
        "Rare":     ["Koi", "Red Arowana"],
        "Boss":     ["Aspidochelone", "Ahuitzotl", "Snallygaster"],
        "Mythic":   ["Glowlight Neontetra", "Green Neontetra", "Black Neontetra", "Neontetra", "Bloodfin Neontetra", "Insane Fish"],
    },
    "Mystic Pond": {
        "Normal":   ["Flying Fish", "Goldfish", "Guppy", "Crayfish", "Box Turtle", "Weather Loach", "Clown Loach", "Snapping Turtle", "Crappie", "Bass"],
        "Rare":     ["Spectral Fish", "Koi", "Peters's Elephant-Nose Fish"],
        "Boss":     ["Vodyanoy", "Ogua"],
        "Mythic":   ["Pink Leech", "Colorful Leech", "Glowlight Neontetra", "Green Neontetra", "Black Neontetra", "Neontetra", "Bloodfin Neontetra", "Insane Fish"],
    },
    "Scurvy Waters": {
        "Normal":   ["Blue Tang", "Wahoo", "Lionfish", "Parrotfish", "Starfish", "Shrimp", "Sardine", "Smooth Oreo", "Shad", "Jellyfish"],
        "Rare":     ["Kathzilla", "Sailfish", "Butterfly Fish", "Leafy Sea Dragon"],
        "Boss":     ["Lusca", "Anglerfish"],
        "Mythic":   ["Megalodon", "Colorful Hoopfish", "Amethyst Hoopfish", "Sapphire Hoopfish", "Ruby Hoopfish", "Diamond Hoopfish", "Golden Hoopfish", "Purple Tang", "Seaman Fish", "Rainbow Fish"],
    },
    "Underwater Sanctuary": {
        "Normal":   ["Sardine", "Tuna", "Cod", "Mahi Mahi", "Swordfish", "Barracuda", "Salmon", "Vampire Squid", "Sablefish", "Clownfish"],
        "Rare":     ["Marlin", "Giant Squid", "Coelcanth", "Roundnose Grenadier"],
        "Boss":     ["Leviathan", "Kraken"],
        "Mythic":   ["Megalodon", "Seaman Fish", "Rainbow Fish"],
    },
    "Vertigo Beach": {
        "Normal":   ["Shrimp", "Sardine", "Cod", "Pufferfish", "Jellyfish", "Starfish", "Flounder", "Ocean Sunfish", "Boxfish", "Mandarinfish"],
        "Rare":     ["Butterfly Fish", "Hammerhead Shark", "Leafy Sea Dragon", "Stingray"],
        "Boss":     ["Charybdis", "Scylla"],
        "Mythic":   ["Colorful Hoopfish", "Amethyst Hoopfish", "Sapphire Hoopfish", "Ruby Hoopfish", "Diamond Hoopfish", "Golden Hoopfish", "Purple Tang", "Seaman Fish", "Rainbow Fish"],
    },
    "Wily River": {
        "Normal":   ["Rainbow Bass", "Electric Eel", "Piranha", "Catfish", "Crayfish", "Salmon", "Sturgeon", "Pearl Danio", "Redbreast Sunfish", "Oscar", "Minnow", "Trout"],
        "Rare":     ["Red Arowana", "Golden Dorado", "Arapaima"],
        "Boss":     ["Jormungandr", "Bunyip"],
        "Mythic":   ["Pink Leech", "Colorful Leech", "Insane Fish"],
    },
    "Abstraction Bay": {
        "Normal":   ["Jellyfish", "Shrimp", "Starfish", "Boxfish", "Mandarinfish", "Lionfish", "Blue Tang", "Sardine", "Pink Stripe", "Neon Tiger Fish", "Sad Yellow Shark"],
        "Rare":     ["Festive Koi", "Bony Crescent Fish", "Montezuma Fish"],
        "Boss":     ["Killer Triangle"],
    },
    "Crypt Keeper's Pond": {
        "Normal":   ["Ghost Fish", "Skeleton Fish", "Zombie Fish", "Piranha", "Electric Eel"],
        "Rare":     ["Spectral Fish", "Sea-Real Killer"],
        "Boss":     ["Gorgolox", "Witch Fish"],
    },
    "Desolate Crevasse": {
        "Normal":   ["Fleshfish", "Forktail Biter", "Guppy", "Flying Fish", "Subject 217", "Catfish"],
        "Boss":     ["Draethar", "Ogua"],
    },
    "Ice Caves": {
        "Normal":   ["Narwhal", "Beluga", "Arctic Char", "Jellyfish", "Sturgeon", "Ocean Sunfish", "Vampire Squid"],
        "Rare":     ["Coelcanth", "Leafy Sea Dragon"],
        "Boss":     ["Pliosaur"],
    },
    "Lake of Fire": {
        "Normal":   ["Demonfish", "Crispfin", "Fodderfeed", "Skeleton Fish"],
        "Rare":     ["Spectral Fish", "Fleshbiter"],
        "Boss":     ["Zephyris", "Snallygaster"],
    },
    "Love Island": {
        "Normal":   ["Chocolate Fish", "Rosefish", "Red Heartfish", "Purple Heartfish", "Pink Heartfish"],
        "Rare":     ["Lonely Fish", "Cupid Fish"],
        "Boss":     ["Lovecauser", "Heartbreaker"],
    },
    "Northpoint Cabin": {
        "Normal":   ["Arctic Char", "Nelma", "Striped Sweetfish", "Minnow", "Electric Eel", "Crappie", "Flying Fish", "Guppy", "Bluegill", "Bass"],
        "Rare":     ["Desolate Yetifish", "Gronchfish"],
        "Boss":     ["Issrakr"],
    },
    "Snowy Mountain": {
        "Normal":   ["Nelma", "Arctic Char", "Flying Fish", "Bluegill", "Guppy"],
        "Rare":     ["Arapaima", "Spectral Fish"],
        "Boss":     ["Issrakr"],
    },
}

# item shadow in every location
SHADOW_ITEM = "Item"

# highest priority first; shadow always last
CATEGORY_ORDER = ["Mythic", "Boss", "Rare", "Normal", "General Shadow"]
CATEGORY_RANK  = {"Mythic": 0, "Boss": 1, "Rare": 2, "Normal": 3, "General Shadow": 4}

CATEGORY_COLOURS = {
    "General Shadow": "#4a4a4a",
    "Normal": "#888888",
    "Rare":   "#4a9eff",
    "Boss":   "#e06c3a",
    "Mythic": "#c97be8",
}


# Public API

def get_selection() -> tuple[str, list[str]]:
    # Returns (location, items_in_priority_order)
    app = SelectorApp()
    app.mainloop()
    return app.result


# Helpers
def _all_items_for(loc: str) -> dict[str, list[str]]:
    cats = dict(LOCATIONS[loc])
    cats["General Shadow"] = [SHADOW_ITEM]
    return cats


def _apply_dark_style(root: tk.Tk):
    # background and foreground colors
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure(".",
        background=BG, foreground=FG,
        fieldbackground=BG3, troughcolor=BG2,
        bordercolor=BG3, darkcolor=BG3, lightcolor=BG3,
        selectbackground=SEL_BG, selectforeground=SEL_FG,
        insertcolor=FG,
    )
    s.configure("TFrame",       background=BG)
    s.configure("TLabel",       background=BG,  foreground=FG)
    s.configure("TButton",      background=BTN_BG, foreground=FG, borderwidth=0)
    s.map("TButton",
        background=[("active", BTN_ACT), ("pressed", BTN_ACT)],
        foreground=[("active", FG)],
    )
    s.configure("TCheckbutton", background=BG, foreground=FG)
    s.map("TCheckbutton",
        background=[("active", BG)],
        foreground=[("active", FG)],
        indicatorcolor=[("selected", "#4a9eff"), ("!selected", BG3)],
    )
    s.configure("TRadiobutton", background=BG, foreground=FG)
    s.map("TRadiobutton",
        background=[("active", BG)],
        indicatorcolor=[("selected", "#4a9eff"), ("!selected", BG3)],
    )
    s.configure("Vertical.TScrollbar",
        background=BG3, troughcolor=BG2, bordercolor=BG, arrowcolor=FG_DIM,
    )
    s.map("Vertical.TScrollbar", background=[("active", BTN_ACT)])


# Scrollable frame

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=BG)
        sb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = ttk.Frame(self.canvas, padding=(8, 4))
        self._win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda _e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(
            self._win_id, width=e.width))

        for w in (self.canvas, self.inner):
            self._bind_wheel(w)

    def _bind_wheel(self, w):
        w.bind("<MouseWheel>", self._scroll)
        w.bind("<Button-4>",   self._scroll)
        w.bind("<Button-5>",   self._scroll)

    def _scroll(self, e):
        if   e.num == 4: self.canvas.yview_scroll(-1, "units")
        elif e.num == 5: self.canvas.yview_scroll( 1, "units")
        else:            self.canvas.yview_scroll(int(-1 * e.delta / 120), "units")

    def propagate_wheel(self, widget):
        self._bind_wheel(widget)
        for child in widget.winfo_children():
            self.propagate_wheel(child)

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)


# Main app

class SelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Item Selector")
        self.geometry("680x460")
        self.minsize(520, 320)

        _apply_dark_style(self)

        self.result: tuple[str, list[str]] = ("", [])

        self.vars:          dict[str, dict[str, tk.BooleanVar]] = {}
        self.cat_vars:      dict[str, dict[str, tk.BooleanVar]] = {}
        self.mythic_var:    dict[str, tk.StringVar]             = {}
        self.priority_items: dict[str, list[tuple[str, str]]]   = {}

        self._current_loc: str | None = None
        self._drag_idx:    int | None = None
        self._updating = False

        self._init_state()
        self._build_ui()

    # State

    def _init_state(self):
        for loc in LOCATIONS:
            cats = _all_items_for(loc)
            self.vars[loc]            = {}
            self.cat_vars[loc]        = {}
            self.mythic_var[loc]      = tk.StringVar(value="")
            self.priority_items[loc]  = []

            for cat, items in cats.items():
                if cat == "Mythic":
                    continue
                self.cat_vars[loc][cat] = tk.BooleanVar(value=False)
                for item in items:
                    self.vars[loc][item] = tk.BooleanVar(value=False)

    # UI shell

    def _build_ui(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=8, pady=(8, 4))

        # Left: location list
        sidebar = ttk.Frame(main, width=158)
        sidebar.pack(side="left", fill="y", padx=(0, 8))
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="Location",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w", pady=(0, 4))

        loc_f = ttk.Frame(sidebar)
        loc_f.pack(fill="both", expand=True)
        loc_sb = ttk.Scrollbar(loc_f, orient="vertical")
        self.loc_lb = tk.Listbox(
            loc_f, selectmode="single", exportselection=False,
            yscrollcommand=loc_sb.set, activestyle="none",
            relief="flat", borderwidth=0,
            bg=BG2, fg=FG, selectbackground=SEL_BG, selectforeground=SEL_FG,
            highlightthickness=0,
        )
        loc_sb.configure(command=self.loc_lb.yview)
        loc_sb.pack(side="right", fill="y")
        self.loc_lb.pack(side="left", fill="both", expand=True)
        for loc in LOCATIONS:
            self.loc_lb.insert("end", loc)
        self.loc_lb.bind("<<ListboxSelect>>", self._on_loc_select)

        # Middle: item checkboxes
        mid = ttk.Frame(main)
        mid.pack(side="left", fill="both", expand=True)
        ttk.Label(mid, text="Items",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w", pady=(0, 4))
        self.scroll = ScrollableFrame(mid)
        self.scroll.pack(fill="both", expand=True)

        # Right: priority queue
        right = ttk.Frame(main, width=172)
        right.pack(side="left", fill="y", padx=(8, 0))
        right.pack_propagate(False)

        ttk.Label(right, text="Priority",
                  font=("TkDefaultFont", 9, "bold")).pack(anchor="w", pady=(0, 1))
        ttk.Label(right, text="drag to reorder",
                  font=("TkDefaultFont", 7, "italic"),
                  foreground=FG_DIM).pack(anchor="w", pady=(0, 4))

        prio_f = ttk.Frame(right)
        prio_f.pack(fill="both", expand=True)
        prio_sb = ttk.Scrollbar(prio_f, orient="vertical")
        self.prio_lb = tk.Listbox(
            prio_f, selectmode="single", exportselection=False,
            yscrollcommand=prio_sb.set, activestyle="dotbox",
            relief="flat", borderwidth=0,
            bg=BG2, fg=FG, selectbackground=SEL_BG, selectforeground=SEL_FG,
            highlightthickness=0,
        )
        prio_sb.configure(command=self.prio_lb.yview)
        prio_sb.pack(side="right", fill="y")
        self.prio_lb.pack(side="left", fill="both", expand=True)

        self.prio_lb.bind("<Button-1>",        self._drag_start)
        self.prio_lb.bind("<B1-Motion>",       self._drag_motion)
        self.prio_lb.bind("<ButtonRelease-1>", self._drag_release)

        # Bottom
        bot = ttk.Frame(self)
        bot.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(bot, text="Confirm", command=self._confirm).pack(side="right")

        self.loc_lb.select_set(0)
        self.loc_lb.event_generate("<<ListboxSelect>>")

    # Location change
    def _on_loc_select(self, _=None):
        sel = self.loc_lb.curselection()
        if not sel:
            return
        loc = list(LOCATIONS.keys())[sel[0]]
        if loc == self._current_loc:
            return
        self._current_loc = loc
        self._rebuild_items(loc)
        self._refresh_priority(loc)

    # Item panel
    def _rebuild_items(self, loc: str):
        frame = self.scroll.inner
        for w in frame.winfo_children():
            w.destroy()

        cats = _all_items_for(loc)
        row = 0

        for cat in CATEGORY_ORDER:
            if cat not in cats:
                continue

            colour  = CATEGORY_COLOURS[cat]
            items   = cats[cat]
            is_myth = (cat == "Mythic")

            # Header
            hdr = ttk.Frame(frame)
            hdr.grid(row=row, column=0, sticky="ew", pady=(10, 2))

            if is_myth:
                tk.Label(hdr, text=f"✦  {cat}", fg=colour, bg=BG,
                         font=("TkDefaultFont", 9, "bold")).pack(side="left")
                tk.Label(hdr, text="   pick one  ", fg=colour, bg=BG,
                         font=("TkDefaultFont", 8, "italic")).pack(side="left")
                ttk.Button(
                    hdr, text="✕ clear", width=7,
                    command=lambda l=loc: self._on_mythic_clear(l),
                ).pack(side="right", padx=(0, 4))
            else:
                tk.Checkbutton(
                    hdr, variable=self.cat_vars[loc][cat],
                    fg=colour, bg=BG, activebackground=BG, activeforeground=colour,
                    selectcolor=BG3, relief="flat",
                    command=lambda l=loc, c=cat: self._on_cat_toggled(l, c),
                ).pack(side="left")
                tk.Label(hdr, text=f"✦  {cat}", fg=colour, bg=BG,
                         font=("TkDefaultFont", 9, "bold")).pack(side="left")
            row += 1

            if is_myth:
                ttk.Radiobutton(
                    frame, text="none",
                    variable=self.mythic_var[loc], value="",
                    command=lambda l=loc: self._on_mythic_changed(l),
                ).grid(row=row, column=0, sticky="w", padx=(20, 0))
                row += 1

            for item in items:
                if is_myth:
                    ttk.Radiobutton(
                        frame, text=item,
                        variable=self.mythic_var[loc], value=item,
                        command=lambda l=loc: self._on_mythic_changed(l),
                    ).grid(row=row, column=0, sticky="w", padx=(20, 0))
                else:
                    tk.Checkbutton(
                        frame, text=item, bg=BG, fg=FG,
                        activebackground=BG, activeforeground=FG,
                        selectcolor=BG3, relief="flat",
                        variable=self.vars[loc][item],
                        command=lambda l=loc, i=item, c=cat: self._on_item_toggled(l, i, c),
                    ).grid(row=row, column=0, sticky="w", padx=(20, 0))
                row += 1

        self.scroll.scroll_to_top()
        self.after(50, lambda: self.scroll.propagate_wheel(frame))

    # Priority helpers
    def _insert_at_default(self, loc: str, item: str, cat: str):
        plist = self.priority_items[loc]
        if any(it == item for it, _ in plist):
            return
        rank = CATEGORY_RANK[cat]
        insert_at = len(plist)
        for i, (_, c) in enumerate(plist):
            if CATEGORY_RANK[c] > rank:
                insert_at = i
                break
        plist.insert(insert_at, (item, cat))

    def _refresh_priority(self, loc: str):
        lb = self.prio_lb
        lb.delete(0, "end")
        for idx, (item, cat) in enumerate(self.priority_items[loc]):
            lb.insert("end", f"  {idx + 1}.  {item}")
            lb.itemconfig(idx, fg=CATEGORY_COLOURS[cat])

    # Callbacks

    def _on_item_toggled(self, loc: str, item: str, cat: str):
        if self.vars[loc][item].get():
            self._insert_at_default(loc, item, cat)
        else:
            self.priority_items[loc] = [
                (it, c) for it, c in self.priority_items[loc] if it != item
            ]
        self._refresh_priority(loc)
        self._updating = True
        cats = _all_items_for(loc)
        all_on = all(self.vars[loc][it].get() for it in cats[cat])
        self.cat_vars[loc][cat].set(all_on)
        self._updating = False

    def _on_cat_toggled(self, loc: str, cat: str):
        if self._updating:
            return
        state = self.cat_vars[loc][cat].get()
        cats = _all_items_for(loc)
        for item in cats[cat]:
            self.vars[loc][item].set(state)
            if state:
                self._insert_at_default(loc, item, cat)
            else:
                self.priority_items[loc] = [
                    (it, c) for it, c in self.priority_items[loc] if it != item
                ]
        self._refresh_priority(loc)

    def _on_mythic_changed(self, loc: str):
        new = self.mythic_var[loc].get()
        self.priority_items[loc] = [
            (it, c) for it, c in self.priority_items[loc] if c != "Mythic"
        ]
        if new:
            self.priority_items[loc].insert(0, (new, "Mythic"))
        self._refresh_priority(loc)

    def _on_mythic_clear(self, loc: str):
        self.mythic_var[loc].set("")
        self._on_mythic_changed(loc)

    # Drag

    def _drag_start(self, e):
        idx = self.prio_lb.nearest(e.y)
        if idx >= 0:
            self._drag_idx = idx
            self.prio_lb.selection_clear(0, "end")
            self.prio_lb.selection_set(idx)

    def _drag_motion(self, e):
        if self._drag_idx is None:
            return
        target = self.prio_lb.nearest(e.y)
        if target < 0 or target == self._drag_idx:
            return
        loc = self._current_loc
        plist = self.priority_items[loc]
        plist[self._drag_idx], plist[target] = plist[target], plist[self._drag_idx]
        self._drag_idx = target
        self._refresh_priority(loc)
        self.prio_lb.selection_clear(0, "end")
        self.prio_lb.selection_set(target)

    def _drag_release(self, _e):
        self._drag_idx = None

    # Confirm
    def _confirm(self):
        loc = self._current_loc or list(LOCATIONS.keys())[0]
        self.result = (loc, [item for item, _ in self.priority_items[loc]])
        self.destroy()


if __name__ == "__main__":
    location, selection = get_selection()
    print(f"Selection: {selection}")