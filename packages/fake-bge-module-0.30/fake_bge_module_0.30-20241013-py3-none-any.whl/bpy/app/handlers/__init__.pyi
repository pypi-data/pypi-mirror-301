"""
This module contains callback lists


--------------------

This script shows the most simple example of adding a handler.

```../examples/bpy.app.handlers.py```


--------------------

By default handlers are freed when loading new files, in some cases you may
want the handler stay running across multiple files (when the handler is
part of an add-on for example).

For this the bpy.app.handlers.persistent decorator needs to be used.

```../examples/bpy.app.handlers.1.py```


--------------------

Altering data from handlers should be done carefully. While rendering the
frame_change_pre

 and frame_change_post

 handlers are called from one
thread and the viewport updates from a different thread. If the handler changes
data that is accessed by the viewport, this can cause a crash of Blender. In
such cases, lock the interface (Render → Lock Interface or
bpy.types.RenderSettings.use_lock_interface) before starting a render.

Below is an example of a mesh that is altered from a handler:

```../examples/bpy.app.handlers.2.py```

"""

import typing
import collections.abc
import typing_extensions
import bpy.types

depsgraph_update_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on depsgraph update (post)
"""

depsgraph_update_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on depsgraph update (pre)
"""

frame_change_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" Called after frame change for playback and rendering, after the data has been evaluated for the new frame.
"""

frame_change_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" Called after frame change for playback and rendering, before any data is evaluated for the new frame. This makes it possible to change data and relations (for example swap an object to another mesh) for the new frame. Note that this handler is not to be used as 'before the frame changes' event. The dependency graph is not available in this handler, as data and relations may have been altered and the dependency graph has not yet been updated for that.
"""

game_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on ending the game engine
"""

game_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on starting the game engine
"""

load_factory_preferences_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading factory preferences (after)
"""

load_factory_startup_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading factory startup (after)
"""

load_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading a new blend file (after)
"""

load_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading a new blend file (before)
"""

persistent: typing.Any
""" Function decorator for callback functions not to be removed when loading new files
"""

redo_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading a redo step (after)
"""

redo_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading a redo step (before)
"""

render_cancel: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on canceling a render job
"""

render_complete: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on completion of render job
"""

render_init: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on initialization of a render job
"""

render_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on render (after)
"""

render_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on render (before)
"""

render_stats: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on printing render statistics
"""

render_write: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on writing a render frame (directly after the frame is written)
"""

save_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on saving a blend file (after)
"""

save_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on saving a blend file (before)
"""

undo_post: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading an undo step (after)
"""

undo_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on loading an undo step (before)
"""

version_update: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on ending the versioning code
"""

xr_session_start_pre: list[collections.abc.Callable[[bpy.types.Scene], None]]
""" on starting an xr session (before)
"""
