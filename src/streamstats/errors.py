class StreamStatsError(Exception):
    pass

class UnsupportedFormatError(StreamStatsError):
    pass

class InvalidEventError(StreamStatsError):
    pass

class InvalidTimestampError(StreamStatsError):
    pass

class CLIConfigError(StreamStatsError):
    pass

class InvalidDelimiterError(StreamStatsError):
    pass

class UnmatchedFormatsError(StreamStatsError):
    pass
