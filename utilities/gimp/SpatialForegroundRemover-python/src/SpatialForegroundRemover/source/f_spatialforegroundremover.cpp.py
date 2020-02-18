##define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <commctrl.h>
#include <stdio.h>
#include <vd2/VDXFrame/VideoFilter.h>
#include <vd2/VDXFrame/VideoFilterDialog.h>
#include "../resource.h"
#include "f_spatialforegroundremover.h"
#include <ctime>
#include "pimage.h"
#include "pmath.h"

extern int g_VFVAPIVersion

using namespace ProtoArmor

#######################################/

PMathStatic* pmathstatic=NULL

def DlgProc(self, msg, wParam, lParam):
    switch(msg)
    case WM_INITDIALOG:
        return not OnInit()

    case WM_DESTROY:
        OnDestroy()
        break

    case WM_COMMAND:
        if OnCommand(LOWORD(wParam)):
            return TRUE
        break

    case WM_HSCROLL:
        if mifp and SaveToConfig():
            mifp.RedoFrame()
        return TRUE


    return FALSE


def OnInit(self):
    mOldConfig = mConfig

    SendDlgItemMessage(mhdlg, IDC_REACH, TBM_SETRANGE, TRUE, MAKELONG(0, 2000))
    SendDlgItemMessage(mhdlg, IDC_RADIALSAMPLES, TBM_SETRANGE, TRUE, MAKELONG(0, 2000))
    SendDlgItemMessage(mhdlg, IDC_DIFFUSION, TBM_SETRANGE, TRUE, MAKELONG(0, 2000))

    LoadFromConfig()

    hwndFirst = GetDlgItem(mhdlg, IDC_REACH)
    if hwndFirst:
        SendMessage(mhdlg, WM_NEXTDLGCTL, (WPARAM)hwndFirst, TRUE)

    hwndPreview = GetDlgItem(mhdlg, IDC_PREVIEW)
    if hwndPreview and mifp:
        EnableWindow(hwndPreview, TRUE)
        mifp.InitButton((VDXHWND)hwndPreview)


    return False


def OnDestroy(self):
    if mifp:
        mifp.InitButton(NULL)


def OnCommand(self, cmd):
    switch(cmd)
    case IDOK:
        SaveToConfig()
        EndDialog(mhdlg, True)
        return True

    case IDCANCEL:
        mConfig = mOldConfig
        EndDialog(mhdlg, False)
        return True

    case IDC_PREVIEW:
        if mifp:
            mifp.Toggle((VDXHWND)mhdlg)
        return True


    return False


def LoadFromConfig(self):
    SendDlgItemMessage(mhdlg, IDC_REACH, TBM_SETPOS, TRUE, (int)(0.5f + mConfig.mReach * 1000.0f))
    SendDlgItemMessage(mhdlg, IDC_RADIALSAMPLES, TBM_SETPOS, TRUE, (int)(0.5f + mConfig.mRadialSamples * 1000.0f))
    SendDlgItemMessage(mhdlg, IDC_DIFFUSION, TBM_SETPOS, TRUE, (int)(0.5f + mConfig.mDiffusion * 1000.0f))


def SaveToConfig(self):
    fReach = (float)SendDlgItemMessage(mhdlg, IDC_REACH, TBM_GETPOS, 0, 0) / 1000.0f
    fRadialSamples = (float)SendDlgItemMessage(mhdlg, IDC_RADIALSAMPLES, TBM_GETPOS, 0, 0) / 1000.0f
    fDiffusion = (float)SendDlgItemMessage(mhdlg, IDC_DIFFUSION, TBM_GETPOS, 0, 0) / 1000.0f

    if (fReach != mConfig.mReach
            or fRadialSamples != mConfig.mRadialSamples
            or fDiffusion != mConfig.mDiffusion)
        mConfig.mReach	= fReach
        mConfig.mRadialSamples	= fRadialSamples
        mConfig.mDiffusion	= fDiffusion
        return True


    return False


VDXVF_BEGIN_SCRIPT_METHODS(SpatialForegroundRemoverFilter)
VDXVF_DEFINE_SCRIPT_METHOD(SpatialForegroundRemoverFilter, ScriptConfig, "iii")
VDXVF_END_SCRIPT_METHODS()

SpatialForegroundRemoverFilter.~SpatialForegroundRemoverFilter()
    if pmathstatic!=NULL:
        delete pmathstatic
        pmathstatic=NULL

    if fx_buffer!=NULL:
        free(fx_buffer)
        fx_buffer=NULL



