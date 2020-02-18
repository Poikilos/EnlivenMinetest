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

#ifndef f_VD2_VDXFRAME_VIDEOFILTER_H
#define f_VD2_VDXFRAME_VIDEOFILTER_H

#include <stdlib.h>
#include <stddef.h>
#include <new>

#include <vd2/plugin/vdvideofilt.h>

#####################################/
#/	\class VDXVideoFilter
#/
#/	This class handles most of the grimy work of creating the interface
#/	between your filter and VirtualDub.
#/
class VDXVideoFilter
public:
    VDXVideoFilter()
    virtual ~VDXVideoFilter()

    void SetHooks(VDXFilterActivation *fa, *ff)

    # linkage routines

    virtual bool Init()
    virtual uint32 GetParams()=0
    virtual void Start()
    virtual void Run() = 0
    virtual void End()
    virtual bool Configure(VDXHWND hwnd)
    virtual void GetSettingString(char *buf, maxlen)
    virtual void GetScriptString(char *buf, maxlen)
    virtual int Serialize(char *buf, maxbuf)
    virtual int Deserialize( char *buf, maxbuf)
    virtual sint64 Prefetch(sint64 frame)
    virtual bool Prefetch2(sint64 frame, *prefetcher)

    virtual bool OnEvent(uint32 event, *eventData)
    virtual bool OnInvalidateCaches()

    static void __cdecl FilterDeinit   (VDXFilterActivation *fa, *ff)
    static int  __cdecl FilterRun      ( VDXFilterActivation *fa, *ff)
    static long __cdecl FilterParam    (VDXFilterActivation *fa, *ff)
    static int  __cdecl FilterConfig   (VDXFilterActivation *fa, *ff, hWnd)
    static int  __cdecl FilterStart    (VDXFilterActivation *fa, *ff)
    static int  __cdecl FilterEnd      (VDXFilterActivation *fa, *ff)
    static void __cdecl FilterString   ( VDXFilterActivation *fa, *ff, *buf)
    static bool __cdecl FilterScriptStr(VDXFilterActivation *fa, *, *, int)
    static void __cdecl FilterString2  ( VDXFilterActivation *fa, *ff, *buf, maxlen)
    static int  __cdecl FilterSerialize    (VDXFilterActivation *fa, *ff, *buf, maxbuf)
    static void __cdecl FilterDeserialize  (VDXFilterActivation *fa, *ff, *buf, maxbuf)
    static sint64 __cdecl FilterPrefetch( VDXFilterActivation *fa, *ff, frame)
    static bool __cdecl FilterPrefetch2( VDXFilterActivation *fa, *ff, frame, *prefetcher)
    static bool __cdecl FilterEvent( VDXFilterActivation *fa, *ff, event, *eventData)

    # member variables
    VDXFilterActivation *fa
     VDXFilterFunctions *ff

    static  VDXScriptFunctionDef sScriptMethods[]

protected:
    void SafePrintf(char *buf, maxbuf, *format, ...)


#####################################/
# Script method support
#
# To declare a Config() script method, add
#
#	VDXVF_DECLARE_SCRIPT_METHODS()
#
# to the public portion of your class definition, then add a method
# table at namespace scope:
#
#	VDXVF_BEGIN_SCRIPT_METHODS(SpatialForegroundRemoverFilter)
#	VDXVF_DEFINE_SCRIPT_METHOD(SpatialForegroundRemoverFilter, ScriptConfig, "iii")
#	VDXVF_END_SCRIPT_METHODS()
#
# Use VDXVF_DEFINE_SCRIPT_METHOD() for the first method, then
# VDXVF_DEFINE_SCRIPT_METHOD2() for any overloads.

#define VDXVF_DECLARE_SCRIPT_METHODS()	static  VDXScriptFunctionDef sScriptMethods[]

#define VDXVF_BEGIN_SCRIPT_METHODS(klass)  VDXScriptFunctionDef klass.sScriptMethods[] =#define VDXVF_DEFINE_SCRIPT_METHOD(klass, method, args) { (VDXScriptFunctionPtr)VDXVideoFilterScriptAdapter<klass, &klass.method>.AdaptFn, "Config", "0" args },
#define VDXVF_DEFINE_SCRIPT_METHOD2(klass, method, args) { (VDXScriptFunctionPtr)VDXVideoFilterScriptAdapter<klass, &klass.method>.AdaptFn, NULL, "0" args },
#define VDXVF_END_SCRIPT_METHODS() { NULL }

