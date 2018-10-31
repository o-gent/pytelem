#ifndef list_H
#define list_H

class List{
    private:
        int* num_array[20][13] = {{0}};
        int queue[20];
        int list_index;
    public:
        void make(int key, int* values);
        int get_values(int key);

        int add(int value);
        int pop();
        int len();
};

#endif