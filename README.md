# conan-juce
Conan.io recipe for the JUCE cross-platform C++ framework.

[ ![Download](https://api.bintray.com/packages/impsnldavid/public-conan/juce%3Aimpsnldavid/images/download.svg?version=5.3.2%3Atesting) ](https://bintray.com/impsnldavid/public-conan/juce%3Aimpsnldavid/5.3.2%3Atesting/link)

Although JUCE contains it's own project management system (the Projucer) which favours the approach of directly including all JUCE source code in each project individually, this package is designed to build all JUCE modules as a static/dynamic library.

The package script will first build the Projucer, then use this generate compiler specific projects using conan settings and options. These projects are then used to build the library.

Currently only MSVC builds are supported, although support for  XCode and Linux is planned.

