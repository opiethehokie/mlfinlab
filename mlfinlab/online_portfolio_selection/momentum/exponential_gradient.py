# pylint: disable=missing-module-docstring
import numpy as np
from mlfinlab.online_portfolio_selection.online_portfolio_selection import OLPS


class ExponentialGradient(OLPS):
    """
    This class implements the Exponential Gradient Portfolio strategy. It is reproduced with modification from the
    following paper: Li, B., Hoi, S. C.H., 2012. OnLine Portfolio Selection: A Survey. ACM Comput. Surv. V, N,
    Article A (December YEAR), 33 pages. DOI:http://dx.doi.org/10.1145/2512962.

    Exponential gradient strategy tracks the best performing stock in the last period while keeping previous portfolio
    information by using a regularization term
    """

    def __init__(self, eta=0.05, update_rule='MU'):
        """
        Initializes with eta and update_rule

        :param eta: (float) learning rate
        :param update_rule: (str) 'MU': Multiplicative Update, 'GP': Gradient Projection, 'EM': Expectation Maximization
        """
        self.eta = eta
        self.update_rule = update_rule
        super().__init__()

    def update_weight(self,
                      _time):
        """
        Updates portfolio weights

        :param _time: (int) current time period
        :return new_weight: (np.array) new portfolio weights using exponential gradient
        """
        # gets the last window's price relative
        past_relative_return = self.relative_return[_time - 1]

        # takes the dot product of the two
        dot_product = np.dot(self.weights, past_relative_return)

        # calculate for multiplicative update
        if self.update_rule == 'MU':
            new_weight = self.weights * np.exp(self.eta * past_relative_return / dot_product)

        # calculate for gradient projection
        elif self.update_rule == 'GP':
            new_weight = self.weights + self.eta * (past_relative_return - np.sum(past_relative_return) /
                                                    self.number_of_assets) / dot_product

        # calculate for expectation maximization
        elif self.update_rule == 'EM':
            new_weight = self.weights * (1 + self.eta * (past_relative_return / dot_product - 1))
        new_weight = self.normalize(new_weight)
        return new_weight