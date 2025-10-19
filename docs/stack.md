# Library Stack

The current prototype depends on a small set of cross-platform libraries:

- **pynput** – global keyboard listener and controller that works on Windows, macOS, and Linux without elevated privileges.
- **PySide6** – Qt-based UI toolkit for the future configuration interface; mature bindings with active maintenance.
- **platformdirs** – resolves user-specific configuration paths consistently across platforms.
- **pyinstaller** – packages the application into native executables for each target OS.
