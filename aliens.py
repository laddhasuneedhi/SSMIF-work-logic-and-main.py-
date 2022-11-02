
import numpy as np
dict = {}
indice_tracker = set()
string_value = ""
beta_rate = ""
first_indice_tracker = [[], []]
def modified_binary_search(num_array, l, r, i): #modified binary string that finds the first occurence one within an array at a given  time complexity lg(n)
   result = -1
   while l <= r:
    mid = l + ((r-l) //2)
    mid_string = num_array[mid]
    if mid_string[i] == "1":
        result = mid 
        r = mid -1
    else:
        l = mid + 1
   return result

#this function converts a given binary string into a decimal format
def binary_to_decimal(string_value):
    reversed_string_value = string_value[::-1]
    number = 0
    for indice,values in enumerate(reversed_string_value):
        number = number + (pow(2,indice) * int(values))
    return number

def delta_rate(num_array, indice_tracker): #finds the delta rate using the modified binary search algorithm. Total time complexity (nlgn)
    i = 0
    while len(num_array) != 1:
        if i != 0: #since index 0 was already accounted for in the previous step
            return_value = modified_binary_search(num_array, 0, len(num_array) -1, i )
            if return_value != -1:
                if len(num_array) -  return_value > return_value:
                    num_array = num_array[return_value:]
                elif len(num_array) - return_value < return_value:
                    num_array = num_array[0:return_value]
                else:
                    num_array = num_array[return_value:] 
        i = i + 1
    return binary_to_decimal(num_array.pop())   

def omega_rate(num_array, indice_tracker): #finds the delta rate using the modified binary search alogrith total  time is (nlgn)
      i = 0
      while len(num_array) != 1: #while the array is larger than 1 element
        if i != 0: #since index 0 was already accounted for in the previous step
            """this basically checks to see in which index of the sorted array  1 was encountered. It substracts that occurence with 
            the length of the array to see check if there were more 1's or 0's if more 1's than use 0's and if more 0's than 1's use 1's """
            return_value = modified_binary_search(num_array, 0, len(num_array) -1, i )
            if return_value != -1: 
                if len(num_array) -  return_value > return_value:
                    num_array = num_array[0:return_value]
                elif len(num_array) - return_value < return_value:
                    num_array = num_array[return_value:]
                else:
                    num_array = num_array[0:return_value] 
        i = i + 1    
      return binary_to_decimal(num_array.pop())    

       

with open("logic_input.txt", 'r') as f:
    lines = [entry.strip() for entry in f.readlines()]
    for line in lines:
        line = line.strip('\n')
        for indice,characters in enumerate(line):
            if indice == 0:
                first_indice_tracker[int(characters)].append((line)) #basically tracks the number of 1's and 0's occuring at each index using a dict where they key is the index and the value is an array where the count of 0s is stored i
            if indice not in indice_tracker:                        #in 0th position and the count of 1s is stored in the first position
                indice_tracker.add(indice)
                dict[indice] = [0,0]
                num_in_indice = int(characters)
                old_val = dict[indice][num_in_indice]
                new_val = old_val + 1
                dict[indice][num_in_indice] = new_val
            else:
                num_in_indice = int(characters)
                old_val = dict[indice][num_in_indice]
                new_val = old_val + 1
                dict[indice][num_in_indice] = new_val
    indice_tracker = sorted(indice_tracker) #indice tracker keeps track of the number of digits in the binary numbers
    for i in indice_tracker:
        current_value_indice = dict[i].index(max(dict[i])) #get the index of the maximum occuring character
        string_value = string_value + str(current_value_indice) #add it to the string as we go along
    alpha_rate = binary_to_decimal(string_value) #convert it into decimal
    print("Alpha Rate", alpha_rate) #print alpha rate
    for values in string_value: #omega rate is basically the inverse
        if values == '1':
            beta_rate = beta_rate + "0"
        else:
            beta_rate = beta_rate + "1"
    beta_rate = binary_to_decimal(beta_rate)
    print("beta rate", beta_rate)
    print("Part 1 total:", beta_rate * alpha_rate)


    #start this by finding the binary numbers with the most frequent left-most bit
    #select the the array which contains the number with this bit
    ######################################################################################################################################
                                       ######Part2##########
    if first_indice_tracker[0] < first_indice_tracker[1]: #if the sub array at index 0
        delta_tracker = first_indice_tracker[1]
        omega_tracker = first_indice_tracker[0]
    elif first_indice_tracker[1] < first_indice_tracker[0]:
        delta_tracker = first_indice_tracker[0]
        omega_tracker = first_indice_tracker[1]
    else:
        delta_tracker = first_indice_tracker[1]
        omega_tracker = first_indice_tracker[0]
    delta_tracker = sorted(delta_tracker)
    delta_val = delta_rate(delta_tracker, indice_tracker)
    print("Delta Rate:", delta_val)
    omega_tracker = sorted(omega_tracker)
    omega_val = omega_rate(omega_tracker, indice_tracker)
    print("Omega Rate:" ,omega_val )
    print("total for part 2",omega_val * delta_val )

    
    


            
            

        

    

   

   
    
    
    
  


    

 
               
               
               

            
                
                

                

            


        