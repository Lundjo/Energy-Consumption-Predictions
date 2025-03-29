import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TrainModel from "./TrainModel";
import PredictConsumption from "./PredictConsumption";
import PredictionResults from "./PredictionResults";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TrainModel />} />
        <Route path="/predict" element={<PredictConsumption />} />
        <Route path="/results" element={<PredictionResults />} />
      </Routes>
    </Router>
  );
}

export default App;