def GetParams(self):
    if g_VFVAPIVersion >= 12:
        switch(fa.src.mpPixmapLayout.format)
        case nsVDXPixmap.kPixFormat_XRGB8888:
            break
        case nsVDXPixmap.kPixFormat_YUV444_Planar:
            break
        case nsVDXPixmap.kPixFormat_YUV422_Planar:
            break
        case nsVDXPixmap.kPixFormat_YUV420_Planar:
            break
        case nsVDXPixmap.kPixFormat_YUV411_Planar:
            break
        case nsVDXPixmap.kPixFormat_YUV410_Planar:
            break
        default:
            return FILTERPARAM_NOT_SUPPORTED



    fa.dst.offset = fa.src.offset
    return FILTERPARAM_SUPPORTS_ALTFORMATS



def Start(self):
    #PReporting.setIsMegaDebug(True);#debug only
    if (pmathstatic==NULL) pmathstatic=new PMathStatic();#PMathStatic pmathstatic

    fx_buffer_w=0
    fx_buffer_h=0
    fx_buffer_BytesPP=0
    fx_buffer_Stride=0
    fx_buffer=NULL
    fx_buffer_BytesTotal=0
    time_t rawtime; ##include <ctime> #<time.h>
    struct tm * timeinfo
    time(&rawtime)
    timeinfo=localtime(&rawtime)
    cerr<<(timeinfo.tm_year+1900)<<"-"<<(timeinfo.tm_mon+1)<<"-"<<(timeinfo.tm_mday)<<" "<<timeinfo.tm_hour<<":"<<timeinfo.tm_min<<":"<<timeinfo.tm_sec<<endl


def DrawDebugSquareTo_fx_buffer(self):
    for (int iDebug=0; iDebug<=fa.pfsi.lCurrentSourceFrame; iDebug++)
        for (int yDebug=0; yDebug<=fa.pfsi.lCurrentSourceFrame; yDebug++)
            if iDebug<fa.dst.w and yDebug<fa.dst.h:
                int iLocDebug=yDebug*fx_buffer_Stride+iDebug*fx_buffer_BytesPP
                fx_buffer[iLocDebug]=128
                if fx_buffer_BytesPP>2:
                    fx_buffer[iLocDebug+1]=128
                    fx_buffer[iLocDebug+2]=128

                #targaMask.arrbyData[yDebug*targaMask.Stride()+iDebug*targaMask.BytesPP()+mask_Channel]=255;#fx_buffer[iLocDebug+3]=255;#alpha



}#end DrawDebugSquareTo_fx_buffer
def DrawDebugCircleTo_fx_buffer(self):
    for (int iDebug=0; iDebug<PMath.ppiCache_Used and iDebug<fa.pfsi.lCurrentSourceFrame; iDebug++)
        if PMath.ppiCache[iDebug].x<fa.dst.w and PMath.ppiCache[iDebug].y<fa.dst.h:
            int iLocDebug=PMath.ppiCache[iDebug].y*fx_buffer_Stride+PMath.ppiCache[iDebug].x*fx_buffer_BytesPP
            fx_buffer[iLocDebug]=255
            fx_buffer[iLocDebug+1]=255
            fx_buffer[iLocDebug+2]=255
            #targaMask.arrbyData[PMath.ppiCache[iDebug].y*targaMask.Stride()+PMath.ppiCache[iDebug].x*targaMask.BytesPP()+mask_Channel]=255;#fx_buffer[iLocDebug+3]=255;#alpha
        }#if within range
    }#debug only (result should be WHITE circle inside GRAY square)


