# okay, this is where i put all my loggers - thi sis exciting I'm actually getting stuff working somehow
# and this is the sort of thing that goes into actually big projects... so it's exciting in the extreme yay!
# anyhow, let's use classes to build loggers!

import numpy as np
from utils import *

# this is the base logger class, but who knwos?

# function to convert the dictionary of dictoinary to list of lists format
def convert_logs_to_numpy_arrays(logs):
	if type(logs) is 'numpy.ndarray':
		return logs
	if type(logs) is 'dict':
		return convert_logs_to_lists(logs)
	if type(logs) is 'list':
		return np.array(logs)
	else:
		raise TypeError('Type not recognised. Should be dict or list or numpy array; got: ' + str(type(logs)))


def convert_logs_to_lists(logs):
	if type(logs) is 'list':
		return logs
	if type(logs) is 'dict':
		l = []
		for v in logs.values():
			l.append(convert_logs_to_lists(v))
		return l
	else:
		raise TypeError('Something went wrong with types here. Expected list or dict. Got: ' + str(type(logs)))

class BaseLogger():

	def __init__(self, save_name):
		self.save_name = save_name
		self.logs = {}
		self.current_epoch = 0

	def get_save_name(self):
		return self.save_name

	def _set_save_name(self, save_name):
		self.save_name = save_name

	def save(self):
		save(self.logs, save_name)
		return True

	def get_logs(self):
		return self.logs

	def _set_logs(self, logs):
		self.logs = logs

	def get_current_epoch(self):
		return self.current_epoch

	def _set_current_epoch(self, epoch):
		self.current_epoch = epoch


	def log(self, input_class):
		pass

	def on_training_end(self):
		self.save()

	# these are the key functions to be honest by default it will save at the end of training
	# and will add logs to logs... btut who nkwos in actuality!

# to be fair I should probably actually use the keras example of callbacks as simple things instead of loggers
# and the like for the library as they are more general, but who knwos really
# at the moment it just saves but it probably shouldn't 
# i.e. it just does on epoch end but who knwos! it's cool I can actually begin to understand keras code
# in a fairly straightfowrwad way... it's nice!


class BasicLogger(BaseLogger):

	# okay the aim here is to figure out what it wants you to log
	# and try to log it generally
	# as a dict which it then saves, so let's figure it out
	def __init__(self, save_name,log_list = ['predictions','prediction_errors','weights','activations'], epoch_per_log=1):
		print type(save_name)
		if type(save_name) is not type('str'):
			raise TypeError('Save name should be a string')
		self.save_name = save_name
		if type(log_list) is type([1,2]) or type(log_list) is type('str'):
			if type(log_list) is type([1,2]):
				self.log_list = log_list
			if type(log_list) is type('str'):
				self.log_list = [log_list]
		else:
			raise TypeError('Log list must either be a list of loggable attributes or a string of a single loggable attribute. You inputted: ' + str(type(log_list)))
		
		print self.log_list
		if type(epoch_per_log) is not type(3):
			raise TypeError('Number of epochs per log must be an integer. You inputted: ' + str(type(epoch_per_log)))

		#now do the value error
		if epoch_per_log <=0:
			raise ValueError('Epoch per log must be a positive nonzero number')

		# initizliase the logs
		self.logs = {}
		self.current_epoch = 0
		self.epoch_per_log = epoch_per_log

	def log(self, input_class):
		# so what this does is return a dict of the current epoch and for each epoch it calculates this stuff
		if self.current_epoch % self.epoch_per_log == 0:
			# only log after the correct nmber of epochs
			l = {}
			# it's got to be a dictoinary of dictionaries!
			# so it's important just to get the layers right
			# and then do it from there
			# so first just get the model, that seems reasonable!
			if hasattr(input_class, 'model'):
				layers = getattr(input_class, 'model')
				for i in xrange(len(layers)):
					layer = layers[i]
					vals = {}
					for attr in self.log_list:
						# should try this and if it fails then raise
						if hasattr(input_class, attr) and layer.__trainable == True:
							vals[attr] = getattr(input_class, attr)
						else:
							raise AttributeError('Layer ' + str(i) + ' does not have the attribute: ' + str(attr))
				#after the list add it to l
					l['Layer_'+str(i)] = vals
			else:
				raise AttributeError('Model class should have model attribute containing the layers of the modell')

			logs['epoch_' + str(current_epoch)] = l
		# increment the epochs!
		self.current_epoch += 1
	# hopefully this will be sufficient. who knows!
	# it's a fairly straightforward logging activity this logger and it is fairly comprehensive in actuality
	# so it might work. it's quite cool!


	# another thing I really need to do now is to reread all the things and figure out the bogacz model so it's not that difficult
	# because the bogacz tutorial is pretty perfect really
	# and I will need to actually fulfill the friston model with a large amount of tutorials and the like
	# as this is generally a very impressive library
	# and I should start a research blog and so forth perhaps also. to get my persnoal brand out there in the world
	# seems like something that could/should be reasonable!