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
#include <windows.h>
#include <vd2/VDXFrame/VideoFilterDialog.h>

namespace
#if defined(_MSC_VER) and _MSC_VER >= 1300
extern "C" char __ImageBase

def GetLocalHInstance(self):
    return (HINSTANCE)&__ImageBase

#else:
def GetLocalHInstance(self):
    meminfo = {0
    if not VirtualQuery(GetLocalHInstance, &meminfo, sizeof(meminfo)):
        return NULL

    return (HINSTANCE)meminfo.AllocationBase

#endif


VDXVideoFilterDialog.VDXVideoFilterDialog()
    : mhdlg(NULL)


def Show(self, hInst, templName, parent):
    if not hInst:
        hInst = GetLocalHInstance()

    return DialogBoxParamA(hInst, templName, parent, StaticDlgProc, (LPARAM)self)


def Show(self, hInst, templName, parent):
    if not hInst:
        hInst = GetLocalHInstance()

    return DialogBoxParamW(hInst, templName, parent, StaticDlgProc, (LPARAM)self)


def ShowModeless(self, hInst, templName, parent):
    if not hInst:
        hInst = GetLocalHInstance()

    return CreateDialogParamA(hInst, templName, parent, StaticDlgProc, (LPARAM)self)


def ShowModeless(self, hInst, templName, parent):
    if not hInst:
        hInst = GetLocalHInstance()

    return CreateDialogParamW(hInst, templName, parent, StaticDlgProc, (LPARAM)self)


INT_PTR CALLBACK VDXVideoFilterDialog.StaticDlgProc(HWND hdlg, msg, wParam, lParam)
    VDXVideoFilterDialog *pThis

    if msg == WM_INITDIALOG:
        pThis = (VDXVideoFilterDialog *)lParam
        SetWindowLongPtr(hdlg, DWLP_USER, (LONG_PTR)pThis)
        pThis.mhdlg = hdlg

    else:
        pThis = (VDXVideoFilterDialog *)GetWindowLongPtr(hdlg, DWLP_USER)

    return pThis ? pThis.DlgProc(msg, wParam, lParam) : FALSE


def DlgProc(self, msg, wParam, lParam):
    return FALSE

