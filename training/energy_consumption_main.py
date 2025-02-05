import time
from training.ann_regression import AnnRegression
from training.custom_preparer import CustomPreparer
from training.scorer import Scorer
import preprocessing.preprocessing

NUMBER_OF_COLUMNS = 11
SHARE_FOR_TRAINING = 0.85

def mainTraining(layers, neurons_first_layer, neurons_other_layers, epochs):
    # load the dataset
    dataframe = preprocessing.preprocessing.dataPreprocesing()

    # prepare data
    preparer = CustomPreparer(dataframe, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING);
    trainX, trainY, testX, testY = preparer.prepare_for_training()

    # make predictions
    ann_regression = AnnRegression(epochs, layers, neurons_first_layer, neurons_other_layers)
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

    ann_regression.model.save('D:/model.keras')