import os
from conans import ConanFile, CMake, tools
from conans.tools import Version
from conans.errors import ConanInvalidConfiguration

# TODO: 'clangToolingRefactor': True,
llvm_libs = [
    'LLVMAnalysis',
    'clangARCMigrate',
    'clangAnalysis',
    'clangAST',
    'clangASTMatchers',
    'clangBasic',
    'clangCodeGen',
    'clangDriver',
    'clangDynamicASTMatchers',
    'clangEdit',
    'clangFormat',
    'clangFrontend',
    'clangFrontendTool',
    'clangIndex',
    'clangLex',
    'clangParse',
    'clangRewrite',
    'clangRewriteFrontend',
    'clangSema',
    'clangSerialization',
    'clangStaticAnalyzerCheckers',
    'clangStaticAnalyzerCore',
    'clangStaticAnalyzerFrontend',
    'clangTooling',
    'clangToolingCore',
]

default_llvm_libs = llvm_libs

cling_libs = [
    'clingInterpreter',
    'clingMetaProcessor',
    # /usr/lib/x86_64-linux-gnu/libdl.so: error adding symbols: DSO missing from command line
    'clingUtils',
    'cling',
]

default_cling_libs = cling_libs

# Users locally they get the 1.0.0 version,
# without defining any env-var at all,
# and CI servers will append the build number.
# USAGE
# version = get_version("1.0.0")
# BUILD_NUMBER=-pre1+build2 conan export-pkg . my_channel/release
def get_version(version):
    bn = os.getenv("BUILD_NUMBER")
    return (version + bn) if bn else version

class ClingConan(ConanFile):
    name = "cling_conan"

    version = get_version("v0.9")
    cling_version = "v0.9"
    llvm_version = "cling-v0.9"
    clang_version = "cling-v0.9"

    #llvm_source_version = "6.0.1"

    description = "conan package for cling https://root.cern.ch/root/htmldoc/guides/users-guide/Cling.html"
    topics = ("c++", "conan", "cling", "clang", "root", "llvm", "cern")
    #url = "https://github.com/bincrafters/conan-folly" # TODO
    #homepage = "https://github.com/facebook/folly" # TODO
    #license = "Apache-2.0" # TODO

    # Constrains build_type inside a recipe to Release!
    settings = "os_build", "build_type", "arch_build", "compiler", "arch"

    options = {
      **{
        'with_' + library : [True, False] for library in llvm_libs },
      **{
        'with_' + library : [True, False] for library in cling_libs },
      "link_ltinfo": [True, False]
    }

    default_options = {
      **{
        'with_' + library : library in default_llvm_libs for library in llvm_libs },
      **{
        'with_' + library : library in default_cling_libs for library in cling_libs },
      "link_ltinfo": False
    }

    exports = ["LICENSE.md"]

    exports_sources = ["LICENSE", "README.md", "include/*", "src/*",
                       "cmake/*", "CMakeLists.txt", "tests/*", "benchmarks/*",
                       "scripts/*"]

    generators = 'cmake_find_package', "cmake", "cmake_paths"
    
    llvm_repo_url = "http://root.cern.ch/git/llvm.git"
    cling_repo_url = "http://root.cern.ch/git/cling.git"
    clang_repo_url = "http://root.cern.ch/git/clang.git"

    # conan search double-conversion* -r=conan-center
#    requires = (
#        "openssl/1.1.1-stable@conan/stable",
#    )    
    
