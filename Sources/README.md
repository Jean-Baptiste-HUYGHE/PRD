# A NIfTI (nii.gz) 3D Visualizer using VTK and Qt5

<img src="https://github.com/adamkwolf/3d-nii-visualizer/blob/master/images/visualization.png" style="width: 100px;"/>

### Description
The project is a python project that allows you to display a 3D brain model from a Nifti file. This project also allows to display a graph in 3D .

### Installation

1.  Install Python `apt update; apt install python3`
2.  Create and use a virtual environment. Mac and Linux can use virtualenv or conda. Windows must use conda.
3.  Install the dependencies (PyQt5, vtk, and sip) `pip3 install -r requirements.txt`

### Run the program

Start the program `python3 ./visualizer/brain_tumor_3d.py -i "./sample_data/10labels_example/T1CE.nii.gz" -m "./sample_data/10labels_example/mask.nii.gz"`

### Run prebuilt executables
Go into project directory and run `./dist/Theia -i "./sample_data/10labels_example/T1CE.nii.gz" -m "./sample_data/10labels_example/mask.nii.gz"`

### Generate PyInstaller Binaries
**Note**: Must modify the paths in .spec file to match your project directory
* Mac: `pyinstaller Theia_Mac.spec`
* Windows: `pyinstaller Theia_Windows.spec`

### Tests
* `python3 -m pytest`


### License
It's a MIT license, you can do what you want with that project.

The only restriction is that you must incorporate a license of your choice into the project.

### Acknowledgements

[1] The original project: Adam Wolf, Ryan-Efendy, Omair Bhore "https://github.com/adamkwolf/3d-nii-visualizer"

[2] S.Bakas et al, "Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features", Nature Scientific Data, 4:170117 (2017) DOI: 10.1038/sdata.2017.117

[3] B.Menze et al, "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)", IEEE Transactions on Medical Imaging 34(10), 1993-2024 (2015) DOI: 10.1109/TMI.2014.2377694
