#include <windows.h>
#include <shroudtopia.h>
#include <filesystem>
#include <iostream>
int main(int argc,char** argv) {
    auto check=[](bool value,const char* message){if(!value){std::cerr<<"FAIL: "<<message<<'\n';ExitProcess(1);}std::cout<<"PASS: "<<message<<'\n';};
    const auto root=std::filesystem::current_path();
    auto proxy=LoadLibraryW(L"Winmm.dll");check(proxy!=nullptr,"same basename LoadLibraryW call as current game succeeds");
    wchar_t loaded[32768]{};GetModuleFileNameW(proxy,loaded,32768);
    check(std::filesystem::equivalent(loaded,root/"winmm.dll"),"application-local proxy selected");
    auto loader=GetModuleHandleW(L"shroudtopia.dll");check(loader!=nullptr,"proxy loaded Shroudtopia");
    GetModuleFileNameW(loader,loaded,32768);
    check(std::filesystem::equivalent(loaded,root/"shroudtopia.dll"),"exact staged Shroudtopia selected");
    wchar_t system[32768]{};GetSystemDirectoryW(system,32768);
    for(const char* name:{"timeBeginPeriod","timeEndPeriod"}) {
        auto address=GetProcAddress(proxy,name);check(address!=nullptr,"required timer export resolves");
        HMODULE owner{};
        check(GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(address),&owner)!=FALSE,"forwarded export owner resolves");
        GetModuleFileNameW(owner,loaded,32768);
        check(std::filesystem::equivalent(loaded,std::filesystem::path(system)/"winmm.dll"),"timer export forwards to system WINMM");
    }
    ModContext context{};context.game.isClient=true;context.Log=[](const char*){};
    for(int i=1;i<argc;++i) {
        auto dll=LoadLibraryA(argv[i]);check(dll!=nullptr,"candidate DLL loads in isolated host");
        auto factory=reinterpret_cast<Mod*(*)()>(GetProcAddress(dll,"CreateModInstance"));check(factory!=nullptr,"Shroudtopia factory is exported");
        auto* mod=factory();check(mod!=nullptr,"candidate instance constructs");
        mod->Load(&context);mod->Activate(&context);
        check(!mod->active,"candidate rejects unsupported host without activation");
        mod->Deactivate(&context);mod->Unload(&context);delete mod;
        check(FreeLibrary(dll)!=FALSE,"unpublished candidate unloads cleanly");
    }
    // Shroudtopia owns a resident worker. Do not hot-unload that loader.
    return 0;
}