#    @property
#    def _build_subfolder(self):
#        return "llvm_source_subfolder/cling_source_subfolder"

    @property
    def _llvm_source_subfolder(self):
        # can't use same 'src' dir as in https://root.cern.ch/cling-build-instructions
        # cause it is auto-created by conan
        return "llvm_src"

    @property
    def _cling_source_subfolder(self):
        return "cling"

    @property
    def _clang_source_subfolder(self):
        return "clang"

    @property
    def _libcxx(self):
      return str(self.settings.get_safe("compiler.libcxx"))

    #def config_options(self):
    #    if self.settings.os_build == "Windows":
    #        del self.options.fPIC
    #        del self.options.shared
    #    elif self.settings.os_build == "Macos":
    #        del self.options.shared

    def configure(self):
        compiler_version = Version(self.settings.compiler.version.value)
        if self.settings.build_type != "Release":
            raise ConanInvalidConfiguration("This library is compatible only with Release builds. Debug build of llvm may take a lot of time or crash due to lack of RAM or CPU")

    def requirements(self):
        print('self.settings.compiler {}'.format(self.settings.compiler))

    def source(self):
        # see https://root.cern.ch/cling-build-instructions
        self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.llvm_version, self.llvm_repo_url, self._llvm_source_subfolder))
        with tools.chdir(self._llvm_source_subfolder):
            self.run('git checkout {}'.format(self.llvm_version))
            with tools.chdir("tools"):
                self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.cling_version, self.cling_repo_url, self._cling_source_subfolder))
                with tools.chdir(self._cling_source_subfolder):
                    self.run('git checkout {}'.format(self.cling_version))
                self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.clang_version, self.clang_repo_url, self._clang_source_subfolder))
                with tools.chdir(self._clang_source_subfolder):
                    self.run('git checkout {}'.format(self.clang_version))

    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        cmake.verbose = True

        # don't hang all CPUs and force OS to kill build process
        cpu_count = max(tools.cpu_count() - 3, 1)
        self.output.info('Detected %s CPUs' % (cpu_count))

        cmake.definitions["LLVM_INSTALL_CCTOOLS_SYMLINKS"]="OFF"
        cmake.definitions["LLVM_INSTALL_BINUTILS_SYMLINKS"]="OFF"
        cmake.definitions["LLVM_INSTALL_UTILS"]="OFF"

        # cmake.definitions["LLVM_INCLUDE_TOOLS"]="OFF"
        # cmake.definitions["LLVM_BUILD_TOOLS"]="OFF"

        # see Building LLVM with CMake https://llvm.org/docs/CMake.html
        cmake.definitions["LLVM_PARALLEL_COMPILE_JOBS"]=cpu_count
        cmake.definitions["LLVM_COMPILER_JOBS"]=cpu_count
        cmake.definitions["LLVM_PARALLEL_LINK_JOBS"]=1
        #cmake.definitions["LLVM_LINK_LLVM_DYLIB"]=1

        # see https://www.productive-cpp.com/improving-cpp-builds-with-split-dwarf/
        #cmake.definitions["LLVM_USE_SPLIT_DWARF"]="ON"

        # force Release build
        #cmake.definitions["CMAKE_BUILD_TYPE"]="Release"

        if self.options.link_ltinfo:
            # https://github.com/MaskRay/ccls/issues/556
            cmake.definitions["CMAKE_CXX_LINKER_FLAGS"]="-ltinfo"

        cmake.definitions["CMAKE_CXX_STANDARD"]="17"
        cmake.definitions["BUILD_SHARED_LIBS"]="OFF"
        #cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"]="ON"
        cmake.definitions["BUILD_TESTS"]="OFF"
        cmake.definitions["LLVM_BUILD_TESTS"]="OFF"
        cmake.definitions["LLVM_BUILD_EXAMPLES"]="OFF"
        cmake.definitions["LLVM_INCLUDE_TESTS"]="OFF"
        cmake.definitions["LLVM_INCLUDE_BENCHMARKS"]="OFF"
        cmake.definitions["LLVM_INCLUDE_EXAMPLES"]="OFF"
        cmake.definitions["LLVM_ENABLE_DOXYGEN"]="OFF"
        #cmake.definitions["LLVM_ENABLE_RTTI"]="OFF"
        cmake.definitions["LLVM_ENABLE_RTTI"]="ON"
        cmake.definitions["LLVM_OPTIMIZED_TABLEGEN"]="ON"
        cmake.definitions["LLVM_ENABLE_ASSERTIONS"]="OFF"

        # clang clang-tools-extra libunwind lld compiler-rt
        # cmake.definitions["LLVM_ENABLE_PROJECTS"]="clang;libcxx;libcxxabi"

        # https://bugs.llvm.org/show_bug.cgi?id=44074
        cmake.definitions["EXECUTION_ENGINE_USE_LLVM_UNWINDER"]="ON"

        # # allow changing clang version by environment variables `CC` and `CXX`, fallback to `clang`
        # cmake.definitions["CMAKE_C_COMPILER"]="clang-6.0" if ("CC" not in os.environ) else os.environ['CC']
        # cmake.definitions["CMAKE_CXX_COMPILER"]="clang++-6.0" if ("CXX" not in os.environ) else os.environ['CXX']
        # cmake.definitions["LLVM_ENABLE_LLD"]="ON"
        # # LLVM_ENABLE_LIBCXX build parameter to compile using libc++ instead of the system default
        # cmake.definitions["LLVM_ENABLE_LIBCXX"]="ON"

        # LLVM_ENABLE_LLD
        
        # Keep symbols for JIT resolution
        #cmake.definitions["LLVM_NO_DEAD_STRIP"]="1"

        #cmake.definitions["CMAKE_INSTALL_PREFIX"]="../release"
        #cmake.definitions["CMAKE_BUILD_TYPE"]="Release"

        #if self.settings.compiler == 'gcc':
        #    cmake.definitions["CMAKE_C_COMPILER"] = "gcc-{}".format(
        #        self.settings.compiler.version)
        #    cmake.definitions["CMAKE_CXX_COMPILER"] = "g++-{}".format(
        #        self.settings.compiler.version)

        #cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = 'conan_paths.cmake'

        # The CMakeLists.txt file must be in `source_folder`
        cmake.configure(source_folder=self._llvm_source_subfolder)

        return cmake

    # Importing files copies files from the local store to your project.
    def imports(self):
        dest = os.getenv("CONAN_IMPORT_PATH", "bin")
        self.output.info("CONAN_IMPORT_PATH is ${CONAN_IMPORT_PATH}")
        self.copy("license*", dst=dest, ignore_case=True)
        self.copy("*.dll", dst=dest, src="bin")
        self.copy("*.so", dst=dest, src="bin")
        self.copy("*.dylib*", dst=dest, src="lib")
        self.copy("*.lib*", dst=dest, src="lib")
        self.copy("*.a*", dst=dest, src="lib")

    def build(self):   
        with tools.vcvars(self.settings, only_diff=False): # https://github.com/conan-io/conan/issues/6577         
            #with tools.chdir(self._llvm_source_subfolder):
            #    with tools.chdir(self._cling_source_subfolder):

            #tools.patch(base_path=self._source_subfolder, patch_file='0001-compiler-options.patch')
            #tools.patch(base_path=self._llvm_source_subfolder, patch_file='0002-clang-cling-conan-support.patch')
            cmake = self._configure_cmake()

            # don't hang all CPUs and force OS to kill build process
            cpu_count = max(tools.cpu_count() - 2, 1)
            self.output.info('Detected %s CPUs' % (cpu_count))

            # -j flag for parallel builds
            cmake.build(args=["--", "-j%s" % cpu_count])

    def package(self):
        with tools.vcvars(self.settings, only_diff=False): # https://github.com/conan-io/conan/issues/6577     
            self.copy(pattern=self._llvm_source_subfolder, dst="src", src=self.build_folder)
            self.copy(pattern="LICENSE", dst="licenses", src=self._llvm_source_subfolder)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.h", dst="include", src="include", keep_path=True)

            # need to copy lib/cmake/cling/ClingTargets.cmake required by ClingConfig.cmake
            self.copy('*', src='%s/lib/cmake' % (self.build_folder), dst='lib/cmake')

            #if self.settings.os_build == 'Darwin':
            #    libext = 'dylib'
            #elif self.settings.os_build == 'Linux':
            #    libext = 'so'

            #self.copy('*', src='%s/include'  % self.install_dir, dst='include')

            #for f in list(llvm_libs.keys()):
            #    self.copy('lib%s.%s' % (f, libext), src='%s/lib' % self._llvm_source_subfolder, dst='lib')
            #self.copy('*', src='%s/lib/clang/%s/lib/darwin' % (self._llvm_source_subfolder, self.llvm_source_version), dst='lib/clang/%s/lib/darwin' % self.llvm_source_version)
            # Yes, these are include files that need to be copied to the lib folder.
            #self.copy('*', src='%s/lib/clang/%s/include' % (self._llvm_source_subfolder, self.llvm_source_version), dst='lib/clang/%s/include' % self.llvm_source_version)

            cmake = self._configure_cmake()
            cmake.install()

    # NOTE: do not append packaged paths to env_info.PATH, env_info.LD_LIBRARY_PATH, etc.
    # because it can conflict with system compiler
    # https://stackoverflow.com/q/54273632
    def package_info(self):
        #self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.libs.sort(reverse=True)

        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin", "libexec"]
        #self.env_info.LD_LIBRARY_PATH.append(
        #    os.path.join(self.package_folder, "lib"))
        #self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        #for libpath in self.deps_cpp_info.lib_paths:
        #    self.env_info.LD_LIBRARY_PATH.append(libpath)

        if self.settings.os_build == "Linux":
            self.cpp_info.system_libs.extend(["pthread", "unwind", "z", "m", "dl", "ncurses", "tinfo"])
            if self.settings.compiler == "clang" and self._libcxx == "libstdc++":
                self.cpp_info.system_libs.append("atomic")
        elif self.settings.os_build == "Windows" and self.settings.compiler == "Visual Studio":
            self.cpp_info.system_libs.extend(["ws2_32", "Iphlpapi", "Crypt32"])

        if (self.settings.os_build == "Linux" and self.settings.compiler == "clang" and
           Version(self.settings.compiler.version.value) == "6" and self._libcxx == "libstdc++") or \
           (self.settings.os_build == "Macos" and self.settings.compiler == "apple-clang" and
           Version(self.settings.compiler.version.value) == "9.0" and self._libcxx == "libc++"):
            self.cpp_info.system_libs.append("atomic")

        self.cpp_info.includedirs.append(os.path.join(self.package_folder, "include"))
        self.cpp_info.includedirs.append(self.package_folder)        

        self.cpp_info.libdirs.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libdirs.append(self.package_folder)

        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        #self.env_info.PATH.append(bindir)

        libdir = os.path.join(self.package_folder, "lib")
        self.output.info("Appending PATH environment variable: {}".format(libdir))
        #self.env_info.PATH.append(libdir)

        enabled_cling_libs = [library for library in cling_libs \
          if getattr(self.options, 'with_' + library)]
        self.output.info('Enabled LLVM libs: {}'.format(', '.join(enabled_cling_libs)))
        self.cpp_info.libs.extend(enabled_cling_libs)

        enabled_llvm_libs = [library for library in llvm_libs \
          if getattr(self.options, 'with_' + library)]
        self.output.info('Enabled LLVM libs: {}'.format(', '.join(enabled_llvm_libs)))
        self.cpp_info.libs.extend(enabled_llvm_libs)

        #self.cpp_info.libs += ['c++abi']
        #self.cpp_info.libs.remove('profile_rt')
        #self.cpp_info.libs = [lib for lib in self.cpp_info.libs if "profile_rt" not in lib]

        #self.cpp_info.defines += ['LLVMDIR=%s' % (cpu_count)]

        self.output.info("LIBRARIES: %s" % self.cpp_info.libs)
        self.output.info("Package folder: %s" % self.package_folder)
        self.env_info.CONAN_CLING_ROOT = self.package_folder

    # We use Cling as library, so compiler settings and arch matter!
    # You must use same CXX ABI as Cling libs
    # otherwise you will get link errors!
    def package_id(self):
        self.info.include_build_settings()
        if self.settings.os_build == "Windows":
            del self.info.settings.arch_build # same build is used for x86 and x86_64
