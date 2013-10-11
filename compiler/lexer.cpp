//
//  lexer.cpp
//  kaleidoscope
//
//  Created by Daniel Hardman on 8/27/13.
//  Copyright (c) 2013 Daniel Hardman. All rights reserved.
//

#include <cstdlib> //for strtod
#include <string>
#include "lexer.h"

void lexer::init(char * source) {
    text = source;
    p = text;
}

void lexer::init(char const * source) {
    size_t char_count = strlen(source) + 1;
    text = new char[char_count];
    p = text;
    memcpy(text, source, char_count);
}

lexer::lexer(char * source) {
    init(source);
}

lexer::lexer(char const * source) {
    init(source);
}

lexer::lexer(std::string const & source) {
    init(source.c_str());
}

lexer::lexer(FILE * f) {
    if (f) {
        if (fseek(f, 0, SEEK_END) == 0) {
            size_t file_len = ftell(f);
            const size_t MAX_FILE_SIZE = 1024 * 1024;
            if (file_len > 0 && file_len < MAX_FILE_SIZE) {
                if (fseek(f, 0, SEEK_SET) == 0) {
                    char * data = new char[file_len + 1];
                    if (fread(data, 1, file_len, f) > 0) {
                        init(data);
                        return;
                    }
                }
            }
        }
    }
    init("");
}

lexer::~lexer() {
    delete[] text;
}

int lexer::get_next_token() {
    // Skip any whitespace.
    while (isspace(*p)) {
        ++p;
    }
    if (isalpha(*p)) { // identifier: [a-zA-Z][a-zA-Z0-9]*
        identifier.clear();
        do {
            identifier += *p++;
        } while (isalnum(*p));
                
        if (identifier == "def") {
            return tok_def;
        }
        if (identifier == "extern") {
            return tok_extern;
        }
        return tok_identifier;
    }
    
    if (isdigit(*p) || *p == '.') {   // Number: [0-9.]+
        std::string s;
        do {
            s += *p;
            ++p;
        } while (isdigit(*p) || *p == '.');
        
        num_val = strtod(s.c_str(), 0);
        return tok_number;
    }
    
    if (*p == '#') {
        // Comment until end of line.
        do {
            ++p;
        } while (*p && *p != '\n' && *p != '\r');
        
        if (*p)
            return get_next_token();
        }
    
    // Check for end of file.  Don't eat the EOF.
    if (*p == 0) {
        return tok_eof;
    }
    
    // Otherwise, just return the character as its ascii value.
    return *p++;
}
