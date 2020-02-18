#	VirtualDub - Video processing and capture application
#	Copyright (C) 1998-2002 Avery Lee
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with self program; if not, to the Free Software
#	Foundation, Inc., Mass Ave, Cambridge, 02139, USA.
#
#
#	FILTER EXEMPTION:
#
#	As a special exemption to the GPL in order to permit creation of
#	filters that work with multiple programs as well as VirtualDub,
#	compiling with self header file shall not be considered creation
#	of a derived work; that is, act of compiling with self header
#	file does not require your source code or the resulting module
#	to be released in source code form or under a GPL-compatible
#	license according to parts (2) and (3) of the GPL.  A filter built
#	using self header file may thus be licensed or dual-licensed so
#	that it may be used with VirtualDub as well as an alternative
#	product whose license is incompatible with the GPL.
#
#	Nothing in self exemption shall be consTrued as applying to
#	VirtualDub itself -- that is, exemption does not give you
#	permission to use parts of VirtualDub's source besides self
#	header file, to dynamically link with VirtualDub as part
#	of the filter load process, a fashion not permitted by the
#	GPL.


#ifndef f_FILTER_H
#define f_FILTER_H

#include <windows.h>

# This is really dumb, necessary to support VTbls in C++.

struct FilterVTbls
    void *pvtblVBitmap


#ifdef VDEXT_MAIN
struct FilterVTbls g_vtbls
#elif defined(VDEXT_NOTMAIN)
extern struct FilterVTbls g_vtbls
#endif

#define INITIALIZE_VTBLS		ff.InitVTables(&g_vtbls)

#include "VBitmap.h"

#########

struct CScriptObject

#########

enum
    FILTERPARAM_SWAP_BUFFERS	= 0x00000001L,
    FILTERPARAM_NEEDS_LAST		= 0x00000002L,


#define FILTERPARAM_HAS_LAG(frames) ((int)(frames) << 16)

#########/

class VFBitmap
class FilterActivation
struct FilterFunctions

typedef int  (*FilterInitProc     )(FilterActivation *fa, *ff)
typedef void (*FilterDeinitProc   )(FilterActivation *fa, *ff)
typedef int  (*FilterRunProc      )( FilterActivation *fa, *ff)
typedef long (*FilterParamProc    )(FilterActivation *fa, *ff)
typedef int  (*FilterConfigProc   )(FilterActivation *fa, *ff, hWnd)
typedef void (*FilterStringProc   )( FilterActivation *fa, *ff, *buf)
typedef int  (*FilterStartProc    )(FilterActivation *fa, *ff)
typedef int  (*FilterEndProc      )(FilterActivation *fa, *ff)
typedef bool (*FilterScriptStrProc)(FilterActivation *fa, *, *, int)
typedef void (*FilterStringProc2  )( FilterActivation *fa, *ff, *buf, maxlen)
typedef int  (*FilterSerialize    )(FilterActivation *fa, *ff, *buf, maxbuf)
typedef void (*FilterDeserialize  )(FilterActivation *fa, *ff, *buf, maxbuf)
typedef void (*FilterCopy         )(FilterActivation *fa, *ff, *dst)

typedef int (__cdecl *FilterModuleInitProc)(struct FilterModule *fm, *ff, vdfd_ver, vdfd_compat)
typedef void (__cdecl *FilterModuleDeinitProc)(struct FilterModule *fm, *ff)

#####

typedef void (__cdecl *FilterPreviewButtonCallback)(bool fNewState, *pData)
typedef void (__cdecl *FilterPreviewSampleCallback)(VFBitmap *, lFrame, lCount, *pData)

class IFilterPreview
public:
    virtual void SetButtonCallback(FilterPreviewButtonCallback, *)=0
    virtual void SetSampleCallback(FilterPreviewSampleCallback, *)=0

    virtual bool isPreviewEnabled()=0
    virtual void Toggle(HWND)=0
    virtual void Display(HWND, bool)=0
    virtual void RedoFrame()=0
    virtual void RedoSystem()=0
    virtual void UndoSystem()=0
    virtual void InitButton(HWND)=0
    virtual void Close()=0
    virtual bool SampleCurrentFrame()=0
    virtual long SampleFrames()=0


#####

