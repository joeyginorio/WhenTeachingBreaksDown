# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------

import itertools
import numpy as np
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater

class InferenceMachine():
	"""
		Main project class. Combines the tools for hypothesis generation and updates
		to generate the final inferences of interest, namely the probability that a
		specific example would be taught out of the space of all examples.

	"""

	def evaluateExample(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
							independent=True, option=0):
		"""
			Returns value for an example V(e). Equivalent to the posterior belief of
			the trueHypothesis for the learner.

			Params:
				hypothesisSpace - Fed from HypothesisSpaceGenerator()
				examples - a list of teacher examples e.g. ['A','B',['B','C']]
				trueHypothesis - the combination that turns blicket detector on e.g. 'A'
				hUpdater - instance of HypothesisSpaceUpdater class, calculates posterior 
							belief of the learner.
				lambda_noise - how much does learner mistrust teacher data 
				option - chooses recursive/nonrecursive update

		"""

		# Find index of trueHypothesis in learner's hypothesis space
		trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
		
		# Run a hypothesis update on learner using the examples provided
		hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples,
					lambda_noise,independent, option)

		# Calculate V(e) of example
		return hUpdater.hSpacePosterior[trueHypothesisIndex]

	def probabilityOfExamples(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
								 independent=True, option=0, tau=.1):
		"""
			Returns the probability of teaching an example.

			Params:
				hypothesisSpace - Fed from HypothesisSpaceGenerator()
				examples - a list of teacher example e.g. ['A','B',['B','C']]
				trueHypothesis - the combination that turns blicket detector on e.g. 'A'
				hUpdater - instance of HypothesisSpaceUpdater class, calculates posterior 
							belief of the learner.
				lambda_noise - how much does learner mistrust teacher data 
				option - chooses recursive/nonrecursive update
				
		"""

		# Saves actionSpace contained in hypothesisSpace from generator
		self.actionSpace = hypothesisSpace[2]
		self.actionSpace = list(itertools.permutations(self.actionSpace, len(examples)))

		# Removes actionSpace from hypothesisSpace list
		hypothesisSpace = hypothesisSpace[0:2]

		# Saves example index, to look up probability later
		exampleIndex = self.actionSpace.index(tuple(examples))

		# Initialize the probability distribution 
		actionDistribution = list()

		# For each possible example, calculate its value, V(e)
		for action in self.actionSpace:
			actionDistribution.append(self.evaluateExample(hypothesisSpace, trueHypothesis, 
				list(action), lambda_noise, independent, option))

		# Turn the list of values into a distribution through softmax
		self.actionDistribution = self.softMax(actionDistribution,tau)

		# Returns probability of example being taught out of all possible examples
		
		return self.actionDistribution[exampleIndex]


	def softMax(self, arg, tau):
		"""
			Returns the softmax of arg.

			Params:
				arg - a list of values
				tau - rationality paramater 

		"""
		# e^(i/tau) for each value in arg
		# arg = [np.exp(i/tau) for i in arg]
		arg = np.array(arg)
		arg = np.exp(arg/tau)

		# compute sum to normalize
		arg /= arg.sum()
		
		return list(arg)


