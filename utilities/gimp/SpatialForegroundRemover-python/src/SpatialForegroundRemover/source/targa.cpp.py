#ifndef TARGA_CPP
#define TARGA_CPP

#include <iostream>
#include <iomanip>
#include <fstream>
#include <memory>
#include "targa.h"
##include "E:\Projects-cpp\Base\targa.h"

using namespace std

namespace ProtoArmor
##region static targa functions
def RLESizeUncompressed(self, arrbySrc, iStart, iSrcSize, iBytesPerChunk):
    byte* arrbyNull=null
    return RLEUncompress(arrbyNull, 0, arrbySrc, iSrcSize, iBytesPerChunk, 0, iStart, True)

def Compare(self, arrbySrc1, iSrcLoc1, arrbySrc2, iSrcLoc2, iRun):
    bool bMatch=False
    int iMatch=0
    try
        for (int iNow; iNow<iRun; iNow++)
            if (arrbySrc1[iSrcLoc1+iNow]==arrbySrc2[iSrcLoc2+iNow]) iMatch++

        if (iMatch==iRun) bMatch=True

    catch (exception& exn)
        PReporting.ShowExn(exn,"Compare")

    catch (...)
        PReporting.ShowUnknownExn("","Compare")

    return bMatch


def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesToParse, iBytesPerChunk):
    return RLECompress(iReturnLength, arrbySrc, iSrcStart, iBytesToParse, iBytesPerChunk, False)

def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesToParse, iBytesPerChunk, bCountOnlyAndReturnNull):
    bool bGood=True
    iReturnLength=0
    int iTotal=0
    byte* arrbyReturn=null
    try
        if not bCountOnlyAndReturnNull:
            byte* test=RLECompress(iTotal,arrbySrc,iSrcStart,iBytesToParse,iBytesPerChunk,True)
            if iTotal>0) arrbyReturn=(byte*)malloc(iTotal:
            else:
                bGood=False
                PReporting.ShowErr("Compressed total of "+Convert.ToString(iTotal)+Convert.ToString(" wasn't calculated correctly"),"","RLECompress")


        if bGood:
            int iSrcAbs=iSrcStart
            int iRun=0
            bool bRunIsCompressed=False
            int iSrcRel=0
            #int iNow
            bool bPartOfThisTypeOfRun
            int iPacketByte=0
            while (iSrcRel<iBytesToParse)
                bRunIsCompressed=( (iSrcRel+iBytesPerChunk*2<=iBytesToParse) and Compare(arrbySrc,iSrcAbs,arrbySrc,iSrcAbs+iBytesPerChunk,iBytesPerChunk) )  ?  True  :  False
                iRun=bRunIsCompressed?1:0
                bPartOfThisTypeOfRun=True
                iPacketByte=iReturnLength
                iReturnLength++; #advance past RLE packet header byte (set it later)
                while (bPartOfThisTypeOfRun)
                    #Advance through chunk and copy it:
                    for (int iNow=0; iNow<iBytesPerChunk; iNow++)
                        if not bRunIsCompressed or iRun==1:
                            if not bCountOnlyAndReturnNull:
                                arrbyReturn[iReturnLength]=arrbySrc[iSrcAbs]
                            iReturnLength++

                        iSrcRel++
                        iSrcAbs++

                    iRun++
                    #calculate booleans for NEXT run:
                    if (iRun==128) bPartOfThisTypeOfRun=False
                    else:
                        if bRunIsCompressed:
                            bPartOfThisTypeOfRun=( (iSrcRel+iBytesPerChunk*2<=iBytesToParse) and Compare(arrbySrc,iSrcAbs,arrbySrc,iSrcAbs+iBytesPerChunk,iBytesPerChunk) )  ?  True  :  False
                        else:
                            bPartOfThisTypeOfRun=( (iSrcRel+iBytesPerChunk*2<=iBytesToParse) and not Compare(arrbySrc,iSrcAbs,arrbySrc,iSrcAbs+iBytesPerChunk,iBytesPerChunk) )  ?  True  :  False
                    }#end else not too long

                if not bCountOnlyAndReturnNull:
                    if bRunIsCompressed) arrbyReturn[iPacketByte]=0x80 & (byte)(iRun-1:
                    else arrbyReturn[iPacketByte]=(byte)(iRun-1)

            }#end while iSrcRel<iBytesToParse
        }#end if bGood

    catch (exception& exn)
        PReporting.ShowExn(exn,"RLECompress")

    catch (...)
        PReporting.ShowUnknownExn("","RLECompress")

    return arrbyReturn
}#end RLECompress

#RLEUncompress(arrbyDest, iDestSize, arrbySrc, iSrcSize, iBytesPerChunk)
def RLEUncompress(self, arrbyDest, iDestSize, arrbySrc, iSrcSize, iBytesPerChunk):
    if (iDestSize<0) iDestSize=0
    return RLEUncompress(arrbyDest, iDestSize, arrbySrc, iSrcSize, iBytesPerChunk, 0, 0, False)

#int iBytesFound=RLEUncompress(arrbyDest, iDestSizeIrrelevantIfCountOnlyIsTrue, arrbySrc, iSrcSize, iBytesPerChunk, iSrcStart, bCountOnlyAndDontTouchDest)
def RLEUncompress(self, arrbyDest, iDestSizeIrrelevantIfCountOnlyIsTrue, arrbySrc, iSrcSize, iBytesPerChunk, iDestStart, iSrcStart, bCountOnlyAndDontTouchDest):
    bool bGood=True
    int iDestAbs=iDestStart
    int iDestRel=0
    int iTotal=0
    try
        if bGood:
            int iSrcAbs=iSrcStart
            int iRun=0
            bool bRunIsCompressed=False
            int iSrcRel=0
            int iChunkRelNow
            while (iSrcAbs<iSrcSize)
                if (arrbySrc[iSrcAbs]>=128)   #if high bit is True
                    bRunIsCompressed=True
                    iRun=((int)arrbySrc[iSrcAbs]-128)+1

                else:
                    bRunIsCompressed=False
                    iRun=(int)arrbySrc[iSrcAbs]+1

                #first advance past packet header byte:
                iSrcRel++
                iSrcAbs++
                for (iChunkRelNow=0; iChunkRelNow<iRun and iSrcAbs<iSrcSize; iChunkRelNow++)
                    for (int iChunkSubByte=0; iChunkSubByte<iBytesPerChunk and (iSrcAbs+iChunkSubByte)<iSrcSize; iChunkSubByte++)
                        if not bCountOnlyAndDontTouchDest:
                            if iDestAbs>=iDestSizeIrrelevantIfCountOnlyIsTrue:
                                PReporting.ShowErr("Compressed data wanted destination bigger than "+Convert.ToString(iDestSizeIrrelevantIfCountOnlyIsTrue)+" bytes.","","RLEUncompress")
                                return 0

                            arrbyDest[iDestAbs]=arrbySrc[iSrcAbs+iChunkSubByte]
                        }#end if actually uncompressing
                        iDestAbs++
                        iDestRel++

                    if not bRunIsCompressed:
                        #has to be incremented separately here in case pixel needed to be used multiple times in self outer loop
                        #It is important that we increment past the whole chunk now (self makes sure alignment will be right) instead of iBytesCopiedNow
                        iSrcRel+=iBytesPerChunk
                        iSrcAbs+=iBytesPerChunk

                }#end for iChunkRelNow of run
                if bRunIsCompressed:
                    #has to be incremented separately here so that pixel could be used multiple times above
                    #It is important that we increment past the whole chunk now (self makes sure alignment will be right) instead of iBytesCopiedNow
                    iSrcRel+=iBytesPerChunk
                    iSrcAbs+=iBytesPerChunk

            }#end while still any data (iSrcAbs<iSrcSize)


    catch (exception& exn)
        PReporting.ShowExn(exn,"RLEUncompress")

    catch (...)
        PReporting.ShowUnknownExn("","RLEUncompress")

    #Run-length packet:
    #--byte with high bit=True
    #  --the rest of the bits are the run-length minus 1 (128 max, 0 is 1 long)
    #--then one pixel of raw data, a palette index (to be repeated by run-length)
    #Raw packet:
    #--byte with high bit=False
    #  --the rest of the bits are the number of raw pixels minus 1 (128 max, 0 is 1 long)
    #  --then run-length number of pixels of raw data, palette indeces
    if (not bGood) iDestRel=0
    return iDestRel
}#end RLEUncompress
##endregion static Targa functions

