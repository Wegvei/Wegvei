from gi.repository import Adw
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject, Gio, GLib,Pango
from .constants import Models

import random
import string
import colorsys,io
import time,json
import threading,os
def get_parameters(win):
    if win.image_height==0 or win.get_height() == 0:
        return {"size":{"height":1,"width":1},"margin":{"margin_top":0,"margin_start":0}}
    if win.image_width / win.image_height > win.get_width()/win.get_height():
        width = win.get_width()
        height = win.get_width() / win.image_width * win.image_height
        margin_top = (win.get_height() - height) / 2
        margin_start = 0
    else:
        width = win.get_height() / win.image_height * win.image_width
        height = win.get_height()
        margin_top = 0
        margin_start = (win.get_width() - width) / 2
    return {"size":{"height":height,"width":width},"margin":{"margin_top":margin_top,"margin_start":margin_start}}

def is_image_brighter_than_average(image_path):
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        total_brightness = 0
        total_pixels = pixbuf.get_width() * pixbuf.get_height()
        pixels = pixbuf.get_pixels()
        n_channels = pixbuf.get_n_channels()
        rowstride = pixbuf.get_rowstride()
        for y in range(pixbuf.get_height()):
            for x in range(pixbuf.get_width()):
                i = y * rowstride + x * n_channels
                red = pixels[i]
                green = pixels[i + 1]
                blue = pixels[i + 2]
                brightness = (red + green + blue) / 3
                total_brightness += brightness

        average_brightness = total_brightness / total_pixels
        threshold = 128
        return average_brightness > threshold
    except Exception as e:
        return False



