def calculate_prefix_sum(arr, n):
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + arr[i - 1]
    return prefix_sum

def get_subarray_mean(prefix_sum, left, right):
    subarray_sum = prefix_sum[right] - prefix_sum[left - 1]
    subarray_length = right - left + 1
    return subarray_sum // subarray_length

def main():
    input_line = input().split()
    n = int(input_line[0])
    q = int(input_line[1])
    
    arr = []
    input_numbers = input().split()
    for num in input_numbers:
        arr.append(int(num))
    
    prefix_sum = calculate_prefix_sum(arr, n)
    
    for _ in range(q):
        query = input().split()
        left = int(query[0])
        right = int(query[1])
        result = get_subarray_mean(prefix_sum, left, right)
        print(result)

if __name__ == "__main__":
    main()