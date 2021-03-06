#include "ast.h"

#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/Analysis/Verifier.h"

using namespace llvm;

Module *TheModule;
static IRBuilder<> Builder(getGlobalContext());
static std::map<std::string, Value*> NamedValues;




NumberExprAST::NumberExprAST(double val) : Val(val) {
}

Value *NumberExprAST::Codegen() {
    return ConstantFP::get(getGlobalContext(), APFloat(Val));
}



PrototypeAST::PrototypeAST(const std::string &name, const std::vector<std::string> &args):
    Name(name), Args(args) {
}

Function *PrototypeAST::Codegen() {
    // Make the function type:  double(double,double) etc.
    std::vector<Type*> Doubles(Args.size(),
                               Type::getDoubleTy(getGlobalContext()));
    FunctionType * FT = FunctionType::get(Type::getDoubleTy(getGlobalContext()),
                                         Doubles, false);
    
    Function * F = Function::Create(FT, Function::ExternalLinkage, Name, TheModule);
    
    // If F conflicted, there was already something named 'Name'.  If it has a
    // body, don't allow redefinition or reextern.
    if (F->getName() != Name) {
        // Delete the one we just made and get the existing one.
        F->eraseFromParent();
        F = TheModule->getFunction(Name);
        
        // If F already has a body, reject this.
        if (!F->empty()) {
            ErrorF("redefinition of function");
            return 0;
        }
        
        // If F took a different number of args, reject.
        if (F->arg_size() != Args.size()) {
            ErrorF("redefinition of function with different # args");
            return 0;
        }
    }
    
    // Set names for all arguments.
    unsigned Idx = 0;
    for (Function::arg_iterator AI = F->arg_begin(); Idx != Args.size();
         ++AI, ++Idx) {
        AI->setName(Args[Idx]);
        
        // Add arguments to variable symbol table.
        NamedValues[Args[Idx]] = AI;
    }
    
    return F;
}



Function *FunctionAST::Codegen() {
    NamedValues.clear();
    
    Function *TheFunction = Proto->Codegen();
    if (TheFunction == 0)
        return 0;
    
    // Create a new basic block to start insertion into.
    BasicBlock *BB = BasicBlock::Create(getGlobalContext(), "entry", TheFunction);
    Builder.SetInsertPoint(BB);
    
    if (Value *RetVal = Body->Codegen()) {
        // Finish off the function.
        Builder.CreateRet(RetVal);
        
        // Validate the generated code, checking for consistency.
        verifyFunction(*TheFunction);
        
        return TheFunction;
    }
    
    // Error reading body, remove function.
    TheFunction->eraseFromParent();
    return 0;
}

FunctionAST::FunctionAST(PrototypeAST *proto, ExprAST *body)
    : Proto(proto), Body(body) {
}



ExprAST * Error(const char *str) {
    fprintf(stderr, "Error: %s\n", str);
    return 0;
}

PrototypeAST * ErrorP(const char *str) {
    Error(str);
    return 0;
}

FunctionAST * ErrorF(const char *str) {
    Error(str);
    return 0;
}

Value *ErrorV(const char *Str) {
    Error(Str); return 0;
}



Value *VariableExprAST::Codegen() {
    // Look this variable up in the function.
    Value *V = NamedValues[Name];
    return V ? V : ErrorV("Unknown variable name");
}



BinaryExprAST::BinaryExprAST(char op, ExprAST *lhs, ExprAST *rhs)
: Op(op), LHS(lhs), RHS(rhs) {
}

Value *BinaryExprAST::Codegen() {
    Value *L = LHS->Codegen();
    Value *R = RHS->Codegen();
    if (L == 0 || R == 0) return 0;
    
    switch (Op) {
        case '+': return Builder.CreateFAdd(L, R, "addtmp");
        case '-': return Builder.CreateFSub(L, R, "subtmp");
        case '*': return Builder.CreateFMul(L, R, "multmp");
        case '<':
            L = Builder.CreateFCmpULT(L, R, "cmptmp");
            // Convert bool 0/1 to double 0.0 or 1.0
            return Builder.CreateUIToFP(L, Type::getDoubleTy(getGlobalContext()),
                                        "booltmp");
        default: return ErrorV("invalid binary operator");
    }
}



CallExprAST::CallExprAST(const std::string &callee, std::vector<ExprAST*> &args):
    Callee(callee), Args(args) {
}

Value *CallExprAST::Codegen() {
    // Look up the name in the global module table.
    Function *CalleeF = TheModule->getFunction(Callee);
    if (CalleeF == 0)
        return ErrorV("Unknown function referenced");
    
    // If argument mismatch error.
    if (CalleeF->arg_size() != Args.size())
        return ErrorV("Incorrect # arguments passed");
    
    std::vector<Value*> ArgsV;
    for (size_t i = 0, e = Args.size(); i != e; ++i) {
        ArgsV.push_back(Args[i]->Codegen());
        if (ArgsV.back() == 0) return 0;
    }
    
    return Builder.CreateCall(CalleeF, ArgsV, "calltmp");
}
