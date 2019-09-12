#################################################
#												#
# Properties for complete routine				#
#												#
#################################################

metric="NDCG@50"		#"ERR@50"		#"MAP"
relevanceLabel=10
#################################################
#												#
# Functions for complete routine				#
#												#
#################################################

function createDirs {
	mkdir $1
	mkdir $1/data
	mkdir $1/models
	mkdir $1/statistics
}

function runRanker {
	# first argument ranker name, second argument ranker number, third metric used (the metric only has effect on AdaRank, Coordinate Ascent and LambdaMART))

	echo "########################################"
	echo " "
	echo "Start rertrieving the rankers models"
	echo " "
	echo "########################################"
	
	if [ $2 -eq 7 ] 
	then
		java -jar RankLib-2.10.jar -train ../data/formatted_data/features_TRAIN.csv -ranker $2 -kcv 5 -kcvmd ../$dir/$1/models/ -kcvmn model -metric2t $3 -metric2T $3 -gmax $max -norm zscore
		java -jar RankLib-2.10.jar -train ../data/formatted_data/features_RERANKED_TRAIN.csv -ranker $2 -kcv 5 -kcvmd ../$dir/$1/models/ -kcvmn model_RERANKED -metric2t $3 -metric2T $3 -gmax $max -norm zscore

		python3 ../experiments/median.py ../$dir/$1/models/ model model.txt
		python3 ../experiments/median.py ../$dir/$1/models/ model_RERANKED model_RERANKED.txt

	else

		java -jar RankLib-2.10.jar -train ../data/formatted_data/features_TRAIN.csv -ranker $2 -save ../$dir/$1/models/model.txt -metric2t $3 -gmax $max -norm zscore
		java -jar RankLib-2.10.jar -train ../data/formatted_data/features_RERANKED_TRAIN.csv -ranker $2 -save ../$dir/$1/models/model_RERANKED.txt -metric2t $3 -gmax $max -norm zscore

	fi
	
	testdata="features_TEST.csv"

	echo "########################################"
	echo " "
	echo "Rank the test data for $testdata"
	echo " "
	echo "########################################"

	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model.txt -rank ../data/formatted_data/$testdata -indri ../$dir/$1/data/predictions.txt -gmax $max -norm zscore
	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model_RERANKED.txt -rank ../data/formatted_data/$testdata -indri ../$dir/$1/data/predictions_RERANKED.txt -gmax $max -norm zscore

	echo "########################################"
	echo " "
	echo "Statistics for $testdata"
	echo " "
	echo "########################################"

	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model.txt -test ../data/formatted_data/$testdata -metric2T NDCG@50 -idv ../$dir/$1/statistics/ndcg.txt -gmax $max -norm zscore
	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model_RERANKED.txt -test ../data/formatted_data/$testdata -metric2T NDCG@50 -idv ../$dir/$1/statistics/ndcg_RERANKED.txt -gmax $max -norm zscore

	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model.txt -test ../data/formatted_data/$testdata -metric2T MAP -idv ../$dir/$1/statistics/map.txt -gmax $max -norm zscore
	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model_RERANKED.txt -test ../data/formatted_data/$testdata -metric2T MAP -idv ../$dir/$1/statistics/map_RERANKED.txt -gmax $max -norm zscore

	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model.txt -test ../data/formatted_data/$testdata -metric2T ERR@50 -idv ../$dir/$1/statistics/err.txt -gmax $max -norm zscore
	java -jar RankLib-2.10.jar -load ../$dir/$1/models/model_RERANKED.txt -test ../data/formatted_data/$testdata -metric2T ERR@50 -idv ../$dir/$1/statistics/err_RERANKED.txt -gmax $max -norm zscore

	echo "########################################"
	echo " "
	echo "Merge, plot and measure the predictions for $testdata"
	echo " "
	echo "########################################"

	python3 main.py -merge -f "../data/formatted_data/$testdata" -pf "../$dir/$1/data/predictions.txt"
	python3 main.py -merge -f "../data/formatted_data/$testdata" -pf "../$dir/$1/data/predictions_RERANKED.txt"

	python3 main.py -plot -f "../$dir/$1/data/predictions_MERGED.csv" -r "$1" 
	python3 main.py -plot -f "../$dir/$1/data/predictions_RERANKED_MERGED.csv" -r "$1" -rr  

	python3 main.py -measure -f "../$dir/$1/data/predictions_MERGED.csv" -r "$1" -k 1000 -d "../$dir/$1/statistics/" 
	python3 main.py -measure -f "../$dir/$1/data/predictions_RERANKED_MERGED.csv" -r "$1" -k 1000 -d "../$dir/$1/statistics/" -rr 

}

function startExperiment {
	if [ ! -d "../$1/$2" ]; then
		createDirs "../$1/$2"
	fi
	runRanker $2 $3 $4
}


#################################################
#												#
# Start of the complete routine					#
#												#
#################################################
max="$(($relevanceLabel-1))"

cd src/

# initially rank and rerank testdata
python3 main.py -rank -rerank -f "../data/features.csv" -d "../data/formatted_data/" -fa "_TRAIN" -rs 1 -re 50 -rl $relevanceLabel
python3 main.py -rank -rerank -f "../data/features.csv" -d "../data/formatted_data/" -fa "_TEST" -rs 51 -re 60 -rl $relevanceLabel

# create new experiments dir
dir="experiments/experiments_$(date +%Y%m%d_%H%M)"
if [ ! -d "../$dir" ]; then
	echo "New experiments dir created."
 	mkdir ../$dir
fi

# create info file
file="../$dir/info.txt"
if [ -e $file ]; then
  echo "File $file already exists!"
else
  echo "Experiments properties " > $file
  echo "Executed $(date +%d%m%Y) " >> $file
  echo "Relevance labels range: $relevanceLabel" >> $file
  echo "Metric: $metric" >> $file
fi

# start experiments
ranker="MART"
startExperiment $dir $ranker 0 $metric

ranker="ListNet"
startExperiment $dir $ranker 7 $metric

ranker="RankBoost"
startExperiment $dir $ranker 2 $metric

ranker="AdaRank"
startExperiment $dir $ranker 3 $metric

ranker="CoordinateAscent"
startExperiment $dir $ranker 4 $metric

ranker="LambdaMART"
startExperiment $dir $ranker 6 $metric

ranker="RandomForests"
startExperiment $dir $ranker 8 $metric

ranker="RankNet"
startExperiment $dir $ranker 1 $metric

cd ..