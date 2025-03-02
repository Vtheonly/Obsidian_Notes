## TP 1 : 

```c
%{
#include <stdio.h>
%}

ch [0-9]
ident [a-z][a-z0-9]*

%%

{ch}+    {printf("%s\n",yytext);}

{ident}  {printf("identificatuer : %s\n",yytext);}

.        {printf("autre charachter : %s\n",yytext);}


%%


int yywrap(){
	return 1; 
}



int main(int argc,char ** argv){

    if(argc>1){
        yyin=fopen(argv[0],"r");
    }
    else{
        yyin=stdin;
	    yylex();
    }
    
}
```


---

