unset -nocomplain ::env(PYTHONHOME)
unset -nocomplain ::env(PYTHONPATH)
#! /usr/bin/tclsh
proc call_python {} {
    set env(TCL_LIBRARY) <tcl library location>
    set env(TK_LIBRARY) <tk library loaction>
    set python_script_path <the location path you download for new.py>
    set python_exe < location of the python.exe on your system>
    set project_path [get_property DIRECTORY [current_project]]
    set output [exec $python_exe $python_script_path $project_path]
    puts $output
}
call_python
