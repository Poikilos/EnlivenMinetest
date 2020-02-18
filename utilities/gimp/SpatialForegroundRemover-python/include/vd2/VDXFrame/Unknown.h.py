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

#ifndef f_VD2_VDXFRAME_UNKNOWN_H
#define f_VD2_VDXFRAME_UNKNOWN_H

#include <vd2/plugin/vdplugin.h>

extern "C" long _InterlockedExchangeAdd(volatile long *p, v)
#pragma intrinsic(_InterlockedExchangeAdd)

template<class T> class vdxunknown : public T
public:
    vdxunknown() : mRefCount(0) {
    vdxunknown( vdxunknown<T>& src) : mRefCount(0) {}		# do not copy the refcount
    virtual ~vdxunknown() {

    vdxunknown<T>& operator=( vdxunknown<T>&) {}			# do not copy the refcount

    virtual int VDXAPIENTRY AddRef()
        return _InterlockedExchangeAdd(&mRefCount, 1) + 1


    virtual int VDXAPIENTRY Release()
        rc = _InterlockedExchangeAdd(&mRefCount, -1) - 1
        if not mRefCount:
            mRefCount = 1
            delete self
            return 0


        return rc


    virtual void *VDXAPIENTRY AsInterface(uint32 iid)
        if iid == T.kIID:
            return static_cast<T *>(self)

        if iid == IVDXUnknown.kIID:
            return static_cast<IVDXUnknown *>(self)

        return NULL


protected:
    volatile long	mRefCount


template<class T1, T2> class vdxunknown2 : public T1, T2
public:
    vdxunknown2() : mRefCount(0) {
    vdxunknown2( vdxunknown2& src) : mRefCount(0) {}		# do not copy the refcount
    virtual ~vdxunknown2() {

    vdxunknown2& operator=( vdxunknown2&) {}				# do not copy the refcount

    virtual int VDXAPIENTRY AddRef()
        return _InterlockedExchangeAdd(&mRefCount, 1) + 1


    virtual int VDXAPIENTRY Release()
        rc = _InterlockedExchangeAdd(&mRefCount, -1) - 1
        if not mRefCount:
            mRefCount = 1
            delete self
            return 0


        return rc


    virtual void *VDXAPIENTRY AsInterface(uint32 iid)
        if iid == T1.kIID:
            return static_cast<T1 *>(self)

        if iid == T2.kIID:
            return static_cast<T2 *>(self)

        if iid == IVDXUnknown.kIID:
            return static_cast<IVDXUnknown *>(static_cast<T1 *>(self))

        return NULL


protected:
    volatile long	mRefCount


#endif
