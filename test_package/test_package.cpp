#include <cstdlib>
#include <iostream>
#include <iterator>
#include <exception>
#include <string>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <memory>
#include <vector>

// __has_include is currently supported by GCC and Clang. However GCC 4.9 may have issues and
// returns 1 for 'defined( __has_include )', while '__has_include' is actually not supported:
// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63662
#if __has_include(<filesystem>)
#include <filesystem>
#else
#include <experimental/filesystem>
#endif // __has_include

#include <cling/Interpreter/Interpreter.h>
#include <cling/Interpreter/Value.h>
#include "cling/Interpreter/CIFactory.h"
#include "cling/Interpreter/Interpreter.h"
#include "cling/Interpreter/InterpreterCallbacks.h"
#include "cling/Interpreter/Transaction.h"
#include "cling/Interpreter/Value.h"
#include "cling/Interpreter/CValuePrinter.h"
#include "cling/MetaProcessor/MetaProcessor.h"
#include <cling/Utils/Casting.h>
#include "cling/Interpreter/LookupHelper.h"
#include "cling/Utils/AST.h"
#include <cling/Interpreter/Interpreter.h>
#include <cling/Interpreter/Value.h>
#include "cling/Interpreter/CIFactory.h"
#include "cling/Interpreter/Interpreter.h"
#include "cling/Interpreter/InterpreterCallbacks.h"
#include "cling/Interpreter/Transaction.h"
#include "cling/Interpreter/Value.h"
#include "cling/Interpreter/CValuePrinter.h"
#include "cling/MetaProcessor/MetaProcessor.h"
#include <cling/Utils/Casting.h>
#include "cling/Interpreter/LookupHelper.h"
#include "cling/Utils/AST.h"

#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <clang/ASTMatchers/ASTMatchersMacros.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Basic/SourceManager.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <clang/ASTMatchers/ASTMatchersMacros.h>
#include <clang/AST/Type.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Basic/FileManager.h>
#include <clang/Basic/LangOptions.h>
#include <clang/Basic/SourceManager.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Lex/Lexer.h>
#include <clang/Frontend/FrontendAction.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Driver/Options.h>
#include <clang/AST/AST.h>
#include <clang/AST/ASTContext.h>
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/CommonOptionsParser.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Lex/Lexer.h>
#include <clang/Frontend/FrontendAction.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Driver/Options.h>
#include <clang/AST/AST.h>
#include <clang/AST/ASTContext.h>
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/CommonOptionsParser.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <clang/ASTMatchers/ASTMatchersMacros.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Basic/SourceManager.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <clang/ASTMatchers/ASTMatchersMacros.h>
#include <clang/AST/Type.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Basic/FileManager.h>
#include <clang/Basic/LangOptions.h>
#include <clang/Basic/SourceManager.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Lex/Lexer.h>
#include <clang/Frontend/FrontendAction.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Driver/Options.h>
#include <clang/AST/AST.h>
#include <clang/AST/ASTContext.h>
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/CommonOptionsParser.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Sema/Sema.h>
#include <clang/Lex/Lexer.h>
#include <clang/Frontend/FrontendAction.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Driver/Options.h>
#include <clang/AST/AST.h>
#include <clang/AST/ASTContext.h>
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Frontend/ASTConsumers.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Frontend/CompilerInstance.h>
#include <clang/Tooling/CommonOptionsParser.h>
#include <clang/Tooling/Tooling.h>
#include <clang/Rewrite/Core/Rewriter.h>

template<class T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& v)
{
    copy(v.begin(), v.end(), std::ostream_iterator<T>(os, " "));
    return os;
}


namespace cxxctp {

using MatchResult
  = clang::ast_matchers::MatchFinder::MatchResult;

class AnnotationParser {
public:
  AnnotationParser() = default;
};

class AnnotationMatchHandler {
public:
  AnnotationMatchHandler(
    AnnotationParser* annotationParser);

  // may be used to rewrite matched clang declaration
  void matchHandler(
    clang::AnnotateAttr*
    , const cxxctp::MatchResult&
    , clang::Rewriter&
    , const clang::Decl*);

