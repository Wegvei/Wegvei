
import sys
import gi,threading

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk, GObject
from .window import RemoveBGWindow
from .settings import Settings
import sys



class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.Wegvei',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        css = '''
        .selection{
	        background-color:@accent_bg_color;
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.win = []
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('window_resizing', lambda *_: self.resizing(), ['<primary>r'])
        self.create_action('restart', lambda *_: self.restart(), ['<primary>t'])
        self.create_action('deselect', lambda *_: self.deselect(), ['Escape'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('new', self.new)
    def new(self,widget = None, _ = None):
        self.win.append(RemoveBGWindow(application=self))
        self.win[-1].present()
    def resizing(self, widget = None, _ = None):
        if type(self.props.active_window) == RemoveBGWindow:
            self.props.active_window.window_resizing()
    def restart(self, widget = None, _ = None):
        if type(self.props.active_window) == RemoveBGWindow:
            threading.Thread(target=self.props.active_window.restart).start()
    def deselect(self, widget = None, _ = None):
        if type(self.props.active_window) == RemoveBGWindow:
            self.props.active_window.deselect()

    def do_activate(self):
        self.win.append(RemoveBGWindow(application=self))
        self.win[-1].present()

    def on_about_action(self, widget = None, _ = None):
        """Callback for the app.about action."""
        self.about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Wegvei',
                                application_icon='io.github.Wegvei',
                                developer_name='qwersyk',
                                version='0.1.0',
                                developers=['qwersyk'],
                                copyright='© 2023 qwersyk')
        self.about.present()

    def on_preferences_action(self, widget = None, _ = None):
        self.settings = Settings(self.props.active_window)
        self.settings.present()
        self.settings.connect("close-request", self.close_preferences)

    def close_preferences(self, *a):
        self.settings.destroy()
        if type(self.props.active_window) == RemoveBGWindow:
            for win in self.win:
                win.update_model()
        return True

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = Application()
    return app.run(sys.argv)

