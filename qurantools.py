from gi.repository import GObject, Gdk, Gtk, Gedit, Tepl


class QuranTools(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "QuranTools"

    window = GObject.property(type=Gedit.Window)

    CHARS = ["\u06d6", "\u06d7", "\u06da", "\u06d9", "\u06d8", "\u06db", "\u06dc"]
    BUTTON_CSS_CLASS = "QuranButton"

    def __init__(self):
        GObject.Object.__init__(self)
        self.item = None

    def do_activate(self):
        if self.item is not None:
            return

        css = f"""
        .{self.BUTTON_CSS_CLASS} {{
            font-family: "Amiri Quran";
            font-size: 20pt;
        }}
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        box = Gtk.ButtonBox()
        box.set_layout(Gtk.ButtonBoxStyle.CENTER)
        for c in self.CHARS:
            button = Gtk.Button.new_with_label(c)
            button.connect("clicked", self.on_button_clicked)
            button.get_style_context().add_class(self.BUTTON_CSS_CLASS)
            box.pack_start(button, True, True, 0)
        box.show_all()

        panel = self.window.get_bottom_panel()
        self.item = Tepl.PanelItem.new(box, "QuranTools", _("Quran Tools"), None, 0)
        panel.add(self.item)

    def do_deactivate(self):
        if self.item is None:
            return
        panel = self.window.get_bottom_panel()
        panel.remove(self.item)

    def do_update_state(self):
        pass

    def on_button_clicked(self, button):
        doc = self.window.get_active_document()
        if not doc:
            return

        c = button.get_label()
        bounds = doc.get_selection_bounds()
        if bounds:
            doc.delete(bounds[0], bounds[1])
            doc.insert(bounds[0], c)
        else:
            doc.insert_at_cursor(c)