def Run(self):
    #PReporting.setIsUltraDebug(True)
    #mConfig.mReach
    #mConfig.mRadialSamples
    #mConfig.mDiffusion
    bool bHorizontalSearch=True
    bool bVerticalSearch=False

    bool bUnknownPixelFormat=False
    bool bGood=False
    cerr<<"SpatialForegroundRemoverFilter.Run..."<<endl
    try
        #*fa.pfsi.lCurrentFrame#current sequence frame, called output frame
        cerr<<"SpatialForegroundRemoverFilter.Run: frame "<<fa.pfsi.lCurrentSourceFrame<<"..."<<endl
        string MaskFile_Name=""
        string MaskFile_UserInput="spatialforegroundremover.tga";#in current working dir (which is the VirtualDub folder)
        for (int iDigits=0; iDigits<10; iDigits++)
            string sDigits=string("")
            for (int iBuild=0; iBuild<iDigits; iBuild++)
                sDigits+=string("0")

            string sFileTheoretical=string("spatialforegroundremover")+sDigits+string(".tga")
            if  File.Exists(sFileTheoretical) :
                MaskFile_UserInput=sFileTheoretical
                #cerr<<sFileTheoretical<<" sequence start frame found"<<endl
                break

            #else cerr<<sFileTheoretical<<" sequence start frame not found"<<endl

        #string MaskFile_Test1="C:\\Documents and Settings\\Owner\\Desktop\\heal-mask1c-80662.tga"
        #string MaskFile_Test2="E:\\Videos\\Projects\\etc\\OldFHC,The\\heal-mask1c-80662.tga"
        if (File.Exists(MaskFile_UserInput)) MaskFile_Name=MaskFile_UserInput
        #elif (File.Exists(MaskFile_Test1)) MaskFile_Name=MaskFile_Test1
        #elif (File.Exists(MaskFile_Test2)) MaskFile_Name=MaskFile_Test2
        if MaskFile_Name!="":
            string MaskFile_CurrentOrPrev_AbsOrRelName=GetCurrentOrPrevFrameFor(MaskFile_Name,fa.pfsi.lCurrentFrame); #GetCurrentOrPrevFrameFor(MaskFile_Name,fa.pfsi.lCurrentSourceFrame)
            cerr<<"SpatialForegroundRemoverFilter.Run: Loading Mask "<<MaskFile_CurrentOrPrev_AbsOrRelName<<"..."<<flush
            bool bTest=self.targaMask.Load(MaskFile_CurrentOrPrev_AbsOrRelName)
            cerr<<(bTest?"OK":"FAILED")<<endl
        }#end if mask found
        else:
            cerr<<"SpatialForegroundRemoverFilter.Run: Using Mask (none, continue)"<<endl

        unsigned int mask_Channel=0; #NOTE: uses blue if mask is 32- or 24-bit
        rRadialSampleSpacing = ((double)mConfig.mRadialSamples*360.0>1.0) ? (360.0/((double)mConfig.mRadialSamples*360.0)) : 360.0
        cerr<<"{Reach:"<<mConfig.mReach<<"; RadialSamples:"<<mConfig.mRadialSamples<<"; RadialSampleSpacing:"<<rRadialSampleSpacing<<"; Diffusion:"<<mConfig.mDiffusion<<"; PReporting.iDebugLevel:"<<PReporting.getDebugLevel()<<"}..."<<endl;#Console.Error.WriteLine(Convert.ToString("{Reach:")+Convert.ToString(mConfig.mReach)+Convert.ToString("; RadialSamples:")+Convert.ToString(mConfig.mRadialSamples)+Convert.ToString("; Diffusion:")+Convert.ToString(mConfig.mDiffusion)+Convert.ToString("}..."))
        unsigned int vdpixmapSource_BytesPP=3
        #unsigned int targaTemp_BytesPP=4
        if g_VFVAPIVersion >= 12:
             vdpixmapDest = *fa.dst.mpPixmap
             vdpixmapSource = *fa.src.mpPixmap
            #int sw
            #int sh
            #NOTES:
            #-data and pitch are Y
            #-data2 and pitch2 are Cb (U)
            #-data3 and pitch3 are Cr (V)

            #Steps:
            #-load targaMask: if loaded but frame is less than current frame, for a later one <= current
            #-prepare fx_buffer (will become interleaved YUV444)
            #-transfer dest frame to fx_buffer
            #  --if BGR24 then transfer using memcpy
            #  --if YUV (even if 444 since planar) then transfer using YUV4xxSubsampledPlanarToYUV444NonPlanar adding alpha channel
            #  --if BGRA32 transfer using CopySurface_BitdepthSensitive(fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,vdpixmapSource.data,vdpixmapSource_BytesPP,vdpixmapSource.pitch,h)
            #-NOTE: after previous step it is fine for fx_buffer to be either YUV444 or RGB24
            #-DEPRECATED 2010-06: Create targaTemp (re-Init only if different size than dest), at 32-bit
            #-calculate healed color for each pixel of the color channels of of 32-bit (YUV4444 or BGRA) targa where targaMask is nonzero
            #  --using fx_buffer
            #  --keep in mind that self may place YUV values into targa
            #  --NEW 2010-06: use mask to alpha blend the intensity of the effect
            #-DEPRECATED 2010-06: copy value of targaMask to alpha channel of targaTemp
            #-DEPRECATED 2010-06: overlay targaTemp to fx_buffer using alpha
            #-NEW 2010-06: using the three appropriate CopyNonPlanarToPlane calls, healed fx_buffer directly to virtualdub dst planes.
            #-if dest is (YUV444 non-planar [RARE] OR BGR24) copy fx_buffer directly to dest using memcpy
            #  --elif dest is BGRA32 copy using CopySurface_BitdepthSensitive(vdpixmapSource.data,vdpixmapSource_BytesPP,fx_buffer,fx_buffer_BytesPP,h*w)
            #  --else dest is neither YUV444 nor RGB nor RGBA: Copy using YUV444ToYUV4xx

            cerr<<"VirtualDub API version 12 or higher found"<<endl
            CTBufferInit(vdpixmapSource.w,vdpixmapSource.h,4);#fx_buffer=malloc etc

            bool bShowDebugCircle=False;#to be changed below
            bool bShowDebugSquare=False;#to be changed below
            #bool bShowTargaTempDebugCircle
            #bool bShowTargaTempDebugSquare
            bool HasFullLumaRes=True
            bool bSamplesOnSecondLine=False
            switch(vdpixmapSource.format)
            case nsVDXPixmap.kPixFormat_XRGB8888:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=4
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using xRGB32")
                #NOTE: outermost "else" case should use same steps as self case!
                # --EXCEPT accessing fa instead of *fa.dst.mpPixmap (a.k.a. vdpixmapSource)
                CopySurface_BitdepthSensitive((unsigned char*)fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,(unsigned char*)vdpixmapSource.data,vdpixmapSource_BytesPP,vdpixmapSource.pitch,vdpixmapSource.w,vdpixmapSource.h)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)

                #if PReporting.getIsUltraDebug():                #	CopySurface_BitdepthSensitive((unsigned char*)targaTemp.arrbyData,targaTemp.BytesPP(),targaTemp.Stride(),(unsigned char*)vdpixmapSource.data,vdpixmapSource_BytesPP,vdpixmapSource.pitch,vdpixmapSource.w,vdpixmapSource.h)
                #	targaTemp.Save("SpatialForegroundRemover-ARGB32-debug.tga")
                #
                break
            case nsVDXPixmap.kPixFormat_RGB888:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using RGB24")
                memcpy(fx_buffer,vdpixmapSource.data,vdpixmapSource.h*vdpixmapSource.pitch)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)
                #if PReporting.getIsUltraDebug():                #	CopySurface_BitdepthSensitive((unsigned char*)targaTemp.arrbyData,targaTemp.BytesPP(),targaTemp.Stride(),(unsigned char*)vdpixmapSource.data,vdpixmapSource_BytesPP,vdpixmapSource.pitch,vdpixmapSource.w,vdpixmapSource.h)
                #	targaTemp.Save("SpatialForegroundRemover-RGB24-debug.tga")
                #
                break
            case nsVDXPixmap.kPixFormat_YUV444_Planar:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:4:4 Planar")
                HasFullLumaRes=True
                CopyPlaneToNonPlanar(fx_buffer, 0, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data, vdpixmapSource.pitch, vdpixmapSource.w, vdpixmapSource.h, HasFullLumaRes)
                CopyPlaneToNonPlanar(fx_buffer, 1, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data2, vdpixmapSource.pitch2, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                CopyPlaneToNonPlanar(fx_buffer, 2, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data3, vdpixmapSource.pitch3, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,False)
                #if PReporting.getIsUltraDebug():                #	YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, (targaTemp.BytesPP()>3)?True:False, False, fx_buffer, fx_buffer_w*fx_buffer_h)
                #	SaveRaw("debug-SpatialForegroundRemover-converted-to-YUV444NonPlanar.raw",(unsigned char*)fx_buffer,fx_buffer_Stride*fx_buffer_h)
                #	targaTemp.Save("SpatialForegroundRemover-YUV444-debug-to-RGB24.tga")
                #	YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
                #
                break
            case nsVDXPixmap.kPixFormat_YUV422_Planar:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:2:2 Planar")
                HasFullLumaRes=True
                CopyPlaneToNonPlanar(fx_buffer, 0, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data, vdpixmapSource.pitch, vdpixmapSource.w, vdpixmapSource.h, HasFullLumaRes)
                CopyPlaneToNonPlanar(fx_buffer, 1, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data2, vdpixmapSource.pitch2, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                CopyPlaneToNonPlanar(fx_buffer, 2, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data3, vdpixmapSource.pitch3, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)
                #if PReporting.getIsUltraDebug():                #	SaveRaw("debug-SpatialForegroundRemover-converted-to-YUV444NonPlanar.raw",(unsigned char*)fx_buffer,fx_buffer_Stride*fx_buffer_h)
                #	YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, False, False, fx_buffer, vdpixmapSource.w*vdpixmapSource.h)
                #	targaTemp.Save("SpatialForegroundRemover-YUV422Planes-debug-to-RGB24.tga")
                #	#YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
                #

                #TransformY8(vdpixmapDest.data, vdpixmapDest.pitch, vdpixmapDest.w, vdpixmapDest.h, mConfig.mYScale)
                #sw = (vdpixmapSource.w + 1) >> 1
                #sh = vdpixmapSource.h
                #TransformY8(vdpixmapDest.data2, vdpixmapDest.pitch2, sw, sh, mConfig.mUScale)
                #TransformY8(vdpixmapDest.data3, vdpixmapDest.pitch3, sw, sh, mConfig.mVScale)
                break
            case nsVDXPixmap.kPixFormat_YUV420_Planar:
                bSamplesOnSecondLine=False
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:2:0 Planar")
                HasFullLumaRes=True
                #NOTE: fx_buffer is 32-bit (see CTBufferInit(...) call above)
                CopyPlaneToNonPlanar(fx_buffer, 0, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data, vdpixmapSource.pitch, vdpixmapSource.w, vdpixmapSource.h, HasFullLumaRes)
                CopyPlaneToNonPlanar(fx_buffer, 1, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data2, vdpixmapSource.pitch2, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                CopyPlaneToNonPlanar(fx_buffer, 2, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data3, vdpixmapSource.pitch3, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)
                #PReporting.setIsUltraDebug(True);#debug only
                #if PReporting.getIsUltraDebug():                #SaveRaw("debug-SpatialForegroundRemover-converted-to-YUV444NonPlanar.raw",(unsigned char*)fx_buffer,fx_buffer_Stride*fx_buffer_h)
                #YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, False, False, fx_buffer, vdpixmapSource.w*vdpixmapSource.h)

                #targaTemp.Save("SpatialForegroundRemover-YUV420-debug-YUV420Planes-to-RGB.tga")
                #YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
                #
                #TODO:
                #--DEPRECATED 2010-06: copy (without alpha) fx_buffer (444 or BGR) onto targaTemp BGR
                #  (need copy before healing; healed fx_buffer will be drawn onto it using mask)
                #Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Copy to targaTemp")
                if PReporting.getIsUltraDebug():
                    if fx_buffer_BytesPP>3:
                        unsigned char* lpLineNow=fx_buffer
                        unsigned char* lpNow
                        for (unsigned int y=0; y<fx_buffer_h; y++)
                            lpNow=lpLineNow
                            for (unsigned int x=0; x<fx_buffer_w; x++)
                                lpNow[3]=255
                                lpNow+=fx_buffer_BytesPP
                            }#end for x
                            lpLineNow+=fx_buffer_Stride
                        }#end for y
                    }#end if fx_buffer has alpha channel
                }#end if bUltraDebug
                #CopySurface_BitdepthSensitive(targaTemp.arrbyData, targaTemp.BytesPP(), targaTemp.Stride(), fx_buffer, fx_buffer_BytesPP, fx_buffer_Stride, fx_buffer_w, fx_buffer_h)
                #if PReporting.getIsUltraDebug():                #	targaTemp.Save("SpatialForegroundRemover-YUV420-debug1-YUV420Planes-to-RGB.tga")
                #
                #--heal fx_buffer
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: heal fx_buffer...")
                #PReporting.setIsUltraDebug(True);#debug only
                #Heal_WithAveraging_Sequential
                Heal_WithAveraging_Permutations(fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,targaMask.arrbyData,targaMask.BytesPP(),targaMask.Stride(),mask_Channel,fx_buffer_w,fx_buffer_h,(double)mConfig.mReach,rRadialSampleSpacing,(double)mConfig.mDiffusion, bHorizontalSearch, bVerticalSearch)
                #Console.Error.Write("debugging frame "+Convert.ToString(fa.pfsi.lCurrentSourceFrame))
                #Console.Error.WriteLine("done. (debug circle drawing)")
                #Heal_ToNearestPixel(fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,targaMask.arrbyData,targaMask.BytesPP(),targaMask.Stride(),mask_Channel,fx_buffer_w,fx_buffer_h,(double)mConfig.mReach,rRadialSampleSpacing,(double)mConfig.mDiffusion)
                #if PReporting.getIsUltraDebug():                #	#NOTE: copying to targaTemp at self point causes debug to be DESTRUCTIVE
                #	#CopySurface_BitdepthSensitive(targaTemp.arrbyData, targaTemp.BytesPP(), targaTemp.Stride(), fx_buffer, fx_buffer_BytesPP, fx_buffer_Stride, fx_buffer_w, fx_buffer_h)
                #	#SaveRaw("SpatialForegroundRemover-YUV420-debug-YUV420Planes-to-RGB-AFTERHEAL.raw",(unsigned char*)fx_buffer,vdpixmapSource.w*vdpixmapSource.h*fx_buffer_BytesPP)
                #	#targaTemp.Save("SpatialForegroundRemover-YUV420-debug-YUV420Planes-to-RGB-AFTERHEAL-DESTRUCTIVEDEBUG.tga")
                #	Targa targaDebug
                #	targaDebug.From(fx_buffer_w,fx_buffer_h,fx_buffer_BytesPP,fx_buffer,False)
                #	#targaDebug.Init(fx_buffer_w,fx_buffer_h,fx_buffer_BytesPP,True)
                #	#targaDebug.CopyBufferFrom(fx_buffer)
                #	targaDebug.Save("SpatialForegroundRemover-YUV420-debug2-HEAL-STEP1of2-fx_buffer.tga")
                #	targaMask.Save("SpatialForegroundRemover-YUV420-debug0-MASK.tga")
                #
                #--DEPRECATED 2010-06: overlay (with targaMask as alpha) healed fx_buffer (444 or BGR) onto targaTemp BGR
                #Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: overlay healed channels to targaTemp using targaMask...")
                #PImage.Draw(targaTemp.arrbyData,0,0,targaTemp.Width(),targaTemp.Height(),targaTemp.BytesPP(),targaTemp.Stride(),fx_buffer,fx_buffer_w,fx_buffer_h,fx_buffer_BytesPP,fx_buffer_Stride,targaMask.arrbyData,targaMask.BytesPP(),targaMask.Stride(),mask_Channel)
                #if PReporting.getIsUltraDebug():                #	targaTemp.Save("SpatialForegroundRemover-YUV420-debug3-HEAL-STEP2of2-444-after-overlay.tga")
                #

                if PReporting.getIsMegaDebug():
                    bShowDebugCircle=True

                if bShowDebugSquare:
                    DrawDebugSquareTo_fx_buffer()
                }#end if bShowDebugSquare
                #Console.Error.Write("...")
                if bShowDebugCircle:
                    PReporting.setParticiple("showing debug circle")
                    DrawDebugCircleTo_fx_buffer()
                }#end if bShowDebugCircle
                #--DEPRECATED 2010-06: copy non-planar targaTemp (444 or BGR) channels onto vdpixmapDest planes
                #CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data,vdpixmapDest.pitch,HasFullLumaRes,targaTemp.arrbyData,0,targaTemp.BytesPP(),targaTemp.Width(),targaTemp.Height());#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data,vdpixmapDest.pitch,bSamplesOnSecondLine,fx_buffer,0,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                #CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data2,vdpixmapDest.pitch2,bSamplesOnSecondLine,targaTemp.arrbyData,1,targaTemp.BytesPP(),targaTemp.Width(),targaTemp.Height());#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data2,vdpixmapDest.pitch2,bSamplesOnSecondLine,fx_buffer,1,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                #CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data3,vdpixmapDest.pitch3,bSamplesOnSecondLine,targaTemp.arrbyData,2,targaTemp.BytesPP(),targaTemp.Width(),targaTemp.Height());#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data3,vdpixmapDest.pitch3,bSamplesOnSecondLine,fx_buffer,2,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                #--NEW 2010-06: copy fx_buffer non-planar channels to vdpixmapDest planes
                #Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: copy channels to video planes...")
                PReporting.setParticiple("copying planes")
                CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data,vdpixmapDest.pitch,HasFullLumaRes,fx_buffer,0,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h);#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data,vdpixmapDest.pitch,bSamplesOnSecondLine,fx_buffer,0,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data2,vdpixmapDest.pitch2,bSamplesOnSecondLine,fx_buffer,1,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h);#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data2,vdpixmapDest.pitch2,bSamplesOnSecondLine,fx_buffer,1,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data3,vdpixmapDest.pitch3,bSamplesOnSecondLine,fx_buffer,2,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h);#CopyNonPlanarToPlane((unsigned char*)vdpixmapDest.data3,vdpixmapDest.pitch3,bSamplesOnSecondLine,fx_buffer,2,fx_buffer_BytesPP,fx_buffer_w,fx_buffer_h)
                if PReporting.getIsMegaDebug()) Console.Error.WriteLine("Finished case for YUV420Planes-to-RGB in SpatialForegroundRemover":
                break
            case nsVDXPixmap.kPixFormat_YUV411_Planar:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:1:1")
                HasFullLumaRes=True
                CopyPlaneToNonPlanar(fx_buffer, 0, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data, vdpixmapSource.pitch, vdpixmapSource.w, vdpixmapSource.h, HasFullLumaRes)
                CopyPlaneToNonPlanar(fx_buffer, 1, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data2, vdpixmapSource.pitch2, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                CopyPlaneToNonPlanar(fx_buffer, 2, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data3, vdpixmapSource.pitch3, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)
                #if PReporting.getIsUltraDebug():                #	SaveRaw("SpatialForegroundRemover-converted-to-YUV444NonPlanar.raw",(unsigned char*)fx_buffer,fx_buffer_Stride*fx_buffer_h)
                #	YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, False, False, fx_buffer, vdpixmapSource.w*vdpixmapSource.h)
                #	targaTemp.Save("SpatialForegroundRemover-YUV420-debug-YUV411Planes-to-RGB.tga")
                #	#YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
                #
                #TransformY8(vdpixmapDest.data, vdpixmapDest.pitch, vdpixmapDest.w, vdpixmapDest.h, mConfig.mReach)

                #sw = (vdpixmapSource.w + 3) >> 2
                #sh = vdpixmapSource.h
                #TransformY8(vdpixmapDest.data2, vdpixmapDest.pitch2, sw, sh, mConfig.mUScale)
                #TransformY8(vdpixmapDest.data3, vdpixmapDest.pitch3, sw, sh, mConfig.mVScale)
                break
            case nsVDXPixmap.kPixFormat_YUV410_Planar:
                bSamplesOnSecondLine=False
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:1:0")
                HasFullLumaRes=True
                CopyPlaneToNonPlanar(fx_buffer, 0, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data, vdpixmapSource.pitch, vdpixmapSource.w, vdpixmapSource.h, HasFullLumaRes)
                CopyPlaneToNonPlanar(fx_buffer, 1, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data2, vdpixmapSource.pitch2, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)
                CopyPlaneToNonPlanar(fx_buffer, 2, fx_buffer_BytesPP, (unsigned char*)vdpixmapSource.data3, vdpixmapSource.pitch3, vdpixmapSource.w, vdpixmapSource.h, bSamplesOnSecondLine)

                #targaTemp.Init(vdpixmapSource.w,vdpixmapSource.h,targaTemp_BytesPP,True)
                #if PReporting.getIsUltraDebug():                #	SaveRaw("debug-SpatialForegroundRemover-converted-to-YUV444NonPlanar.raw",(unsigned char*)fx_buffer,fx_buffer_Stride*fx_buffer_h)
                #	YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, False, False, fx_buffer, vdpixmapSource.w*vdpixmapSource.h)
                #	targaTemp.Save("SpatialForegroundRemover-YUV420-debug-YUV410Planes-to-RGB.tga")
                #	#YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
                #
                #TransformY8(vdpixmapDest.data, vdpixmapDest.pitch, vdpixmapDest.w, vdpixmapDest.h, mConfig.mReach)

                #sw = (vdpixmapSource.w + 3) >> 2
                #sh = (vdpixmapSource.h + 3) >> 2
                #TransformY8(vdpixmapDest.data2, vdpixmapDest.pitch2, sw, sh, mConfig.mUScale)
                #TransformY8(vdpixmapDest.data3, vdpixmapDest.pitch3, sw, sh, mConfig.mVScale)
                break
            case nsVDXPixmap.kPixFormat_YUV422_UYVY:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:2:2 UYVY")
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run Error: has not yet implemented YUV422_UYVY")
                break
            case nsVDXPixmap.kPixFormat_YUV422_YUYV:
                bSamplesOnSecondLine=True
                vdpixmapSource_BytesPP=3
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run: Using YUV 4:2:2 YUYV")
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run Error: has not yet implemented YUV422_YUYV")
                break
            default:
                Console.Error.WriteLine("SpatialForegroundRemoverFilter.Run Error: has not yet implemented less than 24-bit (has only 24- and 32-bit YUV and RGB formats)")
                bUnknownPixelFormat=True
                break
            }#end switch
            bGood=True
            if (bUnknownPixelFormat) bGood=False

        else:
            vdpixmapSource_BytesPP=3
            cerr<<"SpatialForegroundRemoverFilter.Run: using VirtualDub API less than 12"<<endl
            CopySurface_BitdepthSensitive(fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,(unsigned char*)fa.dst.data,vdpixmapSource_BytesPP,fa.dst.pitch,fa.dst.w,fa.dst.h)
            Heal_WithAveraging_Sequential(fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,targaMask.arrbyData,targaMask.BytesPP(),targaMask.Stride(),mask_Channel,fx_buffer_w,fx_buffer_h,(double)mConfig.mReach,rRadialSampleSpacing,(double)mConfig.mDiffusion)
            CopySurface_BitdepthSensitive((unsigned char*)fa.dst.data,vdpixmapSource_BytesPP,fa.dst.pitch,fx_buffer,fx_buffer_BytesPP,fx_buffer_Stride,fx_buffer_w,fx_buffer_h)
            #targaTemp.Init(fa.dst.w,fa.dst.h,targaTemp_BytesPP,True)
            #if PReporting.getIsUltraDebug():            #	CopySurface_BitdepthSensitive((unsigned char*)targaTemp.arrbyData, targaTemp.BytesPP(), targaTemp.Stride(), (unsigned char*)fa.dst.data, vdpixmapSource_BytesPP, fa.dst.pitch, fa.dst.w, fa.dst.h);#YUV444NonPlanarToRGB((unsigned char*)targaTemp.arrbyData, False, False, (unsigned char*)fa.dst.data, fa.dst.h*fa.dst.w)
            #	targaTemp.Save("SpatialForegroundRemover-RGB(VirtualDub API less than 12)-debug-RGB-to-RGB.tga")
            #	#YUV444NonPlanarToRGB(targaTemp.arrbyData,fx_buffer,targaTemp.BytesBuffer)
            #
            bGood=True


    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"","SpatialForegroundRemover.Run")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","SpatialForegroundRemover.Run")

    if PReporting.getIsUltraDebug():
        Console.Error.WriteLine((bGood?"OK(SpatialForegroundRemover.Run)":"FAILED(SpatialForegroundRemover.Run)"))
        Console.Error.WriteLine("Colorspace Conversion debugging info:")
        Console.Error.WriteLine(Convert.ToString("YCToRgb source (byte to float direct cast) range {")
                                 +Convert.ToString("Y:")+Convert.ToString(YCToRgb_fMinY)+"to"+Convert.ToString(YCToRgb_fMaxY)+Convert.ToString("; ")
                                 +Convert.ToString("U:")+Convert.ToString(YCToRgb_fMinU)+"to"+Convert.ToString(YCToRgb_fMaxU)+Convert.ToString("; ")
                                 +Convert.ToString("V:")+Convert.ToString(YCToRgb_fMinV)+"to"+Convert.ToString(YCToRgb_fMaxV)+Convert.ToString("; ")
                                 +"}")
        Console.Error.WriteLine(Convert.ToString("YCToRgb destination (float to byte) range {")
                                 +Convert.ToString("r:")+Convert.ToString(YCToRgb_byMinR)+"to"+Convert.ToString(YCToRgb_byMaxR)+Convert.ToString("; ")
                                 +Convert.ToString("g:")+Convert.ToString(YCToRgb_byMinG)+"to"+Convert.ToString(YCToRgb_byMaxG)+Convert.ToString("; ")
                                 +Convert.ToString("b:")+Convert.ToString(YCToRgb_byMinB)+"to"+Convert.ToString(YCToRgb_byMaxB)+Convert.ToString("; ")
                                 +"}")
        Console.Error.WriteLine(Convert.ToString("RgbToYC destination (byte to float will be rounded to byte) range {")
                                 +Convert.ToString("y:")+Convert.ToString(RgbToYC_fMinY)+"to"+Convert.ToString(RgbToYC_fMaxY)+Convert.ToString("; ")
                                 +Convert.ToString("u:")+Convert.ToString(RgbToYC_fMinU)+"to"+Convert.ToString(RgbToYC_fMaxU)+Convert.ToString("; ")
                                 +Convert.ToString("v:")+Convert.ToString(RgbToYC_fMinV)+"to"+Convert.ToString(RgbToYC_fMaxV)+Convert.ToString("; ")
                                 +"}")

    if (PReporting.getIsMegaDebug()) cerr<<endl<<endl
    return
}#end SpatialForegroundRemoverFilter.Run

