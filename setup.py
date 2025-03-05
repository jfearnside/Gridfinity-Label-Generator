from cx_Freeze import setup, Executable
import sys
import os

# Include the necessary Qt plugins
qt_plugins_dir = os.path.join(sys.base_prefix, 'Library', 'plugins')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(qt_plugins_dir, 'platforms')

build_exe_options = {
    "packages": ["os", "sys", "PySide6"],
    "include_files": [
        (os.path.join(qt_plugins_dir, 'platforms'), 'platforms'),
        ('meca', 'meca'),  # Include the meca directory
        # Add any other necessary files or directories here
        # Update the paths to the missing DLL files
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DAnimation.dll'), 'Qt63DAnimation.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DCore.dll'), 'Qt63DCore.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DExtras.dll'), 'Qt63DExtras.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DInput.dll'), 'Qt63DInput.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DLogic.dll'), 'Qt63DLogic.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt63DRender.dll'), 'Qt63DRender.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt6Charts.dll'), 'Qt6Charts.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt6DataVisualization.dll'), 'Qt6DataVisualization.dll'),
        (os.path.join(sys.base_prefix, 'Library', 'bin', 'Qt6Graphs.dll'), 'Qt6Graphs.dll'),
    ],
}

setup(
    name="Gridfinity Label Generator",
    version="1.0",
    description="Gridfinity Label Generator Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI")]
)