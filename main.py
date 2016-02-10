#!/usr/bin/env python3
# coding: utf-8

# Created by Louis ETIENNE

import os
from gi.repository import Gtk
from drawer import *

class TrekkeWindow:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('gui.glade')

        handler = {
            'on_save_clicked': self.on_save,
            'on_modulo_changed': self.on_updated,
            'on_factor_changed': self.on_updated,
            'on_reverse_toggled': self.on_updated,
            'on_text_toggled': self.on_updated,
            'on_type_changed': self.on_updated,
            'on_quit_clicked': Gtk.main_quit  
        }

        builder.connect_signals(handler)
        self.window = builder.get_object('window')

        self.type = builder.get_object('type')
        self.preview = builder.get_object('preview')
        self.modulo = builder.get_object('modulo')
        self.factor = builder.get_object('factor')
        self.reverse = builder.get_object('reverse')
        self.text = builder.get_object('text')
        self.save = builder.get_object('save')

        self.save.set_sensitive(False)
        self.on_updated(1)

    def on_save(self, button):
        dialog = Gtk.FileChooserDialog("Enregistrer l'image", self.window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.OK,
                                        Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL))
        self.add_filters(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            image_path, image_ext = os.path.splitext(dialog.get_filename())
            image_name = '{}.png'.format(image_path)

            save_image_to_png(image_name)

        dialog.destroy()

    def add_filters(self, dialog):
        filter_png = Gtk.FileFilter()
        filter_png.set_name("Images PNG")
        filter_png.add_mime_type("image/png")
        dialog.add_filter(filter_png)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Tous les fichiers")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_updated(self, spin):
        if self.type.get_active_id() == 'circles':
            print("Le type cercle n'est pas encore implémenté.")
            #build_image_with_circles(int(self.modulo.get_value()), self.factor.get_value(),
            #                        self.reverse.get_active(), self.text.get_active())
        else:
            build_image_with_chords(int(self.modulo.get_value()), self.factor.get_value(),
                                    self.reverse.get_active(), self.text.get_active())

        self.preview.set_from_file('output.svg')
        self.save.set_sensitive(True)


if __name__ == '__main__':
    app = TrekkeWindow()
    app.window.connect('delete-event', Gtk.main_quit)
    app.window.show_all()
    Gtk.main()