  // may be used to save result after clang-rewrite
  void endSourceFileHandler(
    const clang::FileID&
    , const clang::FileEntry*
    , clang::Rewriter&);

private:
  AnnotationParser* annotationParser_;
};


AnnotationMatchHandler::AnnotationMatchHandler(
  AnnotationParser* annotationParser)
  : annotationParser_(annotationParser)
{
}

void AnnotationMatchHandler::matchHandler(
  clang::AnnotateAttr* annotateAttr
  , const cxxctp::MatchResult& matchResult
  , clang::Rewriter& rewriter
  , const clang::Decl* nodeDecl)
{
}

void AnnotationMatchHandler::endSourceFileHandler(
  const clang::FileID& fileID
  , const clang::FileEntry* fileEntry
  , clang::Rewriter& rewriter)
{
}

class AnnotationMatchOptions
{
 public:
  AnnotationMatchOptions(
    std::string annotateName);

  // name of |clang::AnnotateAttr| to find
  std::string annotateName;

private:
 ~AnnotationMatchOptions() = default;
};

// Called when the |Match| registered for |clang::AnnotateAttr|
// was successfully found in the AST.
class AnnotateMatchCallback
  : public clang::ast_matchers::MatchFinder::MatchCallback
{
public:
  AnnotateMatchCallback(
    clang::Rewriter &rewriter);

  void run(const MatchResult& Result) override;

private:
  clang::Rewriter& rewriter_;
};

// The ASTConsumer will read AST.
// It provides many interfaces to be overridden when
// certain type of AST node has been parsed,
// or after all the translation unit has been parsed.
class AnnotateConsumer
  : public clang::ASTConsumer
{
public:
  explicit AnnotateConsumer(
    clang::Rewriter &Rewriter);

  ~AnnotateConsumer() override = default;

  // HandleTranslationUnit() called only after
  // the entire source file is parsed.
  // Translation unit effectively represents an entire source file.
  void HandleTranslationUnit(clang::ASTContext &Context) override;

private:
  clang::ast_matchers::MatchFinder matchFinder;
};

// We choose an ASTFrontendAction because we want to analyze
// the AST representation of the source code
class AnnotationMatchAction
  : public clang::ASTFrontendAction
{
public:
  using ASTConsumerPointer = std::unique_ptr<clang::ASTConsumer>;

  explicit AnnotationMatchAction();

  ASTConsumerPointer CreateASTConsumer(
    // pass a pointer to the CompilerInstance because
    // it contains a lot of contextual information
    clang::CompilerInstance&
    , llvm::StringRef filename) override;

  bool BeginSourceFileAction(
    // pass a pointer to the CompilerInstance because
    // it contains a lot of contextual information
    clang::CompilerInstance&) override;

  void EndSourceFileAction() override;

private:
  // Rewriter lets you make textual changes to the source code
  clang::Rewriter rewriter_;
};

// frontend action will only consume AST and find all declarations
struct AnnotationMatchFactory
  : public clang::tooling::FrontendActionFactory
{
  AnnotationMatchFactory();

  clang::FrontendAction* create() override;
};

class ClingInterpreter {
public:
  ClingInterpreter(const std::string& debug_id
                   , const std::vector<std::string>& interpreterArgs
                   , const std::vector<std::string>& includePaths);

  // Allows to load files by path like:
  // "../resources/cxtpl/CXTPL_STD.cpp",
  // "../resources/ctp_scripts/app_loop.cpp"
  cling::Interpreter::CompilationResult
    loadFile(const std::string& filePath);

  // |cling::Value| Will hold the result of the expression evaluation.
  cling::Interpreter::CompilationResult
    processCodeWithResult(
      const std::string& code
      , cling::Value& result);

  cling::Interpreter::CompilationResult
    executeCodeNoResult(const std::string& code);

  /// \note requires to wrap all arguments into struct or class
  /// and cast them into |void*|
  /// \note pass as |codeToCastArgumentFromVoid| string similar to:
  /// *(const originalType*)
  /// That way you will cast |void*| to |originalType|
  /// Don't forget to |#include| header with |originalType|
  /// declaration in file loaded by |loadFile|. It must contain
  /// function that you want to call
  /// \note use can use |processCodeWithResult| to call function
  /// without arguments
  cling::Interpreter::CompilationResult
    callFunctionByName(
      const std::string& funcName
      , void* argumentAsVoid
      , const std::string& codeToCastArgumentFromVoid
      , cling::Value& result);

private:
  std::string debug_id_;

  std::unique_ptr<cling::Interpreter> interpreter_;

