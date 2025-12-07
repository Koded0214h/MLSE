import time

num_strings = 10000
test_list = ['test'] * num_strings

# 1. INEFFICIENT: Repeated concatenation using (+)
def repeat_concat(test_list):
    start_time = time.perf_counter()

    result_plus  = ""
    for s in test_list:
        result_plus += s
        
    end_time = time.perf_counter()
    
    return (f"Concatenation (+) Time: {end_time - start_time:.4f}s")
    
# 2. EFFICIENT: Using str.join()
def string_join(test_list):
    start_time = time.perf_counter()
    result_join = "".join(test_list)
    end_time = time.perf_counter()
    
    return (f"Join () Time: {end_time - start_time:.4f}s")
    
print(repeat_concat(test_list))
print(string_join(test_list))