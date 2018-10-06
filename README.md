# Preprocessing with FA*IR

1. [Dependencies](#dependencies)
2. [Quick start](#quick-start)
3. [Project structure](#project-structure)
4. [How to use](#how-to-use)

## Dependencies


| Dependencies        |  |
| -------------| -------|
| python 3.6.3 including:      | birkhoff 0.0.5|
|       | chainer 1.16.0     |
|       | CVXOPT 1.2.0     |
|       | matplotlib 2.1.0     |
|       | numba 0.38.0   |
|       | numpy 1.13.3   |
|       | pandas 0.20.3   |
|       | pip 9.0.1     |
|       | scipy 0.19.1     |
| Java JDK 8 or OpenJDK 8| used version for this implementation openjdk version "1.8.0_181" |
|RankLib-2.10.jar| Download here: https://sourceforge.net/projects/lemur/files/lemur/ |

## Quick start
1. Clone the repository :
` git clone https://github.com/MilkaLichtblau/BA_Gina.git`

2. Move to project directory:
`cd /BA_Gina`

3. Move RankLib jar in project folder:  `BA_Gina/src/`

4. To run the full routine: `./run.sh`
> The execution time of the full routines may take up numerous hours up to a day

5. After the execution of the run script all experiment results can be found in: `experiments/experiments_YYYYMMDD_hhmm/`

#### Execution cycle of full routine

![Image of the routines execution order](https://github.com/MilkaLichtblau/BA_Gina/routine_flow.png)

## Project Structure

The projects structure looks like this:
```bash
├── run.sh (Full routine script)
|
├── data
│   ├── features.csv (Raw data)
│   └── formatted_data (includes all formatted training and test data)
│       
├── experiments (All experiments results are stored here)
│   └── median.py (Mini script to average cross fold validation models for ListNet)
|
└── src (implementation)
    ├── fair (adjusted implementation of Meike Zehlike´s code, original can be found here: https://github.com/MilkaLichtblau/FA-IR_Ranking)
    ├── measures (adjusted implementation of Laura Mons code, original can be found here: https://github.com/MilkaLichtblau/BA_Laura)  
    |
    ├── main.py ( Start point for ranking, re-ranking and formatting the data, merge the predictions, plot the predictions and take fairness measures. For all options use: python src/main.py -h)
    ├── fairnessMeasures.py
    ├── format.py
    ├── globals.py
    ├── merge.py
    ├── plot.py
    ├── RankLib-2.10.jar (Must be included manually)
    ├── rank.py
    └── rerank_with_fair.py
```
## How to use

When you don´t want to use the full routine. You can execute all steps described in the routine figure. For most parameters a default is set. For all options have a look at the help options of the main script with: `python src/main.py -h`

Examples for all distinct steps are listed below:
For all example first switch into src folder:
```
cd src
```

### Ranking the raw dataset

```
python main.py -rank -f "../data/features.csv" -d "../data/formatted_data/" -fa "_TRAIN" -rs 1 -re 50 -rl 10
```

### Re-ranking the dataset

```
python main.py -rerank -f "../data/features.csv" -d "../data/formatted_data/" -fa "_TRAIN" -rs 1 -re 50 -rl 10
```

### Merge predictions

```
python main.py -merge -f "../data/formatted_data/features_TEST.csv" -pf "../experiments/experiments_20181006_1324/ListNet/data/predictions.txt"
```
### Measure predictions

```
python main.py -plot -f "../experiments/experiments_20181006_1324/ListNet/data/predictions_MERGED.csv" -r "ListNet"
```

### Plot predictions

```
python main.py -measure -f "../experiments/experiments_20181006_1324/ListNet/data/predictions_MERGED.csv" -r "ListNet" -k 1000 -d "../experiments/experiments_20181006_1324/ListNet"
```
