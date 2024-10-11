from fetchify import fetch

class Kali:
        def GetTools():
                modules = [
                            "git clone https://github.com/htr-tech/zphisher.git",
                            "git clone https://github.com/th3unkn0n/osi.ig.git",
                            # "git clone https://github.com/thelinuxchoice/inshackle",
                            "git clone https://github.com/htr-tech/nexphisher.git",
                            # "git clone https://github.com/xHak9x/SocialPhish.git",
                            # "git clone https://github.com/suljot/shellphish.git",
                            "git clone https://github.com/iinc0gnit0/BlackPhish",
                            "git clone https://github.com/jaykali/maskphish",
                            "git clone https://github.com/htr-tech/unfollow-plus.git",
                            # "git clone https://github.com/thelinuxchoice/blackeye",
                            "git clone https://github.com/sherlock-project/sherlock.git",
                            "git clone https://github.com/capture0x/XCTR-Hacking-Tools/",
                            "git clone https://github.com/AdrMXR/KitHack.git",
                            "git clone https://github.com/rajkumardusad/IP-Tracer.git",
                            "git clone https://github.com/xadhrit/terra.git",
                            "git clone https://github.com/jaygreig86/dmitry.git",
                            "git clone https://github.com/lanmaster53/recon-ng.git",
                            # "git clone https://github.com/m4ll0k/Infoga.git",
                            "git clone https://github.com/Ultrasecurity/DarkSide",
                            "git clone https://github.com/CybernetiX-S3C/InfoSploit",
                            "git clone https://github.com/Z4nzu/hackingtool.git",
                            "git clone https://github.com/m3n0sd0n4ld/uDork",
                            "git clone https://github.com/jackind424/onex.git",
                            "git clone https://github.com/opsdisk/pagodo.git",
                            "git clone https://github.com/jseidl/GoldenEye.git",
                            "git clone https://github.com/ultrasecurity/Storm-Breaker",
                            "git clone https://github.com/abhisharma404/vault.git",
                            "git clone https://github.com/rezasp/joomscan.git",
                            "git clone https://github.com/m8r0wn/crosslinked",
                            # "git clone https://github.com/GitHackTools/BillCipher",
                            "git clone https://github.com/pwn0sec/PwnXSS",
                            "git clone https://github.com/commixproject/commix.git"
                ]

                import os
                for module in modules:
                    os.system(module)

class Int:
    def __init__(self, number):
        self.number = number

    def is_prime(self):
        if self.number > 1:
            for i in range(2, self.number):
                if (self.number % i) == 0:
                    return False
            else:
                return True
        else:
            return False

    def factorial(self):
        fact = 1
        for i in range(1, self.number + 1):
            fact = fact * i
        return fact

    def is_palindrome(self):
        temp = self.number
        rev = 0
        while self.number > 0:
            dig = self.number % 10
            rev = rev * 10 + dig
            self.number = self.number // 10
        if temp == rev:
            return True
        else:
            return False

    @staticmethod
    def find_primes(start, stop):
        primes = []
        for num in range(start, stop + 1):
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        break
                else:
                    primes.append(num)
        return primes

    @staticmethod
    def reverse(number):
        rn = 0
        while number != 0:
            digit = number % 10
            rn = rn * 10 + digit
            number //= 10
        return rn

    @staticmethod
    def sum_digits(number):
        sum = 0
        temp = number
        while number != 0:
            digit = number % 10
            sum = sum + digit
            number //= 10
        return sum

class Str:
    def __init__(self, string):
        self.string = string

    def is_palindrome(self):
        rev = ""
        for i in self.string:
            rev = i + rev
        if rev == self.string:
            return True
        else:
            return False

    def analyze(self):
        a = 0  # Initial Assign
        u = 0  # Initial Assign
        l = 0  # Initial Assign
        d = 0  # Initial Assign
        al = 0  # Initial Assign
        o = 0  # Initial Assign
        for i in self.string:
            if i.isupper():  # Check for Upper
                u += 1
                al += 1
            elif i.islower():  # Check for Lower
                l += 1
                al += 1
            elif i.isdigit():  # Check for Digits
                d += 1
            else:  # Other Symbols
                o += 1
        a = len(self.string)
        return {"Total": a, "UpperCase": u, "LowerCase": l, "Digits": d, "Alphabets": al, "Others": o}

    def occurrence(self, word):
        ct = 0
        for i in range(len(self.string)):
            if self.string[i] == word[0]:
                if self.string[i:i + len(word)] == word:
                    ct += 1
        return ct

    @staticmethod
    def longest_word(string):
        mx = ""
        ln = 0
        m = 0
        a = string.split()
        l = len(a)
        for i in range(l):
            ln = len(a[i])
            if ln > m:
                m = ln
                mx = a[i]
        return mx

class List:
    def __init__(self, lst):
        self.lst = lst

    def frequency(self):
        result = {}
        for i in self.lst:
            freq = self.lst.count(i)
            if freq > 1:
                result[i] = f"{freq} times"
            elif freq == 1:
                result[i] = f"{freq} time"
        return result

    def maxminrange(self, start, stop):
        lst = self.lst[start:stop+1]
        mn = min(lst)
        mx = max(lst)
        return {"Max": mx, "Min": mn}

    def removedups(self):
        return list(set(self.lst))

class MyTuple:
    def __init__(self, my_tuple):
        self.my_tuple = my_tuple

    def frequency(self):
        result = {}
        for i in self.my_tuple:
            freq = self.my_tuple.count(i)
            if freq > 1:
                result[i] = f"{freq} times"
            elif freq == 1:
                result[i] = f"{freq} time"
        return result

    def removedups(self):
        return tuple(set(self.my_tuple))

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return "Underflow"

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return "Underflow"

    def clear(self):
        self.items = []

    def display(self):
        return self.items

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return "Underflow"

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return "Underflow"

    def clear(self):
        self.items = []

    def display(self):
        return self.items

def binary_search(item, array):
    array.sort()
    first=0
    last=len(array)-1
    mid = (first+last)//2
    found = False
    while( first<=last and not found):
        mid = (first + last)//2
        if array[mid] == item :
             return mid
             found= True
        else:
            if item < array[mid]:
                last = mid - 1
            else:
                first = mid + 1 
       
    if found == False:
        return

def wifi():
    exec(fetch("Tools/WIFI.py", "py"))

