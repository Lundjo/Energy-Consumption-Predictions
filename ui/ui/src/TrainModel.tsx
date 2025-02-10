import { useState } from "react";

export default function TrainModel() {
  const [layers, setLayers] = useState<number | undefined>(undefined);
  const [neuronsFirstLayer, setNeuronsFirstLayer] = useState<number | undefined>(undefined);
  const [neuronsOtherLayers, setNeuronsOtherLayers] = useState<number | undefined>(undefined);
  const [epochs, setEpochs] = useState<number | undefined>(undefined);
  const [selectedFolder, setSelectedFolder] = useState<FileList | null>(null);
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [lastMessage, setLastMessage] = useState<string>(""); // Stanje za poslednju poruku
  const [isProcessing, setIsProcessing] = useState<boolean>(false); // Stanje za indikaciju obrade

  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFolder(e.target.files);
    }
  };

  const CHUNK_SIZE = 500;

  const uploadInChunks = async () => {
    if (!selectedFolder) return;

    setIsProcessing(true); // Postavite stanje obrade na true
    var success = false;

    const filesArray = Array.from(selectedFolder);
    for (let i = 0; i < filesArray.length; i += CHUNK_SIZE) {
      const chunk = filesArray.slice(i, i + CHUNK_SIZE);
      const formData = new FormData();

      chunk.forEach((file) => {
        formData.append("folder", file);
      });

      try {
        const response = await fetch("http://localhost:5000/api/upload", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        setLastMessage(data.message); // Postavite poslednju poruku
        console.log("Chunk upload response:", data);
        if(response.ok)
          success = true;
      } catch (error) {
        console.error("Error uploading chunk:", error);
        setLastMessage("Error uploading chunk"); // Postavite poruku o grešci
        setIsProcessing(false); // Postavite stanje obrade na false u slučaju greške
        return;
      }
    }

    if(success){
      setLastMessage("All chunks uploaded successfully."); // Postavite poruku o uspehu
      console.log("All chunks uploaded successfully.");
    }
    
    setIsProcessing(false); // Postavite stanje obrade na false nakon završetka
  };

  const handleTrain = () => {
    if (new Date(startDate) >= new Date(endDate)) {
      alert("Krajnji datum mora biti veći od početnog datuma.");
      return;
    }

    setIsProcessing(true); // Postavite stanje obrade na true

    const hyperparameters = {
      layers: layers || null,
      neuronsFirstLayer: neuronsFirstLayer || null,
      neuronsOtherLayers: neuronsOtherLayers || null,
      epochs: epochs || null,
      startDate: startDate || null,
      endDate: endDate || null,
    };

    fetch("http://localhost:5000/api/train", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(hyperparameters),
    })
      .then((response) => response.json())
      .then((data) => {
        setLastMessage(data.message); // Postavite poslednju poruku
        console.log("Success:", data);
      })
      .catch((error) => {
        setLastMessage("Error training model"); // Postavite poruku o grešci
        console.error("Error:", error);
      })
      .finally(() => {
        setIsProcessing(false); // Postavite stanje obrade na false nakon završetka
      });
  };

  const isTrainButtonDisabled = !startDate || !endDate || new Date(startDate) >= new Date(endDate);
  const isUploadButtonDisabled = !selectedFolder || isProcessing; // Onemogući dugme ako nije izabran folder ili ako je u toku obrada

  return (
    <div className={`flex justify-center items-center min-h-screen p-6 bg-gray-900 text-white ${isProcessing ? "cursor-wait" : "cursor-auto"}`}>
      <div className="w-full max-w-4xl bg-gray-800 shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8">Train Your Model</h1>

        {/* Prikaz poslednje poruke */}
        {lastMessage && (
          <div className="mt-6 p-0 bg-gray-700 rounded-lg">
            <p className="text-center text-lg font-semibold"> {lastMessage}</p>
          </div>
        )}

        <div className="mb-6 mt-6">
          <div className="flex items-center gap-4">
            <label className="flex-1">
              <span className="font-medium">Upload Folder:</span>
              <input
                type="file"
                {...({ webkitdirectory: "true" } as React.InputHTMLAttributes<HTMLInputElement>)}
                onChange={handleFolderChange}
                className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
              />
            </label>

            <button
              onClick={uploadInChunks}
              disabled={isUploadButtonDisabled} // Onemogući dugme ako nije izabran folder
              className={`bg-green-600 text-white p-4 rounded-lg transition duration-300 hover:bg-green-500 w-72 mt-5 ${isUploadButtonDisabled ? "cursor-not-allowed opacity-50" : "cursor-pointer"}`}
            >
              {isProcessing ? "Uploading..." : "Upload Data"}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="block">
            <span className="font-medium">Number of Layers:</span>
            <input
              type="number"
              value={layers}
              onChange={(e) => setLayers(e.target.value ? Number(e.target.value) : undefined)}
              min={0}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">Neurons in First Layer:</span>
            <input
              type="number"
              value={neuronsFirstLayer}
              onChange={(e) => setNeuronsFirstLayer(e.target.value ? Number(e.target.value) : undefined)}
              min={0}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">Neurons in Other Layers:</span>
            <input
              type="number"
              value={neuronsOtherLayers}
              onChange={(e) => setNeuronsOtherLayers(e.target.value ? Number(e.target.value) : undefined)}
              min={0}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">Epochs:</span>
            <input
              type="number"
              value={epochs}
              onChange={(e) => setEpochs(e.target.value ? Number(e.target.value) : undefined)}
              min={0}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">Start Date:</span>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              max={getTodayDate()}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">End Date:</span>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              max={getTodayDate()}
              min={startDate}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <button
            onClick={handleTrain}
            disabled={isTrainButtonDisabled || isProcessing}
            className={`w-full mt-6 p-4 rounded-lg transition duration-300 col-span-2 ${isTrainButtonDisabled || isProcessing
                ? "bg-gray-500 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-500"
              }`}
          >
            {isProcessing ? "Training..." : "Start Training"}
          </button>
        </div>

        {/* Dodajte spinner ili drugi vizuelni indikator */}
        {isProcessing && (
          <div className="flex justify-center mt-6">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-200"></div>
          </div>
        )}
      </div>
    </div>
  );
}