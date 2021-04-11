"""
    File which contain VTK lib instruction and commands
"""
import vtk

from ErrorObserver import *
from NiiObject import *
from config import *
from NiiLabel import *

error_observer = ErrorObserver()

'''
VTK Pipeline:   reader ->
                extractor ->
                decimate ->
                smoother ->
                normalizer ->
                mapper
'''


def read_volume(file_name):
    """
    :param file_name: The filename of type 'nii.gz'
    :return: vtkNIFTIImageReader (https://www.vtk.org/doc/nightly/html/classvtkNIFTIImageReader.html)
    """
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileNameSliceOffset(1)
    reader.SetDataByteOrderToBigEndian()
    reader.SetFileName(file_name)
    reader.Update()
    return reader


def create_brain_extractor(brain):
    """
    Given the output from brain (vtkNIFTIImageReader) extract it into 3D using
    vtkFlyingEdges3D algorithm (https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html)
    :param brain: a vtkNIFTIImageReader volume containing the brain
    :return: the extracted volume from vtkFlyingEdges3D
    """
    brain_extractor = vtk.vtkFlyingEdges3D()
    brain_extractor.SetInputConnection(brain.reader.GetOutputPort())
    # brain_extractor.SetValue(0, sum(brain.scalar_range)/2)
    return brain_extractor


def create_mask_extractor(mask):
    """
    Given the output from mask (vtkNIFTIImageReader) extract it into 3D using
    vtkDiscreteMarchingCubes algorithm (https://www.vtk.org/doc/release/5.0/html/a01331.html).
    This algorithm is specialized for reading segmented volume labels.
    :param mask: a vtkNIFTIImageReader volume containing the mask
    :return: the extracted volume from vtkDiscreteMarchingCubes
    """
    mask_extractor = vtk.vtkDiscreteMarchingCubes()
    mask_extractor.SetInputConnection(mask.reader.GetOutputPort())
    return mask_extractor


def create_polygon_reducer(extractor):
    """
    Reduces the number of polygons (triangles) in the volume. This is used to speed up rendering.
    (https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html)
    :param extractor: an extractor (vtkPolyDataAlgorithm), will be either vtkFlyingEdges3D or vtkDiscreteMarchingCubes
    :return: the decimated volume
    """
    reducer = vtk.vtkDecimatePro()
    reducer.AddObserver('ErrorEvent', error_observer)  # throws an error event if there is no data to decimate
    reducer.SetInputConnection(extractor.GetOutputPort())
    reducer.SetTargetReduction(0.5)  # magic number
    reducer.PreserveTopologyOn()
    return reducer


def create_smoother(reducer, smoothness):
    """
    Reorients some points in the volume to smooth the render edges.
    (https://www.vtk.org/doc/nightly/html/classvtkSmoothPolyDataFilter.html)
    :param reducer:
    :param smoothness:
    :return:
    """
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(reducer.GetOutputPort())
    smoother.SetNumberOfIterations(smoothness)
    return smoother


def create_normals(smoother):
    """
    The filter can reorder polygons to insure consistent orientation across polygon neighbors. Sharp edges can be split
    and points duplicated with separate normals to give crisp (rendered) surface definition.
    (https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html)
    :param smoother:
    :return:
    """
    brain_normals = vtk.vtkPolyDataNormals()
    brain_normals.SetInputConnection(smoother.GetOutputPort())
    brain_normals.SetFeatureAngle(60.0)  #
    return brain_normals


def create_mapper(stripper):
    """
    Create a VTK mapper
    :param stripper: the object / source to add to the mapper
    :return: the new mapper
    """
    brain_mapper = vtk.vtkPolyDataMapper()
    brain_mapper.SetInputConnection(stripper.GetOutputPort())
    brain_mapper.ScalarVisibilityOff()
    brain_mapper.Update()
    return brain_mapper


def create_property(opacity, color):
    prop = vtk.vtkProperty()
    prop.SetColor(color[0], color[1], color[2])
    prop.SetOpacity(opacity)
    return prop


def create_actor(mapper, prop):
    """
    Create an actor
    :param mapper: the mapper
    :param prop: the actor property
    :return: the actor
    """
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetProperty(prop)
    return actor


