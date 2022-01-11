%{
#include <stdio.h>
#include <stdlib.h>
#define YYDEBUG 1

#define INT_TYPE 1
#define CHAR_TYPE 2
#define STRING_TYPE 3
#define BOOLEAN_TYPE 4

double stack[20];
char productions[100][100];
int sp;

void push(double x)
{ stack[sp++]=x; }

double pop()
{ return stack[--sp]; }

%}

%union {
  	int l_val;
	char *p_val;
}

%token BEGINN
%token CONST
%token DO
%token ELSE
%token END
%token IF
%token PRINT
%token PROGRAM
%token READ
%token THEN
%token VAR
%token WHILE
%token FOR
%token TO


%token ID
%token <p_val> CONST_INT
%token <p_val> CONST_CHAR
%token <p_val> CONST_BOOL
%token <p_val> CONST_STRING

%token CONST_SIR

%token CHAR
%token INTEGER
%token BOOLEAN
%token STRING

%token ATRIB
%token NE
%token LE
%token GE

%left '+' '-'
%left DIV MOD '*' '/'
%left OR
%left AND
%left NOT

%type <l_val> expr_stat factor_stat constant
%%
program:	PROGRAM ID ';' sourcecode '.' { fprintf(stderr, "=== program -> program id ; sourcecode . ===\n"); }
		;
sourcecode:		const_declarations var_declarations cmpdstmt { fprintf(stderr, "=== sourcecode -> const_declarations var_declarations cmpdstmt ===\n"); }
		;
const_declarations:	/* empty */
		| CONST constlist
		;
constlist:	constdecl
		| constlist constdecl
		;
var_declarations:	/* empty */
		| VAR varlist { fprintf(stderr, "=== var_declarations -> var varlist ===\n"); }
		;
varlist:	decl_var { fprintf(stderr, "=== varlist -> decl_var ===\n"); }
		| varlist decl_var { fprintf(stderr, "=== varlist -> varlist decl_var ===\n"); }
		;
constdecl:	ID '=' {sp=0;} expr_stat ';'	{
		printf("*** %d %g ***\n", $4, pop());
					}
		;
decl_var:	lista_id ':' type ';'
		;
lista_id:	ID
		| lista_id ',' ID
		;
type:		simpletype
		;
simpletype:	INTEGER
		| BOOLEAN
		| STRING
		| CHAR
		;
expr_stat:	factor_stat
		| expr_stat '+' expr_stat	{
			if($1==INT_TYPE || $3==INT_TYPE) $$=INT_TYPE;
			else if($1==CHAR_TYPE) $$=CHAR_TYPE;
			else if($1==STRING_TYPE) $$=STRING_TYPE;
			push(pop()+pop());
						}
		| expr_stat '-' expr_stat	{
			if($1==INT_TYPE || $3==INT_TYPE) $$=INT_TYPE;
			else if($1==CHAR_TYPE) $$=CHAR_TYPE;
			else if($1==STRING_TYPE) $$=STRING_TYPE;
			push(-pop()+pop());
						}
		| expr_stat '*' expr_stat	{
			if($1==INT_TYPE || $3==INT_TYPE) $$=INT_TYPE;
			else if($1==CHAR_TYPE) $$=CHAR_TYPE;
			else if($1==STRING_TYPE) $$=STRING_TYPE;
			push(pop()*pop());
						}
		| expr_stat '/' expr_stat	
		| expr_stat DIV expr_stat
		| expr_stat MOD expr_stat
		;
factor_stat:	ID		{}
		| constant
		| '(' expr_stat ')'	{$$ = $2;}
		;
constant:	CONST_INT	{
			//$$ = INT_TYPE;
			//push(atof($1));
			fprintf(stderr, "=== constant -> CONST_INT ===\n");
				}
		| CONST_STRING	{
			//$$ = STRING_TYPE;
			//push(atof($1));
			fprintf(stderr, "=== constant -> CONST_STRING ===\n");

				}
		| CONST_CHAR	{
			//$$ = CHAR_TYPE;
			//push((double)$1[0]);
			fprintf(stderr, "=== constant -> CONST_CHAR ===\n");
				}
		;
