import { useState } from "react";
import { useNavigate } from "react-router-dom";

const cities = ["CAPITL", "CENTRL", "DUNWOD", "GENESE", "HUD VL", "LONGIL", "MHK VL", "MILLWD", "N.Y.C", "NORTH", "WEST"];

export default function PredictConsumption() {
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [selectedCity, setSelectedCity] = useState<string>("");
  const [lastMessage, setLastMessage] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const navigate = useNavigate();

  const handlePredict = (modelType: "new" | "standard") => {
    if (new Date(startDate) >= new Date(endDate)) {
      alert("Krajnji datum mora biti veći od početnog datuma.");
      return;
    }

    const startTimestamp = new Date(startDate).getTime();
    const endTimestamp = new Date(endDate).getTime();
    const dateDifference = Math.abs((endTimestamp - startTimestamp) / (1000 * 60 * 60 * 24));

    if (dateDifference > 7) {
      alert("Razlika između datuma ne sme biti veća od 7 dana.");
      return;
    }

    if (!selectedCity) {
      alert("Morate izabrati grad.");
      return;
    }

    setIsProcessing(true);

    const predictionData = {
      startDate: startDate || null,
      endDate: endDate || null,
      city: selectedCity || null,
      modelType: modelType,
    };

    fetch("http://localhost:5000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(predictionData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.data) {
          navigate("/results", {
            state: {
              data: JSON.parse(data.data),
              startDate,
              endDate,
              city: selectedCity,
              modelType,
            },
          });
        } else {
          setLastMessage(data.message);
        }
        console.log("Success:", data);
      })
      .catch((error) => {
        setLastMessage("Error predicting consumption");
        console.error("Error:", error);
      })
      .finally(() => {
        setIsProcessing(false);
      });
  };

  const isPredictButtonDisabled = !startDate || !endDate || new Date(startDate) >= new Date(endDate) || !selectedCity;

  return (
    <div className={`flex justify-center items-center min-h-screen p-6 bg-gray-900 text-white ${isProcessing ? "cursor-wait" : "cursor-auto"}`}>
      <div className="w-full max-w-4xl bg-gray-800 shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8">Predict Consumption</h1>

        {lastMessage && (
          <div className="mt-6 p-0 bg-gray-700 rounded-lg">
            <p className="text-center text-lg font-semibold"> {lastMessage}</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="block">
            <span className="font-medium">Start Date:</span>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              max={endDate || getTodayDate()}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">End Date:</span>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              min={startDate}
              max={startDate ? new Date(new Date(startDate).getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0] : getTodayDate()}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block col-span-2">
            <span className="font-medium">Select City:</span>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            >
              <option value="">Select a city</option>
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </label>

          <div className="flex justify-between gap-4 mt-6 col-span-2">
            <button
              onClick={() => handlePredict("new")}
              disabled={isPredictButtonDisabled || isProcessing}
              className={`w-full p-4 rounded-lg transition duration-300 ${isPredictButtonDisabled || isProcessing
                ? "bg-gray-500 cursor-not-allowed"
                : "bg-green-600 hover:bg-green-500"
                }`}
            >
              {isProcessing ? "Predicting..." : "Predict Using New Model"}
            </button>

            <button
              onClick={() => handlePredict("standard")}
              disabled={isPredictButtonDisabled || isProcessing}
              className={`w-full p-4 rounded-lg transition duration-300 ${isPredictButtonDisabled || isProcessing
                ? "bg-gray-500 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-500"
                }`}
            >
              {isProcessing ? "Predicting..." : "Predict Using Standard Model"}
            </button>
          </div>
        </div>

        {isProcessing && (
          <div className="flex justify-center mt-6">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-200"></div>
          </div>
        )}
      </div>
    </div>
  );
}