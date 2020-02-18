#ifndef TARGA_CPP
#define TARGA_CPP

#include <iostream>
#include <iomanip>
#include <fstream>
#include <memory>
#include "targa.h"
#include <sstream> #stringstream etc

#NOTE: compression/decompression is NOT yet tested and probably doesn't work right.  If your program locks up you'll need to fix it yourself or else use an uncompressed Targa file.

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
        cerr<<"Compare could not finish: "<<exn.what()<<endl

    catch (...)
        cerr<<"Compare could not finish: unknown exception"<<endl

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
                cerr<<"RLECompress Error: Compressed total of "<<iTotal<<" wasn't calculated correctly"<<endl


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
        cerr<<"RLECompress could not finish: "<<exn.what()<<endl

    catch (...)
        cerr<<"RLECompress could not finish: unknown exception"<<endl

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
                                cerr<<"RLEUncompress Error: Compressed data wanted destination bigger than "<<iDestSizeIrrelevantIfCountOnlyIsTrue<<" bytes."<<endl
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
        cerr<<"RLEUncompress could not finish: "<<exn.what()<<endl

    catch (...)
        cerr<<"RLEUncompress could not finish: unknown exception"<<endl

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
    u32SizeofDump=0

TargaFooter.~TargaFooter()
    if dump!=null:
        free(dump)
        dump=null


def Init(self, arrbyDataSrcToCopyFrom, u32SrcStart, u32Count, u32ActualSourceBufferSize):
    bool bGood=True
    if dump!=null:
        free(dump)
        dump=null

    try
        u32SizeofDump=u32Count
        dump=(byte*)malloc(u32Count)
        uint iSrc=u32SrcStart
        for (uint iNow=0; iNow<u32Count and iSrc<u32ActualSourceBufferSize; iNow++,iSrc++)
            dump[iNow]=arrbyDataSrcToCopyFrom[iSrc]


    catch (exception& exn)
        cerr<<"TargaFooter.Init could not finish: "<<exn.what()<<endl
        bGood=False

    catch (...)
        cerr<<"TargaFooter.Init could not finish: unknown exception"<<endl
        bGood=False

    return bGood

def Init(self, lpbyDataPointerToKeep, u32Size):
    bool bGood=True
    try
        if u32Size>0 and lpbyDataPointerToKeep!=null:
            u32SizeofDump=u32Size
            dump=lpbyDataPointerToKeep
            #TODO: process the footer here

        else:
            u32SizeofDump=0
            dump=null


    catch (exception& exn)
        cerr<<"TargaFooter.Init could not finish ("<<exn.what()<<"): u32Size="<<u32Size<<"; lpbyDataPointerToKeep is"<<((lpbyDataPointerToKeep==null)?"null.":"not null.")<<endl
        bGood=False

    catch (...)
        cerr<<"TargaFooter.Init could not finish (unknown exception): u32Size="<<u32Size<<"; lpbyDataPointerToKeep is"<<((lpbyDataPointerToKeep==null)?"null.":"not null.")<<endl
        bGood=False

    return bGood

def Init(self):
    return Init(null,0)

def Init(self, fileNowToReadToEnd):
    bool bGood=True
    size_t iGot=0
    size_t iMax=1024000
    char* byarrTemp=(char*)malloc(iMax);#debug theoretical maximum
    char byNow=0
    size_t iTotal=0
    do
        iGot=fread(&byNow,1,1,fileNowToReadToEnd)
        iTotal+=iGot
        if iTotal>iMax:
            cerr<<"TargaFooter.Init(FILE*) Error: got more than "<<iMax<<"bytes in Targa footer--skipping remaining bytesnot "<<endl
            bGood=False
            break

        else byarrTemp[iTotal-1]=byNow

    while (iGot>0)
    if iTotal>0:
        self.dump=(byte*)malloc(iTotal)
        for (size_t iByte=0; iByte<iTotal; iByte++)
            self.dump[iByte]=byarrTemp[iByte]


    else self.dump=NULL
    self.u32SizeofDump=(unsigned int)iTotal
    free(byarrTemp)
    return bGood
}#end Init
def WriteTo(self, pfileAlreadyOpen_ToNotCloseInThisMethod):
    size_t iGot=fwrite(dump, 1, u32SizeofDump, pfileAlreadyOpen_ToNotCloseInThisMethod)
    return iGot