##region TargaFooter methods
TargaFooter.TargaFooter(byte* arrbyDataSrcToCopyFrom, u32Start, u32Count, u32ActualSourceBufferSize)
    Init(arrbyDataSrcToCopyFrom, u32Start, u32Count, u32ActualSourceBufferSize)

TargaFooter.TargaFooter(byte* lpbyDataPointerToKeep, u32Size)
    Init(lpbyDataPointerToKeep,u32Size)

TargaFooter.TargaFooter()
    dump=null
    dump_Length=0

TargaFooter.~TargaFooter()
    PMemory.SafeFree(dump)

def Init(self, streamIn_ToReadToEnd):
    bool bGood=True
    PMemory.SafeFree(dump)
    self.dump_Length=0
    unsigned int u32SizeTemp=0
    long long iGot=0
    byte byNow
    long long iPrevPos
    if streamIn_ToReadToEnd.BaseStream_CanRead():
        do
            iPrevPos=streamIn_ToReadToEnd.BaseStream_Position()
            byNow=streamIn_ToReadToEnd.ReadByte()
            iGot=streamIn_ToReadToEnd.BaseStream_Position()-iPrevPos
            if (iGot==1) PMemory.Push(dump,u32SizeTemp,dump_Length,byNow); #ok if dump is null thus far
            else:
                break


        while (iGot>0)

    else:
        PReporting.ShowErr("Unreadable BinaryReader was sent to TargaFooter Init","reading targa footer","")
        bGood=False

    PMemory.Redim(dump,u32SizeTemp,dump_Length)
    return bGood
}#end BinaryReader.Init(BinaryReader&)
def Init(self, arrbyDataSrcToCopyFrom, u32SrcStart, u32Count, u32ActualSourceBufferSize):
    bool bGood=True
    PMemory.SafeFree(dump)
    try
        dump_Length=u32Count
        dump=(byte*)malloc(u32Count)
        uint iSrc=u32SrcStart
        for (uint iNow=0; iNow<u32Count and iSrc<u32ActualSourceBufferSize; iNow++,iSrc++)
            dump[iNow]=arrbyDataSrcToCopyFrom[iSrc]


    catch (exception& exn)
        PReporting.ShowExn(exn, "TargaFooter.Init")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","TargaFooter.Init")

    return bGood

def Init(self, lpbyDataPointerToKeep, u32Size):
    bool bGood=True
    try
        if u32Size>0 and lpbyDataPointerToKeep!=null:
            dump_Length=u32Size
            dump=lpbyDataPointerToKeep
            #TODO: process the footer here

        else:
            dump_Length=0
            dump=null


    catch (exception& exn)
        bGood=False
        string sMsg="u32Size="+Convert.ToString(u32Size)
        sMsg+="; lpbyDataPointerToKeep is"
        sMsg+=((lpbyDataPointerToKeep==null)?"null.":"not null.")
        PReporting.ShowExn(exn,"TargaFooter.Init"+sMsg)

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","TargaFooter.Init")

    return bGood

def Init(self):
    return Init(null,0)

def WriteTo(self, &streamOut):
    bool bGood=True
    for (uint iNow=0; iNow<dump_Length; iNow++)
        long long iPositionPrev=streamOut.BaseStream_Position()
        streamOut.Write(dump[iNow])
        if streamOut.BaseStream_Position()-iPositionPrev!=1:
            bGood=False
            break


    return bGood
}#end WriteTo BinaryWriter
def ByteCount(self):
    return dump_Length

##endregion TargaFooter methods

##region Targa methods
Targa.Targa()
    InitNull()

Targa.~Targa()
    PMemory.SafeFree(arrbyData)

def Width(self):
    return iWidth

def Height(self):
    return iHeight

def BytesPP(self):
    return iBytesPP

def Stride(self):
    return iStride

def BytesAsUncompressed(self):
    return iBytesAsUncompressed

def BytesBuffer(self):
    return iBytesBuffer

