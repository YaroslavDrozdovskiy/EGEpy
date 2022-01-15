import math
from ...GenBase import SingleChoice
from ...LangTable import unpre, table
from ...Prog import make_block

class CountBySign(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        iteration_variable = self.rnd.index_var()[0]
        c_language_comment = unpre(
            f'''/* В программе на языке Си следует считать, что массивы A и B
            индексируются начиная с 1 и состоят из элементов
            A[1], … A[{array_length}], B[1], … B[{array_length}] */'''
        )
        first_loop_body = [
            '=', ['[]', 'A', iteration_variable], [ '*', iteration_variable, iteration_variable ],
        ]
        second_loop_body = [
            '=', [ '[]', 'B', iteration_variable ], [ '-', [ '[]', 'A', iteration_variable ], array_length ],
        ]
        code_block_parts = [
            'for', iteration_variable, 1, array_length, first_loop_body,
            'for', iteration_variable, 1, array_length, second_loop_body,
            '#', { 'C': c_language_comment },
        ]
        code_block = make_block(code_block_parts)
        lang_table = table(code_block, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])
        case = self.rnd.pick([
            { 'name': 'положительные', 'test': lambda x: x > 0 },
            { 'name': 'отрицательные', 'test': lambda x: x < 0 },
            { 'name': 'неотрицательные', 'test': lambda x: x >= 0 },            
        ])
        self.text = f'''Значения двух массивов A и B с индексами от 1 до {array_length}
            задаются при помощи следующего фрагмента программы: {lang_table}
            Какое количество элементов массива B[1..{array_length}] будет принимать
            {case['name']} значения после выполнения данной программы?'''

        array_B = code_block.run_val('B')
        correct = len(list(filter(lambda x: case['test'](x), array_B.values())))
        errors = [
            correct + 1, correct - 1, array_length - correct, array_length - correct + 1, array_length - correct - 1
        ]
        self.set_variants([correct] + self.rnd.pick_n(3, errors))
        return self

class FindMinMax(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        # Нужно гарантировать единственные максимум и минимум.
        value = self.rnd.in_range(array_length // 2 + 1, array_length - 1)
        iteration_variable = self.rnd.index_var()[0]
        d1 = [ '-' ] + self.rnd.shuffle([ iteration_variable, value ])
        d2, d3 = self.rnd.shuffle([
            iteration_variable, [ '-', array_length + 1, iteration_variable]
        ])
        first_loop_body = [
            '=', [ '[]', 'A', iteration_variable ], [ '*', d1, d1 ],
        ]
        second_loop_body = [
            '=', [ '[]', 'B', d2 ], [ '[]', 'A', d3 ],
        ]
        code_block_parts = [
            'for', iteration_variable, 1, array_length, first_loop_body,
            'for', iteration_variable, 1, array_length, second_loop_body,
        ]
        code_block = make_block(code_block_parts)
        lang_table = table(code_block, [ [ 'Basic', 'Pascal', 'Alg' ] ])
        case = self.rnd.pick([
            { 'name': 'наибольшим', 'test': 1 },
            { 'name': 'наименьшим', 'test': -1 },
        ])
        self.text = f'''Значения двух массивов A[1..{array_length}] и B[1..{array_length}]
            задаются с помощью следующего фрагмента программы: {lang_table}
            Какой элемент массива B будет {case['name']}?'''

        # Analoge of '<=>' operator in Perl.
        def sign(x, y):
            if x < y:
                return -1
            elif x == y:
                return 0
            else:
                return 1

        array_B = code_block.run_val('B')
        correct = 1
        wrong = 1
        for i in range(2, array_length + 1):
            sn = sign(array_B[i], array_B[correct]) * case['test']
            if sn > 0:
                correct = i
            elif sn < 0:
                wrong = i
        
        seen = { correct: True }

        def filter_function(value):
            if not (1 <= value <= array_length) or (value in seen and seen[value]):
                return False
            seen[value] = True
            return True

        errors = list(filter(filter_function, [
            correct + 1, correct - 1, array_length - correct, array_length - correct  - 1, wrong, array_length - wrong
        ]))
        self.set_variants([f"B[{variant}]" for variant in [ correct ] + self.rnd.pick_n(3, errors)])
        return self


class CountOddEven(SingleChoice):
    def generate(self):
        return super().generate()

class AlgMinMax(SingleChoice):
    def generate(self):
        return super().generate()

class AlgAvg(SingleChoice):
    def generate(self):
        return super().generate()

class BusStation(SingleChoice):
    def generate(self):
        return super().generate()

    def _gen_schedule_text(self):
        pass

    def _random_routes(self):
        pass

    def _stime(self):
        pass

class CrcMessage(SingleChoice):
    def generate(self):
        return super().generate()

class InfSize(SingleChoice):
    def generate(self):
        return super().generate()