def Configure(self, hwnd):
    SpatialForegroundRemoverFilterDialog dlg(mConfig, fa.ifp)
    return dlg.Show((HWND)hwnd)


def GetSettingString(self, *buf, maxlen):
    SafePrintf(buf, maxlen, " (Reach%.1f%%, RSamples%.1f%%, Diffusion%.1f%%)"
               , mConfig.mReach * 100.0f
               , mConfig.mRadialSamples * 100.0f
               , mConfig.mDiffusion * 100.0f
              )


def GetScriptString(self, *buf, maxlen):
    SafePrintf(buf, maxlen, "Config(%u, %u, %u)"
               , (unsigned)(mConfig.mReach * 1000.0f + 0.5f)
               , (unsigned)(mConfig.mRadialSamples * 1000.0f + 0.5f)
               , (unsigned)(mConfig.mDiffusion * 1000.0f + 0.5f)
              )


def ScriptConfig(self, *isi, *argv, argc):
    mConfig.mReach = argv[0].asInt() / 1000.0f
    mConfig.mRadialSamples = argv[1].asInt() / 1000.0f
    mConfig.mDiffusion = argv[2].asInt() / 1000.0f


def CTBufferInit(self, int w, int h, int BytesPP):
    self.fx_buffer_BytesPP=BytesPP
    self.fx_buffer_h=h
    self.fx_buffer_w=w
    self.fx_buffer_Stride=self.fx_buffer_BytesPP*self.fx_buffer_w
    if  (self.fx_buffer==NULL:
            or (self.fx_buffer_BytesTotal!=(self.fx_buffer_h*self.fx_buffer_Stride)) )
        if self.fx_buffer!=NULL:
            free(self.fx_buffer)
            self.fx_buffer=NULL

        self.fx_buffer_BytesTotal=self.fx_buffer_h*self.fx_buffer_Stride
        self.fx_buffer=(unsigned char*)malloc(self.fx_buffer_BytesTotal)

}#end CTBufferInit

#######################################/

extern filterDef_SpatialForegroundRemover = VDXVideoFilterDefinition<SpatialForegroundRemoverFilter>("ProtoArmor", "Spatial Foreground Remover", "Removes the destination's foreground at pixels that are non-zero in the specified mask by gathering information from the surrounding destination pixels where mask's pixel value is zero.")
