from divisor_app.divisor_matcher import ConsecutiveDivisorMatcher

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    ks = list(map(int, data[1:]))
    max_k = max(ks)
    
    matcher = ConsecutiveDivisorMatcher(max_k)
    
    for k in ks:
        print(matcher.query(k))

if __name__ == "__main__":
    main()