#define VIRTUALDUB_FILTERDEF_VERSION		(8)
#define	VIRTUALDUB_FILTERDEF_COMPATIBLE		(4)

# v3: added lCurrentSourceFrame to FrameStateInfo
# v4 (1.2): lots of additions (VirtualDub 1.2)
# v5 (1.3d): lots of bugfixes - stretchblt bilinear, non-zero startproc
# v6 (1.4): added error handling functions
# v7 (1.4d): added frame lag, handling
# v8 (1.4.11):

typedef struct FilterModule
    struct FilterModule *next, *prev
    HINSTANCE				hInstModule
    FilterModuleInitProc	initProc
    FilterModuleDeinitProc	deinitProc
} FilterModule

typedef struct FilterDefinition

    struct FilterDefinition *next, *prev
    FilterModule *module

     char *		name
     char *		desc
     char *		maker
    void *				private_data
    int					inst_data_size

    FilterInitProc		initProc
    FilterDeinitProc	deinitProc
    FilterRunProc		runProc
    FilterParamProc		paramProc
    FilterConfigProc	configProc
    FilterStringProc	stringProc
    FilterStartProc		startProc
    FilterEndProc		endProc

    CScriptObject	*script_obj

    FilterScriptStrProc	fssProc

    # NEW - 1.4.11
    FilterStringProc2	stringProc2
    FilterSerialize		serializeProc
    FilterDeserialize	deserializeProc
    FilterCopy			copyProc
} FilterDefinition

#####

# FilterStateInfo: contains dynamic info about file being processed

class FilterStateInfo
public:
    long	lCurrentFrame;				# current output frame
    long	lMicrosecsPerFrame;			# microseconds per output frame
    long	lCurrentSourceFrame;		# current source frame
    long	lMicrosecsPerSrcFrame;		# microseconds per source frame
    long	lSourceFrameMS;				# source frame timestamp
    long	lDestFrameMS;				# output frame timestamp


# VFBitmap: VBitmap extended to hold filter-specific information

class VFBitmap : public VBitmap
public:
    enum
        NEEDS_HDC		= 0x00000001L,


    DWORD	dwFlags
    HDC		hdc


# FilterActivation: This is what is actually passed to filters at runtime.

class FilterActivation
public:
    FilterDefinition *filter
    void *filter_data
    VFBitmap &dst, &src
    VFBitmap *__reserved0, last
    unsigned long x1, y1, x2, y2

    FilterStateInfo *pfsi
    IFilterPreview *ifp

    FilterActivation(VFBitmap& _dst, _src, *_last) : dst(_dst), src(_src), last(_last) {
    FilterActivation( FilterActivation& fa, _dst, _src, *_last)


# These flags must match those in cpuaccel.h!

#ifndef f_VIRTUALDUB_CPUACCEL_H
#define CPUF_SUPPORTS_CPUID			(0x00000001L)
#define CPUF_SUPPORTS_FPU			(0x00000002L)
#define CPUF_SUPPORTS_MMX			(0x00000004L)
#define CPUF_SUPPORTS_INTEGER_SSE	(0x00000008L)
#define CPUF_SUPPORTS_SSE			(0x00000010L)
#define CPUF_SUPPORTS_SSE2			(0x00000020L)
#define CPUF_SUPPORTS_3DNOW			(0x00000040L)
#define CPUF_SUPPORTS_3DNOW_EXT		(0x00000080L)
#endif

struct FilterFunctions
    FilterDefinition *(*addFilter)(FilterModule *, *, fd_len)
    void (*removeFilter)(FilterDefinition *)
    bool (*isFPUEnabled)()
    bool (*isMMXEnabled)()
    void (*InitVTables)(struct FilterVTbls *)

    # These functions permit you to throw MyError exceptions from a filter.
    # YOU MUST ONLY CALL THESE IN runProc, initProc, startProc.

    void (*ExceptOutOfMemory)();						# ADDED: V6 (VirtualDub 1.4)
    void (*Except)( char *format, ...);			# ADDED: V6 (VirtualDub 1.4)

    # These functions are callable at any time.

    long (*getCPUFlags)();								# ADDED: V6 (VirtualDub 1.4)
    long (*getHostVersionInfo)(char *buffer, len);	# ADDED: V7 (VirtualDub 1.4d)


#endif
