# Workspace Switcher plugin for Ulauncher

This is a plugin for [uLauncher](https://ulauncher.io/) that lets you search & switch between Linux/X11 Workspaces by name:

![](./screenshots/search.png)

The default keyword in `w`, so just run Ulauncher, then type `w <query>` to filter the workspace list, then select a workspace from the list to switch to that workspace.

## Shortcuts

If you type `<keyword> -`, it'll offer to take you back to your previous workspace - i.e. the one you were on before this one. It will save the current workspace into `$HOME/.lws` just before switching, so this will only work if you use this switcher - it won't know about workspace switches you make by other means. This is intended to work similarly to `cd -`, or `pushd/popd`.

If you type a number, e.g. `<keyword> 12` it'll offer to take you directly to workspace 12.

I used workspace icons from the [Obsidian Icon pack](https://github.com/madmaxms/iconpack-obsidian)

## Requirements

You need `wmctrl` installed. See: https://www.freedesktop.org/wiki/Software/wmctrl/

For Debian/Ubuntu, you can do:

```shell
$ sudo apt install wmctrl
```
