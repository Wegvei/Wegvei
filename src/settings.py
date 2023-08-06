import gi,json
from gi.repository import Gtk, Adw, Gio, GLib
from .constants import Models
import webbrowser
class Settings(Adw.PreferencesWindow):
    def __init__(self,win, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = Gio.Settings.new('io.github.Wegvei')
        self.set_transient_for(win)
        self.set_modal(True)
        self.models = json.loads(self.settings.get_string("models"))

        self.general_page = Adw.PreferencesPage()
        self.add(self.general_page)
        self.models_box = Adw.PreferencesGroup(title=_('Models'))
        self.general_page.add(self.models_box)

        group = Gtk.CheckButton()
        for model in Models:
            model_d = Models[model]
            row = Adw.ExpanderRow(title=model, subtitle=model_d["About"])
            button = Gtk.CheckButton()
            button.set_group(group)
            if model==self.settings.get_string("chosen-model"):
                button.set_active(True)
            button.set_name(model)
            button.connect("toggled", self.choose_model)
            row.add_prefix(button)
            row.set_name(model)
            self.models_box.add(row)
            wbbutton = Gtk.Button(icon_name="web-browser-symbolic")
            wbbutton.add_css_class("flat")
            wbbutton.set_valign(Gtk.Align.CENTER)
            wbbutton.set_name(model_d["Link"])
            wbbutton.connect("clicked", self.open_website)
            row.add_action(wbbutton)
            for name_inputs in model_d["Inputs"]:
                r = Adw.ActionRow(title=name_inputs)
                if model_d["Inputs"][name_inputs]["type"] == "boolean":
                    switch = Gtk.Switch(valign=Gtk.Align.CENTER)
                    if model in self.models and name_inputs in self.models[model]:
                        value = self.models[model][name_inputs]
                    else:
                        value = model_d["Inputs"][name_inputs]["default"]
                    switch.set_active(value)
                    switch.set_name(model+"//"+name_inputs)
                    switch.connect("notify::active", self.setting_change_switch)
                    r.add_suffix(switch)
                    row.add_row(r)
                else:
                    entry = Gtk.Entry(valign=Gtk.Align.CENTER)

                    if model in self.models and name_inputs in self.models[model]:
                        value = self.models[model][name_inputs]
                    else:
                        value = ""
                        if "default" in model_d["Inputs"][name_inputs]:
                            value = model_d["Inputs"][name_inputs]["default"]
                    entry.set_text(value)
                    entry.set_placeholder_text(model_d["Inputs"][name_inputs]["placeholder"])
                    entry.set_name(model+"//"+name_inputs)
                    entry.connect("changed", self.setting_change_entry)
                    r.add_suffix(entry)
                    row.add_row(r)
    def open_website(self, button):
        webbrowser.open(button.get_name())
    def setting_change_switch(self,switch, _):
        value = switch.get_name().split("//")
        if value[0] in self.models:
            self.models[value[0]][value[1]]=switch.get_state()
        else:
            self.models[value[0]]={value[1]:switch.get_state()}
        print(self.models)
        self.settings.set_string("models",json.dumps(self.models))


    def setting_change_entry(self,entry):
        value = entry.get_name().split("//")
        if value[0] in self.models:
            self.models[value[0]][value[1]]=entry.get_text()
        else:
            self.models[value[0]]={value[1]:entry.get_text()}
        self.settings.set_string("models",json.dumps(self.models))
    def choose_model(self, button):
        self.settings.set_string("chosen-model",button.get_name())
        if not(button.get_name() in self.models):
            self.models[button.get_name()]={}
            self.settings.set_string("models",json.dumps(self.models))