def create_mask_table():
    m_mask_opacity = 1
    brain_lut = vtk.vtkLookupTable()
    brain_lut.SetRange(0, 4)
    brain_lut.SetRampToLinear()
    brain_lut.SetValueRange(0, 1)
    brain_lut.SetHueRange(0, 0)
    brain_lut.SetSaturationRange(0, 0)

    brain_lut.SetNumberOfTableValues(10)
    brain_lut.SetTableRange(0, 9)
    brain_lut.SetTableValue(0, 0, 0, 0, 0)
    brain_lut.SetTableValue(1, 1, 0, 0, m_mask_opacity)  # RED
    brain_lut.SetTableValue(2, 0, 1, 0, m_mask_opacity)  # GREEN
    brain_lut.SetTableValue(3, 1, 1, 0, m_mask_opacity)  # YELLOW
    brain_lut.SetTableValue(4, 0, 0, 1, m_mask_opacity)  # BLUE
    brain_lut.SetTableValue(5, 1, 0, 1, m_mask_opacity)  # MAGENTA
    brain_lut.SetTableValue(6, 0, 1, 1, m_mask_opacity)  # CYAN
    brain_lut.SetTableValue(7, 1, 0.5, 0.5, m_mask_opacity)  # RED_2
    brain_lut.SetTableValue(8, 0.5, 1, 0.5, m_mask_opacity)  # GREEN_2
    brain_lut.SetTableValue(9, 0.5, 0.5, 1, m_mask_opacity)  # BLUE_2
    brain_lut.Build()
    return brain_lut


def create_table():
    table = vtk.vtkLookupTable()
    table.SetRange(0.0, 1675.0)  # +1
    table.SetRampToLinear()
    table.SetValueRange(0, 1)
    table.SetHueRange(0, 0)
    table.SetSaturationRange(0, 0)


def add_surface_rendering(nii_object, label_idx, label_value):
    nii_object.labels[label_idx].extractor.SetValue(0, label_value)
    nii_object.labels[label_idx].extractor.Update()

    # if the cell size is 0 then there is no label_idx data
    if nii_object.labels[label_idx].extractor.GetOutput().GetMaxCellSize():
        reducer = create_polygon_reducer(nii_object.labels[label_idx].extractor)
        smoother = create_smoother(reducer, nii_object.labels[label_idx].smoothness)
        normals = create_normals(smoother)
        actor_mapper = create_mapper(normals)
        actor_property = create_property(nii_object.labels[label_idx].opacity, nii_object.labels[label_idx].color)
        actor = create_actor(actor_mapper, actor_property)
        nii_object.labels[label_idx].actor = actor
        nii_object.labels[label_idx].smoother = smoother
        nii_object.labels[label_idx].property = actor_property


def setup_slicer(renderer, brain):
    """
    Setup the brain slicer
    :param renderer: the renderer
    :param brain: the brain Nifti object
    :return: 3 brain slice images for each plan
    """
    x = brain.extent[1]
    y = brain.extent[3]
    z = brain.extent[5]

    axial = vtk.vtkImageActor()
    axial_prop = vtk.vtkImageProperty()
    axial_prop.SetOpacity(0)
    axial.SetProperty(axial_prop)
    axial.GetMapper().SetInputConnection(brain.image_mapper.GetOutputPort())
    axial.SetDisplayExtent(0, x, 0, y, int(z/2), int(z/2))
    axial.InterpolateOn()
    axial.ForceOpaqueOn()

    coronal = vtk.vtkImageActor()
    cor_prop = vtk.vtkImageProperty()
    cor_prop.SetOpacity(0)
    coronal.SetProperty(cor_prop)
    coronal.GetMapper().SetInputConnection(brain.image_mapper.GetOutputPort())
    coronal.SetDisplayExtent(0, x, int(y/2), int(y/2), 0, z)
    coronal.InterpolateOn()
    coronal.ForceOpaqueOn()

    sagittal = vtk.vtkImageActor()
    sag_prop = vtk.vtkImageProperty()
    sag_prop.SetOpacity(0)
    sagittal.SetProperty(sag_prop)
    sagittal.GetMapper().SetInputConnection(brain.image_mapper.GetOutputPort())
    sagittal.SetDisplayExtent(int(x/2), int(x/2), 0, y, 0, z)
    sagittal.InterpolateOn()
    sagittal.ForceOpaqueOn()

    renderer.AddActor(axial)
    renderer.AddActor(coronal)
    renderer.AddActor(sagittal)

    return [axial, coronal, sagittal]


