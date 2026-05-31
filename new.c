#include<stdio.h>
union person{
    int id;
    char name[14];
    int age;
};

int main(){
    int i,n;
    printf("Enter NO:");
    scanf("%d",&n);
    union person p[n];
    for(i=0;i<3;i++){
        printf("ID:");
        scanf("%d",&p[i].id);
        printf("Name:");
        scanf("%s",&p[i].name);
        printf("Age:");
        scanf("%d",&p[i].age);
    }

    printf("\n------Details----\n");
    for(i=0;i<3;i++){
    printf("Detail%d",i+1);
    printf("Id:%d\n",p[i].id);
    printf("name:%s\n",p[i].name);
    printf("age:%d\n",p[i].age);
    }
    return 0;
}