#/<summary>
#/Returns negative or 0 if not all written
#/</summary>
def WriteTo(self, byarrDest, iAtDest, iSizeOfDest):
    int iWritten=0
    for (uint iNow=0; iNow<u32SizeofDump; iNow++)
        if iAtDest+(int)iNow>=iSizeOfDest:
            iWritten*=-1
            break

        byarrDest[iAtDest+iNow]=dump[iNow]
        iWritten++

    return iWritten
}#end WriteTo byter
def ByteCount(self):
    return u32SizeofDump

##endregion TargaFooter methods

##region Targa methods
Targa.Targa()
    InitNull()

Targa.~Targa()
    if arrbyData!=null:
        free(arrbyData)
        arrbyData=null


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
        if arrbyColorMap!=null:
            free(arrbyColorMap)
            arrbyColorMap=null

        iMapLength=0
        sID=""
        if arrbyData!=null:
            free(arrbyData)
            arrbyData=null


    iWidth=iSetWidth
    iHeight=iSetHeight
    iBitDepth=iSetBytesPP*8
    DeriveVars();#does get iBytesPP
    #if (iSetBytesPP==4 or iSetBytesPP==3) TypeTarga=TypeUncompressedTrueColor
    #elif (iSetBytesPP==1) TypeTarga=TypeUncompressedGrayscale
    iBytesBuffer=iBytesAsUncompressed
    if iBytesBuffer<=0:
        cerr<<"Targa.Init Error: iBytesBuffer="<<iBytesBuffer<<"not "<<endl
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


        else cerr<<"Targa CopyTo Warning: Program tried to duplicate null targa."<<endl
        if iMapLength>0:
            targaDest.arrbyColorMap=(byte*)malloc(iMapLength); #array of [] bytes  #[byMapBitDepth*wMapLength] -- the palette
            for (iNow=0; iNow<iMapLength; iNow++)
                targaDest.arrbyColorMap[iNow]=arrbyColorMap[iNow]


        bGood=True

    catch (exception& exn)
        cerr<<"Targa CopyTo could not finish: "<<exn.what()
        bGood=False

    catch (...)
        cerr<<"Targa CopyTo could not finish (Unknown exception)."<<endl
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
                                        cerr<<"DrawFast (same bit depth, uncompressing) Error: Compressed data wanted destination bigger than "<<iDestSize<<" bytes."<<endl
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
                    cerr<<"DrawFast (same bit depth, uncompressing) could not finish: "<<exn.what()<<endl

                catch (...)
                    cerr<<"DrawFast (same bit depth, uncompressing) could not finish (unknown exception)."<<endl

            }#end if compressed
            else  #else uncompressed already
                for (int ySrc=0; ySrc<iHeight; ySrc++,yDest++,iSrcByteLineStart+=iStride,iDestByteLineStart+=iDestStride)
                    iDestByteNow=iDestByteLineStart;#xDest=xAtDest
                    memcpy(&arrbyDest[iDestByteNow],&arrbyData[iSrcByteLineStart],iStrideLimited)
                    #for (iSrcByteNow=iSrcByteLineStart; iSrcByteNow<iLineEnder; iSrcByteNow++, iDestByteNow++) { #for (int xSrc=0; xSrc<iWidth; xSrc++,xDest++)                    #	arrbyDest[iDestByteNow]=arrbyData[iSrcByteNow]
                    #



        else  #else dissimilar bitdepths
            if IsCompressed():
                cerr<<"Targa.DrawFast Error: Not implemented: Can't copy from compressed targa of dissimilar bit depth"<<endl

            else:
                for (int ySrc=0; ySrc<iHeight; ySrc++,yDest++,iSrcByteLineStart+=iStride,iDestByteLineStart+=iDestStride)
                    iDestByteNow=iDestByteLineStart;#xDest=xAtDest
                    memcpy(&arrbyDest[iDestByteNow],&arrbyData[iSrcByteLineStart],iStrideLimited)
                    #for (iSrcByteNow=iSrcByteLineStart; iSrcByteNow<iLineEnder; iSrcByteNow++, iDestByteNow++) { #for (int xSrc=0; xSrc<iWidth; xSrc++,xDest++)                    #	arrbyDest[iDestByteNow]=arrbyData[iSrcByteNow]
                    #




    catch (exception& exn)
        cerr<<"Targa.DrawFast could not finish: "<<exn.what()<<endl
        bGood=False

    catch (...)
        cerr<<"Targa.DrawFast could not finish (Unknown exception)."<<endl
        bGood=False

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
                cerr<<"Targa.From could not finish:"<<exn.what()<<endl

            catch (...)
                bGood=False
                cerr<<"Targa.From could not finish (Unknown exception)."<<endl



    else:
        cerr<<"Targa.From Error: couldn't initialize."<<endl

    return bGood
}#end From a source buffer
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen):
    return SafeCopyFrom(iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, True)