def Init(self, iSetWidth, iSetHeight, iSetBytesPP, bReallocateBuffers):
    bool bGood=True
    if bReallocateBuffers:
        PMemory.SafeFree(arrbyColorMap)
        iMapLength=0
        sID=""
        PMemory.SafeFree(arrbyData)

    iWidth=iSetWidth
    iHeight=iSetHeight
    iBitDepth=iSetBytesPP*8
    DeriveVars();#does set iBytesPP, iStride, iBytesAsUncompressed
    if (TypeTarga<=0)   #don't change if already set
        if (iSetBytesPP==4 or iSetBytesPP==3) TypeTarga=TypeUncompressedTrueColor
        elif iSetBytesPP==1) TypeTarga=TypeUncompressedGrayscale; #assumes no palette (no colormap:

    iBytesBuffer=iBytesAsUncompressed
    if iBytesBuffer<=0:
        PReporting.ShowErr("iBytesBuffer="+Convert.ToString(iBytesBuffer)+"not ","","Targa.Init")
        bGood=False

    if bReallocateBuffers and bGood:
        arrbyData=(byte*)malloc(iBytesBuffer)

    return bGood
}#end Targa.Init
def CopyTo(self, &targaDest):
    bool bGood=False
    try
        targaDest.Init(iWidth,iHeight,iBytesPP,False)
        if iBytesBuffer>0) targaDest.arrbyData=(byte*)malloc(iBytesBuffer:
        targaDest.MapType=MapType; #1 byte
        targaDest.TypeTarga=TypeTarga; #1 byte
        targaDest.iMapOrigin=iMapOrigin; #2 bytes
        targaDest.iMapLength=iMapLength; #2 bytes
        targaDest.iMapBitDepth=iMapBitDepth; #1 byte
        targaDest.xImageLeft=xImageLeft; #2 bytes
        targaDest.yImageBottom=yImageBottom; #2 bytes #TODO: don't flip if not zero
        targaDest.iWidth=iWidth; #2 bytes
        targaDest.iHeight=iHeight; #2 bytes
        targaDest.iBitDepth=iBitDepth; #1 byte #TODO: 16 is 5.5.5.1 (not !not )IF(not !not ) low nibble of descriptor is 1 (otherwise 5.6.5 and descriptor low nibble is zero)
        targaDest.bitsDescriptor=bitsDescriptor; #1 byte  #(default zero)
        targaDest.sID=sID; #array of [iTagLength] bytes  #[bySizeofID] -- custom non-terminated string
        targaDest.iBytesPP=iBytesPP
        targaDest.iStride=iStride
        targaDest.iBytesAsUncompressed=iBytesAsUncompressed;#byte sizeof image data only
        targaDest.iBytesBuffer=iBytesBuffer
        int iNow
        if iBytesBuffer>0:
            for (iNow=0; iNow<iBytesBuffer; iNow++)
                targaDest.arrbyData[iNow]=arrbyData[iNow]


        else PReporting.ShowErr("Warning: Program tried to duplicate null targa.","","Targa CopyTo")
        if iMapLength>0:
            targaDest.arrbyColorMap=(byte*)malloc(iMapLength); #array of [] bytes  #[byMapBitDepth*wMapLength] -- the palette
            for (iNow=0; iNow<iMapLength; iNow++)
                targaDest.arrbyColorMap[iNow]=arrbyColorMap[iNow]


        bGood=True

    catch (exception& exn)
        PReporting.ShowExn(exn,"Targa CopyTo")
        bGood=False

    catch (...)
        PReporting.ShowUnknownExn("","Targa CopyTo")
        bGood=False

    return bGood
}#end Targa.CopyTo(Targa)
def DrawFast(self, arrbyDest, xAtDest, yAtDest, iDestWidth, iDestHeight, iDestBytesPP, iDestStride):
    bool bGood=True
    try
        '''
        byte* lpbySrc
        byte* lpbyDest
        byte* lpbySrcLine=arrbyData
        byte* lpbyDestLine=#&arrbyDest[rectDestAdjusted.Y*iDestStride+rectDestAdjusted
        uint* lpu32Src=(uint*)arrbyData
        uint* lpu32Dest=(uint*)arrbyDest
        ushort lpwSrc=(ushort*)arrbyData
        ushort lpwDest=(ushort*)arrbyDest
        '''
        #int xDest
        int yDest=yAtDest
        int iDestByteLineStart=xAtDest*iDestBytesPP
        int iDestByteNow
        int iSrcByteLineStart=0
        #int iSrcByteNow
        int iSrcStart=0;#NYI (not really used correctly) in compressed mode; only different if cropping self
        int iLineEnder=iStride;#NYI in compressed mode; only different if cropping self
        int iStrideLimited=iStride;#NYI in compressed mode; only different if cropping self, used if doing a direct byte buffer copy for the whole line
        if iDestBytesPP==iBytesPP:
            if IsCompressed():
                bool bGood=True
                int iDestAbs=iDestByteLineStart
                int iDestRel=0
                int iTotal=0
                try
                    if bGood:
                        int iSrcAbs=iSrcStart
                        int iRun=0
                        bool bRunIsCompressed=False
                        int iSrcRel=0
                        int iChunkRelNow
                        int xSrcFake=0
                        int iDestLastXToFirstXOnNextLine=iDestStride-(iWidth*iDestBytesPP)
                        int iSrcSize=iBytesAsUncompressed
                        int iDestSize=iDestStride*iDestHeight
                        while (iSrcAbs<iSrcSize)
                            if (arrbyData[iSrcAbs]>=128)   #if high bit is True
                                bRunIsCompressed=True
                                iRun=((int)arrbyData[iSrcAbs]-128)+1

                            else:
                                bRunIsCompressed=False
                                iRun=(int)arrbyData[iSrcAbs]+1

                            #first advance past packet header byte:
                            iSrcRel++
                            iSrcAbs++
                            for (iChunkRelNow=0; iChunkRelNow<iRun and iSrcAbs<iSrcSize; iChunkRelNow++)
                                for (int iChunkSubByte=0; iChunkSubByte<iBytesPP and (iSrcAbs+iChunkSubByte)<iSrcSize; iChunkSubByte++)
                                    if iDestAbs>=iDestSize:
                                        PReporting.ShowErr("Compressed data wanted destination bigger than "+Convert.ToString(iDestSize)+" bytes.","","DrawFast (same bit depth, uncompressing)")
                                        return 0

                                    arrbyDest[iDestAbs]=arrbyData[iSrcAbs+iChunkSubByte]
                                    iDestAbs++
                                    iDestRel++

                                if not bRunIsCompressed:
                                    #has to be incremented separately here in case pixel needed to be used multiple times in self outer loop
                                    #It is important that we increment past the whole chunk now (self makes sure alignment will be right) instead of iBytesCopiedNow
                                    iSrcRel+=iBytesPP
                                    iSrcAbs+=iBytesPP

                                xSrcFake++
                                if xSrcFake==iWidth:
                                    xSrcFake=0
                                    iDestRel+=iDestLastXToFirstXOnNextLine
                                    iDestAbs+=iDestLastXToFirstXOnNextLine

                            }#end for iChunkRelNow of run
                            if bRunIsCompressed:
                                #has to be incremented separately here so that pixel could be used multiple times above
                                #It is important that we increment past the whole chunk now (self makes sure alignment will be right) instead of iBytesCopiedNow
                                iSrcRel+=iBytesPP
                                iSrcAbs+=iBytesPP

                        }#end while still any data (iSrcAbs<iSrcSize)


                catch (exception& exn)
                    PReporting.ShowExn(exn,"DrawFast (same bit depth, uncompressing)")

                catch (...)
                    PReporting.ShowUnknownExn("","DrawFast (same bit depth, uncompressing)")

            }#end if compressed
            else  #else uncompressed already
                for (int ySrc=0; ySrc<iHeight; ySrc++,yDest++,iSrcByteLineStart+=iStride,iDestByteLineStart+=iDestStride)
                    iDestByteNow=iDestByteLineStart;#xDest=xAtDest
                    memcpy(&arrbyDest[iDestByteNow],&arrbyData[iSrcByteLineStart],iStrideLimited)
                    #for (iSrcByteNow=iSrcByteLineStart; iSrcByteNow<iLineEnder; iSrcByteNow++, iDestByteNow++) { #for (int xSrc=0; xSrc<iWidth; xSrc++,xDest++)                    #	arrbyDest[iDestByteNow]=arrbyData[iSrcByteNow]
                    #



        else  #else dissimilar bitdepths
            if IsCompressed():
                PReporting.ShowErr("Not implemented: Can't copy from compressed targa of dissimilar bit depth","","Targa.DrawFast")

            else:
                for (int ySrc=0; ySrc<iHeight; ySrc++,yDest++,iSrcByteLineStart+=iStride,iDestByteLineStart+=iDestStride)
                    iDestByteNow=iDestByteLineStart;#xDest=xAtDest
                    memcpy(&arrbyDest[iDestByteNow],&arrbyData[iSrcByteLineStart],iStrideLimited)
                    #for (iSrcByteNow=iSrcByteLineStart; iSrcByteNow<iLineEnder; iSrcByteNow++, iDestByteNow++) { #for (int xSrc=0; xSrc<iWidth; xSrc++,xDest++)                    #	arrbyDest[iDestByteNow]=arrbyData[iSrcByteNow]
                    #




    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"Targa.DrawFast")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","Targa.DrawFast")

    return bGood

def ToRect(self, rectReturn):
    rectReturn.Width=iWidth
    rectReturn.Height=iHeight

def ToRect(self, rectReturn):
    rectReturn.Width=(float)iWidth
    rectReturn.Height=(float)iHeight

