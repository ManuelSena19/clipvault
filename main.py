import pyperclip
import tkinter as tk
from tkinter import ttk


class CheckListCtrl(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, selectmode='extended', columns='CopiedText')
        self.heading('#0', text='Index', anchor='w')
        self.heading('CopiedText', text='CopiedText', anchor='w')
        self.column('#0', width=50, stretch=False)
        self.column('CopiedText', width=140, stretch=True)

    def insert_item(self, item):
        index = self.insert('', 'end', text=str(len(self.get_children())))
        self.set(index, 'CopiedText', item)

    def remove_item(self, index):
        self.delete(index)

    def get_selected_items(self):
        return self.selection()

    def select_all_items(self):
        self.selection_set(self.get_children())

    def deselect_all_items(self):
        self.selection_remove(self.get_children())

    def clear_items(self):
        self.delete(*self.get_children())


class ClipboardCopierUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('ClipVault')

        self.clipboardValue = []

        self.main_panel = ttk.Frame(self)
        self.main_panel.pack(fill='both', expand=True, padx=5, pady=5)

        self.left_panel = ttk.Frame(self.main_panel)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        start_button = ttk.Button(self.left_panel, text='Start', command=self.start)
        start_button.pack(side='top', padx=5, pady=5)
        stop_button = ttk.Button(self.left_panel, text='Stop', command=self.stop)
        stop_button.pack(side='top', padx=5, pady=5)
        select_button = ttk.Button(self.left_panel, text='Select', command=self.select)
        select_button.pack(side='top', padx=5, pady=5)
        deselect_button = ttk.Button(self.left_panel, text='Deselect', command=self.deselect)
        deselect_button.pack(side='top', padx=5, pady=5)
        remove_button = ttk.Button(self.left_panel, text='Remove', command=self.remove)
        remove_button.pack(side='top', padx=5, pady=5)

        self.right_panel = ttk.Frame(self.main_panel)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        listbox = tk.Listbox(self.right_panel, width=140)
        listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.list = CheckListCtrl(self.right_panel)
        self.list.pack(fill='both', expand=True, padx=3, pady=3)

        #start_button.bind('<Button-1>', self.start)
        #stop_button.bind('<Button-1>', self.stop)
        #select_button.bind('<Button-1>', self.select)
        #deselect_button.bind('<Button-1>', self.deselect)
        #remove_button.bind('<Button-1>', self.remove)
        listbox.bind('<Double-Button-1>', self.on_item_activated)
        self.timer = None

    def reload_list_items(self):
        self.list.clear_items()
        for item in self.clipboardValue:
            self.list.insert_item(item)

    def load_items(self):
        self.reload_list_items()
        self.start()

    def start(self):
        if self.timer is None:
            self.timer = self.after(100, self.on_timer)

    def stop(self):
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None

    def on_timer(self):
        value = pyperclip.paste()
        if value not in self.clipboardValue:
            self.clipboardValue.append(value)
            self.list.insert_item(value)
        self.timer = self.after(100, self.on_timer)

    def select(self):
        self.list.select_all_items()

    def deselect(self):
        self.list.deselect_all_items()

    def remove(self):
        selected_items = self.list.get_selected_items()
        for item in selected_items:
            self.list.remove_item(item)
            self.clipboardValue.remove(self.list.item(item)['values'][0])

    def on_item_activated(self):
        pyperclip.copy(self.list.get_children(str(self.list.get_selected_items())))


def main():
    app = ClipboardCopierUI()
    app.mainloop()


if __name__ == '__main__':
    main()
