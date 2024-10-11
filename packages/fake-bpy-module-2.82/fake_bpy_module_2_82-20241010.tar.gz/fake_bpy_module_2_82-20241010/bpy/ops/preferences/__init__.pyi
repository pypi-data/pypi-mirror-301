import typing
import collections.abc
import typing_extensions
import bpy.types

def addon_disable(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    module: str = "",
):
    """Disable an add-on

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param module: Module, Module name of the add-on to disable
    :type module: str
    """

def addon_enable(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    module: str = "",
):
    """Enable an add-on

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param module: Module, Module name of the add-on to enable
    :type module: str
    """

def addon_expand(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    module: str = "",
):
    """Display information and preferences for this add-on

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param module: Module, Module name of the add-on to expand
    :type module: str
    """

def addon_install(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    overwrite: bool | None = True,
    target: typing.Literal["DEFAULT", "PREFS"] | None = "DEFAULT",
    filepath: str = "",
    filter_folder: bool | None = True,
    filter_python: bool | None = True,
    filter_glob: str = "*.py;*.zip",
):
    """Install an add-on

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param overwrite: Overwrite, Remove existing add-ons with the same ID
    :type overwrite: bool | None
    :param target: Target Path
    :type target: typing.Literal['DEFAULT','PREFS'] | None
    :param filepath: filepath
    :type filepath: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_python: Filter python
    :type filter_python: bool | None
    :param filter_glob: filter_glob
    :type filter_glob: str
    """

def addon_refresh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Scan add-on directories for new modules

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def addon_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    module: str = "",
):
    """Delete the add-on from the file system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param module: Module, Module name of the add-on to remove
    :type module: str
    """

def addon_show(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    module: str = "",
):
    """Show add-on preferences

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param module: Module, Module name of the add-on to expand
    :type module: str
    """

def app_template_install(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    overwrite: bool | None = True,
    filepath: str = "",
    filter_folder: bool | None = True,
    filter_glob: str = "*.zip",
):
    """Install an application-template

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param overwrite: Overwrite, Remove existing template with the same ID
    :type overwrite: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_glob: filter_glob
    :type filter_glob: str
    """

def copy_prev(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy settings from previous version

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def keyconfig_activate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
):
    """Undocumented contribute <https://developer.blender.org/T51061>

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    """

def keyconfig_export(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
    filepath: str = "keymap.py",
    filter_folder: bool | None = True,
    filter_text: bool | None = True,
    filter_python: bool | None = True,
):
    """Export key configuration to a python script

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All Keymaps, Write all keymaps (not just user modified)
    :type all: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_text: Filter text
    :type filter_text: bool | None
    :param filter_python: Filter python
    :type filter_python: bool | None
    """

def keyconfig_import(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "keymap.py",
    filter_folder: bool | None = True,
    filter_text: bool | None = True,
    filter_python: bool | None = True,
    keep_original: bool | None = True,
):
    """Import key configuration from a python script

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_text: Filter text
    :type filter_text: bool | None
    :param filter_python: Filter python
    :type filter_python: bool | None
    :param keep_original: Keep original, Keep original file after copying to configuration folder
    :type keep_original: bool | None
    """

def keyconfig_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove key config

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def keyconfig_test(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Test key-config for conflicts

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def keyitem_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add key map item

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def keyitem_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    item_id: int | None = 0,
):
    """Remove key map item

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param item_id: Item Identifier, Identifier of the item to remove
    :type item_id: int | None
    """

def keyitem_restore(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    item_id: int | None = 0,
):
    """Restore key map item

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param item_id: Item Identifier, Identifier of the item to remove
    :type item_id: int | None
    """

def keymap_restore(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
):
    """Restore key map(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All Keymaps, Restore all keymaps to default
    :type all: bool | None
    """

def reset_default_theme(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reset to the default theme colors

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def studiolight_copy_settings(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Copy Studio Light settings to the Studio light editor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: index
    :type index: int | None
    """

def studiolight_install(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    directory: str = "",
    filter_folder: bool | None = True,
    filter_glob: str = "*.png;*.jpg;*.hdr;*.exr",
    type: typing.Literal["MATCAP", "WORLD", "STUDIO"] | None = "MATCAP",
):
    """Install a user defined studio light

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param files: File Path
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    :param directory: directory
    :type directory: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_glob: filter_glob
    :type filter_glob: str
    :param type: type
    :type type: typing.Literal['MATCAP','WORLD','STUDIO'] | None
    """

def studiolight_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filename: str = "StudioLight",
):
    """Save custom studio light from the studio light editor settings

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filename: Name
    :type filename: str
    """

def studiolight_show(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Show light preferences

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def studiolight_uninstall(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Delete Studio Light

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: index
    :type index: int | None
    """

def theme_install(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    overwrite: bool | None = True,
    filepath: str = "",
    filter_folder: bool | None = True,
    filter_glob: str = "*.xml",
):
    """Load and apply a Blender XML theme file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param overwrite: Overwrite, Remove existing theme file if exists
    :type overwrite: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_folder: Filter folders
    :type filter_folder: bool | None
    :param filter_glob: filter_glob
    :type filter_glob: str
    """
