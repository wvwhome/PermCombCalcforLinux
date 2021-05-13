#  File routes.py
#
#  03/07/2019 WVW: Permutations-Combinations Calculator.
#  03/14/2019 WVW: Deploy version 2.0 in GCP.
#  11/19/19:  Cosmetic changes for Sublime Linter.  Add route for /math/.
#
#     Only processing data from "POST" requests.
#
#
from flask import render_template, request
from permcalc_pkg import app
from permcalc_pkg.forms import PermEnumForm
from permcalc_pkg.forms import PermEnumWordForm
from permcalc_pkg.forms import PermGenerateForm
from permcalc_pkg.forms import edit_dupes_string
# from pprint import pprint

from perm_counter_sub import perm_counter   # written by me
import platform
import inspect
#
import time
import datetime
#  03/09/2019  request.environ['REMOTE_ADDR'] is only returning 127.0.0.1  for GAE -- needs works
from math import factorial
from collections import Counter
from sympy.utilities.iterables import multiset_permutations
from sympy.utilities.iterables import multiset_combinations
from decimal import Decimal

start_time = datetime.datetime.now()
print()
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! start time:', start_time)
this_program = inspect.currentframe().f_code.co_filename
print('*** program starting=')
print(this_program)
print('version:   ', '11/18/19 B')
print('Python:    ', platform.python_version())

#  Limit the output of list elements to conserve resources on the host
display_limit    = -1
display_limit =   50000
display_limit_edit = f'{display_limit:,d}'

@app.route("/")
@app.route("/home/")
@app.route("/math/")
def home_f():
    return render_template('home.html')

#
@app.route("/enumerate/", methods=['GET', 'POST'])
def perm_enum_f():

    form_enum = PermEnumForm()
    perm_display = ''
    elapsed_time = ''
    sci_display  = ''   # scientific notation display

    # 03/12/2019  A lot of extra handling would be required for GET to work -- don't bother
    # print(request.form)   # testing for GET
    # print('Perm Comb Ind: ', request.args.get('perm_comb_ind'))
    # print('Method: ', request.method)
    # if request.method == 'GET':

    if form_enum.validate_on_submit():
        start_time = time.time()
        number_r = form_enum.number_r.data
        if number_r is None:
            number_r = form_enum.number_n.data
        dupes_list = edit_dupes_string(form_enum.number_dupes_str.data)

        perm_return =  perm_counter(
                              form_enum.perm_comb_ind.data,
                              form_enum.number_n.data,
                              number_r,
                              dupes_list
                              )

        split_list = perm_return.split(' ')
        perm_rc = split_list[0]
        perm_result = split_list[1]

        if int(perm_rc) == 0:
            perm_result_int = int(perm_result)
            perm_display = format(perm_result_int, ',d')
            #  If huge, also display in scientific notation
            if perm_result_int > 10 ** 9:     #  greater than a billion
                sci_display = '%.9E'  % Decimal(perm_result_int)
                #  I like superscripts for powers
                sci_display = sci_display.replace('E+', ' x 10<sup>')  +  '</sup>'
        else:
            perm_display = '*** Error encountered. Contact developer with complete details '  + \
                           'if a fix is desired.  ***'

        elapsed_time = time.time() - start_time
        elapsed_seconds = str(round(elapsed_time, 4))
        elapsed_time = 'Elapsed time '  +  elapsed_seconds

        # log the transaction to stdout for GCP
        print('S\tE\t',
              request.environ['REMOTE_ADDR'], '\t',
              elapsed_seconds,                '\t',
              form_enum.perm_comb_ind.data,   '\t',
              form_enum.number_n.data,        '\t',
              number_r,                       '\t',
              dupes_list,                     '\t',
              perm_return
              )
    else:
        #  Was data actually submitted?
        if request.method == 'POST':
            # log the transaction to stdout for GCP
            print('F\tE\t',
                  request.environ['REMOTE_ADDR'],  '\t',
                  form_enum.perm_comb_ind.data,    '\t',
                  form_enum.perm_comb_ind.errors,  '\t',
                  form_enum.number_n.data,         '\t',
                  form_enum.number_n.errors,       '\t',
                  form_enum.number_r.data,         '\t',
                  form_enum.number_r.errors,       '\t',
                  form_enum.number_dupes_str.data, '\t',
                  form_enum.number_dupes_str.errors
                  )

    #  03/15/2019 debugging code for Radio buttons box enclose problem.
    # print(form_enum)
    # print('\nvars(form_enum): ', 'type: ', type(form_enum))
    # pprint(vars(form_enum))

    # print('\nvars(form_enum.perm_comb_ind): ', 'type: ', type(form_enum.perm_comb_ind))
    # pprint(vars(form_enum.perm_comb_ind))

    # print('\nvars(form_enum.submit):')
    # pprint(vars(form_enum.submit))

    return render_template('perm_enum.html', title='Enumerate', form=form_enum,
                           perm_result=perm_display,
                           perm_sci_result=sci_display,
                           time_display=elapsed_time
                           )

