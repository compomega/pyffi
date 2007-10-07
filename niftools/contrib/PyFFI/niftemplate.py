#!/usr/bin/python

"""A template for writing PyFFI nif scripts."""

# --------------------------------------------------------------------------
# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007, NIF File Format Library and Tools.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENCE BLOCK *****
# --------------------------------------------------------------------------

import NifTester

############################################################################
# custom functions
############################################################################

############################################################################
# testers
############################################################################

# set this variable to True for scripts that need to overwrite of original files
OVERWRITE_FILES = False

def testBlock(block, verbose):
    """Every block will be tested with this function."""
    # modify to your needs
    if isinstance(block, NifFormat.NiObjectNET):
        if verbose >= 2: print "parsing block [%s] %s"%(block.__class__.__name__, block.name)
    else:
        if verbose >= 2: print "parsing block [%s]"%(block.__class__.__name__)

def testRoot(root_block, verbose):
    """Every root block will be tested with this function."""
    # modify to your needs
    pass

def testFile(version, user_version, f, roots, verbose, arg = None):
    """Every file will be tested with this function."""
    # you probably just want to leave this function as it is
    if OVERWRITE_FILES:
        if verbose >= 1: print "rewriting file...",
        f.seek(0)
        NifFormat.write(version, user_version, f, roots)
        f.truncate()
        if verbose >= 1: print "done"

############################################################################
# main program
############################################################################

import sys, os
from optparse import OptionParser

from PyFFI.NIF import NifFormat

def main():
    # parse options and positional arguments
    usage = "%prog [options] <file>|<folder>"
    description="""A template nif script for parsing nif file <file> or all nif files in folder
<folder>. You can use this template to write your own scripts."""
    if OVERWRITE_FILES:
        description += """
WARNING:
This script will modify the nif files, in particular if something goes wrong it
may destroy them. Make a backup before running this script."""
    parser = OptionParser(usage, version="%prog $Rev$", description=description)
    parser.add_option("-v", "--verbose", dest="verbose",
                      type="int",
                      metavar="VERBOSE",
                      default=1,
                      help="verbosity level: 0, 1, or 2 [default: %default]")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments (one required)")

    # get top folder/file
    top = args[0]

    # warning
    if OVERWRITE_FILES:
        print """This script will modify the nif files, in particular if something goes wrong it
may destroy them. Make a backup of your nif files before running this script.
"""
        if raw_input("Are you sure that you want to proceed? [n/Y] ") != "Y": return

    # run tester
    mode = "rb" if not OVERWRITE_FILES else "r+b"
    NifTester.testPath(top, testBlock, testRoot, testFile, NifTester.raise_exception, mode = mode, verbose=options.verbose)

# if script is called...
if __name__ == "__main__":
    main()