def From(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, bUsePointerNotCopyData):
    return From(iWidthTo,iHeightTo,iBytesPP,arrbySrc,bUsePointerNotCopyData,0)

def From(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, bUsePointerNotCopyData, u32SrcStart):
    bool bGood=True
    bGood=Init(iWidthTo,iHeightTo,iBytesPP, bUsePointerNotCopyData)
    if bGood:
        if bUsePointerNotCopyData:
            arrbyData=&arrbySrc[u32SrcStart]

        else:
            try
                memcpy(arrbyData,&arrbySrc[u32SrcStart],iWidthTo*iHeightTo*iBytesPP)

            catch (exception& exn)
                bGood=False
                PReporting.ShowExn(exn,"Targa.From")

            catch (...)
                bGood=False
                PReporting.ShowUnknownExn("","Targa.From")



    else:
        PReporting.ShowErr("couldn't initialize.","","Targa.From")

    return bGood
}#end From a source buffer
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen):
    return SafeCopyFrom(iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, True)

def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, bReInitializeAll):
    return SafeCopyFrom(iWidthTo,iHeightTo,iBytesPP,arrbySrc,u32SrcRealLen,0,bReInitializeAll)

#SafeCopyFrom(iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll)
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, &streamIn, bReInitializeAll):
    int iFound=0
    bool bGood=True
    static bool bFirstRun=True
    string sFuncNow="Targa.SafeCopyFrom"
    if bFirstRun) Console.Error.Write(sFuncNow:
    string sArgs="(w="+Convert.ToString(iWidthTo)+",h="+Convert.ToString(iHeightTo)+",BytesPP="+Convert.ToString(iBytesPP)+","+((not streamIn.BaseStream_CanRead())?"src:CanRead()==FALSE":"src=ok")+",bReInitializeAll="+Convert.ToString(bReInitializeAll)+")"
    sFuncNow+=sArgs
    if bFirstRun) Console.Error.Write(sArgs:
    static bool bFirstFatalSafeCopyFrom=True
    #if streamIn==null:    #	PReporting.ShowErr("Null imagenot  Forcing reinitialize",sFuncNow)
    #	if bFirstFatalSafeCopyFrom:    #		Console.Error.WriteLine()
    #		Console.Error.WriteLine()
    #		Console.Error.WriteLine("IMAGE BUFFER IS NULLnot !not !not !not !not !not !not !not !not !not !not !not !not !not !not !not ")
    #		Console.Error.WriteLine()
    #		bFirstFatalSafeCopyFrom=False
    #
    #	bReInitializeAll=True
    #
    if bReInitializeAll:
        if not Init(iWidthTo,iHeightTo,iBytesPP,True):
            bGood=False
            PReporting.ShowErr("couldn't reinit.","",sFuncNow)


    if bGood:
        #	if arrbySrc==null:        #		bGood=False
        #		PReporting.ShowErr("null sourcenot ",sFuncNow)
        #

    if bGood:
        try
            #int iSrcAbs=(int)u32SrcStart
            int iLen=iWidthTo*iHeightTo*iBytesPP
            #int iSrcRealLen=(int)u32SrcRealLen
            int iNow=0
            int iPlacePrev
            int iGot
            for (iNow=0; iNow<iLen; iNow++)  #, iSrcAbs++) {#and iSrcAbs<iSrcRealLen
                iPlacePrev=(int)streamIn.BaseStream_Position()
                arrbyData[iNow]=(int)streamIn.ReadByte();#arrbySrc[iSrcAbs]
                iGot=(int)streamIn.BaseStream_Position()-iPlacePrev
                if (iGot>0) iFound+=iGot

            if iNow<iLen)  #ok since iNow is now a length (since increments past end then exits loop:
                bGood=False
                PReporting.ShowErr("Only"+Convert.ToString(iNow)+" of "+Convert.ToString(iLen)+" expected bytes of image data were found in file.","",sFuncNow)


        catch (exception& exn)
            bGood=False
            PReporting.ShowExn(exn,sFuncNow)

        catch (...)
            bGood=False
            PReporting.ShowUnknownExn("",sFuncNow)

        if bFirstRun) Console.Error.Write(bGood?"Targa.SafeCopyFrom Success...":"Targa.SafeCopyFrom finished with errors...":

    bFirstRun=False
    return iFound
}#end SafeCopyFrom BinaryReader
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll):
    int iFound=0
    bool bGood=True
    static bool bFirstRun=True
    string sFuncNow="Targa.SafeCopyFrom"
    if bFirstRun) Console.Error.Write(sFuncNow:
    string sArgs="(w="+Convert.ToString(iWidthTo)+",h="+Convert.ToString(iHeightTo)+",BytesPP="+Convert.ToString(iBytesPP)+","+(arrbySrc==null?"src=null":"src=ok")+",len="+Convert.ToString(u32SrcRealLen)+",start="+Convert.ToString(u32SrcStart)+","+Convert.ToString(bReInitializeAll)+")"
    sFuncNow+=sArgs
    if bFirstRun) Console.Error.Write(sArgs:
    static bool bFirstFatalSafeCopyFrom=True
    if arrbyData==null:
        PReporting.ShowErr("Null imagenot  Forcing reinitialize","",sFuncNow)
        if bFirstFatalSafeCopyFrom:
            Console.Error.WriteLine()
            Console.Error.WriteLine()
            Console.Error.WriteLine("IMAGE BUFFER IS NULLnot !not !not !not !not !not !not !not !not !not !not !not !not !not !not !not ")
            Console.Error.WriteLine()
            bFirstFatalSafeCopyFrom=False

        bReInitializeAll=True

    if bReInitializeAll:
        if not Init(iWidthTo,iHeightTo,iBytesPP,True):
            bGood=False
            PReporting.ShowErr("couldn't reinit.","",sFuncNow)


    if bGood:
        if arrbySrc==null:
            bGood=False
            PReporting.ShowErr("null sourcenot ","",sFuncNow)


    if bGood:
        try
            int iSrcAbs=(int)u32SrcStart
            int iLen=iWidthTo*iHeightTo*iBytesPP
            int iSrcRealLen=(int)u32SrcRealLen
            int iNow=0
            for (iNow=0; iNow<iLen and iSrcAbs<iSrcRealLen; iNow++, iSrcAbs++)
                arrbyData[iNow]=arrbySrc[iSrcAbs]
                iFound++

            if iNow<iLen)  #ok since iNow is now a length (since increments past end then exits loop:
                bGood=False
                PReporting.ShowErr("Only"+Convert.ToString(iNow)+" of "+Convert.ToString(iLen)+" expected bytes of image data were found in file.","",sFuncNow)


        catch (exception& exn)
            bGood=False
            PReporting.ShowExn(exn,sFuncNow)

        catch (...)
            bGood=False
            PReporting.ShowUnknownExn("",sFuncNow)

        if bFirstRun) Console.Error.Write(bGood?"Targa.SafeCopyFrom Success...":"Targa.SafeCopyFrom finished with errors...":

    bFirstRun=False
    return iFound
}#end SafeCopyFrom source buffer
def GetBufferPointer(self):
    return arrbyData

def IsLoaded(self):
    return (arrbyData!=null)

def Save(self, sFileNow):
    sFile=sFileNow
    return Save()

