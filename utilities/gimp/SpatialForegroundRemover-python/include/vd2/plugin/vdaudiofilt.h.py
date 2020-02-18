#ifndef f_VD2_PLUGIN_VDAUDIOFILT_H
#define f_VD2_PLUGIN_VDAUDIOFILT_H

#####################################/
#
#	Audio filter support

struct VDAudioFilterDefinition
struct VDXWaveFormat
struct VDPluginCallbacks

enum
    kVDPlugin_AudioAPIVersion		= 2


struct VDAudioFilterPin
    unsigned			mGranularity;			# Block size a filter reads/writes self pin.
    unsigned			mDelay;					# Delay in samples on self input.
    unsigned			mBufferSize;			# The size, samples, the buffer.
    unsigned			mCurrentLevel;			# The number of samples currently in the buffer.
    sint64				mLength;				# Approximate length of self stream in us.
     VDXWaveFormat *mpFormat
    bool				mbVBR
    bool				mbEnded
    char				_pad[2]
    void				*mpBuffer
    unsigned			mSamplesWritten;		# The number of samples just written to the buffer.
    unsigned			mAvailSpace;			# Available room pointed to by mpBuffer (output pins only).

    uint32 (VDAPIENTRY *mpReadProc)(VDAudioFilterPin *pPin, *dst, samples, bAllowFill, format)

    # These helpers are non-virtual inlines and are compiled into filters.
    uint32 Read(void *dst, samples, bAllowFill, format)
        return mpReadProc(self, dst, samples, bAllowFill, format)



struct VDAudioFilterContext

struct VDAudioFilterCallbacks
    VDXWaveFormat *(VDAPIENTRY *AllocPCMWaveFormat)(unsigned sampling_rate, channels, bits, bFloat)
    VDXWaveFormat *(VDAPIENTRY *AllocCustomWaveFormat)(unsigned extra_size)
    VDXWaveFormat *(VDAPIENTRY *CopyWaveFormat)( VDXWaveFormat *)
    void (VDAPIENTRY *FreeWaveFormat)( VDXWaveFormat *)
    void (VDAPIENTRY *Wake)( VDAudioFilterContext *pContext)


struct VDAudioFilterContext
    void *mpFilterData
    VDAudioFilterPin	**mpInputs
    VDAudioFilterPin	**mpOutputs
    IVDPluginCallbacks *mpServices
     VDAudioFilterCallbacks *mpAudioCallbacks
     VDAudioFilterDefinition *mpDefinition
    uint32	mAPIVersion
    uint32	mInputSamples;			# Number of input samples available on all pins.
    uint32	mInputGranules;			# Number of input granules available on all pins.
    uint32	mInputsEnded;			# Number of inputs that have ended.
    uint32	mOutputSamples;			# Number of output sample spaces available on all pins.
    uint32	mOutputGranules;		# Number of output granule spaces available on all pins.
    uint32	mCommonSamples;			# Number of input samples and output sample spaces.
    uint32	mCommonGranules;		# Number of input and output granules.


# This structure is intentionally identical to WAVEFORMATEX, one
# exception -- mExtraSize is *always* present, for PCM.

struct VDXWaveFormat
    enum { kTagPCM = 1

    uint16		mTag
    uint16		mChannels
    uint32		mSamplingRate
    uint32		mDataRate
    uint16		mBlockSize
    uint16		mSampleBits
    uint16		mExtraSize


enum
    kVFARun_OK				= 0,
    kVFARun_Finished		= 1,
    kVFARun_InternalWork	= 2,

    kVFAPrepare_OK			= 0,
    kVFAPrepare_BadFormat	= 1


enum
    kVFARead_Native			= 0,
    kVFARead_PCM8			= 1,
    kVFARead_PCM16			= 2,
    kVFARead_PCM32F			= 3


typedef void *		(VDAPIENTRY *VDAudioFilterExtProc			)( VDAudioFilterContext *pContext, *pInterfaceName)
typedef uint32		(VDAPIENTRY *VDAudioFilterRunProc			)( VDAudioFilterContext *pContext)
typedef sint64		(VDAPIENTRY *VDAudioFilterSeekProc			)( VDAudioFilterContext *pContext, microsecs)
typedef uint32		(VDAPIENTRY *VDAudioFilterPrepareProc		)( VDAudioFilterContext *pContext)
typedef void		(VDAPIENTRY *VDAudioFilterStartProc			)( VDAudioFilterContext *pContext)
typedef void		(VDAPIENTRY *VDAudioFilterStopProc			)( VDAudioFilterContext *pContext)
typedef void		(VDAPIENTRY *VDAudioFilterInitProc			)( VDAudioFilterContext *pContext)
typedef void		(VDAPIENTRY *VDAudioFilterDestroyProc		)( VDAudioFilterContext *pContext)
typedef unsigned	(VDAPIENTRY *VDAudioFilterSuspendProc		)( VDAudioFilterContext *pContext, *dst, size)
typedef void		(VDAPIENTRY *VDAudioFilterResumeProc		)( VDAudioFilterContext *pContext, *src, size)
typedef unsigned	(VDAPIENTRY *VDAudioFilterGetParamProc		)( VDAudioFilterContext *pContext, idx, *dst, size)
typedef void		(VDAPIENTRY *VDAudioFilterSetParamProc		)( VDAudioFilterContext *pContext, idx, *src, variant_count)
typedef bool		(VDAPIENTRY *VDAudioFilterConfigProc		)( VDAudioFilterContext *pContext, HWND__ *hwnd)

enum
    kVFAF_Zero				= 0,
    kVFAF_HasConfig			= 1,				# Filter has a configuration dialog.
    kVFAF_SerializedIO		= 2,				# Filter must execute in the serialized I/O thread.

    kVFAF_Max				= 0xFFFFFFFF,


struct VDAudioFilterVtbl
    uint32								mSize
    VDAudioFilterDestroyProc			mpDestroy
    VDAudioFilterPrepareProc			mpPrepare
    VDAudioFilterStartProc				mpStart
    VDAudioFilterStopProc				mpStop
    VDAudioFilterRunProc				mpRun
    VDAudioFilterSeekProc				mpSeek
    VDAudioFilterSuspendProc			mpSuspend
    VDAudioFilterResumeProc				mpResume
    VDAudioFilterGetParamProc			mpGetParam
    VDAudioFilterSetParamProc			mpSetParam
    VDAudioFilterConfigProc				mpConfig
    VDAudioFilterExtProc				mpExt


struct VDAudioFilterDefinition
    uint32							mSize;				# size of self structure in bytes
    uint32							mFlags

    uint32							mFilterDataSize
    uint32							mInputPins
    uint32							mOutputPins

     VDXPluginConfigEntry		*mpConfigInfo

    VDAudioFilterInitProc			mpInit
     VDAudioFilterVtbl			*mpVtbl


#endif