class HighlightedBox(Adw.Bin):
    __gtype_name__ = 'HighlightedBox'
    def __init__(self,window,size,margin):
        super().__init__(valign=Gtk.Align.START,halign=Gtk.Align.START)
        self.set_css_classes(["selection","card"])
        self.set_opacity(0.25)
        self.name = self.generate_name()
        self.parent = window
        self.margin = margin
        self.size = size
        threading.Thread(target=self.on_active).start()
    def on_active(self):
        self.update_box()
        while self.get_opacity()!=0:
            time.sleep(0.02)
            self.set_opacity(max(self.get_opacity()-0.01,0))
        self.set_css_classes([])
        if self.margin[0]<0 or self.margin[1]<0 or self.margin[0]>1 or self.margin[1]>1 or self.size[0]>1 or self.size[1]>1 or self.margin[0]+self.size[0]>1 or self.margin[1]+self.size[1]>1:
            if self.margin[1]>1 or self.margin[0]>1 or self.margin[0]+self.size[0]<0 or self.margin[1]+self.size[1]<0:
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,valign=Gtk.Align.CENTER,css_classes=["warning"])
                icon = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="dialog-warning"))
                icon.set_icon_size(Gtk.IconSize.LARGE)
                box.append(icon)
                box.append(Gtk.Label(
                    label=_("Cropping isn't right"),
                    margin_top=10, margin_start=10, margin_bottom=10, margin_end=10, wrap=True,
                    wrap_mode=Pango.WrapMode.WORD_CHAR,css_classes=["title-2"]))
                self.set_child(box)
                threading.Thread(target=self.show_animation).start()
            else:
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,valign=Gtk.Align.CENTER,css_classes=["warning"])
                icon = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="dialog-warning"))
                icon.set_icon_size(Gtk.IconSize.LARGE)
                box.append(icon)
                box.append(Gtk.Label(
                    label=_("Cropping is out of bounds"),
                    margin_top=10, margin_start=10, margin_bottom=10, margin_end=10, wrap=True,
                    wrap_mode=Pango.WrapMode.WORD_CHAR,css_classes=["title-2"]))
                button = Gtk.Button(css_classes=["flat"],icon_name="view-restore-symbolic",halign=Gtk.Align.CENTER)
                button.connect('clicked', self.resize)
                box.append(button)
                self.set_child(box)
                threading.Thread(target=self.show_animation).start()
        else:
            threading.Thread(target=self.generate_image_block).start()
    def resize(self,*a):
        if self.margin[1]<0:
            self.size[1]+=self.margin[1]
            self.margin[1]=0
        if self.margin[0]<0:
            self.size[0]+=self.margin[0]
            self.margin[0]=0
        if self.margin[1]+self.size[1]>1:
            self.size[1]=1-self.margin[1]
        if self.margin[0]+self.size[0]>1:
            self.size[0]=1-self.margin[0]
        self.update_box()
        threading.Thread(target=self.generate_image_block).start()
    def restart_button_pressed(self,*a):
        threading.Thread(target=self.generate_image_block).start()
    def show_animation(self):
        while self.get_opacity()!=1:
            time.sleep(0.02)
            self.set_opacity(min(self.get_opacity()+0.02,1))
    def generate_image_block(self):
        spinner = Gtk.Spinner(spinning=True,halign=Gtk.Align.CENTER,valign=Gtk.Align.CENTER)
        spinner.set_size_request(10,10)
        self.set_child(spinner)
        threading.Thread(target=self.show_animation).start()
        self.crop_image(self.parent.image_path, GLib.get_user_cache_dir()+"/"+self.name+".png", self.margin[1], self.margin[0], self.size[0], self.size[1])
        if not (self.generate() and os.path.exists(GLib.get_user_cache_dir()+"/"+self.name+"_no_bg.png")):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,valign=Gtk.Align.CENTER,css_classes=["warning"])
            icon = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="dialog-warning"))
            icon.set_icon_size(Gtk.IconSize.LARGE)
            box.append(icon)
            box.append(Gtk.Label(
                label=_("Couldn't get an image"),
                margin_top=10, margin_start=10, margin_bottom=10, margin_end=10, wrap=True,
                wrap_mode=Pango.WrapMode.WORD_CHAR,css_classes=["title-2"]))
            button = Gtk.Button(css_classes=["flat"],icon_name="view-refresh-symbolic",halign=Gtk.Align.CENTER)
            button.connect('clicked', self.restart_button_pressed)
            box.append(button)
            self.set_child(box)

        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(GLib.get_user_cache_dir()+"/"+self.name+"_no_bg.png")
            self.image = Gtk.Picture.new_for_pixbuf(pixbuf)
            self.image.set_opacity(0.2)
            self.set_child(self.image)
            with open(GLib.get_user_cache_dir()+"/"+self.name+"_no_bg.png", "rb") as file:
                image_data = file.read()
            self.bytes_object = GLib.Bytes.new(image_data)
            self.drag_source = Gtk.DragSource.new()
            self.drag_source.set_actions(Gdk.DragAction.COPY)
            self.drag_source.connect("prepare", self.move)
            self.image.add_controller(self.drag_source)
            while self.image.get_opacity()!=1:
                time.sleep(0.02)
                self.image.set_opacity(min(self.image.get_opacity()+0.01,1))
                self.parent.image.set_opacity(max(self.parent.image.get_opacity()-0.01,0.2))
    def generate(self):
        try:
            return self.parent.model.remove_background(GLib.get_user_cache_dir()+"/"+self.name+".png",new_file_name=GLib.get_user_cache_dir()+"/"+self.name+"_no_bg.png")
        except Exception as e:
            return False

    def crop_image(self,input_path, output_path, top, left, width, height):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(input_path)
        img_width = pixbuf.get_width()
        img_height = pixbuf.get_height()
        x1 = int(left * img_width)
        y1 = int(top * img_height)
        x2 = int((left + width) * img_width)
        y2 = int((top + height) * img_height)
        cropped_pixbuf = pixbuf.new_subpixbuf(x1, y1, x2 - x1, y2 - y1)
        cropped_pixbuf.savev(output_path, 'jpeg', [], [])
    def generate_name(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(5))
    def move(self, drag_source, x, y):
        snapshot = Gtk.Snapshot.new()
        self.do_snapshot(self, snapshot)
        paintable = snapshot.to_paintable()
        drag_source.set_icon(paintable, int(x), int(y))
        return Gdk.ContentProvider.new_for_bytes("image/png",self.bytes_object)
    def update_box(self):
        width = self.parent.parameters["size"]["width"]
        height = self.parent.parameters["size"]["height"]
        margin_top = self.parent.parameters["margin"]["margin_top"]
        margin_start = self.parent.parameters["margin"]["margin_start"]
        self.set_size_request(self.size[0] * width ,self.size[1] * height)
        self.set_margin_top(self.margin[1] * height + margin_top)
        self.set_margin_start(self.margin[0] * width + margin_start)
        self.set_margin_bottom(self.parent.get_height() - self.margin[1] * height + margin_top - self.size[1] * height)
        self.set_margin_end(self.parent.get_width() - self.margin[0] * width + margin_start - self.size[0] * width)


class RemoveBGWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'RemoveBGWindow'
    image_path = None
    allhighlightedbox = []
    cursor_pos = None
    cursor=[0,0]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(400, 200)
        self.set_size_request(400,200)
        button = Gtk.Button(label="Drag and drop or select an image",margin_start=10, margin_end=10,  margin_top=10, margin_bottom=10,css_classes=["flat"])
        button.connect("clicked",self.open_dialog)


        headerbar = Adw.HeaderBar(css_classes=["flat"],valign=Gtk.Align.START,halign=Gtk.Align.END)
        headerbar.set_title_widget(Gtk.Box())

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("New window"), "app.new")
        menu.append(_("Settings"), "app.preferences")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)
        headerbar.pack_end(menu_button)


        main_overlay = Gtk.Overlay()
        main_overlay.add_overlay(headerbar)
        main_overlay.set_child(button)
        self.set_content(main_overlay)

        drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.COPY)
        drop_target.connect('drop', self.handle_file_drag)
        button.add_controller(drop_target)

    def open_dialog(self,widget):
        dialog = Gtk.FileChooserNative(transient_for=self,title=_("Open Image"), modal=True)
        dialog.connect("response", self.process_folder)
        dialog.show()

    def process_folder(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            dialog.destroy()
            self.activate_image(dialog.get_file().get_path())
        return False

    def handle_file_drag(self, DropTarget, data, x, y):
        self.activate_image(data)

    def activate_image(self,image_path):
        self.set_size_request(400,400)

        self.image_path = image_path

        if is_image_brighter_than_average(self.image_path):
            self.get_application().get_style_manager().set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.get_application().get_style_manager().set_color_scheme(Adw.ColorScheme.PREFER_DARK)

        self.image = Gtk.Picture.new_for_filename(self.image_path)

        headerbar = Adw.HeaderBar(css_classes=["flat"],valign=Gtk.Align.START,halign=Gtk.Align.END)
        headerbar.set_title_widget(Gtk.Box())

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(_("New window"), "app.new")
        menu.append(_("Remove all"), "app.restart")
        menu.append(_("Deselect"), "app.deselect")
        menu.append(_("Settings"), "app.preferences")
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)

        headerbar.pack_end(menu_button)

        self.point = Gtk.Box(css_classes=["selection","card"])
        self.point.set_valign(Gtk.Align.START)
        self.point.set_halign(Gtk.Align.START)
        self.point.set_opacity(0.25)

        self.image_width= GdkPixbuf.Pixbuf.new_from_file(self.image_path).get_width()
        self.image_height= GdkPixbuf.Pixbuf.new_from_file(self.image_path).get_height()

        self.overlay = Gtk.Overlay()
        self.overlay.set_child(self.image)

        self.main_overlay = Gtk.Overlay()
        self.main_overlay.add_overlay(headerbar)
        self.main_overlay.add_overlay(self.point)
        self.main_overlay.set_child(self.overlay)

        self.set_content(self.main_overlay)

        self.gesture_click = Gtk.GestureClick.new()
        self.gesture_click.connect("released", self.on_released)
        self.gesture_click.connect("pressed", self.on_pressed)

        self.image.add_controller(self.gesture_click)

        self.image.set_cursor(Gdk.Cursor.new_from_name("crosshair"))

        self.update_model()

        self.connect("notify::default-height", self.window_resizing)
        self.connect("notify::default-width", self.window_resizing)
        self.connect("notify::fullscreened", self.window_resizing)
        self.connect("notify::maximized", self.window_resizing)

        controller = Gtk.EventControllerMotion()
        controller.connect("motion", self.on_motion_notify)

        self.add_controller(controller)

    def on_motion_notify(self, event,x,y):
        if self.image_path!=None:
            self.cursor = [x,y]
            self.update_point(x,y)

    def restart(self):
        while self.image.get_opacity()!=1:
            time.sleep(0.02)
            self.image.set_opacity(min(self.image.get_opacity()+0.01,1))
        for child in self.allhighlightedbox:
            self.overlay.remove_overlay(child)
        self.allhighlightedbox = []

    def deselect(self):
        self.cursor_pos = None
        self.update_point()

    def update_model(self):
        settings = Gio.Settings.new('io.github.Wegvei')
        self.model = Models[settings.get_string("chosen-model")]["Class"](json.loads(settings.get_string("models"))[settings.get_string("chosen-model")])

    def update_point(self,x=None,y=None):
        self.parameters = get_parameters(self)
        if self.cursor_pos and x  and y:
            self.point.set_visible(True)
            self.point.set_size_request(abs(self.cursor_pos[0] * self.parameters["size"]["width"] + self.parameters["margin"]["margin_start"]-x),abs(self.cursor_pos[1] * self.parameters["size"]["height"] + self.parameters["margin"]["margin_top"]-y))
            self.point.set_margin_top(min(self.cursor_pos[1] * self.parameters["size"]["height"] + self.parameters["margin"]["margin_top"],y))
            self.point.set_margin_start(min(self.cursor_pos[0] * self.parameters["size"]["width"] + self.parameters["margin"]["margin_start"],x))
        else:
            self.point.set_visible(False)

    def window_resizing(self,*a):
        if self.image_path:
            self.update_point(*self.cursor)
            for child in self.allhighlightedbox:
                child.update_box()

    def on_pressed(self, gesture, event,x,y):
        self.parameters = get_parameters(self)
        cursor_pos = [(x-self.parameters["margin"]["margin_start"]) / self.parameters["size"]["width"] , (y-self.parameters["margin"]["margin_top"]) / self.parameters["size"]["height"]]
        if self.get_width()<x or 0>x or self.get_height()<y or 0>y:
            return None
        if self.cursor_pos:
            if abs(cursor_pos[1] - self.cursor_pos[1])<0.01 or abs(cursor_pos[0] - self.cursor_pos[0]) < 0.01:
                self.cursor_pos = cursor_pos
                return None
            box = HighlightedBox(self,[abs(cursor_pos[0] - self.cursor_pos[0]) , abs(cursor_pos[1] - self.cursor_pos[1])],[min(cursor_pos[0],self.cursor_pos[0]),min(cursor_pos[1],self.cursor_pos[1])])
            self.overlay.add_overlay(box)
            self.cursor_pos = None
            self.update_point()
            self.allhighlightedbox.append(box)
        else:
            self.cursor_pos = cursor_pos

    def on_released(self,gesture, event,x,y):
        if self.cursor_pos:
            self.on_pressed(gesture, event,x,y)