def Save(self):
    string sMsg="before initialization"
    bool bGood=True
    Console.Error.WriteLine("Creating BinaryWriter {fopen mode:\""+FileMode.OpenWrite+"\"; sFile:"+sFile+"}...")
    BinaryWriter streamOut( File.Open(sFile,FileMode.OpenWrite), True)
    try
        Console.Error.WriteLine("Writing to BinaryWriter...")
        if self.TypeTarga<=0) Console.Error.WriteLine("Warningnot   Invalid image data typenot   {TypeTarga:"+Convert.ToString(self.TypeTarga)+"}":
        #streamOut.OpenWrite(sFile)
        ushort wNow=0
        byte byNow=0
        long long iPlacePrev=0
        uint u32Test=0
        #(byte)(length of id)
        iPlacePrev=streamOut.BaseStream_Position()
        if '''sID!=null and '''sID.length()>255) sID=sID.substr(0,255:
        uint u32IDLenNow=('''sID==null or '''sID=="")?0:(uint)sID.length(); #NEEDED later!
        byNow=Convert.ToByte(u32IDLenNow);#
        streamOut.Write(byNow);#id length (see above)
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(byte)(int)MapType
        iPlacePrev=streamOut.BaseStream_Position()
        byNow=(byte)MapType; #type of palette
        streamOut.Write(byNow); #MapType
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(byte)(int)TypeTarga
        iPlacePrev=streamOut.BaseStream_Position()
        byNow=(byte)TypeTarga
        streamOut.Write(byNow); #TypeTarga
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(ushort)iMapOrigin
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(ushort)iMapOrigin
        streamOut.Write(wNow); #iMapOrigin
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(ushort)iMapLength
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(ushort)iMapLength
        streamOut.Write(wNow); #iMapLength (ushort)
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(byte)iMapBitDepth
        iPlacePrev=streamOut.BaseStream_Position()
        byNow=(byte)iMapBitDepth; #aka map width
        streamOut.Write(byNow); #map bitdepth aka map width (byte)
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(ushort)xImageLeft
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(ushort)xImageLeft
        streamOut.Write(wNow); #image left edge (orientation of raw data)
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(ushort)yImageBottom
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(uint)yImageBottom; #aka y origin
        streamOut.Write(wNow); #image bottom (orientation of raw data)
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(ushort)iWidth
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(ushort)iWidth
        streamOut.Write(wNow); #width
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(ushort)iHeight
        iPlacePrev=streamOut.BaseStream_Position()
        wNow=(ushort)iHeight
        streamOut.Write(wNow); #height
        if (streamOut.BaseStream_Position()-iPlacePrev != 2) bGood=False
        #(byte)iBitDepth
        iPlacePrev=streamOut.BaseStream_Position()
        byNow=(byte)iBitDepth
        streamOut.Write(byNow); #bitdepth
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(byte)bitsDescriptor
        iPlacePrev=streamOut.BaseStream_Position()
        byNow=(byte)bitsDescriptor
        streamOut.Write(byNow); #bitsDescription
        if (streamOut.BaseStream_Position()-iPlacePrev != 1) bGood=False
        #(byte[length of id])sID
        if u32IDLenNow>0)   #NOTE: u32IDLenNow was written earlier (see far above:
            iPlacePrev=streamOut.BaseStream_Position()
            if sID.length()!=u32IDLenNow:
                u32IDLenNow=sID.length()
                PReporting.ShowErr("u32IDLenNow was not equal to length of sID","saving targa","")

            streamOut.Write(sID);#streamOut.WriteAscii(sID,u32IDLenNow)
            if (streamOut.BaseStream_Position()-iPlacePrev != u32IDLenNow) bGood=False

        #(byte[iMapLength])(arrbyColorMap)
        if iMapLength>0:
            iPlacePrev=streamOut.BaseStream_Position()
            streamOut.Write(arrbyColorMap,0,iMapLength)
            #for (int iNow=0; iNow<iMapLength; iNow++)            #	streamOut.Write(arrbyColorMap[iNow])
            #
            if streamOut.BaseStream_Position()-iPlacePrev != iMapLength:
                bGood=False
                sMsg="Not all "+Convert.ToString(iMapLength)+" color map bytes were found."


        else PMemory.SafeFree(arrbyColorMap)
        #(byte[iWidth*iHeight*iBytesPP])(arrbyData)
        if iBytesBuffer>0:
            if arrbyData!=null:
                iPlacePrev=streamOut.BaseStream_Position()
                int iLineOffset=0
                if IsSavedAsFlipped():
                    iLineOffset=(iHeight-1)*self.iStride
                    for (int iLine=self.iHeight-1; iLine>=0; iLine--)
                        if iLineOffset+iStride<=iBytesBuffer) streamOut.Write(arrbyData,iLineOffset,iStride:
                        else PReporting.ShowErr("Data array was supposed to be "+Convert.ToString(iStride*iHeight)+"bytes for "+Convert.ToString(iWidth)+"x"+Convert.ToString(iHeight)+"x"+Convert.ToString(self.iBitDepth)+" but is "+Convert.ToString(self.iBytesBuffer)+"bytesnot ","saving targa","")
                        iLineOffset-=iStride


                else:
                    for (int iLine=0; iLine<self.iHeight; iLine++)
                        streamOut.Write(arrbyData,iLineOffset,iStride)
                        iLineOffset+=iStride


                #for (int iNow=0; iNow<iBytesBuffer; iNow++)                #	streamOut.Write(arrbyData[iNow])
                #
                if streamOut.BaseStream_Position()-iPlacePrev != iBytesAsUncompressed:
                    bGood=False
                    sMsg="Not all "+Convert.ToString(iBytesBuffer)+" uncompressed image data bytes were saveable. {streamOut.BaseStream_Position()-iPlacePrev:"+Convert.ToString((int)(streamOut.BaseStream_Position()-iPlacePrev))+"}"


            else:
                bGood=False
                sMsg="Targa.Save error: can't find any data to save."


        else:
            bGood=False
            sMsg="Targa.Save error: bad header wanted "+Convert.ToString(iBytesBuffer)+" bytes of data"

        #remember to flip
        footer.WriteTo(streamOut)
        #if not streamOut.Save():        #	bGood=False
        #	sMsg="Targa.Save couldn't write file."
        #
        if not bGood:
            PReporting.ShowErr(sMsg,"","Targa.Save")

        streamOut.Close()

    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"Targa.Save")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","Targa.Save")

    Console.Error.WriteLine( (bGood?"OK":"FAILED")+Convert.ToString(" (Targa.Save)") )
    return bGood
}#end Save