def setup_projection(brain, renderer):
    """
    Setup the brain projection
    :param brain: the brain Nifti object
    :param renderer: the renderer
    :return: the brain projection image
    """
    slice_mapper = vtk.vtkImageResliceMapper()
    slice_mapper.SetInputConnection(brain.reader.GetOutputPort())
    slice_mapper.SliceFacesCameraOn()
    slice_mapper.SliceAtFocalPointOn()
    slice_mapper.BorderOff()

    brain_image_prop = vtk.vtkImageProperty()
    brain_image_prop.SetOpacity(0.0)
    brain_image_prop.SetInterpolationTypeToLinear()
    image_slice = vtk.vtkImageSlice()
    image_slice.SetMapper(slice_mapper)
    image_slice.SetProperty(brain_image_prop)
    image_slice.GetMapper().SetInputConnection(brain.image_mapper.GetOutputPort())
    renderer.AddViewProp(image_slice)
    return brain_image_prop


def setup_brain(renderer, file):
    """
    Setup and display the 3D brain
    :param renderer: the renderer
    :param file: the file path
    :return: the brain Nifti object
    """
    brain = NiiObject()
    brain.file = file
    brain.reader = read_volume(brain.file)
    brain.labels.append(NiiLabel(BRAIN_COLORS[0], BRAIN_OPACITY, BRAIN_SMOOTHNESS))
    brain.labels[0].extractor = create_brain_extractor(brain)
    brain.extent = brain.reader.GetDataExtent()

    scalar_range = brain.reader.GetOutput().GetScalarRange()
    bw_lut = vtk.vtkLookupTable()
    bw_lut.SetTableRange(scalar_range)
    bw_lut.SetSaturationRange(0, 0)
    bw_lut.SetHueRange(0, 0)
    bw_lut.SetValueRange(0, 2)
    bw_lut.Build()

    view_colors = vtk.vtkImageMapToColors()
    view_colors.SetInputConnection(brain.reader.GetOutputPort())
    view_colors.SetLookupTable(bw_lut)
    view_colors.Update()
    brain.image_mapper = view_colors
    brain.scalar_range = scalar_range

    add_surface_rendering(brain, 0, sum(scalar_range)/2)  # render index, default extractor value
    renderer.AddActor(brain.labels[0].actor)
    return brain


def setup_mask(renderer, file):
    """
    Setup and display the 3D mask
    :param renderer: the renderer
    :param file: the file path
    :return: the mask Nifti object
    """
    mask = NiiObject()
    mask.file = file
    mask.reader = read_volume(mask.file)
    mask.extent = mask.reader.GetDataExtent()
    n_labels = int(mask.reader.GetOutput().GetScalarRange()[1])
    n_labels = n_labels if n_labels <= 10 else 10

    for label_idx in range(n_labels):
        mask.labels.append(NiiLabel(MASK_COLORS[label_idx], MASK_OPACITY, MASK_SMOOTHNESS))
        mask.labels[label_idx].extractor = create_mask_extractor(mask)
        add_surface_rendering(mask, label_idx, label_idx + 1)
        renderer.AddActor(mask.labels[label_idx].actor)
    return mask

def setup_orientation_marker(interactor):
    """
    Draw a 3D mark (X, Y, Z axes)
    :param interactor: the window interactor
    :return: the orientation parker
    """
    # create and setup the component
    axes = vtk.vtkAxesActor()
    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText('X')
    axes.SetYAxisLabelText('Y')
    axes.SetZAxisLabelText('Z')
    axes.SetTotalLength(1.0, 1.0, 1.0)
    axes.SetCylinderRadius(0.5 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.5 * axes.GetSphereRadius())

    orientationMarker = vtk.vtkOrientationMarkerWidget()
    orientationMarker.SetOrientationMarker(axes)

    # Position it at the left bottom in the 3D vue (viewport)
    orientationMarker.SetViewport(0, 0, 0.2, 0.2)
    orientationMarker.SetInteractor(interactor)
    orientationMarker.EnabledOn()
    orientationMarker.InteractiveOn()
    return orientationMarker

"""
# a 3D red hightlight try for the selection
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # get the new
        self.NewPickedActor = picker.GetActor()

        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            colors = vtk.vtkNamedColors()
            self.NewPickedActor.GetProperty().SetColor(colors.GetColor3d('Red'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.NewPickedActor.GetProperty().EdgeVisibilityOn()

            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor

        self.OnLeftButtonDown()
        return
"""