extern char VDXVideoFilterConfigureOverloadTest(bool (VDXVideoFilter.*)(VDXHWND))
extern double VDXVideoFilterConfigureOverloadTest(...)
extern char VDXVideoFilterPrefetchOverloadTest(sint64 (VDXVideoFilter.*)(sint64))
extern double VDXVideoFilterPrefetchOverloadTest(...)
extern char VDXVideoFilterPrefetch2OverloadTest(bool (VDXVideoFilter.*)(sint64, *))
extern double VDXVideoFilterPrefetch2OverloadTest(...)

template<class T, void (T.*T_Method)(IVDXScriptInterpreter *, *, int)>
class VDXVideoFilterScriptAdapter
public:
    static void AdaptFn(IVDXScriptInterpreter *isi, *fa0, *argv, argc)
        VDXFilterActivation *fa = (VDXFilterActivation *)fa0
        VDXVideoFilter *base = *(VDXVideoFilter **)fa.filter_data
        (static_cast<T *>(base).*T_Method)(isi, argv, argc)



template<class T>
class VDXVideoFilterScriptObjectAdapter
public:
    static  VDXScriptObject sScriptObject


template<class T>
 VDXScriptObject VDXVideoFilterScriptObjectAdapter<T>.sScriptObject =
    NULL, (T.sScriptMethods == VDXVideoFilter.sScriptMethods) ? NULL : (VDXScriptFunctionDef *)static_cast< VDXScriptFunctionDef *>(T.sScriptMethods), NULL


#####################################/
#/	\class VDXVideoFilterDefinition
#/
#/	This template creates the FilterDefinition structure for you based on
#/	your filter class.
#/
template<class T>
class VDXVideoFilterDefinition : public VDXFilterDefinition
public:
    VDXVideoFilterDefinition( char *pszAuthor, *pszName, *pszDescription)
        _next			= NULL
        _prev			= NULL
        _module			= NULL

        name			= pszName
        desc			= pszDescription
        maker			= pszAuthor
        private_data	= NULL
        inst_data_size	= sizeof(T) + sizeof(VDXVideoFilter *)

        initProc		= FilterInit
        deinitProc		= T.FilterDeinit
        runProc			= T.FilterRun
        paramProc		= T.FilterParam
        configProc		= sizeof(VDXVideoFilterConfigureOverloadTest(&T.Configure)) > 1 ? T.FilterConfig : NULL
        stringProc		= T.FilterString
        startProc		= T.FilterStart
        endProc			= T.FilterEnd

        script_obj		= T.sScriptMethods ? const_cast<VDXScriptObject *>(&VDXVideoFilterScriptObjectAdapter<T>.sScriptObject) : 0
        fssProc			= T.FilterScriptStr

        stringProc2		= T.FilterString2
        serializeProc	= T.FilterSerialize
        deserializeProc	= T.FilterDeserialize
        copyProc		= FilterCopy
        copyProc2		= FilterCopy2

        prefetchProc	= sizeof(VDXVideoFilterPrefetchOverloadTest(&T.Prefetch)) > 1 ? T.FilterPrefetch : NULL
        prefetchProc2	= sizeof(VDXVideoFilterPrefetch2OverloadTest(&T.Prefetch2)) > 1 or sizeof(VDXVideoFilterPrefetchOverloadTest(&T.Prefetch)) > 1 ? T.FilterPrefetch2 : NULL

        eventProc		= T.FilterEvent


private:
    static int  __cdecl FilterInit     (VDXFilterActivation *fa, *ff)
        T *pThis = new((char *)fa.filter_data + sizeof(VDXVideoFilter *)) T
        *(VDXVideoFilter **)fa.filter_data = static_cast<VDXVideoFilter *>(pThis)

        pThis.SetHooks(fa, ff)

        try
            if not pThis.Init():
                pThis.~T()
                return 1


            return 0

        catch(...)
            pThis.~T()
            throw



    static void __cdecl FilterCopy         (VDXFilterActivation *fa, *ff, *dst)
        T *p = new((char *)dst + sizeof(VDXVideoFilter *)) T(*static_cast<T *>(*reinterpret_cast<VDXVideoFilter **>(fa.filter_data)))
        p.ff = ff
        *(VDXVideoFilter **)dst = p


    static void __cdecl FilterCopy2        (VDXFilterActivation *fa, *ff, *dst, *fanew, *ffnew)
        T *p = new((char *)dst + sizeof(VDXVideoFilter *)) T(*static_cast<T *>(*reinterpret_cast<VDXVideoFilter **>(fa.filter_data)))
        p.ff = ffnew
        p.fa = fanew
        *(VDXVideoFilter **)dst = p



#endif