def Load(self, sFileNow):
    PReporting.setParticiple("before initialization")
    static bool bFirstRun=True
    if bFirstRun) Console.Error.Write("Targa.Load...":
    sFile=sFileNow
    bool bGood=True
    PReporting.setParticiple("opening file")
    BinaryReader streamIn(File.Open(sFile,FileMode.OpenRead),True)
    try
        PReporting.setParticiple("reading targa header")
        if bFirstRun) Console.Error.Write("calling BinaryReader {sFile:"+sFileNow+"; mode:\""+FileMode.OpenRead+"\" }...":
        #streamIn.OpenRead(sFile)
        ushort wNow=0
        byte byNow=0
        __int64 iPlacePrev=0
        uint u32Test=0
        #(byte)(length of id)
        iPlacePrev=(int)streamIn.BaseStream_Position()
        if bFirstRun) Console.Error.Write("reading at["+Convert.ToString((__int64)streamIn.BaseStream_Position())+"]{":
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "idLen:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        uint u32IDLenNow=(uint)byNow
        #(byte)(int)MapType
        iPlacePrev=(int)streamIn.BaseStream_Position()
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "MapType:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        MapType=(int)byNow
        #(byte)(int)TypeTarga
        iPlacePrev=streamIn.BaseStream_Position()
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "TypeTarga:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        TypeTarga=(int)byNow
        #(ushort)iMapOrigin
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "iMapOrigin:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : ("missing; streamIn.BaseStream.Position-iPlacePrev:"+Convert.ToString((int)(streamIn.BaseStream_Position()-iPlacePrev))+"; iPlacePrev:"+Convert.ToString(iPlacePrev)+"; streamIn.BaseStream.Position:"+Convert.ToString(streamIn.BaseStream_Position())+"; ") )  :
        iMapOrigin=(int)wNow
        #(ushort)iMapLength
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "iMapLength:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : ("missing; streamIn.BaseStream.Position-iPlacePrev:"+Convert.ToString((int)(streamIn.BaseStream_Position()-iPlacePrev))+"; iPlacePrev:"+Convert.ToString(iPlacePrev)+"; streamIn.BaseStream.Position:"+Convert.ToString(streamIn.BaseStream_Position())+"; ") )  :
        iMapLength=(int)wNow
        #(byte)iMapBitDepth
        iPlacePrev=streamIn.BaseStream_Position()
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "iMapBitDepth:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        iMapBitDepth=(int)byNow
        #(ushort)xImageLeft
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "ImageLeft:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : "missing; " )  :
        xImageLeft=(int)wNow
        #(ushort)yImageBottom
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "ImageBottom:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : "missing; " )  :
        yImageBottom=(int)wNow
        #(ushort)iWidth
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "iWidth:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : "missing; " )  :
        iWidth=(int)wNow
        #(ushort)iHeight
        iPlacePrev=streamIn.BaseStream_Position()
        wNow=streamIn.ReadUInt16();#streamIn.Read(wNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 2) bGood=False
        if bFirstRun) Console.Error.Write(  "iHeight:"  +  (  bGood ? (Convert.ToString((int)wNow)+"; ") : "missing; " )  :
        iHeight=(int)wNow
        #(byte)iBitDepth
        iPlacePrev=streamIn.BaseStream_Position()
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "iBitDepth:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        iBitDepth=(int)byNow
        iBytesPP=iBitDepth/8

        #(byte)bitsDescriptor
        iPlacePrev=streamIn.BaseStream_Position()
        byNow=streamIn.ReadByte();#streamIn.Read(byNow)
        if (streamIn.BaseStream_Position()-iPlacePrev != 1) bGood=False
        if bFirstRun) Console.Error.Write(  "(AttributeBitsSum:"  +  (  bGood ? (Convert.ToString((int)byNow)+"; ") : "missing; " )  :
        bitsDescriptor=byNow
        #(byte[length of id])sID
        if u32IDLenNow>0:
            iPlacePrev=streamIn.BaseStream_Position()
            sID=streamIn.ReadChars_octects(u32IDLenNow)
            if (sID.length()!=u32IDLenNow) bGood=False;#if (not streamIn.ReadAscii(sID,u32IDLenNow,u32Test)) bGood=False
            if bFirstRun) Console.Error.Write(  "id:"  +  (  bGood ? (sID+"; ") : "missing; " )  :
            if (u32Test!=u32IDLenNow) bGood=False

        else sID=""

        #MUST init with True option BEFORE loading map since True option deletes map
        Init(iWidth,iHeight,iBytesPP,True); #DOES DeriveVars, buffer; True deletes map; DeriveVars() DOES set iBytesPP, iStride, iBytesAsUncompressed

        #(byte[iMapLength])(arrbyColorMap)
        if bFirstRun) Console.Error.Write("map:":
        if iMapLength>0:
            arrbyColorMap=(byte*)malloc(iMapLength)
            iPlacePrev=streamIn.BaseStream_Position()
            for (int iNow=0; iNow<iMapLength; iNow++)
                arrbyColorMap[iNow]=streamIn.ReadByte();#streamIn.Read(arrbyColorMap[iNow])

            if streamIn.BaseStream_Position()-iPlacePrev != iMapLength:
                PReporting.ShowErr("Not all "+Convert.ToString(iMapLength)+" color map bytes were found.","reading palette","Targa.Load")
                if bFirstRun) Console.Error.Write("only "+Convert.ToString(streamIn.BaseStream_Position()-iPlacePrev)+"not ; ":
                bGood=False

            else:
                if bFirstRun) Console.Error.Write("good; ":


        else:
            PMemory.SafeFree(arrbyColorMap)
            if bFirstRun) Console.Error.Write("none; ":

        #(byte[iWidth*iHeight*iBytesPP])(arrbyData)
        #iBytesBuffer=streamIn.BytesLeftUsed()
        #TODO: iBytesBuffer=#finish thisnot  Count compressed area, by output size, load rest into footer!
        #if (iBytesAsUncompressed<iBytesBuffer) iBytesBuffer=iBytesAsUncompressed
        if bFirstRun) Console.Error.Write("buffer:"+Convert.ToString(iBytesBuffer)+"; ":
        int iFound=0

        if iBytesBuffer<=0:
            bGood=False
            PReporting.ShowErr("Only "+Convert.ToString(iBytesBuffer)+" were expected given self file's header","","Targa.Load")


        PReporting.setParticiple("reading targa image data area")
        if bGood:
            #the following is ONLY OK SINCE called Init above
            if bFirstRun) Console.Error.Write("( ":
            if IsCompressed():
                if bFirstRun) Console.Error.Write("compression found...":
                #int iStart=streamIn.BaseStream_Position()
                #iBytesBuffer=RLESizeUncompressed(streamIn.arrbyData,iStart,iBytesLeft,iBytesPP)
                PMemory.SafeFree(arrbyData)
                int iGot=0
                int iPrevPos
                unsigned int uiBufferSizeTemp=0
                unsigned int uiBufferSizeUsed=0
                byte byNow

                do
                    iPrevPos=(int)streamIn.BaseStream_Position()
                    byNow=streamIn.ReadByte()
#TODO: uncompress NOW, after buffer is filled, remaining bytes into footer -- FINISH THIS asdf
                    iGot=(int)streamIn.BaseStream_Position()-iPrevPos
                    if iGot>0:
                        PMemory.Push(arrbyData,uiBufferSizeTemp,uiBufferSizeUsed,byNow)
                        iFound+=iGot


                while (iGot>0)
                PMemory.Redim(arrbyData,uiBufferSizeTemp,uiBufferSizeUsed);#frees if size<=0
                #arrbyData=(byte*)malloc(iBytesBuffer)


                #int iPosPrev=streamIn.BaseStream_Position()
                #for (int iNow=0; iNow<iBytesBuffer; iNow++)                #	arrbyData[iNow]=streamIn.arrbyData[iStart+iNow]
                #	iFound++
                #
                #int iGot=(int)((int)streamIn.BaseStream_Position()-iPosPrev)
                #int iGot=streamIn.Read_octets((unsigned char*)self.arrbyData,0,iBytesBuffer)
                #if iGot!=iBytesBuffer:                #	bGood=False
                #	PReporting.ShowErr("Expected "+Convert.ToString(iBytesBuffer)+" compressed bytes but found "+Convert.ToString(iGot)+"...","","Targa.Load")
                #
                #iFound+=iGot
                #streamIn.Advance(iFound)

            else  #else uncompressed
                iBytesBuffer=iBytesAsUncompressed
                if self.arrbyData!=NULL:
                    free(self.arrbyData)
                    self.arrbyData=NULL

                self.arrbyData=(byte*)malloc(iBytesBuffer)
                if bFirstRun) Console.Error.Write("no compression...":
                int iTest=SafeCopyFrom(iWidth,iHeight,iBytesPP,streamIn,False);#int iTest=SafeCopyFrom(iWidth,iHeight,iBytesPP,streamIn.arrbyData,streamIn.Length(),streamIn.BaseStream_Position(),False)

                if iTest!=iBytesBuffer:
                    bGood=False
                    PReporting.ShowErr("Expected "+Convert.ToString(iBytesBuffer)+" but found "+Convert.ToString(iTest)+"...","","Targa.Load")

                #streamIn.Advance(iTest)

            if bFirstRun) Console.Error.Write(" )...":

        if bGoodandIsSavedAsFlipped():
            if IsCompressed():
                if not SetCompressionRLE(False):
                    bGood=False
                    PReporting.ShowErr("Failed to uncompress for flipnot ","","Targa.Load")

                if not Flip():
                    bGood=False
                    PReporting.ShowErr("Failed to uncompress for flipnot ","","Targa.Load")

                if not SetCompressionRLE(True):
                    bGood=False
                    PReporting.ShowErr("Failed to recompress after flipnot ","","Targa.Load")


            else:
                if not Flip():
                    bGood=False
                    PReporting.ShowErr("Failed to flip targanot ","","Targa.Load")

                elif bFirstRun:
                    Console.Error.Write("Flip():success...")



        if bFirstRun) Console.Error.Write("footer:":
        #if streamIn.BytesLeftUsed()>0:        footer.Init(streamIn)
        if bFirstRun) Console.Error.Write(Convert.ToString(footer.ByteCount())+"; ":
        #
        if bFirstRun) Console.Error.Write("} ":
        if bFirstRun) Console.Error.Write(bGood?"Targa.Load Success--dump":"Targa.Load Done with errors--dump":
        if bFirstRun) Console.Error.Write(Dump():
        if not bGood:
            Console.Error.WriteLine("FAILED (Targa.Load)")

        streamIn.Close()

    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"","Targa.Load")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","Targa.Load")

    bFirstRun=False
    return bGood
}#end Targa.Load

