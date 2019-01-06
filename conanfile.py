#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, MSBuild, tools
from shutil import copy2, copytree
import os
import xml.etree.ElementTree


class JuceConan(ConanFile):
    name = "juce"
    version = "5.3.2"
    url = "https://github.com/WeAreROLI/JUCE"
    description = "The JUCE cross-platform C++ framework"
    license = "GPLv3"
    exports = ["README.md"]
    exports_sources = ["libjuce.jucer", "projucer*"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "report_app_usage": [True, False],
        "display_splash_screen": [True, False],
        "splash_screen_color": ["Dark", "Light"],
        "cpp_standard": ["11", "14", "17", "Latest"],
        "juce_force_debug": [True, False],
        "juce_log_assertions": [True, False],
        "juce_check_memory_leaks": [True, False],
        "juce_dont_autolink_to_win32_libraries": [True, False],
        "juce_include_zlib_code": [True, False],
        "juce_use_curl": [True, False],
        "juce_catch_unhandled_exceptions": [True, False],
        "juce_allow_static_null_variables": [True, False],
        "juce_asio": [True, False],
        "juce_wasapi": [True, False],
        "juce_wasapi_exclusive": [True, False],
        "juce_directsound": [True, False],
        "juce_alsa": [True, False],
        "juce_jack": [True, False],
        "juce_bela": [True, False],
        "juce_use_android_oboe": [True, False],
        "juce_use_android_opensles": [True, False],
        "juse_use_winrt_midi": [True, False],
        "juce_disable_audio_mixing_with_other_apps": [True, False],
        "juce_use_flac": [True, False],
        "juce_use_oggvorbis": [True, False],
        "juce_use_mp3audioformat": [True, False],
        "juce_use_lame_audio_format": [True, False],
        "juce_use_windows_media_format": [True, False],
        "juce_pluginhost_vst": [True, False],
        "juce_pluginhost_vst3": [True, False],
        "juce_pluginhost_au": [True, False],
        "juce_pluginhost_ladspa": [True, False],
        "juce_use_cdreader": [True, False],
        "juce_use_cdburner": [True, False],
        "juce_assertion_firfilter": [True, False],
        "juce_dsp_use_intel_mkl": [True, False],
        "juce_dsp_use_shared_fftw": [True, False],
        "juce_dsp_use_static_fftw": [True, False],
        "juce_dsp_enable_snap_to_zero": [True, False],
        "juce_execute_app_suspend_on_ios_background_task": [True, False],
        "juce_use_coreimage_loader": [True, False],
        "juce_use_directwrite": [True, False],
        "juce_enable_repaint_debugging": [True, False],
        "juce_use_xrandr": [True, False],
        "juce_use_xinerama": [True, False],
        "juce_use_xshm": [True, False],
        "juce_use_xrender": [True, False],
        "juce_use_xcursor": [True, False],
        "juce_web_browser": [True, False],
        "juce_enable_live_constant_editor": [True, False],
        "juce_use_camera": [True, False]
    }
    default_options = (
        "shared=False",
        "report_app_usage=False",
        "display_splash_screen=False",
        "splash_screen_color=Dark",
        "cpp_standard=14",
        "juce_force_debug=False",
        "juce_log_assertions=False",
        "juce_check_memory_leaks=True",
        "juce_dont_autolink_to_win32_libraries=False",
        "juce_include_zlib_code=True",
        "juce_use_curl=False",
        "juce_catch_unhandled_exceptions=True",
        "juce_allow_static_null_variables=True",
        "juce_asio=False",
        "juce_wasapi=True",
        "juce_wasapi_exclusive=False",
        "juce_directsound=True",
        "juce_alsa=True",
        "juce_jack=False",
        "juce_bela=False",
        "juce_use_android_oboe=False",
        "juce_use_android_opensles=False",
        "juse_use_winrt_midi=False",
        "juce_disable_audio_mixing_with_other_apps=False",
        "juce_use_flac=True",
        "juce_use_oggvorbis=True",
        "juce_use_mp3audioformat=False",
        "juce_use_lame_audio_format=False",
        "juce_use_windows_media_format=True",
        "juce_pluginhost_vst=False",
        "juce_pluginhost_vst3=False",
        "juce_pluginhost_au=False",
        "juce_pluginhost_ladspa=False",
        "juce_use_cdreader=False",
        "juce_use_cdburner=False",
        "juce_assertion_firfilter=True",
        "juce_dsp_use_intel_mkl=False",
        "juce_dsp_use_shared_fftw=False",
        "juce_dsp_use_static_fftw=False",
        "juce_dsp_enable_snap_to_zero=True",
        "juce_execute_app_suspend_on_ios_background_task=False",
        "juce_use_coreimage_loader=True",
        "juce_use_directwrite=True",
        "juce_enable_repaint_debugging=False",
        "juce_use_xrandr=True",
        "juce_use_xinerama=True",
        "juce_use_xshm=True",
        "juce_use_xrender=False",
        "juce_use_xcursor=True",
        "juce_web_browser=True",
        "juce_enable_live_constant_editor=False",
        "juce_use_camera=False"
    )
    short_paths = True

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    
    def configure_jucer(self):
        print("Configuring Projucer project with conan build settings...")
    
        tree = xml.etree.ElementTree.parse("libjuce.jucer")
        root = tree.getroot()
        
        if self.options.shared == "True":
            root.set("defines", root.attrib["defines"] + " JUCE_DLL_BUILD=1")
        
        root.set("projectType", "dll" if self.options.shared == "True" else "library" )
        
        if self.settings.os == "Windows":
            configs_vs2013 = root.find("EXPORTFORMATS/VS2013/CONFIGURATIONS")
            configs_vs2015 = root.find("EXPORTFORMATS/VS2015/CONFIGURATIONS")
            configs_vs2017 = root.find("EXPORTFORMATS/VS2017/CONFIGURATIONS")
                
            for c in configs_vs2013.findall("CONFIGURATION") + configs_vs2015.findall("CONFIGURATION") + configs_vs2017.findall("CONFIGURATION"):
                c.set("winArchitecture", "x64" if self.settings.arch == "x86_64" else "Win32")
                c.set("useRuntimeLibDLL", "1" if self.settings.compiler.runtime == "MD" or self.settings.compiler.runtime == "MDd" else "0")

        # PROJECT OPTIONS
        root.set("reportAppUsage", "1" if self.options.report_app_usage == "True" else "0" )
        root.set("displaySplashScreen", "1" if self.options.display_splash_screen == "True" else "0" )
        root.set("splashScreenColour", str(self.options.splash_screen_color))
        root.set("cppLanguageStandard", str(self.options.cpp_standard))

        juce_options = root.find("JUCEOPTIONS")
        
        # JUCE_CORE
        juce_options.set("JUCE_FORCE_DEBUG", "1" if self.options.juce_force_debug == "True" else "0" )
        juce_options.set("JUCE_LOG_ASSERTIONS", "1" if self.options.juce_log_assertions == "True" else "0" )
        juce_options.set("JUCE_CHECK_MEMORY_LEAKS", "1" if self.options.juce_check_memory_leaks == "True" else "0" )
        juce_options.set("JUCE_DONT_AUTOLINK_TO_WIN32_LIBRARIES", "1" if self.options.juce_dont_autolink_to_win32_libraries == "True" else "0" )
        juce_options.set("JUCE_INCLUDE_ZLIB_CODE", "1" if self.options.juce_include_zlib_code == "True" else "0" )
        juce_options.set("JUCE_USE_CURL", "1" if self.options.juce_use_curl == "True" else "0" )
        juce_options.set("JUCE_CATCH_UNHANDLED_EXCEPTIONS", "1" if self.options.juce_catch_unhandled_exceptions == "True" else "0" )
        juce_options.set("JUCE_ALLOW_STATIC_NULL_VARIABLES", "1" if self.options.juce_allow_static_null_variables == "True" else "0" )
        
        # JUCE_AUDIO_DEVICES
        juce_options.set("JUCE_ASIO", "1" if self.options.juce_asio == "True" else "0" )
        juce_options.set("JUCE_WASAPI", "1" if self.options.juce_wasapi == "True" else "0" )
        juce_options.set("JUCE_WASAPI_EXCLUSIVE", "1" if self.options.juce_wasapi_exclusive == "True" else "0" )
        juce_options.set("JUCE_DIRECTSOUND", "1" if self.options.juce_directsound == "True" else "0" )
        juce_options.set("JUCE_ALSA", "1" if self.options.juce_alsa == "True" else "0" )
        juce_options.set("JUCE_JACK", "1" if self.options.juce_jack == "True" else "0" )
        juce_options.set("JUCE_BELA", "1" if self.options.juce_bela == "True" else "0" )
        juce_options.set("JUCE_USE_ANDROID_OBOE", "1" if self.options.juce_use_android_oboe == "True" else "0" )
        juce_options.set("JUCE_USE_ANDROID_OPENSLES", "1" if self.options.juce_use_android_opensles == "True" else "0" )
        juce_options.set("JUCE_USE_WINRT_MIDI", "1" if self.options.juse_use_winrt_midi == "True" else "0" )
        juce_options.set("JUCE_DISABLE_AUDIO_MIXING_WITH_OTHER_APPS", "1" if self.options.juce_disable_audio_mixing_with_other_apps == "True" else "0" )
        
        # JUCE_AUDIO_FORMATs
        juce_options.set("JUCE_USE_FLAC", "1" if self.options.juce_use_flac == "True" else "0" )
        juce_options.set("JUCE_USE_OGGVORBIS", "1" if self.options.juce_use_oggvorbis == "True" else "0" )
        juce_options.set("JUCE_USE_MP3AUDIOFORMAT", "1" if self.options.juce_use_mp3audioformat == "True" else "0" )
        juce_options.set("JUCE_USE_LAME_AUDIO_FORMAT", "1" if self.options.juce_use_lame_audio_format == "True" else "0" )
        juce_options.set("JUCE_USE_WINDOWS_MEDIA_FORMAT", "1" if self.options.juce_use_windows_media_format == "True" else "0" )
        
        # JUCE_AUDIO_PROCESSORS
        juce_options.set("JUCE_PLUGINHOST_VST", "1" if self.options.juce_pluginhost_vst == "True" else "0" )
        juce_options.set("JUCE_PLUGINHOST_VST3", "1" if self.options.juce_pluginhost_vst3 == "True" else "0" )
        juce_options.set("JUCE_PLUGINHOST_AU", "1" if self.options.juce_pluginhost_au == "True" else "0" )
        juce_options.set("JUCE_PLUGINHOST_LADSPA", "1" if self.options.juce_pluginhost_ladspa == "True" else "0" )
        
        # JUCE_AUDIO_UTILS
        juce_options.set("JUCE_USE_CDREADER", "1" if self.options.juce_use_cdreader == "True" else "0" )
        juce_options.set("JUCE_USE_CDBURNER", "1" if self.options.juce_use_cdburner == "True" else "0" )
        
        # JUCE_DSP
        juce_options.set("JUCE_ASSERTION_FIRFILTER", "1" if self.options.juce_assertion_firfilter == "True" else "0" )
        juce_options.set("JUCE_DSP_USE_INTEL_MKL", "1" if self.options.juce_dsp_use_intel_mkl == "True" else "0" )
        juce_options.set("JUCE_DSP_USE_SHARED_FFTW", "1" if self.options.juce_dsp_use_shared_fftw == "True" else "0" )
        juce_options.set("JUCE_DSP_USE_STATIC_FFTW", "1" if self.options.juce_dsp_use_static_fftw == "True" else "0" )
        juce_options.set("JUCE_DSP_ENABLE_SNAP_TO_ZERO", "1" if self.options.juce_dsp_enable_snap_to_zero == "True" else "0" )
        
        # JUCE_EVENTS
        juce_options.set("JUCE_EXECUTE_APP_SUSPEND_ON_IOS_BACKGROUND_TASK", "1" if self.options.juce_execute_app_suspend_on_ios_background_task == "True" else "0" )
        
        # JUCE_GRAPHICS
        juce_options.set("JUCE_USE_COREIMAGE_LOADER", "1" if self.options.juce_use_coreimage_loader == "True" else "0" )
        juce_options.set("JUCE_USE_DIRECTWRITE", "1" if self.options.juce_use_directwrite == "True" else "0" )
        
        # JUCE_GUI_BASICS
        juce_options.set("JUCE_ENABLE_REPAINT_DEBUGGING", "1" if self.options.juce_enable_repaint_debugging == "True" else "0" )
        juce_options.set("JUCE_USE_XRANDR", "1" if self.options.juce_use_xrandr == "True" else "0" )
        juce_options.set("JUCE_USE_XINERAMA", "1" if self.options.juce_use_xinerama == "True" else "0" )
        juce_options.set("JUCE_USE_XSHM", "1" if self.options.juce_use_xshm == "True" else "0" )
        juce_options.set("JUCE_USE_XRENDER", "1" if self.options.juce_use_xrender == "True" else "0" )
        juce_options.set("JUCE_USE_XCURSOR", "1" if self.options.juce_use_xcursor == "True" else "0" )
        
        # JUCE_GUI_EXTRA
        juce_options.set("JUCE_WEB_BROWSER", "1" if self.options.juce_web_browser == "True" else "0" )
        juce_options.set("JUCE_ENABLE_LIVE_CONSTANT_EDITOR", "1" if self.options.juce_enable_live_constant_editor == "True" else "0" )
        
        # JUCE_VIDEO
        juce_options.set("JUCE_USE_CAMERA", "1" if self.options.juce_use_camera == "True" else "0" )
        
        tree.write("libjuce.jucer")
        
        
    def build_projucer(self):
    
        print("Building Projucer...")
    
        if self.settings.os == "Windows":
        
            projucer_project_folder = os.path.join(self.source_subfolder, "extras/Projucer/ConanBuilds", self.msvc_version_lookup())
            
            if self.settings.arch == "x86_64":
                arch_name = "x64"
            else:
                arch_name = "Win32"
        
            msbuild = MSBuild(self)
            msbuild.build(os.path.join(projucer_project_folder, "Projucer.sln"), build_type="Release", platforms={"x86":"Win32", "x86_64":"x64"})
            
            copy2(os.path.join(projucer_project_folder, arch_name, "Release/App/Projucer.exe"), ".")
        
        elif self.settings.os == "Macos":
        
            projucer_project_folder = os.path.join(self.source_subfolder, "extras/Projucer/ConanBuilds/MacOSX")

            self.run("xcodebuild -project {0}/Projucer.xcodeproj -configuration Release CONFIGURATION_BUILD_DIR={1}".format(projucer_project_folder, os.getcwd()))
        
        
    def source(self):
        source_url = "https://github.com/WeAreROLI/JUCE"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        
        # Need to replace Projucer builds folder with package version containing more build archs
        copytree("projucer_builds", os.path.join(self.source_subfolder, "extras/Projucer/ConanBuilds"))
        
        self.build_projucer()

        
    def build(self):
        self.configure_jucer()
        
        if self.settings.os == "Windows":
            self.run("Projucer --resave libjuce.jucer")
            msbuild = MSBuild(self)
            msbuild.build(os.path.join("Builds", self.msvc_version_lookup(), "libjuce.sln"), platforms={"x86":"Win32", "x86_64":"x64"})
            
        elif self.settings.os == "Macos":
            self.run("Projucer.app/Contents/MacOS/Projucer --resave libjuce.jucer")
            self.build_xcode()    

    def build_xcode(self):
        self.run("xcodebuild -project Builds/MacOSX/libjuce.xcodeproj -configuration {0}".format(self.settings.build_type))
            
    def package(self):
        self.copy(pattern="README.md", src=self.source_subfolder, keep_path=False)
        self.copy(pattern="*.h", dst="include", src=os.path.join(self.source_subfolder, "modules"))
        self.copy(pattern="*.h", dst="include", src="JuceLibraryCode", keep_path=False)
            
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.dylib", dst="bin", keep_path=False)


    def package_info(self):
        self.cpp_info.cppflags.append("-std=c++14")
        if self.settings.build_type == "Debug":
            self.cpp_info.cppflags.append("-DDEBUG")
            self.cpp_info.cppflags.append("-D_DEBUG")
        else:
            self.cpp_info.cppflags.append("-DNDEBUG")
            self.cpp_info.cppflags.append("-D_NDEBUG")
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Macos":
            self.cpp_info.sharedlinkflags.append("-framework Accelerate")
            self.cpp_info.sharedlinkflags.append("-framework AudioToolbox")
            self.cpp_info.sharedlinkflags.append("-framework AVFoundation")
            self.cpp_info.sharedlinkflags.append("-framework AVKit")
            self.cpp_info.sharedlinkflags.append("-framework Carbon")
            self.cpp_info.sharedlinkflags.append("-framework Cocoa")
            self.cpp_info.sharedlinkflags.append("-framework CoreAudio")
            self.cpp_info.sharedlinkflags.append("-framework CoreMedia")
            self.cpp_info.sharedlinkflags.append("-framework CoreMIDI")
            self.cpp_info.sharedlinkflags.append("-framework IOKit")
            self.cpp_info.sharedlinkflags.append("-framework OpenGL")
            self.cpp_info.sharedlinkflags.append("-framework QuartzCore")
            self.cpp_info.sharedlinkflags.append("-framework WebKit")
            self.cpp_info.exelinkflags.append("-framework Accelerate")
            self.cpp_info.exelinkflags.append("-framework AudioToolbox")
            self.cpp_info.exelinkflags.append("-framework AVFoundation")
            self.cpp_info.exelinkflags.append("-framework AVKit")
            self.cpp_info.exelinkflags.append("-framework Carbon")
            self.cpp_info.exelinkflags.append("-framework Cocoa")
            self.cpp_info.exelinkflags.append("-framework CoreAudio")
            self.cpp_info.exelinkflags.append("-framework CoreMedia")
            self.cpp_info.exelinkflags.append("-framework CoreMIDI")
            self.cpp_info.exelinkflags.append("-framework IOKit")
            self.cpp_info.exelinkflags.append("-framework OpenGL")
            self.cpp_info.exelinkflags.append("-framework QuartzCore")
            self.cpp_info.exelinkflags.append("-framework WebKit")

        
    def msvc_version_lookup(self):
        if self.settings.compiler.version == "12":
            return "VisealStudio2013"
        elif self.settings.compiler.version == "14":
            return "VisualStudio2015"
        elif self.settings.compiler.version == "15":
            return "VisualStudio2017"
        else:
            assert False

