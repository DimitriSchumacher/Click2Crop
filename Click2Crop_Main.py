import numpy as np
import napari
import h5py
import skimage as ski
from tkinter import Tk
from tkinter import filedialog
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

viewer = napari.Viewer()

storage = []
names = []
size = []
counter = -1

def storage_array(viewer, size):

    global storage, counter

    counter = -1

    img_layers = []

    layers = viewer.layers

    for layer in layers:

        if type(layer) == napari.layers.image.image.Image:
                
                img_layers.append(layer)

    storage = np.zeros((len(img_layers), int(size),  int(size)))

    print("Storage array initialized... Shape: " + str(storage.shape))

def save_all_imgs(name):

    global names 

    root = Tk()
    root.withdraw()

    path = filedialog.askdirectory()

    hf_name = path + "/" + name + ".h5"

    hf = h5py.File(hf_name, "w")

    i = -1 

    for img in storage:

        i += 1

        hf.create_dataset(names[i], data=img)

    hf.close()

def save_all_imgs_tif(name):

    global names 

    root = Tk()
    root.withdraw()

    path = filedialog.askdirectory()

    i = -1 

    for img in storage:

        i += 1

        tif_name = path + "/" + name + "_Crop_" + str(i) + ".tif"

        ski.io.imsave(tif_name, img)

@viewer.mouse_drag_callbacks.append
def pointandcrop(viewer, event):

    global storage, counter, names, size

    if "Alt" in event.modifiers:
        
        counter += 1

        coords = event.position
        x = int(np.round(coords[1]))
        y = int(np.round(coords[0]))

        img_layer = viewer.layers.selection.active
        img = img_layer.data

        crop = img[y-int(int(size.text())/2):y+int(int(size.text())/2), x-int(int(size.text())/2):x+int(int(size.text())/2)]

        viewer.layers.remove(img_layer)

        if len(viewer.layers) > 0:
            viewer.layers.selection.active = viewer.layers[-1]   

        storage[counter] = crop

        name = "Crop " +  str(counter) + " - " + img_layer.name
        names.append(name)

class CenteringWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        
        global size

        self.setWindowTitle("Hdf5 Viewer Widget")
        
        layout = QVBoxLayout()
        label = QLabel("Click 2 Crop Widget")
        size_label = QLabel("Size")
        size = QLineEdit("50")
        init_button = QPushButton("Initialize Storage Array")
        text_box = QLineEdit("File_Name")
        save_button = QPushButton("Save to hdf5")
        save_tif_button = QPushButton("Save to tif")

        widgets = [label, 
                   size_label,
                   size,
                   init_button,
                   text_box,
                   save_button,
                   save_tif_button]
        
        for w in widgets:
            layout.addWidget(w)
            
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
        init_button.clicked.connect(lambda: storage_array(viewer, size=int(size.text())))
        save_button.clicked.connect(lambda: save_all_imgs(name=text_box.text()))
        save_tif_button.clicked.connect(lambda: save_all_imgs_tif(name=text_box.text()))

widget = CenteringWidget()

viewer.window.add_dock_widget(widget)

napari.run()

print("FINISHED")