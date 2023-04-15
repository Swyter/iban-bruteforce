'''
    https://en.wikipedia.org/wiki/International_Bank_Account_Number#cite_note-tr201-20
    ESkk bbbb ssss xxcc cccc cccc
    kk = Iban check digits code
    b = National bank
    s = Branch code
    x = Check digits
    c = Account number 
'''

weights = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]

bank_branch_code = "00" + "20801795"
total = 0
for i, elem in enumerate(bank_branch_code):
    print(i, elem)
    total += int(elem) * weights[i]


print(total, 11 - (total % 11))
#account_num = 499916****

exit(0)



iban = "ES04 2080 1795 2549 9916 ****" # ES0420801795254999165252
ibstrip = iban.replace(" ", "").upper()
ibstrip = ibstrip[4:] + ibstrip[:4]

print(iban, ibstrip)

ibarray = []

for char in ibstrip:
    print(char, char > 'A', )

    try:
        num = int(char)
    except:
        if ord(char) >= ord('A') and ord(char) <= ord('Z'):
            num = 10 + (ord(char) - ord('A'))
        else:
            num = None

    ibarray.append(num)

ibnum = ""
for i, elem in enumerate(ibarray):
    print (i, elem)
    if elem != None:
        ibnum += str(elem)
    else:
        ibnum += 'X'

print(ibarray, ibnum)
count = 0
for i in range(0000, 9999):
    cur = int("2080179525499916%04u142804" % i)
    if cur % 97 == 1:
        print(f"[i] [{i:04d}] valid: {cur}")
        count += 1

print(f" -- total: {count}")