def IsOK(self):
    bool bGood=(iWidth>0 and iHeight>0 and iBytesPP>0 and arrbyData!=null)
    if not IsCompressed():
        if iBytesBuffer!=(iWidth*iHeight*iBytesPP):
            bGood=False
            cerr<<"Targa.IsOK Error: buffer of uncompressed image is not expected length based on dimensions and color depth"<<endl

        if iBytesBuffer!=iBytesAsUncompressed:
            bGood=False
            cerr<<"Targa.IsOK Error: buffer of uncompressed image is not size of buffer"<<endl


    return bGood

def Flip(self):
    bool bGood=True
    if not IsOK():
        bGood=False
        PReporting.ShowErr("Targa is corrupt or did not load properly (IsOK() returned False)not ","","Targa.Flip")

    if bGoodandIsCompressed():
        bGood=False
        PReporting.ShowErr("Targa is still compressed and cannot be flipped before uncompressednot ","","Targa.Flip")

    if bGood:
        try
            byte* arrbyTemp=(byte*)malloc(iBytesBuffer)
            int xSrc=0, ySrc=iHeight-1, xDest, yDest
            for (yDest=0; yDest<iHeight; yDest++, ySrc--)
                xSrc=0
                for (xDest=0; xDest<iWidth; xDest++, xSrc++)
                    for (int iChan=0; iChan<iBytesPP; iChan++)
                        arrbyTemp[yDest * iStride + xDest * iBytesPP + iChan]=
                            arrbyData[ySrc  * iStride + xSrc  * iBytesPP + iChan]



            PMemory.SafeFree(arrbyData)
            arrbyData=arrbyTemp

        catch (exception& exn)
            bGood=False
            PReporting.ShowExn(exn,"Targa.Flip")

        catch (...)
            bGood=False
            PReporting.ShowUnknownExn("","Targa.Flip")


    return bGood

def HasAttrib(self, bit):
    return ( (bitsDescriptor&bit) != 0 )

def IsSavedAsFlipped(self):
    return not ( (yImageBottom!=0)or(HasAttrib(bitNoFlip_NonTruevision)) )

def IsCompressed(self):
    return (TypeTarga==TypeCompressedColorMapped
            orTypeTarga==TypeCompressedTrueColor
            orTypeTarga==TypeCompressedGrayscale
            orTypeTarga==TypeCompressedColorMappedHuffmanAndDeltaAndRLE
            orTypeTarga==TypeCompressedColorMappedHuffmanAndDeltaAndRLE4PassQuadTree)

def SetCompressionRLE(self, bOn):
    bool bGood=True
    try
        if iWidth*iHeight*iBytesPP<=0:
            PReporting.ShowErr("Tried to turn compression "+Convert.ToString(bOn?"on":"off")+" for "+Convert.ToString(iWidth)+Convert.ToString("x")+Convert.ToString(iHeight)+Convert.ToString("x")+Convert.ToString(iBytesPP)+Convert.ToString(" imagenot "),"","Targa.SetCompressionRLE("+Convert.ToString(bOn)+")")

        elif iBytesBuffer<=0:
            PReporting.ShowErr("Tried to turn compression "+Convert.ToString(bOn?"on":"off")+" for "+Convert.ToString(iBytesBuffer)+"-buffer "+Convert.ToString(BytesAsUncompressed())+"-length imagenot ","","Targa.SetCompressionRLE("+Convert.ToString(bOn)+")")

        else:
            if bOn:
                if (not IsCompressed())   #Compress
                    byte* arrbyCompressed=RLECompress(iBytesBuffer, arrbyData, 0, iBytesBuffer, iBytesPP)
                    PMemory.SafeFree(arrbyData)
                    arrbyData=arrbyCompressed


            else:
                if (IsCompressed())   #Uncompress
                    int iNewSize=iWidth*iHeight*iBytesPP
                    byte* arrbyUncompressed=(byte*)malloc(iNewSize); #byte* arrbyUncompress=RLEUncompress(iBytesBuffer, arrbyData, 0, iBytesBuffer, iBytesPP)
                    int iTest=RLEUncompress(arrbyUncompressed, iNewSize, arrbyData, iBytesBuffer, iBytesPP)
                    if iTest!=iNewSize:
                        PReporting.ShowErr("Uncompressed "+Convert.ToString(iTest)+" bytes but expected "+Convert.ToString(iNewSize)+" ("+Convert.ToString(iWidth)+"x"+Convert.ToString(iHeight)+" at "+Convert.ToString(iBytesPP*8)+"bpp ["+Convert.ToString(iBytesPP)+" bytes per pixel])","","Targa.SetCompressionRLE("+Convert.ToString(bOn)+")")

                    PMemory.SafeFree(arrbyData)
                    arrbyData=arrbyUncompressed
                    iBytesBuffer=iNewSize




    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"Targa.SetCompressionRLE("+Convert.ToString(bOn)+")")

    catch (...)
        bGood=False
        PReporting.ShowUnknownExn("","Targa.SetCompressionRLE("+Convert.ToString(bOn)+")")

    return bGood
}#end SetCompressionRLE
def Dump(self):
    return Dump(False)

