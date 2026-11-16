"""Tkinter desktop interface for BEE2.5."""

from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from bee25.content.catalog import BUILTIN_STYLES, BUILTIN_VOICES, DEFAULT_SKYBOX
from bee25.export.portal2 import ExportError, export_vmf_to_portal2
from bee25.packages.manager import PackageManager
from bee25.packages.vmf import VMFError
from bee25.profiles import ProfileStore


class BEE25App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("BEE2.5 — Portal 2 package studio")
        self.root.geometry("980x700")
        self.root.minsize(780, 560)

        self.packages = PackageManager()
        self.profiles = ProfileStore()
        self.vmf_path = tk.StringVar()
        self.game_path = tk.StringVar()
        self.map_name = tk.StringVar()
        self.style_id = tk.StringVar()
        self.skybox_id = tk.StringVar()
        self.voice_id = tk.StringVar()
        self._style_values: dict[str, str] = {}
        self._skybox_values: dict[str, str] = {}
        self._voice_values: dict[str, str] = {}

        self._configure_theme()
        self._build_ui()
        self.refresh_packages()
        self.refresh_presets()

    def _configure_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook", padding=6)
        style.configure("TNotebook.Tab", padding=(14, 8))
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("Hint.TLabel", foreground="#666666")
        style.configure("Accent.TButton", padding=(12, 7))

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="BEE2.5", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Portal 2 package and map workspace • early development",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)

        self.package_tab = ttk.Frame(self.tabs, padding=14)
        self.preset_tab = ttk.Frame(self.tabs, padding=14)
        self.export_tab = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(self.package_tab, text="Packages")
        self.tabs.add(self.preset_tab, text="Styles / Skyboxes / Voices")
        self.tabs.add(self.export_tab, text="Export to Portal 2")

        self._build_packages_tab()
        self._build_presets_tab()
        self._build_export_tab()

        footer = ttk.Label(
            outer,
            text="VMF compiling is supported when Portal 2 compiler tools are installed. "
            "Puzzle Maker style application is not implemented yet.",
            style="Hint.TLabel",
            wraplength=900,
        )
        footer.pack(fill="x", pady=(10, 0))

    def _build_packages_tab(self) -> None:
        ttk.Label(self.package_tab, text="Installed packages", style="Title.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        self.package_list = tk.Listbox(self.package_tab, height=18, activestyle="dotbox")
        self.package_list.pack(fill="both", expand=True)

        buttons = ttk.Frame(self.package_tab)
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(
            buttons, text="Import package folder…", command=self.import_package
        ).pack(side="left")
        ttk.Button(
            buttons, text="New package…", command=self.create_package
        ).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Import VMF as package…", command=self.import_vmf).pack(
            side="left", padx=8
        )
        ttk.Button(
            buttons, text="Import ZIP…", command=self.import_package_archive
        ).pack(side="left")
        ttk.Button(buttons, text="Refresh", command=self.refresh_packages).pack(side="right")

        self.package_status = ttk.Label(
            self.package_tab,
            text=f"Package directory: {self.packages.root}",
            style="Hint.TLabel",
            wraplength=850,
        )
        self.package_status.pack(anchor="w", pady=(10, 0))

    def _build_presets_tab(self) -> None:
        ttk.Label(
            self.preset_tab, text="Choose content presets", style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

        self.style_combo = self._add_selector(
            self.preset_tab, 1, "Style", self.style_id, self._style_values
        )
        ttk.Button(
            self.preset_tab, text="Add custom style…", command=self.add_custom_style
        ).grid(row=1, column=2, sticky="ew", padx=(8, 0))

        self.skybox_combo = self._add_selector(
            self.preset_tab, 2, "Skybox", self.skybox_id, self._skybox_values
        )
        ttk.Button(
            self.preset_tab, text="Add custom skybox…", command=self.add_custom_skybox
        ).grid(row=2, column=2, sticky="ew", padx=(8, 0))

        self.voice_combo = self._add_selector(
            self.preset_tab, 3, "Voice", self.voice_id, self._voice_values
        )
        ttk.Label(
            self.preset_tab,
            text="Voice options are selectable presets. Custom voice asset importing "
            "and sound replacement will be added with package resource support.",
            style="Hint.TLabel",
            wraplength=780,
        ).grid(row=4, column=0, columnspan=3, sticky="w", pady=(16, 0))

        ttk.Label(
            self.preset_tab,
            text="Custom style entries currently inherit one of the listed base styles. "
            "Custom skyboxes store a material path; the material itself must be supplied "
            "inside a package.",
            style="Hint.TLabel",
            wraplength=780,
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(8, 0))
        self.preset_tab.columnconfigure(1, weight=1)

    @staticmethod
    def _add_selector(
        parent: ttk.Frame, row: int, label: str, variable: tk.StringVar, values: dict[str, str]
    ) -> ttk.Combobox:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=7)
        combo = ttk.Combobox(parent, state="readonly", textvariable=variable)
        combo.grid(row=row, column=1, sticky="ew", padx=10, pady=7)
        return combo

    def _build_export_tab(self) -> None:
        ttk.Label(self.export_tab, text="Compile a VMF map", style="Title.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 14)
        )
        ttk.Label(self.export_tab, text="VMF file").grid(row=1, column=0, sticky="w")
        ttk.Entry(self.export_tab, textvariable=self.vmf_path).grid(
            row=1, column=1, sticky="ew", padx=8
        )
        ttk.Button(self.export_tab, text="Browse…", command=self.choose_vmf).grid(
            row=1, column=2
        )

        ttk.Label(self.export_tab, text="Portal 2 install folder").grid(
            row=2, column=0, sticky="w", pady=8
        )
        ttk.Entry(self.export_tab, textvariable=self.game_path).grid(
            row=2, column=1, sticky="ew", padx=8
        )
        ttk.Button(self.export_tab, text="Browse…", command=self.choose_game).grid(
            row=2, column=2
        )

        ttk.Label(self.export_tab, text="Output map name").grid(row=3, column=0, sticky="w")
        ttk.Entry(self.export_tab, textvariable=self.map_name).grid(
            row=3, column=1, sticky="ew", padx=8, pady=5
        )

        self.export_button = ttk.Button(
            self.export_tab, text="Compile and export BSP", style="Accent.TButton",
            command=self.start_export,
        )
        self.export_button.grid(row=4, column=1, sticky="w", pady=12)

        ttk.Label(self.export_tab, text="Build log").grid(
            row=5, column=0, columnspan=3, sticky="w"
        )
        self.export_log = tk.Text(self.export_tab, height=15, wrap="word", state="disabled")
        self.export_log.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(5, 0))
        self.export_tab.columnconfigure(1, weight=1)
        self.export_tab.rowconfigure(6, weight=1)

        ttk.Label(
            self.export_tab,
            text="This compiles a VMF into a BSP and copies it to portal2/maps. "
            "The current build does not yet inject BEE2 Puzzle Maker items, style assets, "
            "skybox materials, or voice lines into the game.",
            style="Hint.TLabel",
            wraplength=820,
        ).grid(row=7, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def refresh_packages(self) -> None:
        self.package_list.delete(0, "end")
        packages = self.packages.list_packages()
        for package in packages:
            self.package_list.insert(
                "end",
                f"{package.manifest.name}  ·  {package.manifest.version}  ·  "
                f"{package.manifest.package_id}",
            )
        if not packages:
            self.package_list.insert("end", "No packages installed yet.")

    def create_package(self) -> None:
        name = simpledialog.askstring("New package", "Package display name:", parent=self.root)
        if not name:
            return
        default_id = "".join(
            char.lower() if char.isalnum() else "_" for char in name
        ).strip("_") or "my_package"
        package_id = simpledialog.askstring(
            "Package ID", "Unique lowercase package ID:",
            initialvalue=default_id[:64],
            parent=self.root,
        )
        if not package_id:
            return
        try:
            package = self.packages.create_package(package_id, name)
        except Exception as exc:
            messagebox.showerror("Could not create package", str(exc))
            return
        self.refresh_packages()
        messagebox.showinfo(
            "Package created",
            f"Created {package.manifest.name} at:\\n{package.path}",
        )

    def import_package(self) -> None:
        folder = filedialog.askdirectory(title="Select a BEE2.5 package folder")
        if not folder:
            return
        try:
            package = self.packages.install_package(Path(folder))
        except Exception as exc:
            messagebox.showerror("Package import failed", str(exc))
            return
        self.refresh_packages()
        messagebox.showinfo("Package imported", f"Installed {package.manifest.name}")

    def import_package_archive(self) -> None:
        filename = filedialog.askopenfilename(
            title="Select BEE2.5 ZIP package",
            filetypes=[("ZIP package", "*.zip"), ("All files", "*.*")],
        )
        if not filename:
            return
        try:
            package = self.packages.install_package_archive(Path(filename))
        except Exception as exc:
            messagebox.showerror("Package import failed", str(exc))
            return
        self.refresh_packages()
        messagebox.showinfo("Package imported", f"Installed {package.manifest.name}")

    def import_vmf(self) -> None:
        filename = filedialog.askopenfilename(
            title="Select a VMF map",
            filetypes=[("Valve Map Format", "*.vmf"), ("All files", "*.*")],
        )
        if not filename:
            return
        path = Path(filename)
        default_id = "".join(
            char.lower() if char.isalnum() else "_" for char in path.stem
        ).strip("_") or "my_map"
        package_id = simpledialog.askstring(
            "Package ID", "Use lowercase letters, digits, dots, underscores or hyphens:",
            initialvalue=default_id[:64],
            parent=self.root,
        )
        if not package_id:
            return
        name = simpledialog.askstring(
            "Package name", "Display name for this map package:",
            initialvalue=path.stem,
            parent=self.root,
        )
        if not name:
            return
        try:
            package, info = self.packages.create_vmf_package(path, package_id, name)
        except (ValueError, OSError, VMFError) as exc:
            messagebox.showerror("VMF import failed", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("VMF import failed", str(exc))
            return
        self.refresh_packages()
        messagebox.showinfo(
            "VMF imported",
            f"Created package {package.manifest.name}\n"
            f"Blocks: {info.block_count} • Entities: {info.entity_count}\n"
            f"Saved to: {package.path}",
        )

    def refresh_presets(self) -> None:
        self._style_values = {item["name"]: item["id"] for item in BUILTIN_STYLES}
        for item in self.profiles.list_profiles("styles"):
            self._style_values[item["name"]] = item["id"]
        self._skybox_values = {DEFAULT_SKYBOX["name"]: DEFAULT_SKYBOX["id"]}
        for item in self.profiles.list_profiles("skyboxes"):
            self._skybox_values[item["name"]] = item["id"]
        self._voice_values = {item["name"]: item["id"] for item in BUILTIN_VOICES}

        for combo, values in (
            (self.style_combo, self._style_values),
            (self.skybox_combo, self._skybox_values),
            (self.voice_combo, self._voice_values),
        ):
            combo["values"] = list(values.keys())
        self._set_combo_first(self.style_combo)
        self._set_combo_first(self.skybox_combo)
        self._set_combo_first(self.voice_combo)

    @staticmethod
    def _set_combo_first(combo: ttk.Combobox) -> None:
        values = list(combo["values"])
        if values:
            combo.set(values[0])

    def _selected_id(self, combo: ttk.Combobox, values: dict[str, str]) -> str:
        return values.get(combo.get(), "")

    def add_custom_style(self) -> None:
        name = simpledialog.askstring("Custom style", "Style name:", parent=self.root)
        if not name:
            return
        profile_id = simpledialog.askstring("Custom style", "Unique ID:", parent=self.root)
        if not profile_id:
            return
        bases = [item["name"] for item in BUILTIN_STYLES]
        base_name = simpledialog.askstring(
            "Base style",
            "Enter the base style name:\n" + ", ".join(bases),
            initialvalue=bases[0],
            parent=self.root,
        )
        if not base_name:
            return
        base_id = next(
            (item["id"] for item in BUILTIN_STYLES if item["name"].lower() == base_name.lower()),
            None,
        )
        if base_id is None:
            messagebox.showerror("Invalid base style", "Choose one of the listed built-in styles.")
            return
        try:
            self.profiles.add_style(profile_id, name, base_id)
        except Exception as exc:
            messagebox.showerror("Could not add style", str(exc))
            return
        self.refresh_presets()

    def add_custom_skybox(self) -> None:
        name = simpledialog.askstring("Custom skybox", "Skybox name:", parent=self.root)
        if not name:
            return
        profile_id = simpledialog.askstring("Custom skybox", "Unique ID:", parent=self.root)
        if not profile_id:
            return
        material = simpledialog.askstring(
            "Skybox material",
            "Relative VMT path (example: skybox/my_skybox):",
            parent=self.root,
        )
        if not material:
            return
        try:
            self.profiles.add_skybox(profile_id, name, material)
        except Exception as exc:
            messagebox.showerror("Could not add skybox", str(exc))
            return
        self.refresh_presets()

    def choose_vmf(self) -> None:
        filename = filedialog.askopenfilename(
            title="Select VMF",
            filetypes=[("Valve Map Format", "*.vmf"), ("All files", "*.*")],
        )
        if filename:
            self.vmf_path.set(filename)
            if not self.map_name.get():
                self.map_name.set(Path(filename).stem)

    def choose_game(self) -> None:
        folder = filedialog.askdirectory(title="Select Portal 2 install folder")
        if folder:
            self.game_path.set(folder)

    def _append_log(self, message: str) -> None:
        self.export_log.configure(state="normal")
        self.export_log.insert("end", message + "\n")
        self.export_log.see("end")
        self.export_log.configure(state="disabled")

    def start_export(self) -> None:
        vmf = Path(self.vmf_path.get()) if self.vmf_path.get() else None
        game = Path(self.game_path.get()) if self.game_path.get() else None
        if vmf is None or game is None:
            messagebox.showwarning("Missing paths", "Select both a VMF file and Portal 2 folder.")
            return
        selected_style = self._selected_id(self.style_combo, self._style_values)
        selected_skybox = self._selected_id(self.skybox_combo, self._skybox_values)
        selected_voice = self._selected_id(self.voice_combo, self._voice_values)
        self.export_button.configure(state="disabled")
        self._append_log("Starting export…")

        def worker() -> None:
            try:
                result = export_vmf_to_portal2(
                    vmf,
                    game,
                    self.map_name.get().strip() or None,
                    style_id=selected_style,
                    skybox_id=selected_skybox,
                    voice_id=selected_voice,
                    progress=lambda msg: self.root.after(0, self._append_log, msg),
                )
            except (ExportError, OSError, ValueError) as exc:
                self.root.after(0, self._export_failed, str(exc))
            else:
                self.root.after(0, self._export_finished, str(result.bsp_path))

        threading.Thread(target=worker, daemon=True).start()

    def _export_failed(self, message: str) -> None:
        self._append_log("ERROR: " + message)
        self.export_button.configure(state="normal")
        messagebox.showerror("Export failed", message)

    def _export_finished(self, destination: str) -> None:
        self._append_log("Success: " + destination)
        self.export_button.configure(state="normal")
        messagebox.showinfo("Export complete", f"Compiled map copied to:\n{destination}")


def run() -> None:
    root = tk.Tk()
    BEE25App(root)
    root.mainloop()
