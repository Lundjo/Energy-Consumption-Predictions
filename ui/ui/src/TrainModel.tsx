import { useState } from "react";

export default function TrainModel() {
  const [layers, setLayers] = useState<number | undefined>(undefined);
  const [neuronsFirstLayer, setNeuronsFirstLayer] = useState<number | undefined>(undefined);
  const [neuronsOtherLayers, setNeuronsOtherLayers] = useState<number | undefined>(undefined);
  const [epochs, setEpochs] = useState<number | undefined>(undefined);
  const [costFunction, setCostFunction] = useState("mape");
  const [optimizer, setOptimizer] = useState("nadam");
  const [kernelInitializer, setKernelInitializer] = useState("he_normal");
  const [activationFunction, setActivationFunction] = useState("leaky_relu");
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const [selectedFolder, setSelectedFolder] = useState<FileList | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(e.target.files);
    }
  };

  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFolder(e.target.files);
    }
  };

  const handleUpload = () => {
    const formData = new FormData();

    if (selectedFiles) {
      Array.from(selectedFiles).forEach((file) => {
        formData.append("files", file);
      });
    }

    if (selectedFolder) {
      Array.from(selectedFolder).forEach((file) => {
        formData.append("folder", file);
      });
    }

    // Call backend API to upload files/folder
    fetch("/api/upload", {
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
    // Call backend API to start training with selected hyperparameters
  };

  return (
    <div className="flex justify-center items-center min-h-screen p-6 bg-gray-900 text-white">
      <div className="w-full max-w-4xl bg-gray-800 shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8">Train Your Model</h1>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Upload Data</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <label className="block">
              <span className="font-medium">Upload CSV Files:</span>
              <input
                type="file"
                accept=".csv"
                multiple
                onChange={handleFileChange}
                className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
              />
            </label>

            <label className="block">
              <span className="font-medium">Upload Folder:</span>
              <input
                type="file"
                {...({ webkitdirectory: "true" } as React.InputHTMLAttributes<HTMLInputElement>)}
                onChange={handleFolderChange}
                className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
              />
            </label>

            <button
              onClick={handleUpload}
              className="w-full bg-green-600 text-white p-4 rounded-lg transition duration-300 hover:bg-green-500 col-span-2"
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
            <span className="font-medium">Cost Function:</span>
            <select
              value={costFunction}
              onChange={(e) => setCostFunction(e.target.value)}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            >
              <option value="mape">MAPE</option>
              <option value="mse">MSE</option>
              <option value="mae">MAE</option>
            </select>
          </label>

          <label className="block">
            <span className="font-medium">Optimizer:</span>
            <select
              value={optimizer}
              onChange={(e) => setOptimizer(e.target.value)}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            >
              <option value="nadam">Nadam</option>
              <option value="adam">Adam</option>
              <option value="sgd">SGD</option>
            </select>
          </label>

          <label className="block">
            <span className="font-medium">Kernel Initializer:</span>
            <select
              value={kernelInitializer}
              onChange={(e) => setKernelInitializer(e.target.value)}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            >
              <option value="he_normal">He Normal</option>
              <option value="glorot_uniform">Glorot Uniform</option>
              <option value="random_normal">Random Normal</option>
            </select>
          </label>

          <label className="block">
            <span className="font-medium">Activation Function:</span>
            <select
              value={activationFunction}
              onChange={(e) => setActivationFunction(e.target.value)}
              className="w-full p-4 border border-gray-600 bg-gray-700 rounded-lg text-white"
            >
              <option value="leaky_relu">Leaky ReLU</option>
              <option value="relu">ReLU</option>
              <option value="sigmoid">Sigmoid</option>
            </select>
          </label>

          <button
            onClick={handleTrain}
            className="w-full mt-6 bg-blue-600 text-white p-4 rounded-lg transition duration-300 hover:bg-blue-500 col-span-2"
          >
            Start Training
          </button>
        </div>
      </div>
    </div>
  );
}