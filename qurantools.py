from gi.repository import GObject, Gdk, Gtk, Gedit

class QuranTools(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "QuranTools"

    window = GObject.property(type=Gedit.Window)

    CHARS = ["\u06D6", "\u06D7", "\u06D8", "\u06D9", "\u06DA", "\u06DB",
             "\u06DC"]
    BUTTON_CSS_CLASS = "QuranButton"

    def __init__(self):
        GObject.Object.__init__(self)
        self.box = None

    def do_activate(self):
        if self.box is not None:
            return

        css = f'''
        .{self.BUTTON_CSS_CLASS} {{
            font-family: "Amiri Quran";
            font-size: 20pt;
        }}
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.box = Gtk.ButtonBox()
        self.box.set_layout(Gtk.ButtonBoxStyle.CENTER)
        for c in self.CHARS:
            button = Gtk.Button.new_with_label(c)
            button.connect("clicked", self.on_button_clicked)
            button.get_style_context().add_class(self.BUTTON_CSS_CLASS)
            self.box.pack_start(button, True, True, 0)
        self.box.show_all()

        panel = self.window.get_bottom_panel()
        panel.add_titled(self.box, "QuranTools", _("Quran Tools"))

    def do_deactivate(self):
        if self.box is None:
            return
        panel = self.window.get_bottom_panel()
        panel.remove(self.box)

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