#
#
@app.route("/enumerate_word/", methods=['GET', 'POST'])
def perm_enum_word_f():

    form_enum = PermEnumWordForm()    #  using the same object name this time
    perm_display = ''
    elapsed_time = ''

    if form_enum.validate_on_submit():
        start_time = time.time()

        wk_word = form_enum.word_in.data

        number_r = form_enum.number_r.data
        wk_word = wk_word.replace(' ', '')  # remove spaces
        char_list = list(wk_word)           # character_list
        N = len(char_list)
        if number_r is None:
            number_r = N
        #  Get the frequency of each character
        #  this contains a dictionary like this:
        #  Counter({'B': 2, 'A': 1, 'Y': 1})
        freq_char_list = Counter(wk_word)
        dupes_list = []
        for char in freq_char_list:
            dupes_list.append(freq_char_list[char])

        perm_return =  perm_counter(
                              form_enum.perm_comb_ind.data,
                              N,
                              number_r,
                              dupes_list
                              )

        split_list = perm_return.split(' ')
        perm_rc = split_list[0]
        perm_result = split_list[1]

        if int(perm_rc) == 0:
            perm_display = format(int(perm_result), ',d')
        else:
            perm_display = '*** Error encountered. Contact developer with complete details '  + \
                           'if a fix is desired.  ***'

        elapsed_time = time.time() - start_time
        elapsed_seconds = str(round(elapsed_time, 4))
        elapsed_time = 'Elapsed time '  +  elapsed_seconds

        # log the transaction to stdout for GCP
        print('S\tEW\t',
              request.environ['REMOTE_ADDR'], '\t',
              elapsed_seconds,                '\t',
              form_enum.perm_comb_ind.data,   '\t',
              form_enum.word_in.data,         '\t',
              N,                              '\t',
              form_enum.number_r.data,        '\t',
              dupes_list,                     '\t',
              perm_return
              )
    else:
        #  Was data actually submitted?
        if request.method == 'POST':
            # log the transaction to stdout for GCP
            print('F\tEW\t',
                  request.environ['REMOTE_ADDR'],  '\t',
                  form_enum.perm_comb_ind.data,    '\t',
                  form_enum.perm_comb_ind.errors,  '\t',
                  form_enum.word_in.data,          '\t',
                  form_enum.word_in.errors,        '\t',
                  form_enum.number_r.data,         '\t',
                  form_enum.number_r.errors
                  )

    return render_template('perm_enum_word.html', title='Enumerate Word', form=form_enum,
                           perm_result=perm_display,
                           time_display=elapsed_time
                           )

