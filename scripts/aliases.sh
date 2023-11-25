#!/bin/bash

################################################################################
# Title: Common shell functions that can be used by other scripts
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

echo "alias starta=\"$SCINTILLA_ROOT/container/start.sh arm\"" >> ~/.bashrc
echo "alias start=\"$SCINTILLA_ROOT/container/start.sh x86\"" >> ~/.bashrc
echo "alias stopa=\"$SCINTILLA_ROOT/container/stop.sh arm\"" >> ~/.bashrc
echo "alias stop=\"$SCINTILLA_ROOT/container/stop.sh x86\"" >> ~/.bashrc
echo "alias intoa=\"$SCINTILLA_ROOT/container/into.sh arm\"" >> ~/.bashrc
echo "alias into=\"$SCINTILLA_ROOT/container/into.sh x86\"" >> ~/.bashrc
echo "alias builda=\"$SCINTILLA_ROOT/container/build.sh arm\"" >> ~/.bashrc
echo "alias build=\"$SCINTILLA_ROOT/container/build.sh x86\"" >> ~/.bashrc
