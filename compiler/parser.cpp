// These are only required by the Handlexyz functions below. Those functions
// should ultimately be moved into a compiler class, so that the parser's
// responsibility ends when the AST has been built.
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/Analysis/Verifier.h"

using namespace llvm;


#include "parser.h"
#include "lexer.h"

/// BinopPrecedence - This holds the precedence for each binary operator that is
/// defined.
std::map<char, int> & get_binary_operator_precedence_map() {
    static std::map<char, int> theMap;
    static bool inited = false;
    if (!inited) {
        inited = true;
        theMap['<'] = 10;
        theMap['+'] = 20;
        theMap['-'] = 20;
        theMap['*'] = 40;
    }
    return theMap;
}

// Take ownership of specified lexer. Used in testing.
parser::parser(lexer * _lex): lex(_lex) {
}

/// Used to parse a file. Most common invocation.
parser::parser(FILE * source): lex(new lexer(source)) {
}

/// Used to parse an arbitrary, null-terminated buffer.
parser::parser(char * source): lex(new lexer(source)) {
}

/// Mainly used to parse string literals in testing.
parser::parser(char const * source): lex(new lexer(source)) {
}

/// Used to eval() strings.
parser::parser(std::string const & source): lex(new lexer(source)) {
}

parser::~parser() {
    delete lex;
}

int parser::getNextToken() {
    return CurTok = lex->get_next_token();
}

/// GetTokPrecedence - Get the precedence of the pending binary operator token.
int parser::GetTokPrecedence() {
    if (!isascii(CurTok))
        return -1;
    
    // Make sure it's a declared binop.
    std::map<char, int> & binop_map = get_binary_operator_precedence_map();
    int TokPrec = binop_map.operator[](static_cast<char>(CurTok));
    if (TokPrec <= 0) return -1;
    return TokPrec;
}

/// identifierexpr
///   ::= identifier
///   ::= identifier '(' expression* ')'
ExprAST * parser::ParseIdentifierExpr() {
    std::string IdName = lex->identifier;
    
    getNextToken();  // eat identifier.
    
    if (CurTok != '(') // Simple variable ref.
        return new VariableExprAST(IdName);
    
    // Call.
    getNextToken();  // eat (
    std::vector<ExprAST*> Args;
    if (CurTok != ')') {
        while (1) {
            ExprAST *Arg = ParseExpression();
            if (!Arg) return 0;
            Args.push_back(Arg);
            
            if (CurTok == ')') break;
            
            if (CurTok != ',')
                return Error("Expected ')' or ',' in argument list");
            getNextToken();
        }
    }
    
    // Eat the ')'.
    getNextToken();
    
    return new CallExprAST(IdName, Args);
}

/// numberexpr ::= number
ExprAST * parser::ParseNumberExpr() {
    ExprAST *Result = new NumberExprAST(lex->num_val);
    getNextToken(); // consume the number
    return Result;
}

/// parenexpr ::= '(' expression ')'
ExprAST * parser::ParseParenExpr() {
    getNextToken();  // eat (.
    ExprAST *V = ParseExpression();
    if (!V) return 0;
    
    if (CurTok != ')')
        return Error("expected ')'");
    getNextToken();  // eat ).
    return V;
}

/// primary
///   ::= identifierexpr
///   ::= numberexpr
///   ::= parenexpr
ExprAST * parser::ParsePrimary() {
    switch (CurTok) {
        default:
            return Error("unknown token when expecting an expression");
        case tok_identifier:
            return ParseIdentifierExpr();
        case tok_number:
            return ParseNumberExpr();
        case '(':
            return ParseParenExpr();
    }
}

/// binoprhs
///   ::= ('+' primary)*
ExprAST * parser::ParseBinOpRHS(int ExprPrec, ExprAST *LHS) {
    // If this is a binop, find its precedence.
    while (1) {
        int TokPrec = GetTokPrecedence();
        
        // If this is a binop that binds at least as tightly as the current binop,
        // consume it, otherwise we are done.
        if (TokPrec < ExprPrec)
            return LHS;
        
        // Okay, we know this is a binop.
        int BinOp = CurTok;
        getNextToken();  // eat binop
        
        // Parse the primary expression after the binary operator.
        ExprAST *RHS = ParsePrimary();
        if (!RHS) return 0;
        
        // If BinOp binds less tightly with RHS than the operator after RHS, let
        // the pending operator take RHS as its LHS.
        int NextPrec = GetTokPrecedence();
        if (TokPrec < NextPrec) {
            RHS = ParseBinOpRHS(TokPrec+1, RHS);
            if (RHS == 0) return 0;
        }
        
        // Merge LHS/RHS.
        LHS = new BinaryExprAST(BinOp, LHS, RHS);
    }
}

/// expression
///   ::= primary binoprhs
///
ExprAST * parser::ParseExpression() {
    ExprAST *LHS = ParsePrimary();
    if (!LHS) return 0;
    
    return ParseBinOpRHS(0, LHS);
}

/// prototype
///   ::=  id '(' id* ')'
PrototypeAST * parser::ParsePrototype() {
    if (CurTok != tok_identifier)
        return ErrorP("Expected function name in prototype");
    
    std::string FnName = lex->identifier;
    getNextToken();
    
    if (CurTok != '(')
        return ErrorP("Expected '(' in prototype");
    
    std::vector<std::string> ArgNames;
    while (getNextToken() == tok_identifier)
        ArgNames.push_back(lex->identifier);
    if (CurTok != ')')
        return ErrorP("Expected ')' in prototype");
    
    // success.
    getNextToken();  // eat ')'.
    
    return new PrototypeAST(FnName, ArgNames);
}

/// definition ::= 'def' prototype expression
FunctionAST * parser::ParseDefinition() {
    getNextToken();  // eat def.
    PrototypeAST *Proto = ParsePrototype();
    if (Proto == 0) return 0;
    
    if (ExprAST *E = ParseExpression())
        return new FunctionAST(Proto, E);
    return 0;
}

/// toplevelexpr ::= expression
FunctionAST * parser::ParseTopLevelExpr() {
    if (ExprAST *E = ParseExpression()) {
        // Make an anonymous proto.
        PrototypeAST *Proto = new PrototypeAST("", std::vector<std::string>());
        return new FunctionAST(Proto, E);
    }
    return 0;
}

/// external ::= 'extern' prototype
PrototypeAST * parser::ParseExtern() {
    getNextToken();  // eat extern.
    return ParsePrototype();
}

//===----------------------------------------------------------------------===//
// Top-Level parsing
//===----------------------------------------------------------------------===//

void parser::HandleDefinition() {
    if (FunctionAST *F = ParseDefinition()) {
        if (Function *LF = F->Codegen()) {
            fprintf(stderr, "Read function definition:");
            LF->dump();
        }
    } else {
        // Skip token for error recovery.
        getNextToken();
    }
}

void parser::HandleExtern() {
    if (PrototypeAST *P = ParseExtern()) {
        if (Function *F = P->Codegen()) {
            fprintf(stderr, "Read extern: ");
            F->dump();
        }
    } else {
        // Skip token for error recovery.
        getNextToken();
    }
}

void parser::HandleTopLevelExpression() {
    // Evaluate a top-level expression into an anonymous function.
    if (FunctionAST *F = ParseTopLevelExpr()) {
        if (Function *LF = F->Codegen()) {
            fprintf(stderr, "Read top-level expression:");
            LF->dump();
        }
    } else {
        // Skip token for error recovery.
        getNextToken();
    }
}
