'''
    https://en.wikipedia.org/wiki/International_Bank_Account_Number#cite_note-tr201-20
    ESkk bbbb ssss xxcc cccc cccc
    kk = Iban check digits code
    b = National bank
    s = Branch code
    x = Check digits
    c = Account number 
'''
# swy: put your Spanish IBAN here, use asterisks for the unknown spots
#      the more missing numbers, the more valid numbers will show up.
iban = "ES04 2080 1795 *549 9916 ****" # e.g. dummy auto-generated one, for testing: ES0420801795254999165252
ibstrip = iban.replace(" ", "").upper()

es_bkbrnch_check_num = ibstrip[12]; es_bkbrnch_check_num_gen = None
es_account_check_num = ibstrip[13]; es_account_check_num_gen = None

es_bkbrnch_can_be_checked = True
es_account_can_be_checked = True

try: es_bkbrnch_check_num = int(es_bkbrnch_check_num);
except: es_bkbrnch_can_be_checked = False
try: es_account_check_num = int(es_account_check_num);
except: es_account_can_be_checked = False


def format_iban(num):
    num_str = str(num)
    return f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]} {num_str[16:20]} {num_str[20:]}"

print(f'''
    {format_iban(ibstrip)}
    ESkk bbbb ssss xxcc cccc cccc
         \___ ___/ {ibstrip[12]}               <- spanish branch/bank check digit
                    {ibstrip[13]}\_ ____ ___/  <- spanish bank account check digit

    \_{ibstrip[2:4]}________________________/  <- iban global check digits

    {ibstrip[:2]}                             <- country code
         {ibstrip[4:8]}                      <- bank number/id
              {ibstrip[8:12]}                 <- the branch number for that bank
                     {ibstrip[14:16]} {ibstrip[16:20]} {ibstrip[20:]}  <- the account number in that branch
'''
)

weights = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]

bank_branch_code = "00" + ibstrip[4:12] # "20801795"

try:
    int(bank_branch_code)
    total = 0
    for i, elem in enumerate(bank_branch_code):
        total += int(elem) * weights[i]

    es_bkbrnch_check_num_gen = 11 - (total % 11)

    print(f"[>] bank/branch checksum: 11 - ({total} % 11) = {es_bkbrnch_check_num_gen}")
    bank_branch_code = int(bank_branch_code)
except:
    print("[e] there are missing numbers; can't compute the bank-branch checksum")

if es_bkbrnch_check_num in range(0, 9) and es_bkbrnch_check_num == es_bkbrnch_check_num_gen:
    print(f"[i] the bank/branch check digit seems to match our own: {es_bkbrnch_check_num}/{es_bkbrnch_check_num_gen} (OK)")
elif es_bkbrnch_check_num_gen:
    print(f"[-] the bank/branch check digit is missing but we can reconstruct it; substituting it with the regenerated one ({es_bkbrnch_check_num_gen})")
    es_bkbrnch_check_num = str(es_bkbrnch_check_num_gen)
    ibstrip = list(ibstrip); ibstrip[12] = es_bkbrnch_check_num; ibstrip = "".join(ibstrip) # swy: absolutely stupid: https://stackoverflow.com/a/68840528/674685
else:
    print("[e] the bank/branch check digit is missing and can't be recalculated/replaced because there are missing digits")


account_num = ibstrip[14:24] # "4999165252"

try:
    int(account_num)
    total = 0
    for i, elem in enumerate(account_num):
        total += int(elem) * weights[i]

    es_account_check_num_gen = 11 - (total % 11)

    print(f"[>] account number checksum: 11 - ({total} % 11) = {es_account_check_num_gen}")
except:
    print("[e] there are missing numbers; can't compute the account number checksum")

if es_account_check_num in range(0, 9) and es_account_check_num == es_account_check_num_gen:
    print(f"[i] the account number check digit seems to match our own: {es_account_check_num}/{es_account_check_num_gen} (OK)")