  std::unique_ptr<cling::MetaProcessor> metaProcessor_;
};

ClingInterpreter::ClingInterpreter(
  const std::string& debug_id
  , const std::vector<std::string>& interpreterArgs
  , const std::vector<std::string>& includePaths)
  : debug_id_(debug_id)
{
  /// \todo
  /// refactor vector<std::string> to vector<const char*> conversion
  std::vector< const char* > interp_args;
  {
      std::vector< std::string >::const_iterator iarg;
      for( iarg = interpreterArgs.begin()
           ; iarg != interpreterArgs.end() ; ++iarg ) {
          interp_args.push_back(iarg->c_str());
      }
  }

  interpreter_
    = std::make_unique<cling::Interpreter>(
        interp_args.size()
        , &(interp_args[0])
        , LLVMDIR);

  for(const std::string& it: includePaths) {
    interpreter_->AddIncludePath(it.c_str());
  }

  interpreter_->enableDynamicLookup(true);

  metaProcessor_
    = std::make_unique<cling::MetaProcessor>(
        *interpreter_, llvm::outs());

  {
    cling::Interpreter::CompilationResult compilationResult
      = interpreter_->process("#define CLING_IS_ON 1");
  }
}

cling::Interpreter::CompilationResult
  ClingInterpreter::loadFile(
    const std::string& filePath)
{
  cling::Interpreter::CompilationResult compilationResult;

  {
    int res = metaProcessor_->process(
      // input_line - the user input
      ".L " + filePath
      // compRes - whether compilation was successful
      , compilationResult
      // result - the cling::Value as result
      // of the execution of the last statement
      , nullptr
      // disableValuePrinting - whether to suppress echoing of the
      // expression result
      , true);
  }

  return compilationResult;
}

cling::Interpreter::CompilationResult
  ClingInterpreter::processCodeWithResult(
    const std::string& code
    , cling::Value& result)
{
  cling::Interpreter::CompilationResult compilationResult;

  {
    ///\see https://github.com/root-project/cling/blob/master/include/cling/Interpreter/Interpreter.h
    ///
    ///\brief Compiles the given input.
    ///
    /// This interface helps to run everything that cling can run. From
    /// declaring header files to running or evaluating single statements.
    /// Note that this should be used when there is no idea of what kind of
    /// input is going to be processed. Otherwise if is known, for example
    /// only header files are going to be processed it is much faster to run the
    /// specific interface for doing that - in the particular case - declare().
    compilationResult
      = interpreter_->process(
          code.c_str()
          , &result);
  }

  return compilationResult;
}

cling::Interpreter::CompilationResult
  ClingInterpreter::callFunctionByName(
    const std::string& funcName
    , void* argumentAsVoid
    , const std::string& codeToCastArgumentFromVoid
    , cling::Value& result)
{
  cling::Interpreter::CompilationResult compilationResult;

  std::ostringstream code_str;

  {
    // scope begin
    code_str << "[](){";
    code_str << "return ";
    // func begin
    code_str << funcName << "( ";
    // func arguments
    code_str << codeToCastArgumentFromVoid << "("
         // Pass a pointer into cling as a string.
         << std::hex << std::showbase
         << reinterpret_cast<size_t>(argumentAsVoid) << ')';
    // func end
    code_str << " );" << ";";
    // scope end
    code_str << "}();";
  }

  {
    ///\see https://github.com/root-project/cling/blob/master/include/cling/Interpreter/Interpreter.h
    ///
    ///\brief Compiles the given input.
    ///
    /// This interface helps to run everything that cling can run. From
    /// declaring header files to running or evaluating single statements.
    /// Note that this should be used when there is no idea of what kind of
    /// input is going to be processed. Otherwise if is known, for example
    /// only header files are going to be processed it is much faster to run the
    /// specific interface for doing that - in the particular case - declare().
    compilationResult
      = processCodeWithResult(
          code_str.str().c_str()
          , result);
  }
  
  return compilationResult;
}

cling::Interpreter::CompilationResult
  ClingInterpreter::executeCodeNoResult(
    const std::string& code)
{
  cling::Interpreter::CompilationResult compilationResult;

  {
    ///\see https://github.com/root-project/cling/blob/master/include/cling/Interpreter/Interpreter.h
    ///
    ///\brief Compiles input line and runs.
    ///
    /// The interface is the fastest way to compile and run a statement or
    /// expression. It just wraps the input into a function definition and runs
    /// that function, without any other "magic".
    compilationResult
      = interpreter_->execute(
          code.c_str());
  }

  return compilationResult;
}

AnnotationMatchOptions::AnnotationMatchOptions(
  std::string annotateName)
  : annotateName(annotateName)
{}

AnnotateMatchCallback::AnnotateMatchCallback(
  clang::Rewriter &rewriter)
  : rewriter_(rewriter)
{
}

void AnnotateMatchCallback::run(
  const MatchResult& matchResult)
{
  const clang::Decl* nodeDecl
    = matchResult.Nodes.getNodeAs<clang::Decl>(
      "annotateName");
  if (!nodeDecl || nodeDecl->isInvalidDecl()) {
    return;
  }

  // When there is a #include <vector> in the source file,
  // our find-decl will print out all the declarations
  // in that included file, because these included files are parsed
  // and consumed as a whole with our source file.
  // To fix this, we need to check if the declarations
  // are defined in our source file
  {
    clang::SourceManager& SM = rewriter_.getSourceMgr();
    const clang::FileID& mainFileID = SM.getMainFileID();
    const auto& FileID = SM.getFileID(nodeDecl->getLocation());
    if (FileID != mainFileID) {
      return;
    }
  }

  clang::AnnotateAttr* annotateAttr
    = nodeDecl->getAttr<clang::AnnotateAttr>();
}

AnnotateConsumer::AnnotateConsumer(
  clang::Rewriter& rewriter)
{
  using namespace clang::ast_matchers;

  auto hasAnnotateMatcher
    = clang::ast_matchers::hasAttr(clang::attr::Annotate);

  //In Clang, there are two basic types of AST classes:
  // Decl and Stmt, which have many subclasses
  // that covers all the AST nodes we will meet in a source file.
  auto finderMatcher
    = clang::ast_matchers::decl(hasAnnotateMatcher)
      .bind("annotateName");

  //matchFinder.addMatcher(finderMatcher, &annotateMatchCallback_);
}

void AnnotateConsumer::HandleTranslationUnit(
  clang::ASTContext &Context)
{
  matchFinder.matchAST(Context);
}

AnnotationMatchAction::AnnotationMatchAction()
{
}

AnnotationMatchAction::ASTConsumerPointer
  AnnotationMatchAction::CreateASTConsumer(
    clang::CompilerInstance& compilerInstance
    , llvm::StringRef filename)
{
  rewriter_.setSourceMgr(
    compilerInstance.getSourceManager()
    , compilerInstance.getLangOpts());

  return std::make_unique<AnnotateConsumer>(
    rewriter_);
}

bool AnnotationMatchAction::BeginSourceFileAction(
  clang::CompilerInstance&)
{
  return true;
}

void AnnotationMatchAction::EndSourceFileAction()
{
  ASTFrontendAction::EndSourceFileAction();

  clang::SourceManager& SM = rewriter_.getSourceMgr();

  const clang::FileID& mainFileID = SM.getMainFileID();

  const clang::FileEntry* fileEntry
    = SM.getFileEntryForID(mainFileID);
}

AnnotationMatchFactory::AnnotationMatchFactory()
  : FrontendActionFactory() {
}

clang::FrontendAction*
  AnnotationMatchFactory::create()
{
  return new AnnotationMatchAction();
}

} // namespace cxxctp