cmpdstmt:	BEGINN stmtlist END { fprintf(stderr, "=== cmpdstmt -> BEGIN stmtlist END ===\n"); }
		;
stmtlist:	stmt { fprintf(stderr, "=== stmtlist -> stmt ===\n"); }
		| stmtlist ';' stmt { fprintf(stderr, "=== stmtlist -> stmtlist ; stmt ===\n"); }
		;
stmt:		/* empty */ { fprintf(stderr, "=== stmt -> epsilon ===\n"); }
		| assignstmt { fprintf(stderr, "=== stmt -> assignstmt ===\n"); }
		| ifstmt { fprintf(stderr, "=== stmt -> ifstmt ===\n"); }
		| whilestmt { fprintf(stderr, "=== stmt -> whilestmt ===\n"); }
		| cmpdstmt { fprintf(stderr, "=== stmt -> cmpdstmt ===\n"); }
		| readstmt { fprintf(stderr, "=== stmt -> readstmt ===\n"); }
		| printstmt { fprintf(stderr, "=== stmt -> printstmt ===\n"); } 
		| forstmt { fprintf(stderr, "=== stmt -> forstmt ===\n"); }
		;

forstmt: FOR assignstmt TO expression DO stmt { fprintf(stderr, "=== FOR assignstmt TO expression DO stmt ===\n"); }
		;
assignstmt:	variable ATRIB expression  { fprintf(stderr, "=== assignstmt -> variable := expression ===\n"); }
		;
variable:	ID
		| ID '[' expression ']'
		| ID '.' ID
		;
expression:	factor { fprintf(stderr, "=== expression -> factor ===\n"); }
		| expression '+' expression { fprintf(stderr, "=== expression -> expression + expression ===\n"); }
		| expression '-' expression { fprintf(stderr, "=== expression -> expression - expression ===\n"); }
		| expression '*' expression { fprintf(stderr, "=== expression -> expression * expression ===\n"); }
		| expression '/' expression { fprintf(stderr, "=== expression -> expression / expression ===\n"); }
		| expression DIV expression { fprintf(stderr, "=== expression -> expression div expression ===\n"); }
		| expression MOD expression { fprintf(stderr, "=== expression -> expression mod expression ===\n"); }
		;
factor:		ID { fprintf(stderr, "=== factor -> IDENTIFIER ===\n"); }
		| constant {} { fprintf(stderr, "=== factor -> constant ===\n"); }
		| ID '(' exprlist ')' { fprintf(stderr, "=== factor -> IDENTIFIER(exprlist) ===\n"); }
		| '(' expression ')' { fprintf(stderr, "=== factor -> (expression) ===\n"); }
		| ID '[' expression ']' { fprintf(stderr, "=== factor -> IDENTIFIER[expression] ===\n"); }
		| ID '.' ID
		;
exprlist:	expression
		| exprlist ',' expression
		;
ifstmt:	IF condition THEN stmt elsebranch
		;
elsebranch:	/* empty */
		ELSE stmt
		;
condition:	expr_logica
		| expression relational_operator expression
		;
expr_logica:	factor_logic
		| expr_logica AND expr_logica
		| expr_logica OR expr_logica
		;
factor_logic:	'(' condition ')'
		| NOT factor_logic
		;
relational_operator:		'='
		| '<'
		| '>'
		| NE
		| LE
		| GE
		;
whilestmt:	WHILE condition DO stmt {fprintf(stderr, "whilestmt -> WHILE condition DO stmt"); }
		;
printstmt:	PRINT '(' elemlist ')'{ fprintf(stderr, "=== printstmt -> outputline(elemlist) ===\n"); }
		;
elemlist:	element
		| elemlist ',' element
		;
element:	expression
		| CONST_SIR
		| ID
		;
readstmt:	READ '(' variableslist ')' { fprintf(stderr, "=== readstmt -> inputLine(variableslist) ===\n"); }
		;
variableslist:	variable
		| variableslist ',' variable
		;

%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if(argc>1) yyin = fopen(argv[1], "r");
  if((argc>2)&&(!strcmp(argv[2],"-d"))) yydebug = 1;

  if(!yyparse()) fprintf(stderr,"\x1b[32mPROGRAM IS CORRECT! PERFECT!\x1b[0m\n");
}

