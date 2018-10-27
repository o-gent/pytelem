#include "datalink.h"


// put an array into the structure
void List::change(int key, int* values){
    num_array[key] = values;
}


int List::get_values(int key){
    return num_array[key];
}



int List::add(int value){
    // add value to next free space
    queue[list_index] = value;
    list_index++;
}


int List::pop(){
    value = queue[list_index - 1] 
    list_index--;
    return value;
}

int List::len(){
    return list_index;
}