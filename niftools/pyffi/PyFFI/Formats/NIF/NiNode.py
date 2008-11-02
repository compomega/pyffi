"""Custom functions for NiNode.

Doctests
========

Old test code
-------------

>>> from PyFFI.Formats.NIF import NifFormat
>>> x = NifFormat.NiNode()
>>> y = NifFormat.NiNode()
>>> z = NifFormat.NiNode()
>>> x.numChildren =1
>>> x.children.updateSize()
>>> y in x.children
False
>>> x.children[0] = y
>>> y in x.children
True
>>> x.addChild(z, front = True)
>>> x.addChild(y)
>>> x.numChildren
2
>>> x.children[0] is z
True
>>> x.removeChild(y)
>>> y in x.children
False
>>> x.numChildren
1
>>> e = NifFormat.NiSpotLight()
>>> x.addEffect(e)
>>> x.numEffects
1
>>> e in x.effects
True

Children
--------

>>> from PyFFI.Formats.NIF import NifFormat
>>> node = NifFormat.NiNode()
>>> child1 = NifFormat.NiNode()
>>> child1.name = "hello"
>>> child2 = NifFormat.NiNode()
>>> child2.name = "world"
>>> node.getChildren()
[]
>>> node.setChildren([child1, child2])
>>> [child.name for child in node.getChildren()]
['hello', 'world']
>>> [child.name for child in node.children]
['hello', 'world']
>>> node.setChildren([])
>>> node.getChildren()
[]
>>> # now set them the other way around
>>> node.setChildren([child2, child1])
>>> [child.name for child in node.getChildren()]
['world', 'hello']
>>> [child.name for child in node.children]
['world', 'hello']
>>> node.removeChild(child2)
>>> [child.name for child in node.children]
['hello']
>>> node.addChild(child2)
>>> [child.name for child in node.children]
['hello', 'world']

Effects
-------

>>> from PyFFI.Formats.NIF import NifFormat
>>> node = NifFormat.NiNode()
>>> effect1 = NifFormat.NiSpotLight()
>>> effect1.name = "hello"
>>> effect2 = NifFormat.NiSpotLight()
>>> effect2.name = "world"
>>> node.getEffects()
[]
>>> node.setEffects([effect1, effect2])
>>> [effect.name for effect in node.getEffects()]
['hello', 'world']
>>> [effect.name for effect in node.effects]
['hello', 'world']
>>> node.setEffects([])
>>> node.getEffects()
[]
>>> # now set them the other way around
>>> node.setEffects([effect2, effect1])
>>> [effect.name for effect in node.getEffects()]
['world', 'hello']
>>> [effect.name for effect in node.effects]
['world', 'hello']
>>> node.removeEffect(effect2)
>>> [effect.name for effect in node.effects]
['hello']
>>> node.addEffect(effect2)
>>> [effect.name for effect in node.effects]
['hello', 'world']
"""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2008, NIF File Format Library and Tools.
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
# ***** END LICENSE BLOCK *****

def addChild(self, child, front=False):
    """Add block to child list.

    @param child: The child to add.
    @type child: L{NifFormat.NiAVObject}
    @kwarg front: Whether to add to the front or to the end of the
        list (default is at end).
    @type front: C{bool}
    """
    # check if it's already a child
    if child in self.children:
        return
    # increase number of children
    num_children = self.numChildren
    self.numChildren = num_children + 1
    self.children.updateSize()
    # add the child
    if not front:
        self.children[num_children] = child
    else:
        for i in xrange(num_children, 0, -1):
            self.children[i] = self.children[i-1]
        self.children[0] = child

def removeChild(self, child):
    """Remove a block from the child list.

    @param child: The child to remove.
    @type child: L{NifFormat.NiAVObject}
    """
    self.setChildren([otherchild for otherchild in self.getChildren()
                      if not(otherchild is child)])

def getChildren(self):
    """Return a list of the children of the block.

    @return: The list of children.
    @rtype: C{list} of L{NifFormat.NiAVObject}
    """
    return [child for child in self.children]

def setChildren(self, childlist):
    """Set the list of children from the given list (destroys existing list).

    @param childlist: The list of child blocks to set.
    @type childlist: C{list} of L{NifFormat.NiAVObject}
    """
    self.numChildren = len(childlist)
    self.children.updateSize()
    for i, child in enumerate(childlist):
        self.children[i] = child

def addEffect(self, effect):
    """Add an effect to the list of effects.

    @param effect: The effect to add.
    @type effect: L{NifFormat.NiDynamicEffect}
    """
    num_effs = self.numEffects
    self.numEffects = num_effs + 1
    self.effects.updateSize()
    self.effects[num_effs] = effect

def removeEffect(self, effect):
    """Remove a block from the effect list.

    @param effect: The effect to remove.
    @type effect: L{NifFormat.NiDynamicEffect}
    """
    self.setEffects([othereffect for othereffect in self.getEffects()
                     if not(othereffect is effect)])

def getEffects(self):
    """Return a list of the effects of the block.

    @return: The list of effects.
    @rtype: C{list} of L{NifFormat.NiDynamicEffect}
    """
    return [effect for effect in self.effects]

def setEffects(self, effectlist):
    """Set the list of effects from the given list (destroys existing list).

    @param effectlist: The list of effect blocks to set.
    @type effectlist: C{list} of L{NifFormat.NiDynamicEffect}
    """
    self.numEffects = len(effectlist)
    self.effects.updateSize()
    for i, effect in enumerate(effectlist):
        self.effects[i] = effect
