#ifndef TARGA_H
#define TARGA_H

#include <iostream>
#include <iomanip>
#include <fstream>
#include <memory>
#include "frameworkdummy.h"
#include "pmemory.h"
#include "preporting.h"

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
#targa.bitsDescriptor low nibble sequential values:
 lownibble565Or888NoAlpha = 0;	#bits 0-3
 lownibbleAlpha5551 = 1;	#bits 0-3 #TODO: read GGGBBBBB ARRRRRGG since targa is always low-high (little endian)
 lownibbleAlpha8888 = 8;	#bits 0-3
#targa.bitsDescriptor bits:
 bitReserved4 = 16;	#bit4
 bitNoFlip_NonTruevision = 32;	#bit5 #Truevision is a registered trademark of Truevision
 bitInterleave4Way = 64;	#bit6 (of 0 to 7)
 bitInterleave2Way = 128;	#bit7 (highest bit)
##region prototypes
def RLESizeUncompressed(self, arrbySrc, iStart, iSrcSize, iBytesPerChunk):
def Compare(self, arrbySrc1, iSrcLoc1, arrbySrc2, iSrcLoc2, iRun):
def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse, bCountOnlyAndReturnNull):
def RLECompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse):
def RLEUncompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse, bCountOnlyAndReturnNull):
def RLEUncompress(self, iReturnLength, arrbySrc, iSrcStart, iBytesPerChunk, iBytesToParse):
def RLEUncompress(self, arrbyDest, iDestSize, arrbySrc, iSrcSize, iBytesPerChunk):
def RLEUncompress(self, arrbyDest, iDestSizeIrrelevantIfCountOnlyIsTrue, arrbySrc, iSrcSize, iBytesPerChunk, iDestStart, iSrcStart, bCountOnlyAndDontTouchDest):
##endregion prototypes

##region TargaFooter
class TargaFooter
private:
    byte *dump
    uint dump_Length
public:
    TargaFooter()
    TargaFooter(byte* lpbyDataPointerToKeep, u32Size)
    TargaFooter(byte* arrbyDataSrcToCopyFrom, u32Start, u32Count, u32ActualSourceBufferSize)
    ~TargaFooter()
    bool Init()
    bool Init(BinaryReader& streamIn_ToReadToEnd)
    bool Init(byte* lpbyDataPointerToKeep, u32Size)
    bool Init(byte* arrbyDataSrc, u32SrcStart, u32Count, u32ActualSourceBufferSize)
    bool WriteTo(BinaryWriter &streamOut)
    uint ByteCount()

##endregion TargaFooter

class Targa
public:
    string sFile
    TargaFooter footer
    byte *arrbyData

    Targa()
    ~Targa()
    int Width()
    int Height()
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
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, &streamIn, bReInitializeAll)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, bReInitializeAll)
    int SafeCopyFrom(int iWidthTo, iHeightTo, iBytesPP, arrbySrc, u32SrcRealLen, u32SrcStart, bReInitializeAll)
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
    void Reflect(int& x, y)
    void Wrap(int& x, y)
    int getChannel_Fast(int x, y, iChan)
    int getChannelReflected(int x, y, iChan)
    void getColorRgbReflected(byte& R, G, B, x, y)
    void getColorArgbReflected(byte& A, R, G, B, x, y)
    void getColorRgb_Fast(byte& R, G, B, x, y)
    void getColorArgb_Fast(byte& A, R, G, B, x, y)
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

    #/<summary>
    #/Bits 0-3: number of bits of the pixel that are the alpha channel (i.e. 8 for BGRA32 or 1 for 5551 or 0 for BGRx32)
    #/Bit 4: reserved
    #/Bit 5: screen origin -- {0:lower left; 1:upper left} usually 0
    #/Bits 7-6: interleaving nibble {00:non-interleaved; 01:even-odd; 10:four way; 11: reserved
    #/</summary>
    byte bitsDescriptor; #1 byte  #(usually zero; 17th byte)

    string sID; #array of [iTagLength] bytes  #[bySizeofID] -- custom non-terminated string
    byte *arrbyColorMap; #array of [] bytes  #[byMapBitDepth*wMapLength] -- the palette
    #arrbyData
    #derived fields:
    int iBytesPP
    int iStride
    int iBytesAsUncompressed;#byte sizeof image data only
    int iBytesBuffer

}#end namespace

#endif
