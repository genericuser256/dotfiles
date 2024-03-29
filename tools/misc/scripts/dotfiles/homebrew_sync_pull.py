#!/usr/bin/env python3

import os
import platform
import subprocess as subp

# Variables
HOME_DIR = os.path.expanduser("~")
DOT_DIR = "{}/dotfiles".format(HOME_DIR)
SCRIPT_DIR = "{}/scripts".format(HOME_DIR)
DOT_SCRIPTS = "{}/dotfiles".format(SCRIPT_DIR)

TAP_FN = "brew_tapped.txt"
LEAVES_FN = "brew_leaves.txt"
CASKS_FN = "brew_casks.txt"

# We need to tap, install formulas, and install casks
# First update homebrew so output not corrupted
cmd = "brew update"
with open(os.devnull, 'w') as devnull:
    stdin = stdout = stderr = devnull
    proc = subp.Popen(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr, cwd=DOT_SCRIPTS)
    proc.wait()



# Figure out what to tap
if [[ -f ${TAP_F} ]]; then
   # The brew_tapped file exists, so find the taps not in it
   untapped=`comm -23 <(brew tap) ${TAP_F}`
   # Convert newlines to spaces
   untapped=`echo ${untapped} | tr '\n' ' '`
   # Tap the untapped
   brew tap ${untapped}
fi

# Figure out the formulas to install
if [[ -f ${LEAVES_F} ]]; then
   # The brew_leaves file exists, so find the formulas not in it
   uninstalled=`comm -23 <(brew leaves) ${LEAVES_F}`
   # Convert newlines to spaces
   uninstalled=`echo ${uninstalled} | tr '\n' ' '`
   # Install the uninstalled
   brew install ${uninstalled}
fi

# Figure out the casks to install
if [[ -f ${CASKS_F} ]]; then
   # The brew_casks file exists, so find the casks not in it
   uninstalled=`comm -23 <(sed -e 's/\s\+/\n/g' <(brew cask list)) ${CASKS_F}`
   # Convert newlines to spaces
   uninstalled=`echo ${uninstalled} | tr '\n' ' '`
   # Install the uninstalled
   brew install ${uninstalled}
fi
