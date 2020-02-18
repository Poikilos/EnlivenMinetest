#ifndef TARGA_H
#define TARGA_H

#include <iostream>
#include <iomanip>
#include <fstream>
#include <memory>
#include "frameworkdummy.h"

using namespace std
namespace ProtoArmor
#Sequential targa.TypeTarga values:
 TypeNoImageData = 0
 TypeUncompressedColorMapped = 1
 TypeUncompressedTrueColor = 2
 TypeUncompressedGrayscale = 3
 TypeCompressedColorMapped = 9
 TypeCompressedTrueColor = 10
 TypeCompressedGrayscale = 11
 TypeCompressedColorMappedHuffmanAndDeltaAndRLE = 32
 TypeCompressedColorMappedHuffmanAndDeltaAndRLE4PassQuadTree = 33
#Sequential targa.MapType values
 MapType256 = 1
#targa.bitsDescriptor bits:
 lownibble565Or888NoAlpha = 0;	#bit3
 lownibbleAlpha5551 = 1;	#bit3 #TODO: read GGGBBBBB ARRRRRGG since targa is always low-high (little endian)
 lownibbleAlpha8888 = 8;	#bit3
 bitReserved4 = 16;	#bit4
 bitNoFlip_NonTruevision = 32;	#bit5 #Truevision is a registered trademark of Truevision
 bitInterleave4Way = 64;	#bit6
 bitInterleave2Way = 128;	#bit7
##region prototypes
def RLESizeUncompressed(self, arrbySrc, iStart, iSrcSize, iBytesPerChunk):
def Compare(self, arrbySrc1, iSrcLoc1, arrbySrc2, iSrcLoc2, iRun):
def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse, bCountOnlyAndReturnNull):
def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse):
def RLEUncompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse, bCountOnlyAndReturnNull):
def RLEUncompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse):
def RLEUncompress(self, arrbyDest, iDestSize, arrbySrc, iSrcSize, iBytesPerChunk):
def RLEUncompress(self, arrbyDest, iDestSizeIrrelevantIfCountOnlyIsTrue, arrbySrc, iSrcSize, iBytesPerChunk, iDestStart, iSrcStart, bCountOnlyAndDontTouchDest):

##region TargaFooter
class TargaFooter
private:
    byte *dump
    uint u32SizeofDump
public:
    TargaFooter()
    TargaFooter(byte* lpbyDataPointerToKeep, u32Size)
    TargaFooter(byte* arrbyDataSrcToCopyFrom, u32Start, u32Count, u32ActualSourceBufferSize)
    ~TargaFooter()
    bool Init()
    bool Init(byte* lpbyDataPointerToKeep, u32Size)
    bool Init(FILE* fileNowToReadToEnd)
    bool Init(byte* arrbyDataSrc, u32SrcStart, u32Count, u32ActualSourceBufferSize)
    int TargaFooter.WriteTo(FILE* pfileAlreadyOpen_ToNotCloseInThisMethod)
    int WriteTo(char* byarrDest, iAtDest, iSizeOfDest)
    uint ByteCount()

##endregion TargaFooter

##endregion prototypes
class Targa
public:
    string sFile
    TargaFooter footer
    byte *arrbyData

    Targa()
    ~Targa()
    int BytesPP()
    int Stride()
    int BytesAsUncompressed()
    int BytesBuffer()
    bool Init(int iSetWidth, iSetHeight, iSetBytesPP, bReallocateBuffers)
    bool CopyTo(Targa &targaDest)
    bool DrawFast(byte* arrbyDest, xAtDest, yAtDest, iDestWidth, iDestHeight, iDestBytesPP, iDestStride)
    void ToRect(ref_Rectangle rectReturn)
    void ToRect(ref_RectangleF rectReturn)
    bool From(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, bUsePointerNotCopyData)
    bool From(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, bUsePointerNotCopyData, u32SrcStart)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, bReInitializeAll)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll)
    #int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, fileNow, u32SrcRealLen)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, fileNow, bReInitializeAll)
    #int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, fileNow, u32SrcStart, bReInitializeAll)
    byte* GetBufferPointer()
    bool IsLoaded()
    bool Save()
    bool Save(string sFileNow)
    bool Load(string sFileNow)
    bool IsOK()
    bool Flip()
    bool HasAttrib(byte bit)
    bool IsSavedAsFlipped()
    bool IsCompressed()
    bool SetCompressionRLE(bool bOn)
    string Dump()
    string Dump(bool bDumpFull)
    string Description()
    string Description(bool bVerbose)
private:
    void DeriveVars()
    void InitNull()
    bool MarkAsCompressed(bool bAsCompressed)
    #header:
    #(byte)(length of id),(byte)(int)MapType,(byte)(int)TypeTarga,(ushort)iMapOrigin,(ushort)iMapLength,(byte)iMapBitDepth,(ushort)xImageLeft,(ushort)yImageBottom,(ushort)iWidth,(ushort)iHeight,(byte)iBitDepth,(byte)bitsDescriptor,(byte[length of id])sID,(byte[iMapLength])(arrbyColorMap),(byte[iBytesAsUncompressed])(arrbyData)
    #int iIDLength; #1 byte implied (length of sID)
    int MapType; #1 byte
    int TypeTarga; #1 byte
    int iMapOrigin; #2 bytes
    int iMapLength; #2 bytes
    int iMapBitDepth; #1 byte
    int xImageLeft; #2 bytes
    int yImageBottom; #2 bytes #TODO: don't flip if not zero
    int iWidth; #2 bytes
    int iHeight; #2 bytes
    int iBitDepth; #1 byte #TODO: 16 is 5.5.5.1 (not !not )IF(not !not ) low nibble of descriptor is 1 (otherwise 5.6.5 and descriptor low nibble is zero)
    byte bitsDescriptor; #1 byte  #(default zero)
    string sID; #array of [iTagLength] bytes  #[bySizeofID] -- custom non-terminated string
    byte *arrbyColorMap; #array of [] bytes  #[byMapBitDepth*wMapLength] -- the palette
    #arrbyData
    #derived fields:
    int iBytesPP
    int iStride
    int iBytesAsUncompressed;#byte sizeof image data only
    int iBytesBuffer
};#end class Targa
}#end namespace
#endif
