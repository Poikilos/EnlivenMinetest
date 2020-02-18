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
#include <vd2/VDXFrame/VideoFilter.h>

#####################################/

VDXVideoFilter.VDXVideoFilter()


VDXVideoFilter.~VDXVideoFilter()


def SetHooks(self, *fa, *ff):
    self.fa = fa
    self.ff = ff


#####################################/

def Init(self):
    return True


def Start(self):


def End(self):


def Configure(self, hwnd):
    return hwnd != NULL


def GetSettingString(self, *buf, maxlen):


def GetScriptString(self, *buf, maxlen):


def Serialize(self, *buf, maxbuf):
    return 0


def Deserialize(self, *buf, maxbuf):
    return 0


def Prefetch(self, frame):
    return frame


def Prefetch2(self, frame, *prefetcher):
    prefetcher.PrefetchFrame(0, Prefetch(frame), 0)
    return True


def OnEvent(self, event, *eventData):
    switch(event)
    case kVDXVFEvent_InvalidateCaches:
        return OnInvalidateCaches()

    default:
        return False



def OnInvalidateCaches(self):
    return False


#####################################/

void __cdecl VDXVideoFilter.FilterDeinit   (VDXFilterActivation *fa, *ff)
    (*reinterpret_cast<VDXVideoFilter **>(fa.filter_data)).~VDXVideoFilter()


int  __cdecl VDXVideoFilter.FilterRun      ( VDXFilterActivation *fa, *ff)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    pThis.Run()
    return 0


long __cdecl VDXVideoFilter.FilterParam    (VDXFilterActivation *fa, *ff)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    return pThis.GetParams()


int  __cdecl VDXVideoFilter.FilterConfig   (VDXFilterActivation *fa, *ff, hwnd)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    return not pThis.Configure(hwnd)


int  __cdecl VDXVideoFilter.FilterStart    (VDXFilterActivation *fa, *ff)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    pThis.Start()
    return 0


int  __cdecl VDXVideoFilter.FilterEnd      (VDXFilterActivation *fa, *ff)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    pThis.End()
    return 0


void __cdecl VDXVideoFilter.FilterString   ( VDXFilterActivation *fa, *ff, *buf)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    pThis.GetScriptString(buf, 80)


bool __cdecl VDXVideoFilter.FilterScriptStr(VDXFilterActivation *fa, *ff, *buf, buflen)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    pThis.GetScriptString(buf, buflen)

    return True


void __cdecl VDXVideoFilter.FilterString2  ( VDXFilterActivation *fa, *ff, *buf, maxlen)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    pThis.GetSettingString(buf, maxlen)


int  __cdecl VDXVideoFilter.FilterSerialize    (VDXFilterActivation *fa, *ff, *buf, maxbuf)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    return pThis.Serialize(buf, maxbuf)


void __cdecl VDXVideoFilter.FilterDeserialize  (VDXFilterActivation *fa, *ff, *buf, maxbuf)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= fa

    pThis.Deserialize(buf, maxbuf)


sint64 __cdecl VDXVideoFilter.FilterPrefetch( VDXFilterActivation *fa, *ff, frame)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    return pThis.Prefetch(frame)


bool __cdecl VDXVideoFilter.FilterPrefetch2( VDXFilterActivation *fa, *ff, frame, *prefetcher)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    return pThis.Prefetch2(frame, prefetcher)


bool __cdecl VDXVideoFilter.FilterEvent( VDXFilterActivation *fa, *ff, event, *eventData)
    VDXVideoFilter *pThis = *reinterpret_cast<VDXVideoFilter **>(fa.filter_data)

    pThis.fa		= const_cast<VDXFilterActivation *>(fa)

    return pThis.OnEvent(event, eventData)


def SafePrintf(self, *buf, maxbuf, *format, ...):
    if maxbuf <= 0:
        return

    va_list val
    va_start(val, format)
    if (unsigned)_vsnprintf(buf, maxbuf, format, val) >= (unsigned)maxbuf:
        buf[maxbuf - 1] = 0
    va_end(val)


 VDXScriptFunctionDef VDXVideoFilter.sScriptMethods[1]= {0
