# gm
A CLI for uploading and managing Garry’s Mod addons.

## Installing
Place `gm.py` in your `GarrysMod\bin` directory. It is recommended that you add `GarrysMod\bin` to the `PATH` environment variable.

There are two methods to execute this script without specifying the Python executable or `.py` extension. This allows you to run the commands using just `gm <command> [<args>]`.

##### Method 1:
Create a file named `gm.cmd` in your `GarrysMod\bin` directory with the contents:
```
@echo off
py "path\to\GarrysMod\bin\gm.py" %*
```

##### Method 2:
Create a `.py` file extension association with the Python executable and add `.PY` to the `PATHEXT` environment variable.

## Update
To update this script run the command `gm update`.