def Dump(self, bDumpFull):
    string sReturn="{"
    sReturn+="dimensions:"+Convert.ToString(iWidth)
             +"x"+Convert.ToString(iHeight)
             +"x"+Convert.ToString(iBytesPP)+"; "
    sReturn+=" buffer:"+Convert.ToString(((arrbyData==null)?"null":"ok"))+"; "
    sReturn+=" BytesAsUncompressed:"+Convert.ToString(iBytesAsUncompressed)+"; "
    sReturn+=" BufferSize:"+Convert.ToString(iBytesBuffer)+"; "
    if bDumpFull:
        #do some stuff here maybe later

    sReturn+="}"
    return sReturn

def Description(self):
    return Description(False)

def Description(self, bVerbose):
    if (bVerbose) return Convert.ToString((arrbyData==null)?"null":"")+Convert.ToString(iWidth)+"x"+Convert.ToString(iHeight)+"x"+Convert.ToString(iBytesPP*8)+" "+Convert.ToString(iBytesAsUncompressed)+"-length "+Convert.ToString(iBytesBuffer)+"-buffer"
    else return Convert.ToString((arrbyData==null)?"null":"")+Convert.ToString(iWidth)+"x"+Convert.ToString(iHeight)+"x"+Convert.ToString(iBytesPP*8)

#private methods:
def DeriveVars(self):
    iBytesPP=iBitDepth/8
    iStride=iWidth*iBytesPP
    iBytesAsUncompressed=iStride*iHeight
    if iBytesPP==4:
        self.bitsDescriptor &= 0xF0; #set nibble to zero first to clear the bits
        self.bitsDescriptor |= 0x0F; #setting low nibble to 8 says 8 bits are alpha


def InitNull(self):
    #bySizeofID=0 (size of sID)
    MapType=0
    TypeTarga=0
    iMapOrigin=0
    iMapLength=0
    iMapBitDepth=0
    xImageLeft=0
    yImageBottom=0
    iWidth=0
    iHeight=0
    iBitDepth=0
    bitsDescriptor=0
    sID=""
    arrbyColorMap=null
    arrbyData=null
    DeriveVars()
    iBytesBuffer=iBytesAsUncompressed

def MarkAsCompressed(self, bAsCompressed):
    bool bGood=False
    if bAsCompressed:
        if TypeTarga==TypeUncompressedColorMapped:
            TypeTarga=TypeCompressedColorMapped
            bGood=True

        elif TypeTarga==TypeUncompressedTrueColor:
            TypeTarga=TypeCompressedTrueColor
            bGood=True

        elif TypeTarga==TypeUncompressedGrayscale:
            TypeTarga=TypeCompressedGrayscale
            bGood=True


    else:
        if TypeTarga==TypeCompressedColorMapped:
            TypeTarga=TypeUncompressedColorMapped
            bGood=True

        elif TypeTarga==TypeCompressedTrueColor:
            TypeTarga=TypeUncompressedTrueColor
            bGood=True

        elif TypeTarga==TypeCompressedGrayscale:
            TypeTarga=TypeUncompressedGrayscale
            bGood=True

        elif TypeTarga==TypeCompressedColorMappedHuffmanAndDeltaAndRLE:
            TypeTarga=TypeUncompressedColorMapped
            bGood=True

        elif TypeTarga==TypeCompressedColorMappedHuffmanAndDeltaAndRLE4PassQuadTree:
            TypeTarga=TypeUncompressedColorMapped
            bGood=True


    return bGood

def Reflect(self, x, y):
    if (x<0) x*=-1; #since reflecting instead of wrapping
    elif (x>=iWidth) x=(iWidth-1)-(x-iWidth); #e.g. x=801 and width 800 results in 799-1; e.g. 800 results in 799
    while (x<0) x+=iWidth; #handled same in either case above

    if (y<0) y*=-1; #since reflecting instead of wrapping
    elif y>=iHeight) y=(iHeight-1)-(x-iHeight:
    while (y<0) y+=iHeight

def Wrap(self, x, y):
    while (x>=iWidth) x-=iWidth
    while (x<0) x+=iWidth
    while (y>=iHeight) y-=iHeight
    while (y<0) y+=iHeight

def getChannel_Fast(self, x, y, iChan):
    if (iChan<=iBytesPP) iChan=iBytesPP-1
    int iAt=y*iStride+x*iBytesPP+iChan
    if self.arrbyData!=null:
        if (iAt<iBytesBuffer) return arrbyData[iAt]

    return 0

def getChannelReflected(self, x, y, iChan):
    Reflect(x,y)
    if (iChan<=iBytesPP) iChan=iBytesPP-1
    int iAt=y*iStride+x*iBytesPP+iChan
    if self.arrbyData!=null:
        if (iAt<iBytesBuffer) return arrbyData[iAt]

    return 0

def getColorRgbReflected(self, R, G, B, x, y):
    Reflect(x,y)
    getColorRgb_Fast(R, G, B, x, y)

def getColorArgbReflected(self, A, R, G, B, x, y):
    Reflect(x,y)
    getColorArgb_Fast(A, R, G, B, x, y)

def getColorRgb_Fast(self, R, G, B, x, y):
    #if  (self.arrbyData!=null) and (self.BytesBuffer>=self.BytesAsUncompressed) :    byte* lpData=&self.arrbyData[y*iStride+x*iBytesPP]
    if self.iMapLength>0:
        int iMapByteDepth=self.iMapBitDepth/8
        byte* lpInPalette=&self.arrbyColorMap[*lpData*iMapByteDepth]
        B=*lpInPalette
        lpInPalette++
        G=*lpInPalette
        lpInPalette++
        R=*lpInPalette

    else  #else no colormap
        B=*lpData
        if iBytesPP>1:
            lpData++
            G=*lpData
            lpData++
            R=*lpData

        else:
            G=*lpData
            R=*lpData

    }#end else does not have palette
    #}#end if any image data
}#end getColorRgb_Fast
def getColorArgb_Fast(self, A, R, G, B, x, y):
    #if  (self.arrbyData!=null) and (self.BytesBuffer>=self.BytesAsUncompressed) :    byte* lpData=&self.arrbyData[y*iStride+x*iBytesPP]
    if self.iMapLength>0:
        int iMapByteDepth=self.iMapBitDepth/8
        byte* lpInPalette=&self.arrbyColorMap[*lpData*iMapByteDepth]
        B=*lpInPalette
        lpInPalette++
        G=*lpInPalette
        lpInPalette++
        R=*lpInPalette
        if iMapByteDepth>3:
            lpInPalette++
            A=*lpInPalette

        else A=255

    else  #else no colormap
        B=*lpData
        if iBytesPP>1:
            lpData++
            G=*lpData
            lpData++
            R=*lpData
            if iBytesPP>3:
                lpData++
                A=*lpData

            else A=255

        else:
            G=*lpData
            R=*lpData
            A=*lpData

    }#end else does not have palette
    #}#end if any image data
}#end getColorArgb_Fast
}#end namespace

#endif
