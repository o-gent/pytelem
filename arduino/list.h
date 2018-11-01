#ifndef list_H
#define list_H

class List{
    private:
        int* num_array[20][13] = {{0}};
        int queue[20];
        int list_index;
    public:
        int add(int value);
        int pop();
        int len();
};

#endif
