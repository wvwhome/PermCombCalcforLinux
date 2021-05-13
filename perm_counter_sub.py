#   perm_counter_sub.py
#    subroutine version
#   Count Permutations and Combinations with duplicates (multiples)
#   Use enumerating generating functions.  See
#    "An Introduction to Combinatorial Analysis"
#    by John Riordan  1958 Wiley original,  republished by Dover Publications 2002
#
#   page 13:
#
#    For R-permutations for p of one kind, and q of a second kind, etc, the enumerating generating function is:
#
#   (1 + t + t**2 / 2! + ... + t**p / p!) (1 + t + t**2 / 2! + ... + t**q / q!) ...
#
#     where p + q + ... = n, though n is independent in this formulation.  p, q, r, ... different than R
#
#   The number of R-permutations is the coefficent of t ** R / R!
#
#
#
#   ==========================================================================================
#
#   Program Author: Warren Van Wyck
#
#   11/26/10 Original Python 2.7 version.
#   12/25/12 Python 3.3.0 with Decimal arithmetic -- now faster
#   03/04/19 Improve rounding.  Need to check out Python polynomial arithmetic also
#   03/07/19 Initialize return_val
#   11/19/19 Cosmetic changes for Sublime Lint.
#
# Examples:
#               t n    r   p1 p2 p3 p4 p5
#               - ---  --  -- -- -- -- --
#               p 100  10  30 20 10 10 30   9765625
#               p 100  10  30 20 10 10      593423823636736
#
#               c 100  10  30 20 10 10 30   1001
#               c 100  10  30 20 10 10      218149207
#
#
#
#
import decimal
# -------------------------------------------------------------------------
def  \
reg_perm(n, r):
    perm = 1
    j = 1
    while j < r + 1:
        perm = perm * (n - j + 1)
        j = j + 1

    return perm

# ------------------------------------------------------------------------
def  \
mult_poly(a, b):
    len_a = len(a)
    len_b = len(b)
    prod = len_a + len_b - 1

    c = [0] * prod
    j = 0
    while j < len_a:
        k = 0
        while k < len_b:
            sub = j + k
            c[sub] = c[sub] + (a[j] * b[k])
            k = k + 1

        j = j + 1

    return c

# ------------------------------------------------------------------------
def  \
reg_comb(n, r):

    d = decimal.Decimal

    comb = d(1)
    j = 1
    if r == n:
        comb = 1
    else:
        while j < r + 1:
            comb = comb * (n - j + 1)  / j
            j = j + 1

    return comb

# ------------------------------------------------------------------------
def  \
 dupes_comb(n, r, p):
    comb = 1
    poly = []
    poly_a = []
    poly_prod = []
    #  Generating function emulated here
    #  Then pick off the proper co-efficient
    j = 0
    while j < len(p):
        poly = [1] * (p[j] + 1)

        if j == 0:
            poly_a = poly
        else:
            poly_prod = mult_poly(poly_a, poly)
            poly_a = poly_prod

        j = j + 1

    comb = poly_prod[r]

    return comb

# ------------------------------------------------------------------------
def \
dupes_perm(n, r, p):

    d = decimal.Decimal

    perm = d(1)
    poly = []
    poly_a = []
    poly_prod = []
    #  Generating function to emulate here
    #  Then pick off the proper co-efficient
    j = 0
    while j < len(p):
        poly = [0] * (p[j] + 1)
        fact = d(1)
        k = 0

        while k <= p[j]:
            if k > 1:
                fact = fact * k

            poly[k] = d(1) / fact
            k = k + 1

        # print 'poly:', poly
        if j == 0:
            poly_a = poly
        else:
            poly_prod = mult_poly(poly_a, poly)
            poly_a = poly_prod

        j = j + 1

    k = 1
    fact = 1
    while k < r + 1:
        fact = fact * k
        k = k + 1

    perm = poly_prod[r] * fact

    return perm

# ------------------------------------------------------------------------
def  \
perm_counter(
    type,
    number_N,
    number_R,
    list_dupe_counts
      ):

    d = decimal.Decimal
    decimal.getcontext().prec = 160      #   handles 100 factorial

    error_msg = ''
    dupe_ind = 0    # are there any duplicate objects?
    ret_code = 0
    return_val = 0

    k = 0
    p = []
    p_int = []
    p_total = 0

    #
    #   Complete validation of input data
    #   If validation fails, set return_code to 4
    #
    # check list_dupe_counts
    if list_dupe_counts == ['']:
        pass
    else:
        for x in list_dupe_counts:
            p.append(x)
            if str(x).isdigit():
                dupe_ind = 1
                p_total = p_total + int(x)
            else:
                error_msg += " all p's must be positive integers. found: "  +  str(x)
            k = k + 1

    if type in ('P', 'C'):
        pass
    else:
        error_msg += " type must be 'C' or 'P' for Combinations or Permutations."

    N = int(number_N)

    R = int(number_R)

    if error_msg == '':
        if R > N:
            error_msg += ' R is greater than N.'

    if error_msg == '':
        p_total = 0
        for x in p:
            # print 'x in p', x
            p_total = p_total + int(x)

        if p_total > N:
            error_msg += " sum of p's is greater than N."

    if error_msg == '':
        p_int = [1] * (len(p) + N - p_total)
        # print 'p_int:', p_int
        k = 0
        # print 'p:', p
        for x in p:
            p_int[k] = int(x)
            k = k + 1

    if error_msg > '':
        ret_code = 4
    else:
        if dupe_ind == 1:
            return_val = 1
            if p_int[0] < N:
                if type == 'P':
                    return_val = dupes_perm(N, R, p_int)
                else:
                    return_val = dupes_comb(N, R, p_int)
        else:
            if type == 'P':
                return_val = reg_perm(N, R)
            else:
                return_val = reg_comb(N, R)

    # take care of rounding -- sometimes a bit low  100 99   '5 6 7'
    # return_val = int(return_val + d(0.1))
    return_val = int(return_val + d(0.4999))     #improve rounding

    return  str(ret_code)  +  ' '  +  str(return_val)  +  '  error msg: '  +  error_msg

# ------------------------------------------------------------------------------------------
