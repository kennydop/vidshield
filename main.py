import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from encdec import EncDec
import threading
import os

class VideoEncryptionApp(tk.Tk):
    def __init__(self, encdec):
        super().__init__()

        self.encdec = encdec
        self.title('VidShield')
        self.geometry('800x600')
        self.resizable(True, True)

        self.style = Style(theme='flatly')
        
        self.create_widgets()

    def create_widgets(self):
        self.label_mode = ttk.Label(self, text='Select Mode:')
        self.label_mode.pack(pady=10)

        self.mode_var = tk.StringVar(value='encrypt')
        self.radio_encrypt = ttk.Radiobutton(self, text='Encrypt', variable=self.mode_var, value='encrypt')
        self.radio_decrypt = ttk.Radiobutton(self, text='Decrypt', variable=self.mode_var, value='decrypt')
        self.radio_encrypt.pack(pady=5)
        self.radio_decrypt.pack(pady=5)

        self.label_input = ttk.Label(self, text='Select Input Video:')
        self.label_input.pack(pady=10)

        input_frame = ttk.Frame(self)
        input_frame.pack(pady=5, padx=10)
        
        self.entry_input = ttk.Entry(input_frame, width=50)
        self.entry_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.button_input = ttk.Button(input_frame, text='Browse', command=self.browse_input_file)
        self.button_input.pack(side=tk.LEFT, padx=5)

        self.label_output = ttk.Label(self, text='Select Output Location:')
        self.label_output.pack(pady=10)

        output_frame = ttk.Frame(self)
        output_frame.pack(pady=5, padx=10,)
        
        self.entry_output = ttk.Entry(output_frame, width=50)
        self.entry_output.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.button_output = ttk.Button(output_frame, text='Browse', command=self.browse_output_file)
        self.button_output.pack(side=tk.LEFT, padx=5)

        self.button_start = ttk.Button(self, text='Start', command=self.start_process, style='TButton', width=20)
        self.button_start.pack(pady=20)

        self.progress = ttk.Progressbar(self, mode='indeterminate', length=360)
        self.progress.pack(pady=10)


    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, file_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, file_path)

    def start_process(self):
        input_file = self.entry_input.get()
        output_file = self.entry_output.get()
        mode = self.mode_var.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        self.progress.start()
        threading.Thread(target=self.run_process, args=(mode, input_file, output_file)).start()

    def run_process(self, mode, input_file, output_file):
        try:
            if mode == 'encrypt':
                self.encdec.encrypt_video(input_file, output_file)
            else:
                self.encdec.decrypt_video(input_file, output_file)
            self.progress.stop()
            messagebox.showinfo("Success", f"{mode.capitalize()}ion completed successfully!")
            self.open_file_location(output_file)
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_file_location(self, file_path):
        directory = os.path.dirname(file_path)
        if os.name == 'nt':
            os.startfile(directory)
        elif os.name == 'posix':
            os.system(f'xdg-open "{directory}"')

key_encrypt = "54da3a085bb24aa4889e99712867880d"
kid_encrypt = "2522b17ecc28451a89d9e733445a6064"
schema_encrypt = "cenc-aes-ctr"
if __name__ == "__main__":
    encdec = EncDec(key_encrypt=key_encrypt, kid_encrypt=kid_encrypt, schema_encrypt=schema_encrypt)
    app = VideoEncryptionApp(encdec)
    app.mainloop()