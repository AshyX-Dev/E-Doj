def convert_to_2d_list(input_list, n):
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]

# مثال
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, True, "G"]
two_d_list = convert_to_2d_list(my_list, 5)

print(two_d_list)
