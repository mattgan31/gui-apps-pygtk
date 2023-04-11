#!/usr/bin/python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="secret",
  database="kasir",
  auth_plugin='mysql_native_password'
)

class MainWindow:

    def __init__(self):
        self._initUI()

    def _initUI(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("window2.glade")
        self.window = self.builder.get_object("window2")

        # create model and fill it with data
        self.liststore = Gtk.ListStore(int, str, int)
        self.load_data()

        # connect model to treeview
        self.treeview = self.builder.get_object("treeview")
        self.treeview.set_model(self.liststore)

        # create columns for treeview
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("ID", renderer_text, text=0)
        self.treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nama Barang", renderer_text, text=1)
        self.treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Harga", renderer_text, text=2)
        self.treeview.append_column(column_text)

        # Button
        self.submit_button1 = self.builder.get_object("button1")
        self.submit_button1.connect("clicked", self.add_form)

        self.submit_button2 = self.builder.get_object("button2")
        self.submit_button2.connect("clicked", self.edit_data)

        self.submit_button2 = self.builder.get_object("button3")
        self.submit_button2.connect("clicked", self.delete_data)

        self.window.connect("destroy", Gtk.main_quit)

        self.window.show_all()

    def load_data(self):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM produk')
        rows = cursor.fetchall()
        for row in rows:
            self.liststore.append(row)
        # db.close()

    def edit_data(self, widget):
        # mendapatkan data yang dipilih pada GtkTreeView
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            # mendapatkan data pada row yang dipilih
            id, nama_barang, harga = model[treeiter]
            # membuat window baru untuk form edit data
            edit_window = EditData(self, id, nama_barang, harga)

    def delete_data(self, widget):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            id = model[treeiter][0]
            delete_confirm = ConfirmDelete(self, id)


    def add_form(self, widget):
        new_window = AddData(self)
        # new_window.show()

    def refresh_data(self, widget):
        self.liststore.clear()
        self.load_data()

class AddData:

    def __init__(self, main_window):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main_window.glade")

        # membuat object builder untuk load ui glade
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")

        # mengambil Entry dari file .glade
        self.entry1 = self.builder.get_object("entry1")
        self.entry2 = self.builder.get_object("entry2")

        self.main_window = main_window

        # mengambil Button dari file .glade
        self.submit_button = self.builder.get_object("button1")
        self.submit_button.connect("clicked", self.on_button_click)


        # self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def on_button_click(self, widget, data=None):
        nama_barang = self.entry1.get_text()
        harga = self.entry2.get_text()
        val = (nama_barang, harga)
        cursor = db.cursor()
        sql = "INSERT INTO produk (nama_barang, harga) VALUES (%s, %s)"
        cursor.execute(sql, val)
        db.commit()
        print(nama_barang, harga)
        print("{} data berhasil disimpan".format(cursor.rowcount))
        # cursor.close()
        # db.close()
        self.window.hide()
        self.main_window.refresh_data(None)

    def on_window2_destroy(self, widget):
        widget.hide()

class EditData:

    def __init__(self, main_window, id, nama_barang, harga):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main_window.glade")

        # membuat object builder untuk load ui glade
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")

        # mengambil Entry dari file .glade
        self.entry1 = self.builder.get_object("entry1")
        self.entry1.set_text(nama_barang)
        self.entry2 = self.builder.get_object("entry2")
        self.entry2.set_text(str(harga))

        self.main_window = main_window
        self.id = id

        # mengambil Button dari file .glade
        self.submit_button = self.builder.get_object("button1")
        self.submit_button.connect("clicked", self.on_button_click)

        # self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def on_button_click(self, widget, data=None):
        nama_barang = self.entry1.get_text()
        harga = self.entry2.get_text()
        val = (nama_barang, harga, self.id)
        cursor = db.cursor()
        sql = "UPDATE produk SET nama_barang = %s, harga = %s WHERE id = %s"
        cursor.execute(sql, val)
        db.commit()
        print("{} data berhasil diubah".format(cursor.rowcount))
        self.window.hide()
        self.main_window.refresh_data(None)

    def on_window2_destroy(self, widget):
        widget.hide()

class ConfirmDelete:
    def __init__(self, main_window, id):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("confirmDelete.glade")

        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window3")

        self.main_window = main_window
        self.id = id

        self.submit_button = self.builder.get_object("buttonNo")
        self.submit_button.connect("clicked", self.on_button_no)
        self.submit_button = self.builder.get_object("buttonYes")
        self.submit_button.connect("clicked", self.on_button_yes)

        self.window.show()

    def on_button_yes(self, widget, data=None):
        print(self.id)
        val = (self.id,)
        cursor = db.cursor()
        sql = "DELETE FROM produk WHERE id = %s"
        cursor.execute(sql, val)
        db.commit()
        print("{} data berhasil dihapus".format(cursor.rowcount))
        self.window.hide()
        self.main_window.refresh_data(None)



    def on_button_no(self, widget):
        self.window.hide()

if __name__ == "__main__":
    window = MainWindow()
    Gtk.main()
