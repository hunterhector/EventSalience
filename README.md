This repository host code and pointers of models to our EMNLP 2018 paper: [Automatic Event Salience Identification](https://aclweb.org/anthology/D18-1154)

# Code
The following is the snapshot of the Code Base at the time of publication.
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/KnowledgeIR-master.zip

The ``salience`` directory contains the code for this project.

The data processing uses codes in [CMU Script repository](https://github.com/hunterhector/cmu-script), which on its own have two dependencies :cold_sweat: , but they should be easily installable with Maven. 

Further, the whole knowledge IR code base is being actively developed, but you proabably don't need them here. But for the sake of completeness, you can find it here:
https://github.com/xiongchenyan/KnowledgeIR

# Model
Two models are shared here, see the instructions [below](https://github.com/hunterhector/EventSalience/blob/master/README.md#instructions-of-running-the-pretrain-model) on how to use them:

The Event salience model: http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/event_salience.model (Note, not zipped)
This model is the one reported in the paper.

The joint Event Entity model: http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/salience_model.tar.gz (Note, this is a tarball)

The performance on events is slightly lower than what is reported on the paper (because the additional effort require to predict entity salience). Yet it is quite useful since it can predict both event salience and entity salience at the same time.

# Data
In this section, you can find the raw data, the annotation, and our preprocessed data. Due to copyright issues, you need to combine the raw data with the preprocessed data to obtain the full version that we used for training.

## Raw Data
The training and testing data are created from [Annotated NYT](https://catalog.ldc.upenn.edu/LDC2008T19), which is distributed by LDC. As restricted by the license, we only relese the annotations and generated parses.

The data split can be found [here](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/split/)

## Preprocessed data
To run our experiments, we recommend using the preprocess data here. These data contains the features extracted, but do not contain the original text.

The preprocessed data (and features) without the original text (i.e. I have replaced the fields "bodyText" and "abstract" with empty strings) can be found here:

   Pre-Train: http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/preprocess/train_no_text.gz
   
   Pre-Test: http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/preprocess/test_no_text.gz

The pretrained word (and entity) embeddings can be found here:
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/preprocess/embedding/

To obtain the text file corresponding to the preprocess data, run the following command in the cmu-script root directory:

```
bin/run_pipeline.sh salience edu.cmu.cs.lti.salience.annotators.SalienceDatasetTextOnlyWriter /Path_to_Annotated_NYT_LDC2008T19/data /Path_for_Text_output_of_LDC2008T19/ all_docs_with_abstract.lst 8
```
Note that 8 is the number of threads to be specified. all_docs_with_abstract.lst is the file listing all docs that have an abstract, which can be taken [here](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/split/all_docs_with_abstract.lst).

This command will create two folders (abstract and body), that contains the original news text. You can now fill in the empty slots in the Pre-Train and Pre-Test by matching the document name, the texts in these two folders correspond to the "abstract" and "bodyText" field respecitvely. After you add them back, let's name them ``train_with_text.json.gz`` and ``test_with_text.json.gz`` respectively


## Standalone annotations
These are annotation only, if you intend to start without using the preprocessing data, these could be useful.

#### Event Annotations:
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/event_data/train.gz
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/event_data/test.gz

#### Entity Annotations:
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/entity_data/train.gz
http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/entity_data/test.gz


# Results of the EMNLP paper

In the following link you can find the raw output of different models (including ablation) that are listed in the EMNLP table:

http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/results_emnlp

Where the [KCM.json](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/results_emnlp/kcm/KCM.json) is the best reported result (output of the full model).


# Reproducing EMNLP experiments
One can easily reproduce our experiments if the preprocessed data is ready. Assume you get the data (train_no_text.json.gz), and fill in the empty bodyText and abstract slots using the text created above into a file name "train_with_text.json.gz" (well, you will have write some simple match code yourself here.)

Now you can hash the training data to integer form for processing.

```
python -m knowledge4ir.salience.prepare.corpus_hashing config/conf_hash_event_train train_with_text.json.gz train_data.json.gz
```

Similarly, for test data:

```
python -m knowledge4ir.salience.prepare.corpus_hashing config/conf_hash_event_train test_with_text.json.gz test_data.json.gz
```

Once you have obtained that, you can use the [joint_center](https://github.com/xiongchenyan/KnowledgeIR/blob/master/knowledge4ir/salience/joint_center.py) script to conduct training and testing. Just simply specify one config file like the following:

```
python -m knowledge4ir.salience.joint_center conf_joint_kcrf_6+7_feature_masked_multi_kernel_type_0_event_label
```

Configs used for hashing can be found [here](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/config/hash/)

All of our config file can be found at this [link](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/config/), the best performing model is [this one](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/event_salience/config/multi_kernel/conf_joint_kcrf_6+7_feature_masked_multi_kernel_type_0_event_label).

Please remember to adapt the configs to your own system paths.


# Instructions of Running the pretrain model
Follow this section if you want to use the model for new texts.

Here is one way to run the pretrained model (i.e. Wikification using DBpedia, you can choose your own Wikification tool). DBpedia allows us to setup web services easily (https://github.com/dbpedia-spotlight/dbpedia-spotlight-model), so first let's set up the webservice following their instruction.

We can then create Wikification data.
You can obtain the freebase_map file [here](http://accra.sp.cs.cmu.edu/~zhengzhl/downloads/freebase_map.tsv)

Assuming that the input data is stored at ```$input_data```, which is a directory contains a list of plain text documents (must with ".txt" extensions). Use the following script in this project to create wikification.

```
en_spotlight_url=http://localhost:2222/en/rest/annotate
python -m event.salience.wikification $en_spotlight_url $input_data wiki freebase_map.tsv dbpedia
```

Now go back to cmu-script and then create featurized input data.
```
cd ../cmu-script
bin/run_pipeline.sh salience edu.cmu.cs.lti.pipeline.SalienceInputPipeline $input_data wiki salience txt /embeddings/joint_corpus.emb_128d
```

Go back to DDSemantics and then run salience. ```$sa_model_path``` should point to the model path you just downloaded.
```
cd ../DDSemantics
python -m knowledge4ir.salience.prepare.corpus_hashing $sa_model_path/hash_conf.py --CorpusHasher.corpus_in=salience/data.json --CorpusHasher.out_name=salience/hashed_data.json
python -m knowledge4ir.salience.joint_center $sa_model_path/test_only.py --Main.test_in=salience/hashed_data.json --Main.test_out=salience/output.json
```

# Overview of Preprocessing
It is possible to run all preprocessing on your own, but it is rather time consuming and complex, so we do not recommend digging into this, it is sufficient to reproduce the experiments with the released data. But here we provide a general overview on how to do this.

There are a couple of preprocessing tools used, most of them are assembled in the [CmuScript repository](https://github.com/hunterhector/cmu-script). You will find the prerequesite repositories in its README.

We have also used [TagMe!](https://github.com/gammaliu/tagme) to tag the named entities. It is possible to use other taggers, but the output will vary.

The overall process is quite complex and tedious, it is much easier to use the preprocessed data released above. Here I am only listing the general steps, hopefully the class are self-explantory:

1. Read the NYT corpus into the UIMA format using the following class:
    - [AnnotatedNytReader](https://github.com/hunterhector/uima-base-tools/blob/master/corpus-reader/src/main/java/edu/cmu/cs/lti/collection_reader/AnnotatedNytReader.java)
1. Parsing steps:
    1. Run parses and frame based event detector with [RunOnlyPipeline](https://github.com/hunterhector/cmu-script/blob/master/event-coref/src/main/java/edu/cmu/cs/lti/event_coref/pipeline/RunOnlyPipeline.java)
    1. Run tagging with TagMe to produce tagged results in JSON.
1. Read the parsed NYT data produced in the previous step, and add the TagMe result with:
    - [NytPreprocessPipeline](https://github.com/hunterhector/cmu-script/blob/master/salience/src/main/java/edu/cmu/cs/lti/pipeline/NytPreprocessPipeline.java)
1. Create the dataset with the following class:
    - [SalienceDataPreparer](https://github.com/hunterhector/cmu-script/blob/master/salience/src/main/java/edu/cmu/cs/lti/pipeline/SalienceDataPreparer.java)


