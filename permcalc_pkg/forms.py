#  forms.py   for the Permutations and Combinations Calculators project
#   03/07/2019: Created Warren Van Wyck using WTForm 2.2.1
#   03/20/2019: Add placeholders
#   11/19/19: Cosmetic changes for Sublime Linter.


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, validators
from wtforms.validators import ValidationError

#  edit the string field of duplicate counts.
#  replace commas with spaces
#  remove leading, trailing, and multiple spaces.
def edit_dupes_string(in_string):
    dupes_str_strip = in_string.strip()
    dupes_str_strip = dupes_str_strip.replace(',', ' ')
    dupes_str_strip = " ".join(dupes_str_strip.split())  # remove internal multiple spaces.
    dupes_list = dupes_str_strip.split(' ')
    return dupes_list

#
class PermEnumForm(FlaskForm):
    perm_comb_ind = RadioField('Choose Type:',
                               choices=[('P', 'Permutations'), ('C', 'Combinations')],
                               default='P'
                               )

    number_n = IntegerField('Enter N, number of elements in the group:',
                   validators=[validators.required(),
                               validators.NumberRange(min=1, max=1000,
                                        message="Must be a positive integer <= %(max)d")],
                               render_kw={"placeholder": "for example, 8"}
                               )

    number_r = IntegerField('Enter R, number of elements in the R-permutations/combinations (optional):',
                   validators=[validators.optional(),
                               validators.NumberRange(min=1, message="Must be a positive integer")],
                               render_kw={"placeholder": "for example, 4"}
                               )

    number_dupes_str = StringField('Enter Counts of duplicate elements in N (optional) -- separated by spaces:',
                               render_kw={"placeholder": "for example, 2 2"}
                               )

    submit = SubmitField('Enumerate (Count)')

#    'convention over configuration'  The validate_ prefix is the magic/convention.
    def validate_number_r(self, number_r):
        if number_r.data is None or self.number_n.data is None:
            pass
        else:
            if number_r.data > self.number_n.data:
                raise ValidationError('N must be greater than or equal to R.')

    def validate_number_dupes_str(self, number_dupes_str):
        #  In case N validation fails
        if number_dupes_str.data is None  or   \
           self.number_n.data    is None  or   \
           number_dupes_str.data == '':
            pass
        else:
            dupes_list = edit_dupes_string(number_dupes_str.data)
            dupes_list_len = len(dupes_list)

            if dupes_list_len > self.number_n.data:
                err_message = f'N must be greater than or equal to the count of duplicate elements.  Counted {dupes_list_len}'
                raise ValidationError(err_message)
            #   Check that every item is a positive integer
            dupes_sum = 0
            for dupe_item in dupes_list:
                try:
                    check_int = int(dupe_item)
                except ValueError:
                    err_message = f'This item is not an integer: "{ dupe_item }"  '
                    raise ValidationError(err_message)
                if check_int < 1:
                    err_message = f'This item is not a positive integer: "{ dupe_item }"  '
                    raise ValidationError(err_message)
                dupes_sum = dupes_sum + check_int

            #  The sum of the counts must not exceed N
            if dupes_sum > self.number_n.data:
                err_message = f'The sum of the duplicate counts "{ dupes_sum }"  is greater than N:  { self.number_n.data }.'
                raise ValidationError(err_message)

#
class PermEnumWordForm(FlaskForm):
    perm_comb_ind = RadioField('Choose Type:',
                               choices=[('P', 'Permutations'), ('C', 'Combinations')],
                               default='P'
                               )
    word_in = StringField('Enter Word/String -- any spaces will be removed:',
                validators=[validators.required(),
                            validators.Length(min=1, max=200,
                                        message="Word length must be <= %(max)d")  ],
                render_kw={"placeholder": "for example, DAFFODIL"}
                )

    number_r = IntegerField('Enter R, number of characters in the R-permutations/combinations (optional):',
                   validators=[validators.optional(),
                               validators.NumberRange(min=1, message="Must be a positive integer")],
                   render_kw={"placeholder": "for example, 4"}
                   )

    submit = SubmitField('Enumerate (Count)')

#
    def validate_number_r(self, number_r):
        if number_r.data is None or number_r.data <= len(self.word_in.data):
            pass
        else:
            raise ValidationError('R must be less than or equal to the length of the Word: '  +  \
                                   str(len(self.word_in.data)))

#
#
class PermGenerateForm(FlaskForm):
    perm_comb_ind = RadioField('Choose Type:',
                                choices=[('P', 'Permutations'), ('C', 'Combinations')],
                                default='P'
                                )

    word_in = StringField('Enter Word/String -- any spaces will be removed:',
                  validators=[validators.required(),
                      validators.Length(min=1, max=200,
                                        message="Word length must be <= %(max)d")  ],
                  render_kw={"placeholder": "for example, DAFFODIL"}
                  )


    number_r = IntegerField('Enter R, number of characters in the R-permutations/combinations (optional):',
                   validators=[validators.optional(),
                               validators.NumberRange(min=1, message="Must be a positive integer")],
                               render_kw={"placeholder": "for example, 4"}
                   )

    submit_word  = SubmitField('Generate Words')
    submit_tuple = SubmitField('Generate Tuples')

#  The length of a subgroup can't exceed the length of the word/string.
    def validate_number_r(self, number_r):
        if number_r.data is None or self.word_in.data is None:
            pass
        else:
            if number_r.data > len(self.word_in.data.replace(' ', '')):
                raise ValidationError('R must be less than or equal to length of Word: '  +  \
                                     str(len(self.word_in.data)))


#  end of module
