import cProfile, pstats, io
from pstats import SortKey
from parsers.markers.location.country import CountryParser
from core import util
from loguru import logger
from main import redact_data, text_to_pii


class ProfilerStat():
    def __init__(self, calls, total_time, percall, cumtime, file):
        self.calls = calls
        self.total_time = total_time
        self.percall = percall
        self.cumtime = cumtime
        self.file = file
    def __str__(self):
        return "File: {0} \n Total Calls: {1} \n Time: {2}".format(self.file, self.calls, self.cumtime)

def run_profiler(text):
    pr = cProfile.Profile()
    pr.enable()
    pii = text_to_pii(text)  # Detect PII in the given text stream
    redacted_text = redact_data(text, pii)
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.strip_dirs().sort_stats(-1).print_stats()
    output = s.getvalue().splitlines()
    total_time_with_functions = output[0].strip()
    profiler_stats = []
    for line in output[5:]:
        stats = line.split(" ")
        if len(stats) > 6:
            profile_list = [i for i in stats if i != ""]
            profiler_stats.append(ProfilerStat(profile_list[0],profile_list[1],profile_list[2],profile_list[3], ''.join(profile_list[5:])))
    logger.info(total_time_with_functions)
    profiler_stats.sort(key=lambda x: x.cumtime, reverse=True)
    logger.info('Top Ten Contributors')
    for stat in profiler_stats[0:10]:
        logger.info(stat)

if __name__ == "__main__":

    DIRECTORY = 'tests/data/'
    small_input_file = 'small_test.txt'
    small_text_file = f'{DIRECTORY}{small_input_file}'
    small_text = open(small_text_file, 'r').read()
    logger.info('Run for Small Text')
    run_profiler(small_text)
    large_input_file = 'large_test.txt'
    large_text_file = f'{DIRECTORY}{large_input_file}'
    large_text = open(large_text_file, 'r').read()
    logger.info('Run for Large Text')
    run_profiler(large_text)

