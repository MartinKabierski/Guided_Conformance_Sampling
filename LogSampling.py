import argparse
import os.path
import pickle
import time
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer

import LogIndexing
from SamplingAlgorithms import FeatureGuidedLogSampler, SequenceGuidedLogSampler, \
    RandomLogSampler, LongestTraceVariantLogSampler


def construct_sample(log_name, model_name, algorithm, sample_size, index_file, alignment_file=None):
    log, model, initial_marking, final_marking = __load_inputs(log_name, model_name)
    t_start = time.time()

    sample = None
    if algorithm == "feature":
        # TODO partition the log during the creation of the sampler
        partitioned_log, _ = LogIndexing.FeatureBasedPartitioning().partition(log, index_file=index_file)
        sampling_controller = FeatureGuidedLogSampler(index_file=index_file)
        #for debug purposes
        if alignment_file is not None:
            sampling_controller.alignment_cache = __load_prebuilt_alignments(log, alignment_file)
        sample = sampling_controller.construct_sample(log, model, initial_marking, final_marking, partitioned_log,
                                                      int(sample_size))
    elif algorithm == "behavioural":
        sampling_controller = SequenceGuidedLogSampler(log, batch_size=5, index_file=index_file)
        #for debug purposes
        if alignment_file is not None:
            sampling_controller.alignment_cache = __load_prebuilt_alignments(log, alignment_file)
        sample = sampling_controller.construct_sample(log, model, initial_marking, final_marking, int(sample_size))

    # only used for debugging and evaluation purposes
    elif algorithm == "Random":
        sampling_controller = RandomLogSampler()
        sample = sampling_controller.construct_sample(log, model, initial_marking, final_marking, int(sample_size))

    elif algorithm == "Longest":
        sampling_controller = LongestTraceVariantLogSampler()
        sample = sampling_controller.construct_sample(log, model, initial_marking, final_marking, int(sample_size))
    else:
        print(f"Algorithm {algorithm} is not supported.")

    if sample is not None:
        print(f"Sampling done. Total time elapsed: {(time.time() - t_start):.3f}")
        print(f"Times: {sample.times}")

    return sample


def __load_inputs(log_name, model_name):
    log = xes_importer.apply(str(log_name))
    model = None
    print("loading model")
    model, initial_marking, final_marking = pm4py.read_pnml(os.path.join(str(model_name)))
    return log, model, initial_marking, final_marking


def __load_prebuilt_alignments(log, alignment_file):
    print("DEBUG: loading precomputed alignments...")
    aligned_traces = pickle.load(open(alignment_file, "rb"))
    trace_keys = []
    for trace in log:
        event_representation = ""
        for event in trace:
            event_representation = event_representation + " >> " + event["concept:name"]
        trace_keys.append(event_representation)

    assert (len(trace_keys) == len(log))
    return dict(zip(trace_keys, aligned_traces))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", help="the sampling strategy to use [feature, behavioural]")
    parser.add_argument("sample_size", help="the size of the final sample")
    parser.add_argument("log_file", help="the name of the xes-log from which to sample")
    parser.add_argument("model_file", help="the name of the .pnml-file used for conformance checking")
    parser.add_argument("-index_file", help="the name of the index file containing the features considered during "
                                            "indexing. If none is supplied, all features are considered")
    parser.add_argument("-alignments", help=argparse.SUPPRESS)
    args = parser.parse_args()
    construct_sample(args.log_file, args.model_file, args.algorithm, args.sample_size, args.index_file, args.alignments)