# 2D silhouette class
class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    """
    Class use to highlight a selected component and generate an event when a component is selected
    """


    def __init__(self, silhouette, silhouette_actor, main_window):
        """
        Constructor
        :param silhouette: the silhouette object
        :param silhouette_actor: the silhouette actor
        :param main_window: the main_window to call events
        """
        self.main_window = main_window
        self.AddObserver("LeftButtonPressEvent", self.onLeftButtonDown)
        self.last_picked_actor = None
        self.silhouette = silhouette
        self.silhouette_actor = silhouette_actor

    def onLeftButtonDown(self, obj, event):
        """
        Method call by a left mouse clic
        :param obj: the vtkInteractorStyleTrackballCamera
        :param event: the LeftButtonPressEvent
        """
        click_pos = self.GetInteractor().GetEventPosition()

        #  Pick from this location.
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, self.GetDefaultRenderer())
        self.last_picked_actor = picker.GetActor()

        # If we picked something before, remove the silhouette actor and generate a new one
        if self.last_picked_actor:
            self.GetDefaultRenderer().RemoveActor(self.silhouette_actor)

            # if it's a node
            if self.last_picked_actor in self.main_window.correspondence_table_nodes.keys():
                selected_node = self.main_window.correspondence_table_nodes[self.last_picked_actor]
                self.main_window.event_node_selected(selected_node)

                # Highlight the picked actor by generating a silhouette
                self.silhouette.SetInputData(self.last_picked_actor.GetMapper().GetInput())
                self.GetDefaultRenderer().AddActor(self.silhouette_actor)

            # if it's an edge
            if self.last_picked_actor in self.main_window.correspondence_table_edges.keys():
                selected_edge = self.main_window.correspondence_table_edges[self.last_picked_actor]
                self.main_window.event_edge_selected(selected_edge)

                # Highlight the picked actor by generating a silhouette
                self.silhouette.SetInputData(self.last_picked_actor.GetMapper().GetInput())
                self.GetDefaultRenderer().AddActor(self.silhouette_actor)

        #  Forward events
        self.OnLeftButtonDown()


def setup_node(renderer, x, y, z, radius):
    """
    Setup a new node in the 3D visualisation
    :param renderer: the renderer
    :param x: node x coord
    :param y: node y coord
    :param z: node z coord
    :param radius: the node radius
    :return: the node actor
    """
    colors = vtk.vtkNamedColors()

    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(x, y, z)
    sphere.SetRadius(radius)

    # mapper
    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    # actor
    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)

    # color the actor
    sphereActor.GetProperty().SetColor(colors.GetColor3d('Yellow'))

    renderer.AddActor(sphereActor)
    return sphereActor

def setup_edge(renderer, x1, y1, z1, x2, y2, z2, size):
    """
    Setup a new edge in the 3D visualisation
    :param renderer: the renderer
    :param x1: the x coord for the point 1
    :param y1: the y coord for the point 1
    :param z1: the z coord for the point 1
    :param x2: the x coord for the point 2
    :param y2: the y coord for the point 2
    :param z2: the z coord for the point 2
    :param size: the edge size
    :return: the edge actor
    """
    colors = vtk.vtkNamedColors()

    line = vtk.vtkLineSource()
    line.SetPoint1((x1, y1, z1))
    line.SetPoint2((x2, y2, z2))

    lineMapper = vtk.vtkPolyDataMapper()
    lineMapper.SetInputConnection(line.GetOutputPort())
    lineActor = vtk.vtkActor()
    lineActor.SetMapper(lineMapper)
    lineActor.GetProperty().SetLineWidth(size)
    lineActor.GetProperty().SetColor(colors.GetColor3d("Peacock"))

    renderer.AddActor(lineActor)
    return lineActor

def setup_graph_selection(main_window):
    """
    Setup the graph selection
    :param main_window: the main_window the call event
    :return: the silhlouette
    """
    # add the custom style
    silhouette, silhouetteActor = _setup_silhouette(main_window.renderer)
    style = MouseInteractorHighLightActor(silhouette, silhouetteActor, main_window)
    style.SetDefaultRenderer(main_window.renderer)
    main_window.interactor.SetInteractorStyle(style)
    return silhouette


def _setup_silhouette(renderer):
    """
    Setup the silhouette to display around an object selected by the mouse
    :param renderer:
    :return: (the silhlouette, the silhouette actor)
    """
    colors = vtk.vtkNamedColors()

    # Create the silhouette pipeline, the input data will be set in the interactor
    silhouette = vtk.vtkPolyDataSilhouette()
    silhouette.SetCamera(renderer.GetActiveCamera())

    # Create mapper and actor for silhouette
    silhouetteMapper = vtk.vtkPolyDataMapper()
    silhouetteMapper.SetInputConnection(silhouette.GetOutputPort())

    silhouetteActor = vtk.vtkActor()
    silhouetteActor.SetMapper(silhouetteMapper)
    silhouetteActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
    silhouetteActor.GetProperty().SetLineWidth(5)
    return silhouette, silhouetteActor


