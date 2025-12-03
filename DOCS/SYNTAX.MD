      # SYNTAX.MD  OpenQM Language Rules, Corrections, and Compatibility Guide

      ## Table of Contents
1.    [Introduction](#intro)
2.    [How to Use This File](#usage)
3.    [QM BASIC Core Rules](#qm-basic-core-rules)
4.    [QM TCL Rules](#qm-tcl-rules)
5.    [Function & Subroutine Rules](#functions)
6.    [String Handling Rules (CHANGE, FIELD, DCOUNT)](#string-handling)
7.    [Command-Line Semantics: @SENTENCE](#sentence)
8.    [Account Path Semantics: @PATH](#path)
9.    [Directory Files vs OS Paths](#dirs)
10.   [UTF-8 Handling & Cleaning](#utf8)
11.   [QM PROC Limitations](#proc-limitations)
12.   [Common UV  QM Translation Table](#uvqm)
13.   [QM BASIC Quick Reference](#quickref)
14.   [Forbidden UniVerse Features in QM](#forbidden)
15.   [Syntax Errors Encountered in This Project](#errors)

      <a name="intro"></a>
      ## 1. Introduction
      This document contains the verified syntax behaviors, constraints, and differences specific to OpenQM on Windows. Every time a syntax error or incompatibility is detected, an entry is added here to prevent repetition.

      <a name="usage"></a>
      ## 2. How to Use This File
      
      **FOR AI AGENTS - CRITICAL INSTRUCTIONS:**
      1. **READ THIS FILE** before writing ANY QM BASIC or QM TCL code
      2. **CHECK Section 15** for all previously encountered syntax errors
      3. **UPDATE Section 15** immediately when you encounter a new syntax error
      4. **COMMIT UPDATES** to this file so future agents learn from mistakes
      5. Treat as authoritative QM Style Guide for correctness and compatibility
      
      **DO NOT:**
      - Skip reading this file before QM programming
      - Repeat errors listed in Section 15
      - Write code without verifying syntax against this document

      <a name="qm-basic-core-rules"></a>
      ## 3. QM BASIC Core Rules
      - Blank lines are allowed.
      - CHANGE() is a function, not a statement.
      - External functions must be declared: `DEFFUN name(params)`.
      - FUNCTION definitions must appear in separate program files:
      FUNCTION NAME(params)
      ...
      RETURN value
      END
      - SUBROUTINEs are invoked with CALL and do not RETURN values.
      - @SENTENCE contains the entire execution line.
      - @PATH returns the OS directory of the current QM account.
      - QM does not interpret UTF-8; multibyte characters display incorrectly unless cleaned.

      <a name="qm-tcl-rules"></a>
      ## 4. QM TCL Rules
      - QM TCL does not support CAT, TYPE, LIST.LINUX.
      - To view OS files on Windows use: SH TYPE filename
      - PROCs are macro expanders only: no variable assignment, no loops, no SHIFT, no expressions.

      <a name="functions"></a>
      ## 5. Function & Subroutine Rules
      ### Valid:
      DEFFUN CLEAN.UTF8(IN)
      ### Invalid UV syntax:
      DEFFUN CLEAN.UTF8
      CHANGE OLD TO NEW IN STRING
      - Functions must RETURN a value.
      - Subroutines need no declaration in callers.
      - Function definitions cannot appear inline inside another program.

      <a name="string-handling"></a>
      ## 6. String Handling Rules (CHANGE, FIELD, DCOUNT)
      - Valid QM syntax: X = CHANGE(X,"OLD","NEW")
      - UV syntax invalid: CHANGE OLD TO NEW IN X
      - FIELD(), DCOUNT(), SEQ(), LEN() all work normally.

      <a name="sentence"></a>
      ## 7. Command-Line Semantics: @SENTENCE
      OpenQM does not support @ARGS or @COMMAND.LINE.
Correct:
      S = @SENTENCE

      <a name="path"></a>
      ## 8. Account Path Semantics: @PATH
      - @PATH returns the full OS directory for the QM account.
      - Use BASE = @PATH and BASE : "\" : RELPATH
      - Never hardcode C:\ paths.

      <a name="dirs"></a>
      ## 9. Directory Files vs OS Paths
      - QM Directory files map only ONE OS directory.
      - They do not show subdirectories or support recursion.
      - Use OPENSEQ with OS paths for nested directories.

      <a name="utf8"></a>
      ## 10. UTF-8 Handling & Cleaning
      - QM on Windows displays UTF-8 multibyte characters as sequences such as ├─│.
      - Use external function CLEAN.UTF8(IN) to sanitize lines.

      <a name="proc-limitations"></a>
      ## 11. QM PROC Limitations
      - QM PROCs cannot:
      assign variables
      loop
         SHIFT arguments
         evaluate expressions
         concatenate strings
         - PROCs may only emit literal TCL commands.

         <a name="uvqm"></a>
         ## 12. Common UV  QM Translation Table
         | UniVerse Syntax              | QM Equivalent                          | Notes                               |
         |------------------------------|------------------------------------------|-------------------------------------|
         | CHANGE X TO Y IN Z           | Z = CHANGE(Z,"X","Y")                   | QM uses functional form only        |
         | @ARGS                        | *(none)*                                | Use @SENTENCE                       |
         | @COMMAND.LINE                | @SENTENCE                               | UV only                             |
         | TYPE filename                | SH TYPE filename                        | QM TCL lacks TYPE                   |
         | CAT filename                 | SH TYPE filename                        | QM TCL lacks CAT                    |
         | LIST.LINUX                   | *(none)*                                | Not supported                       |
         | PROC variable assignment     | *(not supported)*                       | QM PROCs cannot compute             |
         | Directory recursion in DIR files | *(not supported)*                  | Must recurse using OS-level tools   |

         <a name="quickref"></a>
         ## 13. QM BASIC Quick Reference
         ### File I/O
         OPENSEQ path TO F ELSE STOP
         READSEQ LINE FROM F ELSE EXIT
         WRITESEQ LINE TO F ELSE STOP
         CLOSESEQ F
         ### Conditionals
         IF X = Y THEN
            ...
         END ELSE
            ...
         END
         ### Loops
         LOOP
            ...
         REPEAT
         ### Useful Functions
         CHANGE(string, old, new)
         FIELD(string, delimiter, position)
         DCOUNT(string, delimiter)
         SEQ(char)
         LEN(string)

         <a name="forbidden"></a>
         ## 14. Forbidden UniVerse Features in QM
         - CHANGE X TO Y IN Z
         - @ARGS
         - @COMMAND.LINE
         - Inline FUNCTION definitions inside another program
         - PROC variable assignment, SHIFT, loops, concatenation
         - TCL TYPE/CAT commands
         - Directory recursion through QM directory files

         <a name="errors"></a>
         ## 15. Syntax Errors Encountered in This Project
         
         **CRITICAL: Add ALL new syntax errors here immediately with date and description**
         
1.       **CAT/TYPE in QM TCL** → Must use `SH TYPE filename` on Windows
2.       **PROC logic** (`I=1`, SHIFT, LOOP) → Invalid in QM, use QM BASIC instead
3.       **Recursive directory access** via QM directory files → Not supported, use OS-level tools
4.       **@COMMAND.LINE** → Must use `@SENTENCE` (OpenQM equivalent)
5.       **UV CHANGE statement** → QM requires `CHANGE()` function: `X = CHANGE(X,"OLD","NEW")`
6.       **DEFFUN without parameters** → Must be `DEFFUN NAME(IN)` with parameter list
7.       **Inline FUNCTION inside program** → Must be external in separate file
8.       **UTF-8 corruption** → Garbage characters, resolved using `CLEAN.UTF8()` function
9.       **Directory detection** using `IF EXIST` → Failed, replaced with `DIR /AD`
10.      **Windows command quoting** → Resolved using triple-quote concatenation
11.      **PROC variable assignment** → Invalid, moved logic to BASIC program
12.      **OpenQM Dictionary Format** (2025-12-03) → **CRITICAL: LenJ not JLen!**
         - **WRONG**: "R10", "L30" (JustificationLength)
         - **CORRECT**: "10R", "30L" (LengthJustification)
         - DICT attribute 5 format: **LenJ** where Len=width, J=justification
         - Examples: 10R (10 chars right), 30L (30 chars left), 50T (50 chars text)
         - Applies to: BUILD.SCHEMA automatic format generation
         - Conversion codes in DICT attribute 3: "D4-", "MD2,$", etc.
         
         **Template for new errors:**
         ```
         N. **Error Title** (YYYY-MM-DD) → Solution
            - WRONG: [what doesn't work]
            - CORRECT: [what works]
            - Context: [where this applies]
            - Reference: [file/program affected]
         ```

      # End of SYNTAX.MD
      
      ---
      
      **Last Updated**: 2025-12-03  
      **Maintainers**: All AI agents working on HAL project  
      **Purpose**: Prevent repetition of OpenQM syntax errors

