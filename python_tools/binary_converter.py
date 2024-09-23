# Algorithm to convert binary to base-10:
# reverse the binary number using a sorting algorithm
# multiply the 0 or 1 at each index position to 10^i.
# add the values obtained from each index position to get the base-10 representation of the binary.

test = [1,2,3,4,5,6,7]
test = [1,2,3,4,5,6,7,8]

def binary_flip(bin_str):

    rev_bin_list = []

    for num in bin_str:
        rev_bin_list.insert(0, num)

    return rev_bin_list
    
    # start = 0
    # end = len(test)-1

    # while start < end:
    #     temp = test[start]
    #     test[start] = test[end]
    #     test[end] = temp
        
    #     start += 1
    #     end -= 1

def bin_to_base10(array):

    num = 0

    for i, v in enumerate(array):
        temp = (2**i) * int(v)
        num = num + temp
        
    return num

def main():
    #binary = input('Enter binary number: ')
    binary = '1010111'
    bin_list = binary_flip(binary)
    base10 = bin_to_base10(bin_list)
    print(f'The base-10 of {binary} is {base10}')
    
#print(binary_flip('111000'))

if __name__ == '__main__':
    main()


