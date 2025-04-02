import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface PredictionData {
  datetime: string;
  name: string;
  predicted_load: number;
  actual_load?: number;
  absolute_percentage_error?: number;
}

export default function PredictionResults() {
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState<PredictionData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (location.state?.data) {
      setData(location.state.data);
      setIsLoading(false);
    } else {
      const savedData = localStorage.getItem("lastPrediction");
      if (savedData) {
        setData(JSON.parse(savedData));
      }
      setIsLoading(false);
    }
  }, [location.state]);

  // Calculate mean absolute percentage error if available
  const mape = data[0]?.absolute_percentage_error
    ? data.reduce((sum, item) => sum + (item.absolute_percentage_error || 0), 0) / data.length
    : null;

  const chartData = {
    labels: data.map((item) => new Date(item.datetime).toLocaleString()),
    datasets: [
      {
        label: "Predicted Load",
        data: data.map((item) => item.predicted_load),
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.5)",
        tension: 0.1,
      },
      ...(data[0]?.actual_load
        ? [
          {
            label: "Actual Load",
            data: data.map((item) => item.actual_load),
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            tension: 0.1,
          },
        ]
        : []),
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Load Prediction",
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Date/Time",
        },
      },
      y: {
        title: {
          display: true,
          text: "Load",
        },
      },
    },
  };

  const handleRetest = () => {
    navigate("/predict", {
      state: {
        startDate: location.state?.startDate,
        endDate: location.state?.endDate,
        city: location.state?.city,
      },
    });
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data.length) {
    return <div>No prediction data available</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Prediction Results for {data[0].name}
        </h1>

        <div className="flex flex-col lg:flex-row gap-6 mb-6">
          {/* Grafik - smanjujemo flex-1 na flex-[2] da bi greška zauzela više prostora */}
          <div className="bg-gray-800 rounded-lg p-6 flex-[2]">
            <h2 className="text-xl font-semibold mb-4">Chart</h2>
            <div className="h-96">
              <Line data={chartData} options={options} />
            </div>
          </div>

          {/* Novo: Poseban container za grešku sa većim dimenzijama */}
          {mape !== null && (
            <div className="bg-gray-800 rounded-lg p-6 flex-1 flex flex-col justify-center">
              <div className="text-center space-y-4">
                <h3 className="text-2xl font-semibold">Model Accuracy</h3>
                <div className="space-y-2">
                  <p className="text-sm text-gray-300">Mean Absolute Percentage Error</p>
                  <p className="text-5xl font-bold text-red-400">
                    {mape.toFixed(2)}%
                  </p>
                </div>
                <div className="pt-4">
                  <p className="text-xs text-gray-400">
                    Lower values indicate better accuracy
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Data Table</h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-700">
                  <th className="p-3 text-left">Date/Time</th>
                  <th className="p-3 text-left">Predicted Load</th>
                  {data[0]?.actual_load && (
                    <th className="p-3 text-left">Actual Load</th>
                  )}
                  {data[0]?.absolute_percentage_error && (
                    <th className="p-3 text-left">Error %</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr
                    key={index}
                    className={index % 2 === 0 ? "bg-gray-750" : "bg-gray-700"}
                  >
                    <td className="p-3">
                      {new Date(item.datetime).toLocaleString()}
                    </td>
                    <td className="p-3">{item.predicted_load.toFixed(2)}</td>
                    {item.actual_load && (
                      <td className="p-3">{item.actual_load.toFixed(2)}</td>
                    )}
                    {item.absolute_percentage_error && (
                      <td className="p-3">{item.absolute_percentage_error.toFixed(2)}%</td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="flex justify-between gap-4">
          <button
            onClick={() => navigate("/")}
            className="bg-gray-600 hover:bg-gray-500 px-6 py-3 rounded-lg transition"
          >
            Back to Home
          </button>
          <div className="flex gap-4">
            <button
              onClick={() => handleRetest()}
              className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-lg transition"
            >
              Retest
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}