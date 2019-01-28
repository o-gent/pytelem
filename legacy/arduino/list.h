#ifndef list_H
#define list_H

class List{
    private:
        // only stores up to 4 packets - memory saving..
        int* num_array[4][13] = {{0}};
        int queue[5];
        int list_index;
    public:
        int add(int value);
        int pop();
        int len();
};

#endif
