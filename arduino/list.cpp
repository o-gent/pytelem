#include "datalink.h"

int List::add(int value){
    // add value to next free space
    queue[list_index] = value;
    list_index++;
}


int List::pop(){
    int value = queue[list_index - 1];
    list_index--;
    return value;
}

int List::len(){
    return list_index;
}
