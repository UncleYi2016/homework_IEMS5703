import operator

def problem_1(a,b):
    num = 0
    for i in range(a,b):
        if(i % 7 == 0 and i % 3 != 0):
            num += 1
    return num

def problem_2(n):
    result = 0
    if(n < 0 or n > 9):
        return 0
    tmp1 = n*100 + n*10 + n
    tmp2 = n*10000 + n*1000 + tmp1
    result = n + tmp1 + tmp2
    return result

def problem_3(nums):
    max_sum = 0
    length = len(nums)
    for i in range(1, length-1):
        tmp = nums[i-1] + nums[i] + nums[i+1]
        if(max_sum < tmp):
            max_sum = tmp
    return max_sum

def problem_4(sentence):
    output = ''
    sentence_elements = sentence.split(' ')
    sentence_elements.sort()
    length = len(sentence_elements)
    for i in range(0, length):
        output += sentence_elements[i] + ' '
    output = output.strip()
    return output

def problem_5(sentence):
    output = []
    sentence = sentence.lower()
    sentence_elements = sentence.split(' ')
    length = len(sentence_elements)
    output_dir = dict()
    for i in range(length):
        if sentence_elements[i] in output_dir:
            tmp = output_dir[sentence_elements[i]]
            output_dir[sentence_elements[i]] = tmp+1
        else:
            output_dir[sentence_elements[i]] = 1
    output_dir_sort = sorted(output_dir.items(),key = operator.itemgetter(1),reverse = True)
    output_length = 5
    if(len(output_dir_sort) < 5):
        output_length = len(output_dir_sort)
    for j in range(output_length):
        output.append(output_dir_sort[j])
    return output
    
def problem_6(path):
    output = []
    data_file = open(path, 'r')
    column = []
    column_line = data_file.readline()
    column_line = column_line.strip()
    column_elements = column_line.split(',')
    for element in column_elements:
        column.append(element)
    for line in data_file:
        line = line.strip()
        data_elements = line.split(',')
        dict_node = {}
        length = len(data_elements)
        for i in range(length):
            dict_node[column[i]] = data_elements[i]
        output.append(dict_node)
    return output
        

# if __name__ == '__main__':
#    print('problem_1():\n\t' + str(problem_1(10,30)))
#    print('problem_2():\n\t' + str(problem_2(100)))
#    print('problem_3():\n\t' + str(problem_3([1, 3, -2, 4, 8, -9, 0, 5])))
#    print('problem_4():\n\t' + str(problem_4('the chinese university of hong kong')))
#    print('problem_5():\n\t' + str(problem_5('The Transmission Control Protocol (TCP) is one of the main protocols of the Internet')))
#    print('problem_6():\n\t' + str(problem_6('data.csv')))
