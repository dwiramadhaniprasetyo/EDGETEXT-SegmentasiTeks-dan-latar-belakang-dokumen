import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from edge_text_segmenter import segment_text, extract_text_from_image

class EdgeTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EdgeText: Segmentasi Teks Dokumen")
        self.root.geometry("900x600")

        self.image_path = None
        self.original_image = None
        self.segmented_image = None

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Button(frame, text="Unggah Gambar", command=self.load_image).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Segmentasi", command=self.process_segmentation).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Ekstrak Teks (OCR)", command=self.ocr_text).grid(row=0, column=2, padx=5)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="lightgray")
        self.canvas.pack(pady=10)

        self.text_box = tk.Text(self.root, height=10)
        self.text_box.pack(fill="both", padx=10, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)

    def display_image(self, path):
        img = Image.open(path)
        img = img.resize((800, 400))
        self.original_image = img
        tk_img = ImageTk.PhotoImage(img)
        self.canvas.image = tk_img
        self.canvas.create_image(0, 0, anchor="nw", image=tk_img)

    def process_segmentation(self):
        if not self.image_path:
            messagebox.showerror("Error", "Mohon unggah gambar terlebih dahulu.")
            return

        try:
            _, result = segment_text(self.image_path)
            self.segmented_image = result
            img_rgb = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil = img_pil.resize((800, 400))
            tk_img = ImageTk.PhotoImage(img_pil)
            self.canvas.image = tk_img
            self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def ocr_text(self):
        if self.segmented_image is None:
            messagebox.showwarning("Peringatan", "Lakukan segmentasi terlebih dahulu.")
            return

        extracted_text = extract_text_from_image(self.segmented_image)
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, extracted_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeTextApp(root)
    root.mainloop()
