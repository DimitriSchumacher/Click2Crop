---Click2Crop Readme---

Napari program that allows the user to click on an image and crop it with the click-position being the center of the newly cropped image. The size of the crop around the center-point can be specified on the size text-box. 

To crop an image, or a group of images, load them onto napari first. Then initialize the storage array with the initialize storage array button. After initializing the storage, press the "alt" key and click on the active image layer where you want it to be cropped. The clicked images will be removed from the Napari viewer and the cropped images will be saved in the storage. After cropping all, the cropped images can be saved as .tif or hdf5 formats.

There is a test image in the /TestData directory.

Required Python packages: 
numpy
napari
h5py
skimage
tkinter
pyQt5
