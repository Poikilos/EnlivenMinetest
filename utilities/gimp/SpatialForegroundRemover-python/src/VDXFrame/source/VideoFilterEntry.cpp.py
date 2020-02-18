#	VDXFrame - Helper library for VirtualDub plugins
#	Copyright (C) 2008 Avery Lee
#
#	The plugin headers in the VirtualDub plugin SDK are licensed differently
#	differently than VirtualDub and the Plugin SDK themselves.  This
#	particular file is thus licensed as follows (the "zlib" license):
#
#	This software is provided 'as-is', any express or implied
#	warranty.  In no event will the authors be held liable for any
#	damages arising from the use of self software.
#
#	Permission is granted to anyone to use self software for any purpose,
#	including commercial applications, to alter it and redistribute it
#	freely, to the following restrictions:
#
#	1.	The origin of self software must not be misrepresented; you must
#		not claim that you wrote the original software. If you use self
#		software in a product, acknowledgment in the product
#		documentation would be appreciated but is not required.
#	2.	Altered source versions must be plainly marked as such, must
#		not be misrepresented as being the original software.
#	3.	This notice may not be removed or altered from any source
#		distribution.

#include "stdafx.h"
#include <vd2/VDXFrame/VideoFilterEntry.h>

int g_VFVAPIVersion
VDXFilterDefinition **g_VDXRegisteredFilters
int g_VDXRegisteredFilterCount

VDXFilterDefinition *VDXGetVideoFilterDefinition(int index)

def VDXVideoFilterModuleInit2(self, VDXFilterModule *fm, *ff, vdfd_ver, vdfd_compat, ver_compat_target):
    def_count = 0

    while(VDXGetVideoFilterDefinition(def_count))
        ++def_count

    g_VDXRegisteredFilters = (VDXFilterDefinition **)malloc(sizeof(VDXFilterDefinition *) * def_count)
    if not g_VDXRegisteredFilters:
        return 1

    memset(g_VDXRegisteredFilters, 0, sizeof(VDXFilterDefinition *) * def_count)

    for(int i=0; i<def_count; ++i)
        g_VDXRegisteredFilters[i] = ff.addFilter(fm, VDXGetVideoFilterDefinition(i), sizeof(VDXFilterDefinition))

    g_VFVAPIVersion = vdfd_ver
    vdfd_ver        = VIRTUALDUB_FILTERDEF_VERSION
    vdfd_compat     = ver_compat_target

    return 0


def VDXVideoFilterModuleDeinit(self, VDXFilterModule *fm, *ff):
    if g_VDXRegisteredFilters:
        for(int i=g_VDXRegisteredFilterCount-1; i>=0; --i)
            VDXFilterDefinition *def = g_VDXRegisteredFilters[i]

            if def:
                ff.removeFilter(def)


        free(g_VDXRegisteredFilters)
        g_VDXRegisteredFilters = NULL



def VDXGetVideoFilterAPIVersion(self):
    return g_VFVAPIVersion

