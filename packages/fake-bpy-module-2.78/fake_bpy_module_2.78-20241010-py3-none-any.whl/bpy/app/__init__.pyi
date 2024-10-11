"""
This module contains application values that remain unchanged during runtime.

"""

import typing
import collections.abc
import typing_extensions
from . import handlers as handlers
from . import translations as translations

alembic: typing.Any
""" constant value bpy.app.alembic(supported=True, version=(1, 6, 0), version_string=' 1,  6,  0')
"""

autoexec_fail: typing.Any
""" Undocumented
"""

autoexec_fail_message: typing.Any
""" Undocumented
"""

autoexec_fail_quiet: typing.Any
""" Undocumented
"""

background: typing.Any
""" Boolean, True when blender is running without a user interface (started with -b)
"""

binary_path: str
""" The location of blenders executable, useful for utilities that spawn new instances
"""

binary_path_python: typing.Any
""" String, the path to the python executable (read-only)
"""

build_branch: typing.Any
""" The branch this blender instance was built from
"""

build_cflags: typing.Any
""" C compiler flags
"""

build_commit_date: typing.Any
""" The date of commit this blender instance was built
"""

build_commit_time: typing.Any
""" The time of commit this blender instance was built
"""

build_commit_timestamp: typing.Any
""" The unix timestamp of commit this blender instance was built
"""

build_cxxflags: typing.Any
""" C++ compiler flags
"""

build_date: typing.Any
""" The date this blender instance was built
"""

build_hash: typing.Any
""" The commit hash this blender instance was built with
"""

build_linkflags: typing.Any
""" Binary linking flags
"""

build_options: typing.Any
""" constant value bpy.app.build_options(bullet=True, codec_avi=True, codec_ffmpeg=True, codec_quicktime=False, codec_sndfile=False, compositor=True, cycles=True, cycles_osl=True, freestyle=True, gameengine=True, image_cineon=True, image_dds=True, image_frameserver=True, image_hdr=True, image_openexr=True, image_openjpeg=True, image_tiff=True, input_ndof=True, audaspace=True, international=True, openal=True, sdl=True, sdl_dynload=True, jack=True, libmv=True, mod_boolean=True, mod_fluid=True, mod_oceansim=True, ...)
"""

build_platform: typing.Any
""" The platform this blender instance was built for
"""

build_system: typing.Any
""" Build system used
"""

build_time: typing.Any
""" The time this blender instance was built
"""

build_type: typing.Any
""" The type of build (Release, Debug)
"""

debug: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_depsgraph: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_events: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_ffmpeg: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_freestyle: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_gpumem: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_handlers: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_python: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_simdata: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

debug_value: typing.Any
""" Int, number which can be set to non-zero values for testing purposes
"""

debug_wm: typing.Any
""" Boolean, for debug info (started with --debug / --debug_* matching this attribute name)
"""

driver_namespace: typing.Any
""" Dictionary for drivers namespace, editable in-place, reset on file load (read-only)
"""

ffmpeg: typing.Any
""" constant value bpy.app.ffmpeg(supported=True, avcodec_version=(57, 64, 101), avcodec_version_string='57, 64, 101', avdevice_version=(57, 1, 100), avdevice_version_string='57,  1, 100', avformat_version=(57, 56, 100), avformat_version_string='57, 56, 100', avutil_version=(55, 34, 100), avutil_version_string='55, 34, 100', swscale_version=(4, 2, 100), swscale_version_string=' 4,  2, 100')
"""

handlers: typing.Any
""" constant value bpy.app.handlers(frame_change_pre=[], frame_change_post=[], render_pre=[], render_post=[], render_write=[], render_stats=[], render_init=[], render_complete=[], render_cancel=[], load_pre=[], load_post=[], save_pre=[], save_post=[], scene_update_pre=[], scene_update_post=[], game_pre=[], game_post=[], version_update=[<function do_versions at 0x7f994d527378>], persistent=<class 'persistent'>)
"""

ocio: typing.Any
""" constant value bpy.app.ocio(supported=True, version=(1, 0, 9), version_string=' 1,  0,  9')
"""

oiio: typing.Any
""" constant value bpy.app.oiio(supported=True, version=(1, 7, 8), version_string=' 1,  7,  8')
"""

openvdb: typing.Any
""" constant value bpy.app.openvdb(supported=True, version=(3, 1, 0), version_string=' 3,  1,  0')
"""

render_icon_size: typing.Any
""" Reference size for icon/preview renders (read-only)
"""

render_preview_size: typing.Any
""" Reference size for icon/preview renders (read-only)
"""

sdl: typing.Any
""" constant value bpy.app.sdl(supported=True, version=(0, 0, 0), version_string='Unknown', available=False)
"""

tempdir: typing.Any
""" String, the temp directory used by blender (read-only)
"""

translations: typing.Any
""" Application and addons internationalization API
"""

version: tuple[int, int, int]
""" The Blender version as a tuple of 3 numbers. eg. (2, 50, 11)
"""

version_char: typing.Any
""" The Blender version character (for minor releases)
"""

version_cycle: typing.Any
""" The release status of this build alpha/beta/rc/release
"""

version_string: typing.Any
""" The Blender version formatted as a string
"""
