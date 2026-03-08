#include <stdio.h>
#include <stdlib.h>

typedef struct node{
    struct node* left, *right;
    int info;
}Node;

typedef struct stack{
    struct stack* next;
    Node* root;
}Stack;


void PUSH(Stack* S1, Node* N){
    Stack* S = malloc(sizeof(Stack));
    S->next=NULL;
    S->root = N;
    S1->next = S;
}

void Nadji_Stabla(int n, Stack* S, Node** C, int m){
    if (!n){
        Stack *S1 =S;
        for (int i = 0; i<m; i++) {
            if (!S1){
                Stack* S = malloc(sizeof(Stack));
                S->next=NULL;
                S->root = C[i];
            }
            else{
                PUSH(S1, C[i]);
                S1=S1->next;
            }
      }
    }
    else {
        Node** M = malloc(sizeof(Node*)), *N = malloc(sizeof(Node));
        for (int i = 0; i<m-1; i++){
            for (int j = 1; j<m; j++){
                for (int k = 0,t=0; k<m; k++) if (k!=i || k!=j) M[t++]=C[k];
                N->left = C[i];
                N->right = C[j];
                N->info = -1;
                M[m-2] = N;
                Nadji_Stabla(n-1, S, M, m-1);
                N->left = C[j];
                N->right = C[i];
                M[m-2] = N;
                Nadji_Stabla(n-1, S, M, m-1);
                free(M);
            }
        }
    }
}

int inc(int *Z, int n, int i){
    if (!n) return 0;
    Z[i] =(Z[i]+1)%4;
    if (!Z[i] && (n-1)==i) return 0;
    else if (!Z[i]) return inc(Z, n, i+1);
    return 1;
}
double Calc_Tree(Node* root, int *Z, int i){
    if (root->info>0) return root->info;
    else {
        root->info = -Z[i];
        switch (Z[i]){
            case 0: return (Calc_Tree(root->left,Z,i+1) + Calc_Tree(root->right,Z,i+1));
            case 1: return (Calc_Tree(root->left,Z,i+1) + Calc_Tree(root->right,Z,i+1));
            case 2: return (Calc_Tree(root->left,Z,i+1) + Calc_Tree(root->right,Z,i+1));
            case 3: return (Calc_Tree(root->left,Z,i+1) + Calc_Tree(root->right,Z,i+1));
        }
    }
}

Node* Resenje (int* B , double n){
    int i,j;
    double m;
    Node ** Cvorovi = malloc(6*sizeof(Node*));
    for (i=0; i<6; i++){
        Cvorovi[i] = malloc(sizeof(Node));
        Cvorovi[i]->info = B[i];
        Cvorovi[i]->left = NULL;
        Cvorovi[i]->right = NULL;
    }
    Stack* S = NULL;
    for (i=0; i<6; i++){
        Nadji_Stabla(i,S,Cvorovi,6);
        int *Z = calloc(i,sizeof(int));
        for (j=0;j<i;j++) Z[j]=0;
        do{
        Stack* S1=S;
        while (S1){
            m=Calc_Tree(S1->root,Z,0);
            if (m==n) return S1->root;
            S1=S1->next;
        }
        }while(inc(Z,i,0));
        S=NULL;
    }
    return NULL;
}


int main()
{
    int B[6], i;
    double n;
    char Z[4] = {'+','-','*','/'};
    scanf("%lf",&n);
    for (i=0; i<6; i++) scanf("%d", B+i);
    Node *root = Resenje (B,n);

    return 0;
}
