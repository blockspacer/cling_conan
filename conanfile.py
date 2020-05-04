import os
from conans import ConanFile, CMake, tools
from conans.tools import Version
from conans.errors import ConanInvalidConfiguration

class ClingConan(ConanFile):
    name = "cling_conan"

    version = "master"
    llvm_version = "cling-patches"
    clang_version = "cling-patches"

    #llvm_source_version = "6.0.1"

    description = "conan package for cling https://root.cern.ch/root/htmldoc/guides/users-guide/Cling.html"
    topics = ("c++", "conan", "cling", "clang", "root", "llvm", "cern")
    #url = "https://github.com/bincrafters/conan-folly" # TODO
    #homepage = "https://github.com/facebook/folly" # TODO
    #license = "Apache-2.0" # TODO
    settings = "os", "arch", "compiler", "build_type"
    
    options = {"shared": [True, False], "fPIC": [True, False]}

    default_options = {
        "shared": False,
        "fPIC": True,
        "*:shared": False,
        "openssl:shared": True
    }

    exports = ["LICENSE.md"]

    exports_sources = ["LICENSE", "README.md", "include/*", "src/*",
                       "cmake/*", "CMakeLists.txt", "tests/*", "benchmarks/*",
                       "scripts/*"]

    generators = 'cmake_find_package', "cmake", "cmake_paths"
    
    llvm_repo_url = "http://root.cern.ch/git/llvm.git"
    cling_repo_url = "http://root.cern.ch/git/cling.git"
    clang_repo_url = "http://root.cern.ch/git/clang.git"

    llvm_libs = {
        'LLVMAnalysis': 0,
        #'LLVMArchive': 0,
        'LLVMAsmParser': 0,
        'LLVMAsmPrinter': 0,
        'LLVMBitReader': 0,
        'LLVMBitWriter': 0,
        'LLVMCodeGen': 0,
        'LLVMCore': 0,
        #'LLVMDebugInfo': 0,
        'LLVMExecutionEngine': 0,
        'LLVMIRReader': 0,
        'LLVMInstCombine': 0,
        'LLVMInstrumentation': 0,
        'LLVMInterpreter': 0,
        #'LLVMJIT': 0,
        'LLVMLinker': 0,
        'LLVMMC': 0,
        'LLVMMCDisassembler': 0,
        'LLVMMCJIT': 0,
        'LLVMMCParser': 0,
        'LLVMObjCARCOpts': 0,
        'LLVMObject': 0,
        'LLVMOption': 0,
        'LLVMRuntimeDyld': 0,
        'LLVMScalarOpts': 0,
        'LLVMSelectionDAG': 0,
        'LLVMSupport': 0,
        'LLVMTableGen': 0,
        'LLVMTarget': 0,
        'LLVMTransformUtils': 0,
        'LLVMVectorize': 0,
        'LLVMX86AsmParser': 0,
        'LLVMX86AsmPrinter': 0,
        'LLVMX86CodeGen': 0,
        'LLVMX86Desc': 0,
        'LLVMX86Disassembler': 0,
        'LLVMX86Info': 0,
        'LLVMX86Utils': 0,
        #'LLVMipa': 0,
        'LLVMipo': 0,
        'LTO': 0,
        #'c++': 0,
        'clang': 0,
        'clangARCMigrate': 0,
        'clangAST': 0,
        'clangASTMatchers': 0,
        'clangAnalysis': 0,
        'clangBasic': 0,
        'clangCodeGen': 0,
        'clangDriver': 0,
        'clangEdit': 0,
        'clangFormat': 0,
        'clangFrontend': 0,
        'clangFrontendTool': 0,
        'clangLex': 0,
        'clangParse': 0,
        #'clangRewriteCore': 0,
        'clangRewriteFrontend': 0,
        'clangSema': 0,
        'clangSerialization': 0,
        'clangStaticAnalyzerCheckers': 0,
        'clangStaticAnalyzerCore': 0,
        'clangStaticAnalyzerFrontend': 0,
        'clangTooling': 0,
        'profile_rt': 0,
    }

    cling_libs = {
        'clingInterpreter': 0,
        'clingMetaProcessor': 0,
        # /usr/lib/x86_64-linux-gnu/libdl.so: error adding symbols: DSO missing from command line
        #'clingUtils': 0,
        'cling': 0,
    }

    # conan search double-conversion* -r=conan-center