#
#    Generate Permutations given an input Word/String of characters.
#
@app.route("/generate/", methods=['GET', 'POST'])
def perm_generate_f():

    form_gen = PermGenerateForm()
    perm_display_list = []
    elapsed_time = ''
    elapsed_seconds = 0

    raw_perm_limit   = -1
    raw_perm_limit   = 5000000     #   5 million    #  no longer applicable  03/13/2019
    output_type = 'W'                #  Word or Tuples of Characters
    diagnostic_string = ''

    if form_gen.validate_on_submit():
        # pprint(vars(form_gen))
        # print('SW:', form_gen.submit_word.data)   #   True if 'Generate Words' button clicked
        start_time = time.time()
        wk_word = form_gen.word_in.data

        number_r = form_gen.number_r.data
        wk_word = wk_word.replace(' ', '')  # remove spaces
        char_list = list(wk_word)           # character list
        N = len(char_list)
        #    the default for R is N
        if number_r is None:
            number_r = N

        #  Get the frequency of each character
        #  this contains a dictionary like this:
        #  Counter({'B': 2, 'A': 1, 'Y': 1})
        freq_char_list = Counter(wk_word)
        dupes_count_list = []
        for char in freq_char_list:
            dupes_count_list.append(freq_char_list[char])

        #  This is home-grown module
        perm_return =  perm_counter(
                              form_gen.perm_comb_ind.data,
                              N,
                              number_r,
                              dupes_count_list
                              )

        split_list = perm_return.split(' ')
        cooked_perm_count = int(split_list[1])

        # Memory is limited and itertools -- no longer used -- generates all the duplicates tuples first
        # and then set removes duplicates.
        # so calculate the number of tuples (with duplicates) first and hold to a limit.
        raw_perm_count = factorial(N) / factorial(N - number_r)

        if raw_perm_count <= raw_perm_limit  or  \
           raw_perm_limit == -1:
            if cooked_perm_count <= display_limit:
                if form_gen.perm_comb_ind.data == 'P':
                    # this next statement can be VERY inefficient since the duplicated permutations are created first
                    # perm_display_list = set(itertools.permutations(char_list, number_r ))
                    #   03/11/2019  found this:  VERY fast
                    perm_display_gen = multiset_permutations(char_list, number_r)
                else:
                    # perm_display_list = set(itertools.combinations(char_list, number_r ))
                    perm_display_gen = multiset_combinations(char_list, number_r)

                if form_gen.submit_word.data is True:
                    perm_display_list = []
                    for  entry in perm_display_gen:
                        entry_word = ''.join(entry)
                        entry_word = entry_word.strip()
                        perm_display_list.append(entry_word)
                else:
                    perm_display_list = list(perm_display_gen)
                    output_type = 'T'   #  not actual Python tuples

                raw_perm_count_int    = int(raw_perm_count)
                elapsed_time = time.time() - start_time
                elapsed_seconds = str(round(elapsed_time, 4))
                elapsed_time = 'Elapsed time '  +  elapsed_seconds
                diagnostic_string =  \
                               ' Raw count: '      +  f'{raw_perm_count_int:,d}'  +  \
                               '  Cooked count: '  +  format(int(cooked_perm_count), ',d')

                log_list = 'L:'  +  str(len(perm_display_list))
            else:
                perm_display_list  = ['Display limit of ' +  str(display_limit)  + ' exceeded.',
                                      'Generation count of '  +  str(cooked_perm_count)]
                log_list = perm_display_list
        else:
            perm_display_list  = ['Raw Permutation list limit of ' +  str(raw_perm_limit)  + ' exceeded.',
                                      'Calculated count of '  +  str(raw_perm_count)]
            log_list = perm_display_list

        # log the transaction to stdout for GCP.
        print('S\tG\t',
              request.environ['REMOTE_ADDR'], '\t',
              elapsed_seconds,                '\t',
              form_gen.perm_comb_ind.data,    '\t',
              wk_word,                        '\t',
              form_gen.number_r.data,         '\t',
              log_list
              )

    else:
        #  Was data actually submitted?
        if request.method == 'POST':
            # log the transaction to stdout for GCP -- TO DO: add date and time.
            print('F\tG\t',
                  request.environ['REMOTE_ADDR'],      '\t',
                  form_gen.perm_comb_ind.data,         '\t',
                  form_gen.perm_comb_ind.errors,       '\t',
                  form_gen.word_in.data,               '\t',
                  form_gen.word_in.errors,             '\t',
                  form_gen.number_r.data,              '\t',
                  form_gen.number_r.errors)

    return render_template('perm_generate.html', title='Generate',
                           form=form_gen,
                           perm_count=format(len(perm_display_list), ',d'),
                           perm_result=perm_display_list,
                           perm_output_type=output_type,
                           time_display=elapsed_time,
                           perm_diag=diagnostic_string
                           )
#
#
@app.route("/discussion/")
def perm_discussion_f():
    return render_template('discussion.html', title='Discussion',
                           perm_discusss_limit=display_limit_edit,
                          )
