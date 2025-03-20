import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TrainModel from "./TrainModel";
import PredictConsumption from "./PredictConsumption";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TrainModel />} />
        <Route path="/predict" element={<PredictConsumption />} />
      </Routes>
    </Router>
  );
}

export default App;

