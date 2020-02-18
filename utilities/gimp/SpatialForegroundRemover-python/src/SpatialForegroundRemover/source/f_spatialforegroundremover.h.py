#ifndef F_SPATIALFOREGROUNDREMOVER_H
#define F_SPATIALFOREGROUNDREMOVER_H

#include <cstdio>
#include <string>

#include "targa.h"
#include "colorspacetransform.h"

using namespace std
using namespace ProtoArmor

class SpatialForegroundRemoverFilterConfig
public:
    SpatialForegroundRemoverFilterConfig()
        : mReach(1.0f)
        , mRadialSamples(1.0f)
        , mDiffusion(1.0f)


public:
    float mReach
    float mRadialSamples
    float mDiffusion


#######################################/

class SpatialForegroundRemoverFilterDialog : public VDXVideoFilterDialog
public:
    SpatialForegroundRemoverFilterDialog(SpatialForegroundRemoverFilterConfig& config, *ifp) : mConfig(config), mifp(ifp) {

    bool Show(HWND parent)
        return 0 != VDXVideoFilterDialog.Show(NULL, MAKEINTRESOURCE(IDD_FILTER_SPATIALFOREGROUNDREMOVER), parent)


    virtual INT_PTR DlgProc(UINT msg, wParam, lParam)

protected:
    bool OnInit()
    bool OnCommand(int cmd)
    void OnDestroy()

    void LoadFromConfig()
    bool SaveToConfig()

    SpatialForegroundRemoverFilterConfig& mConfig
    SpatialForegroundRemoverFilterConfig mOldConfig
    IVDXFilterPreview * mifp


#######################################/

class SpatialForegroundRemoverFilter : public VDXVideoFilter
public:
    virtual uint32 GetParams()
    virtual void Start()
    virtual void Run()
    virtual bool Configure(VDXHWND hwnd)
    virtual void GetSettingString(char *buf, maxlen)
    virtual void GetScriptString(char *buf, maxlen)

    VDXVF_DECLARE_SCRIPT_METHODS()
    ~SpatialForegroundRemoverFilter()
private:
    Targa targaTemp
    Targa targaMask
    void DrawDebugCircleTo_fx_buffer()
    void DrawDebugSquareTo_fx_buffer()

protected:
    unsigned int fx_buffer_w
    unsigned int fx_buffer_h
    unsigned int fx_buffer_BytesPP
    unsigned int fx_buffer_Stride
    unsigned int fx_buffer_BytesTotal
    unsigned char* fx_buffer

    void ScriptConfig(IVDXScriptInterpreter *isi, *argv, argc)

    void CTBufferInit(unsigned int w, int h, int BytesPP)

    SpatialForegroundRemoverFilterConfig mConfig


#endif