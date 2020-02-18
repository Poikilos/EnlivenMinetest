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

#ifndef f_VD2_VDXFRAME_VIDEOFILTERDIALOG_H
#define f_VD2_VDXFRAME_VIDEOFILTERDIALOG_H

#include <windows.h>

class VDXVideoFilterDialog
public:
    VDXVideoFilterDialog()

protected:
    HWND	mhdlg

    LRESULT Show(HINSTANCE hInst, templName, parent)
    LRESULT Show(HINSTANCE hInst, templName, parent)
    HWND ShowModeless(HINSTANCE hInst, templName, parent)
    HWND ShowModeless(HINSTANCE hInst, templName, parent)

    static INT_PTR CALLBACK StaticDlgProc(HWND hdlg, msg, wParam, lParam)
    virtual INT_PTR DlgProc(UINT msg, wParam, lParam)


#endif