def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, bReInitializeAll):
    return SafeCopyFrom(iWidthTo,iHeightTo,iBytesPP,arrbySrc,u32SrcRealLen,0,bReInitializeAll)

#SafeCopyFrom(iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll)
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, fileNow, bReInitializeAll):
    int iFound=0
    bool bGood=True
    static bool bFirstRun=True
    if bFirstRun:
        cerr<<"Targa.SafeCopyFrom..."<<"(w="<<(iWidthTo)<<",h="<<(iHeightTo)<<",BytesPP="<<(iBytesPP)<<","<<(fileNow==null?"fileNow=null":"fileNow=ok")<<",bReInitializeAll="<<(bReInitializeAll?"True":"False")<<")"<<flush

    static bool bFirstFatalSafeCopyFrom=True
    if fileNow==null:
        cerr<<"Targa.SafeCopyFrom Error: Null imagenot  Forcing reinitialize"
        if bFirstFatalSafeCopyFrom:
            cerr<<endl
            cerr<<endl
            cerr<<"IMAGE BUFFER IS NULLnot !not !not !not !not !not !not !not !not !not !not !not !not !not !not !not "<<endl
            cerr<<endl
            bFirstFatalSafeCopyFrom=False

        bReInitializeAll=True

    if bReInitializeAll:
        if not Init(iWidthTo,iHeightTo,iBytesPP,True):
            bGood=False
            cerr<<"Targa.SafeCopyFrom Error: couldn't reinit."<<endl


    if bGood:
        if fileNow==null:
            bGood=False
            cerr<<"Targa.SafeCopyFrom Error: null source filenot "<<endl


    if bGood:
        try
            int iSrcAbs=0;#(int)u32SrcStart
            int iLen=iWidthTo*iHeightTo*iBytesPP
            #int iSrcRealLen=(int)u32SrcRealLen
            int iNow=0
            iFound=(int)fread(arrbyData,1,iLen,fileNow)
            #for (iNow=0; iNow<iLen and iSrcAbs<iSrcRealLen; iNow++, iSrcAbs++)            #	arrbyData[iNow]=arrbySrc[iSrcAbs]
            #	iFound++
            #
            if iNow<iLen)  #ok since iNow is now a length (since increments past end then exits loop:
                bGood=False
                cerr<<"Targa.SafeCopyFrom Error: "<<"Only"<<(iNow)<<" of "<<(iLen)<<" expected bytes of image data were found in file."<<endl


        catch (exception& exn)
            bGood=False
            cerr<<"Targa.SafeCopyFrom could not finish: "<<exn.what()<<endl

        catch (...)
            bGood=False
            cerr<<"Targa.SafeCopyFrom could not finish (Unknown exception)."<<endl

        if bFirstRun:
            if (bGood) cerr<<"Targa.SafeCopyFrom Success..."<<endl
            else cerr<<"Targa.SafeCopyFrom finished with errors..."<<endl


    bFirstRun=False
    return iFound
}#end SafeCopyFrom source buffer
#int Targa.SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, fileNow, bReInitializeAll)
def SafeCopyFrom(self, iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll):
    int iFound=0
    bool bGood=True
    static bool bFirstRun=True
    if bFirstRun:
        cerr<<"Targa.SafeCopyFrom..."<<"(w="<<(iWidthTo)<<",h="<<(iHeightTo)<<",BytesPP="<<(iBytesPP)<<","<<(arrbySrc==null?"src=null":"src=ok")<<",len="<<(u32SrcRealLen)<<",start="<<(u32SrcStart)<<",bReInitializeAll="<<(bReInitializeAll?"True":"False")<<")"<<flush

    static bool bFirstFatalSafeCopyFrom=True
    if arrbyData==null:
        cerr<<"Targa.SafeCopyFrom Error: Null imagenot  Forcing reinitialize"
        if bFirstFatalSafeCopyFrom:
            cerr<<endl
            cerr<<endl
            cerr<<"IMAGE BUFFER IS NULLnot !not !not !not !not !not !not !not !not !not !not !not !not !not !not !not "<<endl
            cerr<<endl
            bFirstFatalSafeCopyFrom=False

        bReInitializeAll=True

    if bReInitializeAll:
        if not Init(iWidthTo,iHeightTo,iBytesPP,True):
            bGood=False
            cerr<<"Targa.SafeCopyFrom Error: couldn't reinit."<<endl


    if bGood:
        if arrbySrc==null:
            bGood=False
            cerr<<"Targa.SafeCopyFrom Error: null sourcenot "<<endl


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
                cerr<<"Targa.SafeCopyFrom Error: "<<"Only"<<(iNow)<<" of "<<(iLen)<<" expected bytes of image data were found in file."


        catch (exception& exn)
            bGood=False
            cerr<<"Targa.SafeCopyFrom could not finish: "<<exn.what()<<endl

        catch (...)
            bGood=False
            cerr<<"Targa.SafeCopyFrom could not finish (Unknown exception)."<<endl

        if bFirstRun:
            if (bGood) cerr<<"Targa.SafeCopyFrom Success..."<<endl
            else cerr<<"Targa.SafeCopyFrom finished with errors..."<<endl


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
    try
        FILE* pfileOut=NULL
        #cerr<<"WRITING FILE \"\" : "<<lpriffchunk.dwUsed<<"bytes"<<flush
        pfileOut = fopen ( sFile.c_str(), "wb" )
        #fwrite (lpriffchunk.buffer , 1 , lpriffchunk.dwUsed , pfileOut )
        #cerr<<"DONE"<<endl
        #bFirst=False
        ushort wNow=0
        byte byNow=0
        int iPlacePrev=0
        int iPlace=0
        uint u32Test=0
        #(byte)(length of id)
        iPlacePrev=iPlace
        if '''sID!=null and '''sID.length()>255) sID=sID.substr(0,255:
        uint u32IDLenNow=('''sID==null or '''sID=="")?0:(uint)sID.length()
        byNow=(byte)u32IDLenNow
        fwrite((void*)&byNow, 1, 1, pfileOut)
        byNow=(byte)MapType
        fwrite((void*)&byNow, 1, 1, pfileOut)
        byNow=(byte)TypeTarga
        fwrite((void*)&byNow, 1, 1, pfileOut)
        wNow=(ushort)iMapOrigin
        fwrite((void*)&wNow, 2, 1, pfileOut)
        wNow=(ushort)iMapLength
        fwrite((void*)&wNow, 2, 1, pfileOut)
        byNow=(byte)iMapBitDepth
        fwrite((void*)&byNow, 1, 1, pfileOut)
        wNow=(ushort)xImageLeft
        fwrite((void*)&wNow, 2, 1, pfileOut)
        wNow=(ushort)yImageBottom
        fwrite((void*)&wNow, 2, 1, pfileOut)
        wNow=(ushort)iWidth
        fwrite((void*)&wNow, 2, 1, pfileOut)
        wNow=(ushort)iHeight
        fwrite((void*)&wNow, 2, 1, pfileOut)
        byNow=(byte)iBitDepth
        fwrite((void*)&byNow, 1, 1, pfileOut)
        byNow=(byte)bitsDescriptor
        fwrite((void*)&byNow, 1, 1, pfileOut)
        if u32IDLenNow>0:
             char* carrID=sID.c_str()
            for (size_t iChar=0; iChar<sID.length(); iChar)
                byNow=(byte)carrID[iChar]
                fwrite((void*)&byNow, 1, 1, pfileOut)


        #(byte[iMapLength])(arrbyColorMap)
        if iMapLength>0:
            for (int iNow=0; iNow<iMapLength; iNow++)
                fwrite((void*)&arrbyColorMap[iNow], 1, 1, pfileOut)


        elif arrbyColorMap!=null:
            free(arrbyColorMap)
            arrbyColorMap=null

        #(byte[iWidth*iHeight*iBytesPP])(arrbyData)
        if iBytesBuffer>0:
            if arrbyData!=null:
                for (int iNow=0; iNow<iBytesBuffer; iNow++)
                    fwrite((void*)&arrbyData[iNow], 1, 1, pfileOut)


            else:
                bGood=False
                cerr<<"Targa.Save error: can't find any data to save."<<endl


        else:
            bGood=False
            cerr<<"Targa.Save error: bad header wanted "<<(iBytesBuffer)<<" bytes of data"<<endl

        footer.WriteTo(pfileOut)
        fclose(pfileOut)

    catch (exception& exn)
        bGood=False
        cerr<<"Targa.Save could not finish: "<<exn.what()<<endl

    catch (...)
        bGood=False
        cerr<<"Targa.Save could not finish (Unknown exception)."<<endl

    return bGood
}#end Save
def Load(self, sFileNow):
    static bool bFirstRun=True
    if (bFirstRun) cerr<<"Targa.Load..."
    sFile=sFileNow
    string sMsg="before initialization"
    bool bGood=True
    FILE* fileNow=null
    size_t iGot=0
    try
        if (bFirstRun) cerr<<"calling fopen..."<<flush
        fileNow=fopen(sFileNow.c_str(),"rb");#rb for read+binary (?)
        ushort wNow=0
        byte byNow=0
        int iPlacePrev=0
        uint u32Test=0
        #(byte)(length of id)

        if (bFirstRun) cerr<<"reading at["<<0<<"]{"<<flush
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"idLen:"  <<flush
            if (bGood) cerr<<(int)byNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        uint u32IDLenNow=(uint)byNow
        #(byte)(int)MapType
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"MapType:"  <<flush
            if (bGood) cerr<<(int)byNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        MapType=(int)byNow
        #(byte)(int)TypeTarga
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"TypeTarga:"<<flush
            if (bGood) cerr<<(int)byNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        TypeTarga=(int)byNow
        #(ushort)iMapOrigin
        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"iMapOrigin:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        iMapOrigin=(int)wNow
        #(ushort)iMapLength
        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"iMapLength:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        iMapLength=(int)wNow
        #(byte)iMapBitDepth
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"iMapBitDepth:"<<flush
            if (bGood) cerr<<(int)byNow<<"; "<<flush
            else cerr<<"missing; "<<flush

        iMapBitDepth=(int)byNow
        #(ushort)xImageLeft
        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"ImageLeft:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "
            else cerr<<"missing; "<<flush

        xImageLeft=(int)wNow
        #(ushort)yImageBottom

        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"ImageBottom:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "
            else cerr<<"missing; "<<flush

        yImageBottom=(int)wNow
        #(ushort)iWidth
        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"iWidth:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "
            else cerr<<"missing; "<<flush

        iWidth=(int)wNow
        #(ushort)iHeight

        iGot=fread((void*)&wNow,2,1,fileNow)
        if (iGot!=2) bGood=False
        if bFirstRun:
            cerr<<"iHeight:"<<flush
            if (bGood) cerr<<(int)wNow<<"; "
            else cerr<<"missing; "<<flush

        iHeight=(int)wNow
        #(byte)iBitDepth
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"iBitDepth:"<<flush
            if (bGood) cerr<<(int)byNow<<"; "
            else cerr<<"missing; "<<flush

        iBitDepth=(int)byNow
        iBytesPP=iBitDepth/8
        #(byte)bitsDescriptor
        iGot=fread((void*)&byNow,1,1,fileNow)
        if (iGot!=1) bGood=False
        if bFirstRun:
            cerr<<"AttributeBitsSum:"<<flush
            if (bGood) cerr<<(int)byNow<<"; "
            else cerr<<"missing; "<<flush

        bitsDescriptor=byNow
        #(byte[length of id])sID
        if u32IDLenNow>0:
            char* carrIn=(char*)malloc(u32IDLenNow+1)
            iGot=fread((void*)&carrIn,1,u32IDLenNow,fileNow)
            carrIn[u32IDLenNow]='\0'; #ok since size is u32IDLenNow+1
            sID=(string)carrIn
            free(carrIn)
            if (iGot!=u32IDLenNow) bGood=False
            if bFirstRun:
                cerr<<"id:"<<flush
                if (not bGood) cerr<<sID<<"; "<<flush
                else cerr<<"missing; "<<flush

            if (sID.length()!=u32IDLenNow) bGood=False

        else sID=""
        Init(iWidth,iHeight,iBytesPP,True); #DOES DeriveVars and create buffer
        #(byte[iMapLength])(arrbyColorMap)
        if (bFirstRun) cerr<<"map:"
        if iMapLength>0:
            arrbyColorMap=(byte*)malloc(iMapLength)

            iGot=fread((void*)arrbyColorMap,1,iMapLength,fileNow)
            #for (int iNow=0; iNow<iMapLength; iNow++)            #	iGot=fread((void*)&arrbyColorMap[iNow],1,1,fileNow)
            #
            if iGot!=iMapLength:
                cerr<<"Not all "<<(iMapLength)<<" color map bytes were found."<<flush
                if (bFirstRun) cerr<<"only "<<iGot<<"not ;"<<flush
                bGood=False

            else:
                if bFirstRun) cerr<<("good;":


        else:
            if arrbyColorMap!=null:
                free(arrbyColorMap)
                arrbyColorMap=null

            if bFirstRun) cerr<<("none;":

        #(byte[iWidth*iHeight*iBytesPP])(arrbyData)
        #iBytesBuffer=bytes remaining
        #TODO: iBytesBuffer=#finish thisnot  Count compressed area, by output size, load rest into footer!
        if (iBytesAsUncompressed<iBytesBuffer) iBytesBuffer=iBytesAsUncompressed
        if (bFirstRun) cerr<<"buffer:"<<(iBytesBuffer)<<"; "
        int iFound=0

        if iBytesBuffer<=0:
            bGood=False
            cerr<<"Targa.Load Error: Only "<<(iBytesBuffer)<<" were expected given self file's header"

        if bGood:
            #the following is ONLY OK SINCE called Init above
            if bFirstRun) cerr<<("( ":
            if IsCompressed():
                if bFirstRun) cerr<<("compression found...":
                #int iStart=iPlace
                #iBytesBuffer=RLESizeUncompressed(byterNow.arrbyData,iStart,iBytesLeft,iBytesPP)
                if arrbyData!=null:
                    free(arrbyData)
                    arrbyData=null

                arrbyData=(byte*)malloc(iBytesBuffer)
                for (int iNow=0; iNow<iBytesBuffer; iNow++)
                    #arrbyData[iNow]=alldata[iStart+iNow]
                    iFound++

                #advance file by (iFound)

            else:
                if (bFirstRun) cerr<<"no compression..."
                int iTest=SafeCopyFrom(iWidth,iHeight,iBytesPP,fileNow,False)
                if iTest!=iBytesBuffer:
                    bGood=False
                    cerr<<"Expected "<<(iBytesBuffer)<<" but found "<<(iTest)<<"..."<<endl

                # Advance file position by (iTest)

            if bFirstRun) cerr<<(" )...":

        if bGoodandIsSavedAsFlipped():
            if IsCompressed():
                if not SetCompressionRLE(False):
                    bGood=False
                    cerr<<"Targa.Load Error: Failed to uncompress for flipnot "

                if not Flip():
                    bGood=False
                    cerr<<"Targa.Load Error: Failed to uncompress for flipnot "

                if not SetCompressionRLE(True):
                    bGood=False
                    cerr<<"Targa.Load Error: Failed to recompress after flipnot "


            else:
                if not Flip():
                    bGood=False
                    cerr<<"Targa.Load Error: Failed to flip targanot "

                elif bFirstRun:
                    cerr<<"Flip():success..."<<flush



        if bFirstRun) cerr<<("footer:":
        #if byterNow.BytesLeftUsed()>0:        footer.Init(fileNow)
        if (bFirstRun) cerr<<footer.ByteCount()<<"; "
        #
        if (bFirstRun) cerr<<"} "
        if bFirstRun) cerr<<(bGood?"Targa.Load Success--dump":"Targa.Load Done with errors--dump":
        if bFirstRun) cerr<<Dump(:
        if not bGood:
            cerr<<"  Targa.Load had error(s)."<<endl

        fclose(fileNow)

    catch (exception& exn)
        bGood=False
        cerr<<"Targa.Load could not finish"<<exn.what()<<endl

    catch (...)
        bGood=False
        cerr<<"Targa.Load could not finish (Unknown exception)."<<endl

    bFirstRun=False
    return bGood
}#end Targa.Load
def IsOK(self):
    bool bGood=(iWidth>0 and iHeight>0 and iBytesPP>0 and arrbyData!=null)
    if not IsCompressed():
        if (iBytesBuffer!=(iWidth*iHeight*iBytesPP)) bGood=False
        if (iBytesBuffer!=iBytesAsUncompressed) bGood=False

    return bGood

