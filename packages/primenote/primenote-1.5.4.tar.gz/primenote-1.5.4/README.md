# PrimeNote
PrimeNote is a clever and highly adaptable note-editing tool designed for both Linux and Windows. Its functionality allows for swift editing, storage, organization, and backup of an unlimited number of notes. With PrimeNote, users can take advantage of advanced text operations and an extensive range of modes encompassing text and image processing, as well as a built-in terminal emulator and Vim integration for advanced users. Its main features include;

- **Always-On-Top** - Notes stay at the forefront without causing any clutter on the taskbar.
- **Druide Antidote Grammar Tools** - PrimeNote offers built-in support for versions 9, 10 and 11.
- **Smart Formatting** - Input is standardized through the use of 'enhanced plain text', permitting basic text decorations.
- **Cross-Platform Compatibility** - Out of the box support available for Linux and Windows 7-10.
- **Well-Organized Layout** - Data is preserved in a folder structure using user-friendly formats.
- **Fernet Encryption** - Ensures the protection of critical and sensitive data.
- **Quick Search** - An in-built, keyboard-driven tool to swiftly flick through note titles and content.
- **Special Paste** - Quick text copying from PDF documents at your fingertips.
- **Image Support** - Offers basic image viewing features.
- **Customizability** - Extensive personalization, including appearance, menus, hotkeys, and mouse events, powered by CSS styling.
- **Virtual Machine Support** - Facilitates real-time editing and easy sharing of content within a shared note repository across multiple operating systems.
- **Command-Line Interface** - Get thorough access to all notes (exclusive to Linux, refer to 'pnote -h' for details).

# Getting Started — Installation
## Microsoft Windows
- For Windows 7 and above, download and execute the latest **[NSIS installer](https://gitlab.com/william.belanger/storage/-/raw/primenote/primenote-1.5.4.exe?inline=false)**

## Arch Linux
- Install `primenote-git` from the [Arch User Repository](https://aur.archlinux.org/packages/primenote-git) (AUR)
- To enable `console` and `vim` modes, install `qtermwidget` and `gvim` community packages.

## Debian Linux
As a convenience, a one-step install script is provided. As piping unknown scripts to bash is a controversial topic, use the manual installation procedure if preferred. In case that `pipx` is used for the first time, re-login after the installation may be required in order for `primenote` to be accessible from the command line.

### One-step automated install
* **Installation** `curl -sSL https://install.primenote.cc | bash`
* **Upgrade** `pipx upgrade primenote`
* **Uninstall** `pipx uninstall primenote`

### Manual install
```
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install PrimeNote using the 'pipx' tool
sudo apt-get install pipx
pipx install --include-deps primenote
pipx ensurepath
```

### Vim and Console modes support
- Manually install `QTermWidget` with PyQt bindings enabled. Refer to the [QTermWidget project page](https://github.com/lxqt/qtermwidget) for more details.
- Install `vim-gtk` with client-server mode enabled

<br/>

# Advanced Features
## Customizable window styles and palettes
- All notes are decorated using CSS files located at the program root;
  - `ui/global.css`: defines the overall geometry and style for all notes
  - `ui/styles/*`: overrides and extend `global.css` attributes
  - `ui/palettes/*`: handles widgets and icons color schemes
- Users can extend those with custom palettes and styles, override or ignore them
- PrimeNote adds its own CSS selector `NoteDecorations` for enhanced customization

## Console mode
- In this mode, the text box is replaced with a native terminal emulator
- When a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) is found, the file content is automatically executed in the terminal
- More QTermWidget color schemes can be added into `ui/terminal`

## Vim mode
- Provides a fully featured Vim instance in every note
- System-independent `vimrc` file and theme files
- Two-way communication between Vim servers and PrimeNote command-line interface
- Default settings allow for a seamless design between the text editing modes

## Virtual machine support
PrimeNote can be used simultaneously across two operating systems (OS). Thus, one can share a note folder with another user, a backup server or a virtual machine.<br/>

PrimeNote fully supports symbolic links (symlinks) on Linux, and partially on Windows. Hence, all notes can be stored in a remote location simply by replacing the notes repository folder with a symlink. Likewise, a symlink can be added into the repository. On Windows, however, please note that shortcuts do not equal symlinks, which require administrator privileges. Thankfully, PrimeNote provide a utility to ease the addition of symlinks into the note repository.

**Virtual machine**
- Create a symlink to the host notes repository
- Place it into a folder shared with the client machine
- On the client side, open a PrimeNote instance and right click on the tray icon
- Select `Open in a file manager`
- Replace the opened folder by the symlink, or add the symlink into it

**Limitations**
- `Rename` and `move` operations on symlinks will behave unexpectedly if used across two OS
- Nested symlinks are not yet supported on Windows

<br/>

# Issues and bugs report
PrimeNote has been developed for X11 and Windows 7-10. Wayland is not currently supported. If you encounter any bugs, please report them in the [issues](https://gitlab.com/william.belanger/primenote/-/issues) section, including the last session log. Logs can be located at `~/.config/primenote/logs` on Linux and `C:\Users\<user>\primenote\logs` on Windows.

<br/>

# Contribution
* C++ developers: Help is needed for an upstream contribution to [LXQt's QTermWidget project](https://github.com/lxqt/qtermwidget), in order to streamline PyQt-compatible deployment across Linux distributions.
* Python developers: We need unit tests for everything.
* Graphic artists: We would welcome assistance to create a logo, banner, and corresponding application icon.
* [Donations](https://www.paypal.com/donate?hosted_button_id=7UTK3HPH6Q5DG) are greatly appreciated and help cover hosting costs.

