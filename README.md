# MyVCS
Simple version control system

Supported commands and usage:

init : initialize files and settings required to start versioning the working directory content

snapshot : snap the current content as a backup version, include message optional

latest: retrieve the newest snapped version

current : print current version number in the terminal

checkout <n> : revert to version num <n>

diff <x> <y>: print changes between versions <x> and <y> on terminal : modified common files, files /sub directories only in version <x>, files / sub directories only in version <y>. Color print lines according to status (red is modified, only left-side files are yellow, only right sides are blue)

status : same as previous, but shows diff between current working version and active backup

log: print log status – messages with time stamps, taking branching into consideration ( for example when you snap versions from 1 to 11 and then revert to version number 8 because you made some design mistake, next three snaps you take will be numbered 12-15 but when you run the log command, you want to see what was going on for versions 1-8 and 12-15)