def Flip(self):
    bool bGood=True
    if not IsOK():
        bGood=False
        cerr<<"Targa.Flip Error: Targa is corrupt or did not load properly (IsOK() returned False)not "

    if bGoodandIsCompressed():
        bGood=False
        cerr<<"Targa.Flip Error: Targa is still compressed and cannot be flipped before uncompressednot "

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



            if arrbyData!=null:
                free(arrbyData)
                arrbyData=NULL

            arrbyData=arrbyTemp

        catch (exception& exn)
            bGood=False
            cerr<<"Targa.Flip could not finish: "<<exn.what()<<endl

        catch (...)
            bGood=False
            cerr<<"Targa.Flip could not finish (unknown exception)."<<endl


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
            cerr<<"Tried to turn compression "<<(bOn?"on":"off")<<" for "<<(iWidth)<<("x")<<(iHeight)<<("x")<<(iBytesPP)<<(" imagenot ")

        elif iBytesBuffer<=0:
            cerr<<"Tried to turn compression "<<(bOn?"on":"off")<<" for "<<(iBytesBuffer)<<"-buffer "<<(BytesAsUncompressed())<<"-length imagenot "

        else:
            if bOn:
                if (not IsCompressed())   #Compress
                    byte* arrbyCompressed=RLECompress(iBytesBuffer, arrbyData, 0, iBytesBuffer, iBytesPP)
                    if arrbyData!=NULL:
                        free(arrbyData)
                        arrbyData=NULL

                    arrbyData=arrbyCompressed


            else:
                if (IsCompressed())   #Uncompress
                    int iNewSize=iWidth*iHeight*iBytesPP
                    byte* arrbyUncompressed=(byte*)malloc(iNewSize); #byte* arrbyUncompress=RLEUncompress(iBytesBuffer, arrbyData, 0, iBytesBuffer, iBytesPP)
                    int iTest=RLEUncompress(arrbyUncompressed, iNewSize, arrbyData, iBytesBuffer, iBytesPP)
                    if iTest!=iNewSize:
                        cerr<<"Targa.SetCompressionRLE("<<(bOn)<<") Error:"<<"Uncompressed "<<(iTest)<<" bytes but expected "<<(iNewSize)<<" ("<<(iWidth)<<"x"<<(iHeight)<<" at "<<(iBytesPP*8)<<"bpp ["<<(iBytesPP)<<" bytes per pixel])"<<endl

                    if arrbyData!=NULL:
                        free(arrbyData)
                        arrbyData=NULL

                    arrbyData=arrbyUncompressed
                    iBytesBuffer=iNewSize




    catch (exception& exn)
        bGood=False
        cerr<<"Targa.SetCompressionRLE("<<(bOn)<<") could not finish: "<<exn.what()<<endl

    catch (...)
        bGood=False
        cerr<<"Targa.SetCompressionRLE("<<(bOn)<<") could not finish (Unknown exception)"<<endl

    return bGood
}#end SetCompressionRLE
def Dump(self):
    return Dump(False)

