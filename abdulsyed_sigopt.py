from sigopt import Connection
import matplotlib.pyplot as plt

"""
This is Abdul Syed's solution to SigOpts best seen trace fetching.

References used:
SigOpt Docs:
https://arxiv.org/pdf/1605.06170.pdf - to better understand SigOpt tools.
https://sigopt.com/docs/overview/pagination - learn about pagination
https://sigopt.com/docs/endpoints/observations/list_detail - Observation object
http://blog.sigopt.com/post/144221180573/evaluating-hyperparameter-optimization-strategies blog post


Other references:
http://matplotlib.org/users/pyplot_tutorial.html - to learn how to plot in python.
"""

TOKEN = "VAIKECTPQCWFBIVMWRYEYFIRUUKXRVAUFCSTAENZLEJWAXUV"

def getSigOptConnection(client_token):
    """Return connection to SigOpt by taking token as input."""
    return Connection(client_token)

def fetchObervations(experiment_id, connection):
    """Return list of Observations based on experiment ID and
    existing connection."""
    return list(connection.experiments(experiment_id).observations().fetch().iterate_pages())

def returnObservationsFromEarliestToLatest(observations):
    """Helper function to reverse list of observations, so it's from earliest
    to latest."""
    return reversed(observations)

def findBestSeenTrace(observations):
    """Function to populate best seen trace."""
    #instantiate variables and set max_value to 0
    best_seen_trace = []
    max_value = 0
    for observation in returnObservationsFromEarliestToLatest(observations):
        # This should cover the case for Null. Tested in Python and any number
        # value > None. So if first value is Null, then this should just
        # get populated as 0.
        if observation.value > max_value:
            best_seen_trace.append(observation.value)
            max_value = observation.value
        else:
            best_seen_trace.append(max_value)
    return best_seen_trace

def plotBestSeenTrace(best_seen_trace):
    """Plot best seen trace using Matlab lib."""
    plt.plot(best_seen_trace)
    plt.ylabel('Value')
    plt.xlabel('Observations')
    plt.show()

def getBestSeenTrace(experiment_id, token, return_plot=False):
    """Get best seen trace for users.

    Args:
        experiment_id: ID of the experiment in SigOpt.
        token: Token provided by SigOpt to make connection.
        return_plot: bool value that determines whether to return a best seen
              trace plot.
    Returns:
        best_seen_trace: list of best seen trace
        plot: if user selects this option, then plot is returned.
    """
    best_observations = findBestSeenTrace(
        fetchObervations(6110, getSigOptConnection(token)))
    if return_plot:
        plotBestSeenTrace(best_observations)
    else:
        return best_observations

def main():
    print (getBestSeenTrace(6110, TOKEN, False))
    print (getBestSeenTrace(6110, TOKEN, True))


if __name__ == '__main__':
  main()
