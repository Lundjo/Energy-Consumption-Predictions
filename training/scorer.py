import numpy as np

class Scorer:
    def get_score(self, trainY, trainPredict, testY, testPredict):
        # Izračunavanje MAPE za trening set
        mape_train = np.mean(np.abs((trainY - trainPredict) / trainY)) * 100

        # Izračunavanje MAPE za test set
        mape_test = np.mean(np.abs((testY - testPredict) / testY)) * 100

        return mape_train, mape_test