# Simple Mod List Version Control Server Example

Here you can see an example of a finished server that updates the version of OptiFine for Minecraft. You can also find out the description of JSON files.

`All rights to OptiFine belong to its developer.`

## version.json

    The main file used by client to identify an available update

`"version": x`

    Where `x` is version number. The client searches for `x.json`

## 1.json

    File that used by clients as an installation instructions

`"destinationFolder": path`

    `path` where mods stored on server and client

`"removeList": [ "preview_OptiFine_1.20_HD_U_I5_pre5.jar" ]`

    List of the files that will be removed after update

`"addList": [ "OptiFine_1.20.1_HD_U_I5.jar" ]`

    List of the files that will be downloaded from server
