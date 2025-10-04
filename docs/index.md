## agio Launcher Package

Used to prepare and run any applications in the context of a pipeline.

Command example

`agio -w [UUID] launch --app-name [APPNAME] --app-version [APPVERSION] --app-mode [APPMODE] -- --arg1 --arg2 ...`

This command creates a separate venv for each software version and adds it to `PYTHONPATH`,
which eliminates compatibility issues between the built-in interpreter and library versions.