#    requires = (
#        "openssl/OpenSSL_1_1_1-stable@conan/stable",
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

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.shared
        elif self.settings.os == "Macos":
            del self.options.shared

    def configure(self):
        compiler_version = Version(self.settings.compiler.version.value)

    def requirements(self):
        print('self.settings.compiler {}'.format(self.settings.compiler))

    def source(self):
        # see https://root.cern.ch/cling-build-instructions
        self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.llvm_version, self.llvm_repo_url, self._llvm_source_subfolder))
        with tools.chdir(self._llvm_source_subfolder):
            self.run('git checkout {}'.format(self.llvm_version))
            with tools.chdir("tools"):
                self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.version, self.cling_repo_url, self._cling_source_subfolder))
                with tools.chdir(self._cling_source_subfolder):
                    self.run('git checkout {}'.format(self.version))
                self.run('git clone -b {} --progress --depth 100 --recursive --recurse-submodules {} {}'.format(self.clang_version, self.clang_repo_url, self._clang_source_subfolder))
                with tools.chdir(self._clang_source_subfolder):
                    self.run('git checkout {}'.format(self.clang_version))

    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        cmake.verbose = True

        # don't hang all CPUs and force OS to kill build process
        cpu_count = max(tools.cpu_count() - 3, 1)
        self.output.info('Detected %s CPUs' % (cpu_count))

        # see Building LLVM with CMake https://llvm.org/docs/CMake.html
        cmake.definitions["LLVM_PARALLEL_COMPILE_JOBS"]=cpu_count
        cmake.definitions["LLVM_COMPILER_JOBS"]=cpu_count
        cmake.definitions["LLVM_PARALLEL_LINK_JOBS"]=1
        #cmake.definitions["LLVM_LINK_LLVM_DYLIB"]=1

        # see https://www.productive-cpp.com/improving-cpp-builds-with-split-dwarf/
        cmake.definitions["LLVM_USE_SPLIT_DWARF"]="ON"

        cmake.definitions["CMAKE_CXX_STANDARD"]="17"
        cmake.definitions["BUILD_SHARED_LIBS"]="OFF"
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"]="ON"
        cmake.definitions["BUILD_TESTS"]="OFF"
        #cmake.definitions["LLVM_BUILD_TOOLS"]="OFF"
        cmake.definitions["LLVM_BUILD_TOOLS"]="ON"
        cmake.definitions["LLVM_BUILD_TESTS"]="OFF"
        cmake.definitions["LLVM_BUILD_EXAMPLES"]="OFF"
        cmake.definitions["LLVM_INCLUDE_TESTS"]="OFF"
        cmake.definitions["LLVM_INCLUDE_BENCHMARKS"]="OFF"
        cmake.definitions["LLVM_INCLUDE_EXAMPLES"]="OFF"
        cmake.definitions["LLVM_ENABLE_DOXYGEN"]="OFF"
        cmake.definitions["LLVM_ENABLE_RTTI"]="OFF"
        cmake.definitions["LLVM_OPTIMIZED_TABLEGEN"]="ON"
        cmake.definitions["LLVM_ENABLE_ASSERTIONS"]="OFF"
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
        self.output.info('self.settings.os: %s' % (self.settings.os))
        self.output.info('self.settings.build_type: %s' % (self.settings.build_type))

        self.copy(pattern=self._llvm_source_subfolder, dst="src", src=self.build_folder)
        self.copy(pattern="LICENSE", dst="licenses", src=self._llvm_source_subfolder)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.h", dst="include", src="include", keep_path=True)

        #if self.settings.os == 'Darwin':
        #    libext = 'dylib'
        #elif self.settings.os == 'Linux':
        #    libext = 'so'

        #self.copy('*', src='%s/include'  % self.install_dir, dst='include')

        #for f in list(self.llvm_libs.keys()):
        #    self.copy('lib%s.%s' % (f, libext), src='%s/lib' % self._llvm_source_subfolder, dst='lib')
        #self.copy('*', src='%s/lib/clang/%s/lib/darwin' % (self._llvm_source_subfolder, self.llvm_source_version), dst='lib/clang/%s/lib/darwin' % self.llvm_source_version)
        # Yes, these are include files that need to be copied to the lib folder.
        #self.copy('*', src='%s/lib/clang/%s/include' % (self._llvm_source_subfolder, self.llvm_source_version), dst='lib/clang/%s/include' % self.llvm_source_version)

        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)        
        self.cpp_info.libs.sort(reverse=True)

        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.env_info.LD_LIBRARY_PATH.append(
            os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        for libpath in self.deps_cpp_info.lib_paths:
            self.env_info.LD_LIBRARY_PATH.append(libpath)

        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "m", "dl"])
            if self.settings.compiler == "clang" and self.settings.compiler.libcxx == "libstdc++":
                self.cpp_info.libs.append("atomic")
        elif self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.cpp_info.libs.extend(["ws2_32", "Iphlpapi", "Crypt32"])

        if (self.settings.os == "Linux" and self.settings.compiler == "clang" and
           Version(self.settings.compiler.version.value) == "6" and self.settings.compiler.libcxx == "libstdc++") or \
           (self.settings.os == "Macos" and self.settings.compiler == "apple-clang" and
           Version(self.settings.compiler.version.value) == "9.0" and self.settings.compiler.libcxx == "libc++"):
            self.cpp_info.libs.append("atomic")

        self.cpp_info.includedirs.append(os.path.join(self.package_folder, "include"))
        self.cpp_info.includedirs.append(self.package_folder)        

        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

        libdir = os.path.join(self.package_folder, "lib")
        self.output.info("Appending PATH environment variable: {}".format(libdir))
        self.env_info.PATH.append(libdir)

        self.cpp_info.libs = list(self.cling_libs.keys())
        self.cpp_info.libs += list(self.llvm_libs.keys())
        #self.cpp_info.libs += ['c++abi']
        self.cpp_info.libs.remove('profile_rt')

        #self.cpp_info.defines += ['LLVMDIR=%s' % (cpu_count)]



