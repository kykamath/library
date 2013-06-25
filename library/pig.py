from classes import GeneralMethods
import inspect

class Pig(object):
    def __init__(self, input_pig_scripts, params):
        self.input_pig_scripts = input_pig_scripts
        self.params_str = self.get_params_str(params)
        self.output_pig_script = inspect.stack()[1][1].split('/')[-1][:-3] + '.pig'
    def get_params_str(self, params):
        if params:
            return ' -p ' + ' -p '.join(map(lambda (k,v): '%s=%s'%(k,v), params))
        return ''
    def combine_files(self, input_files, output_file):
        with open(output_file, 'w') as f:
            dash = ' --------------------------------- '
            for input_file in input_files:
                print 'Adding %s'%input_file
                f.write(dash + input_file + dash + '\n')
                map(lambda line: f.write(line), open(input_file).readlines())
                f.write(dash + dash + '\n\n\n')
    def generate_output_pig_script(self):
        print 'Generating %s script...'%self.output_pig_script
        self.combine_files(self.input_pig_scripts, self.output_pig_script)
        print 'Done.'
    def run(self):
        self.generate_output_pig_script()
        print 'Running pig script'
        GeneralMethods.runCommand('pig %s %s'%(self.params_str, self.output_pig_script))