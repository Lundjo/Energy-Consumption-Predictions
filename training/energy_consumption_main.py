import time
import pandas
from ann_regression import AnnRegression
from custom_plotting import CustomPloting
from custom_preparer import CustomPreparer
from scorer import Scorer

NUMBER_OF_COLUMNS = 11
SHARE_FOR_TRAINING = 0.85

# load the dataset
dataframe = pandas.read_csv('D:/Energy-Consumption-Predictions/new_output.csv', engine='python', sep=',')

# prepare data
preparer = CustomPreparer(dataframe, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING);
trainX, trainY, testX, testY = preparer.prepare_for_training()

# make predictions
ann_regression = AnnRegression()
time_begin = time.time();
trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
time_end = time.time()
print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

# invert predictions
trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

# calculate root mean squared error
scorer = Scorer()
trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
print('Train Score: %.2f MAPE' % (trainScore))
print('Test Score: %.2f MAPE' % (testScore))

ann_regression.model.save('C:/model.keras')