import sys

def progress_bar(iteration, total, bar_length=50):
    """
    Call in a loop to create a terminal progress bar.
    
    Parameters:
    - iteration (int): Current iteration.
    - total (int): Total number of iterations.
    - bar_length (int): Character length of the progress bar. Default is 10.
    """
    percent_complete = iteration / total
    num_x = int(percent_complete * bar_length)
    bar = '|' + '#' * num_x + '-' * (bar_length - num_x) + '|'

    # Print progress bar
    sys.stdout.write(f'\r{bar} {int(percent_complete * 100)}%')
    sys.stdout.flush()

    # Print a newline at the end of the progress
    if iteration == total - 1:
        print("\nDone!")
