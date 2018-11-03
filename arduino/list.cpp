#include "datalink.h"

int List::add(int value){
    // add value to next free space
    queue[list_index] = value;
    list_index++;
}


int List::pop(){
    list_index--;
    return queue[list_index];
}

int List::len(){
    return list_index;
}
