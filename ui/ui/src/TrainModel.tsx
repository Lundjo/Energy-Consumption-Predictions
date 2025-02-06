import { useState } from "react";

export default function TrainModel() {
  const [layers, setLayers] = useState<number | undefined>(undefined);
  const [neuronsFirstLayer, setNeuronsFirstLayer] = useState<number | undefined>(undefined);
  const [neuronsOtherLayers, setNeuronsOtherLayers] = useState<number | undefined>(undefined);
  const [epochs, setEpochs] = useState<number | undefined>(undefined);
  const [selectedFolder, setSelectedFolder] = useState<FileList | null>(null);
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  // Funkcija za dobijanje današnjeg datuma u formatu YYYY-MM-DD
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

  const CHUNK_SIZE = 500; // Broj fajlova po chunku

  const uploadInChunks = async () => {
    if (!selectedFolder) return;

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
        console.log("Chunk upload response:", data);
      } catch (error) {
        console.error("Error uploading chunk:", error);
        return;
      }
    }

    console.log("All chunks uploaded successfully.");
  };


  const handleUpload = () => {
    const formData = new FormData();

    if (selectedFolder) {
      Array.from(selectedFolder).forEach((file) => {
        formData.append("folder", file);
      });
    }

    // Call backend API to upload files/folder
    fetch("http://localhost:5000/api/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleTrain = () => {
    if (new Date(startDate) >= new Date(endDate)) {
      alert("Krajnji datum mora biti veći od početnog datuma.");
      return;
    }

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
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  // Provera da li su oba datuma izabrana i da li je krajnji datum veći od početnog
  const isTrainButtonDisabled = !startDate || !endDate || new Date(startDate) >= new Date(endDate);

  return (
    <div className="flex justify-center items-center min-h-screen p-6 bg-gray-900 text-white">
      <div className="w-full max-w-4xl bg-gray-800 shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8">Train Your Model</h1>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Upload Data</h2>
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
              className="bg-green-600 text-white p-4 rounded-lg transition duration-300 hover:bg-green-500 w-72 mt-5"
            >
              Upload Data
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
              max={getTodayDate()} // Onemogućava buduće datume
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <label className="block">
            <span className="font-medium">End Date:</span>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              max={getTodayDate()} // Onemogućava buduće datume
              min={startDate} // Krajnji datum ne može biti pre početnog
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            />
          </label>

          <button
            onClick={handleTrain}
            disabled={isTrainButtonDisabled}
            className={`w-full mt-6 p-4 rounded-lg transition duration-300 col-span-2 ${isTrainButtonDisabled
                ? "bg-gray-500 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-500"
              }`}
          >
            Start Training
          </button>
        </div>
      </div>
    </div>
  );
}