def Dump(self, bDumpFull):
    stringstream ssReturn
    ssReturn<<"{"
    ssReturn<<"dimensions:"<<(iWidth)
            <<"x"<<(iHeight)
            <<"x"<<(iBytesPP)<<";"
    ssReturn<<" buffer:"<<(((arrbyData==null)?"null":"ok"))<<"; "
    ssReturn<<" ImageSize:"<<(iBytesAsUncompressed)<<"; "
    ssReturn<<" BufferSize:"<<(iBytesBuffer)<<"; "
    if bDumpFull:
        #do some stuff here maybe later

    ssReturn<<"}"
    string sReturn
    sReturn=ssReturn.str()
    return sReturn

def Description(self):
    return Description(False)

def Description(self, bVerbose):
    std.stringstream ssReturn
    if (bVerbose) ssReturn <<((arrbyData==null)?"null":"")<<(iWidth)<<"x"<<(iHeight)<<"x"<<(iBytesPP*8)<<" "<<(iBytesAsUncompressed)<<"-length "<<(iBytesBuffer)<<"-buffer"
    else ssReturn <<((arrbyData==null)?"null":"")<<(iWidth)<<"x"<<(iHeight)<<"x"<<(iBytesPP*8)
    std.string sReturn
    sReturn=ssReturn.str()
    return sReturn

#private methods:
def DeriveVars(self):
    iBytesPP=iBitDepth/8
    iStride=iWidth*iBytesPP
    iBytesAsUncompressed=iStride*iHeight

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

}#end namespace
#endif