elif es_account_check_num_gen:
    print(f"[-] the account number check digit is missing but we can reconstruct it; substituting it with the regenerated one ({es_account_check_num_gen})")
    es_account_check_num = str(es_account_check_num_gen)
    ibstrip = list(ibstrip); ibstrip[13] = es_account_check_num; ibstrip = "".join(ibstrip) # swy: absolutely stupid: https://stackoverflow.com/a/68840528/674685
else:
    print("[e] the account number check digit is missing and can't be recalculated/replaced because there are missing digits")

#exit(0)

# swy: split each digit into an array, find wildcard characters, and turn alphanumeric characters into numbers
ibstrip = ibstrip[4:] + ibstrip[:4]
ibarray = []
unknown_spaces = 0
for char in ibstrip:
    try:
        num = int(char)
    except:
        if ord(char) >= ord('A') and ord(char) <= ord('Z'):
            num = 10 + (ord(char) - ord('A'))
        else:
            num = None
            unknown_spaces += 1

    ibarray.append(num)

print(f"[i] {unknown_spaces} unknown spaces")

# swy: this function fills out the empty digits with the generated ones, putting them in the right spots
def fill_out_unknown(ibarray, generated_num = None):
    if generated_num != None:
        generated_num = ("0" * unknown_spaces) + str(generated_num)
        generated_num = generated_num[-unknown_spaces:]
        next_generated = 0
    else:
        next_generated = 99999
    ibnum = ""
    for i, elem in enumerate(ibarray):
        if elem != None:
            ibnum += str(elem)
        else:
            if next_generated > unknown_spaces:
                ibnum += 'X'
            else:
                ibnum += generated_num[next_generated]
                next_generated += 1
    return ibnum

print(ibarray, fill_out_unknown(ibarray))
count_a = 0; count_b = 0; count_c = 0; count_both = 0
for i in range(0000, 10 ** unknown_spaces):
    valid_a = False; valid_b = False; valid_c = False
    cur_str = fill_out_unknown(ibarray, i) # ("2080179525499916%04u142804" % i)
    cur     = int(cur_str)

    if cur % 97 == 1:
        #print(f"[i] [{i:04d}] valid: {cur}")
        count_a += 1
        valid_a = True

    bank_branch_code = "00" + cur_str[0:8]
    account_num = cur_str[10:20]
    es_bkbrnch_check_num = cur_str[8]
    es_account_check_num = cur_str[9]

    if True: #es_bkbrnch_can_be_checked:
        total = 0
        for j, elem in enumerate(bank_branch_code):
            total += int(elem) * weights[j]
        
        check_num = 11 - (total % 11)

        if check_num == int(es_bkbrnch_check_num):
            #print(f"[-] [{i:04d}] valid Spanish check no: {account_num}")
            count_b += 1
            valid_b = True

    if True: #es_account_can_be_checked:
        total = 0
        for j, elem in enumerate(account_num):
            total += int(elem) * weights[j]
        
        check_num = 11 - (total % 11)

        if check_num == int(es_account_check_num):
            #print(f"[-] [{i:04d}] valid Spanish check no: {account_num}")
            count_c += 1
            valid_c = True

    if valid_a and valid_b and valid_c:
        print(f"[i] [{i:05d}] valid: {cur} % 97 == 1")
        print(f"[-] [{i:05d}] valid Spanish check no: {bank_branch_code}")
        print(f"[-] [{i:05d}] valid Spanish check no: {account_num}")

        reconstructed_iban = ibstrip[-4:-2] + cur_str[-2:] + cur_str[:20]
        print(
            f"  \ both are valid for the tentative IBAN number [{format_iban(reconstructed_iban)}]"
        )
        count_both += 1

print(f" -- valid for a: {count_a}, valid for b: {count_b}, valid for c: {count_c}, valid for both: {count_both}")