import inspect
import os

class Pig(object):
    def __init__(self, input_pig_scripts, params, output_file_name):
        self.input_pig_scripts = input_pig_scripts
        self.params_str = self.get_params_str(params)
        if output_file_name == None:
            self.output_pig_script = inspect.stack()[1][1].split('/')[-1][:-3] + '.pig'
        else: self.output_pig_script = output_file_name
    def get_params_str(self, params):
        if params:
            return ' -p ' + ' -p '.join(map(lambda (k,v): '%s=%s'%(k,v), params))
        return ''
    def combine_files(self, input_files, output_file):
        dash = ' --------------------------------- '
        f = open(output_file, 'w') 
        for input_file in input_files:
            print 'Adding %s'%input_file
            f.write(dash + input_file + dash + '\n')
            map(lambda line: f.write(line), open(input_file).readlines())
            f.write(dash + dash + '\n\n\n')
        f.close()
    def generate_output_pig_script(self):
        print 'Generating %s script...'%self.output_pig_script
        self.combine_files(self.input_pig_scripts, self.output_pig_script)
        print 'Done.'
    def run(self, just_check=True):
        self.generate_output_pig_script()
        print 'Running pig script'
        if just_check: command = 'pig -c %s %s'%(self.params_str, self.output_pig_script)
        else: command = 'pig %s %s'%(self.params_str, self.output_pig_script)
        print '=> ',command; os.system(command)