int main(int argc, char* argv[]) 
{
  std::vector< const char* > args_vec{"clang_app", "-extra-arg=-DCLANG_ENABLED=1", "-help"};

  int args_arc = args_vec.size();

  const char **args_argv = &(args_vec[0]);
  
  // see http://llvm.org/docs/doxygen/html/classllvm_1_1cl_1_1OptionCategory.html
  llvm::cl::OptionCategory UseOverrideCategory("Use override options");

  // parse the command-line args passed to your code
  // see http://clang.llvm.org/doxygen/classclang_1_1tooling_1_1CommonOptionsParser.html
  clang::tooling::CommonOptionsParser op(args_arc, args_argv,
    UseOverrideCategory);
      
  std::vector< const char* > interp_args;
  cling::Interpreter interpreter(interp_args.size()
        , &(interp_args[0])
        , LLVMDIR);

  std::vector<std::string> clingIncludePaths{".", "../"};
  std::vector<std::string> clingInterpreterArgs{"EmbedCling", "-DCLING_ENABLED=1", "-DCLING_IS_ON=1"};

  cxxctp::ClingInterpreter clingInterpreter(
        "MainClingInterpreter_debug_id"
        , clingInterpreterArgs
        , clingIncludePaths);

  return EXIT_SUCCESS;
}
