#include <iostream>
#include "parser.h"
#include "lexer.h"

using std::cin;
using std::cout;

using namespace llvm;

extern Module *TheModule;

int main() {
    
    LLVMContext &Context = getGlobalContext();
    // Make the module, which holds all the code.
    TheModule = new Module("my cool jit", Context);
    
    std::string code;
    cout << "Enter a snippet: ";
    while (cin) {
        std::getline(cin, code);
    }
    parser parser(code);
    parser.getNextToken();
    bool done = false;
    do {
        switch (parser.CurTok) {
            case tok_eof:
                done = true;
                break;
            case ';':
                parser.getNextToken();
                break;  // ignore top-level semicolons.
            case tok_def:
                parser.HandleDefinition();
                break;
            case tok_extern:
                parser.HandleExtern();
                break;
            default:
                parser.HandleTopLevelExpression();
                break;
        }
    } while (!done);
    
    // Print out all of the generated code.
    TheModule->dump();

    return 0;
}
