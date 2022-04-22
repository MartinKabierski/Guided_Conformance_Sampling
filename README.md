# Relevance-guided Sampling for Conformance Checking

This repository contains an implementation, as well as the used experimental result data for the article ["Sampling What Matters: Relevance-guided Sampling of Event Logs"](https://ieeexplore.ieee.org/document/9576875).

The proposed sampling procedures guide the selection of traces to be included in a sample by learning which features of a trace correlate with trace properties of interest (so far we used deviating traces as interesting).

## How to use ##
### Using the command line interface ###
To generate a sample of the log from the command line, run:

```
python3 Logsampling.py <-index_file INDEX_FILE> <feature|behavioural> <sample size> <log_file> <model_file>
```

The parameters are
* ``algorithm`` - the indexing type to use. Can be either "feature" or "behavioural"
* ``sample size`` - the desired sample size
* ``log_file`` - the provided log file, in .xes format
* ``model_file`` - the model file used during sampling, in .pnml format
* ``index_file`` - (Optional)  the index file, containing the features to consider during sampling

### Invoking the classes from code ###
Alternatively, you can invoke the provided classes in your own project. To do this, add the following lines to your project:

#### Feature-based ####
```python
partitioned_log = LogIndexing.FeatureBasedPartitioning().partition(log, index_file=index_file)
sampler = FeatureGuidedLogSampler(index_file=index_file)
sample = sampler.construct_sample(log, model, initial_marking, final_marking, partitioned_log, sample_size)
```

#### Behavioural-based ####
```python
sampler = SequenceGuidedLogSampler(log, batch_size=5, index_file=index_file)
sample = sampler.construct_sample(log, model, initial_marking, final_marking, sample_size)
```

## Index Files ##
By providing an index-file, you can specify, what log attributes may be considered as relevant during the generation of the sample.
In this xml-file you can specify the trace-level attributes, event-level attributes, k-gram lengths and potential preceeding discreditization steps, that comprise the feature index, that guides the sampling procedure.

The structure of the .xml-file is as follows
```xml
<index>
  <k>3</k>                                        #use activity k-grams of length 3
  <discretize>
    <attribute>attribute a</attribute>            #discretize trace-level attribute 'a' using a bucket size of 10
    <trace-level>true</trace-level>
    <bucket_width>10</bucket_width>
  </discretize>
    <discretize>
    <attribute>attribute b</attribute>             #discretize event-level attribute 'b' using a bucket size of 5
    <trace-level>false</trace-level>
    <bucket_width>5</bucket_width>
  </discretize>
  <discretize>                                    #additional attributes that need discretization
    ...
  </discretize>
  
  <features>
    <trace-level>
      <attribute>attribute a</attribute>          #incorporate trace-level attribue 'a'
      ...                                         #additional trace-level attributes to incorporate
    </trace-level>
    <event-level>
      <attribute>attribute b</attribute>          #incorporate event-level attribue 'b'
      ...                                         #additional event-level attributes to incorporate
    </event-level>
  </features>
</index>
```
If no index file is provided, all features without discretization, as well as 3-grams, are considered.

## Evaluation and result files ##
Under [results](https://github.com/MartinKabierski/Guided_Conformance_Sampling/tree/master/results), we provide the scripts used for the experimental evaluation of the proposed sampling procedures ([eval.py](https://github.com/MartinKabierski/Guided_Conformance_Sampling/blob/MartinKabierski-patch-1/eval.py)) and plot generation ([generate_plots.py](https://github.com/MartinKabierski/Guided_Conformance_Sampling/blob/MartinKabierski-patch-1/generate_plots.py)). Furthermore, the directory contains the .csv-files and the plots generated using those scripts, that were used in the article.


## Citing this work ##
If you use this repository, please cite the article:
```
@INPROCEEDINGS{9576875,
  author={Kabierski, Martin and 
    Nguyen, Hoang Lam and 
    Grunske, Lars and 
    Weidlich, Matthias},
  booktitle={2021 3rd International Conference on Process Mining (ICPM)}, 
  title={Sampling What Matters: Relevance-guided Sampling of Event Logs}, 
  year={2021},
  volume={},
  number={},
  pages={64-71},
  doi={10.1109/ICPM53251.2021.9576875}}
}
```
