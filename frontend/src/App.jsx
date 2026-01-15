import React, { useState } from "react";

// ---------------- Components ----------------
import SearchBox from "./components/SearchBox";
import CandlestickChart from "./components/CandlestickChart";
import TechnicalDashboard from "./components/TechnicalDashboard";
import FundamentalsDashboard from "./components/FundamentalsDashboard";
import ForecastDashboard from "./components/ForecastDashboard";
import DecisionPanel from "./components/DecisionPanel"; 
import ExplanationPanel from "./components/ExplanationPanel";

// Technical + Fundamental + Confidence
// import ExplanationPanel from "./components/ExplanationPanel"; // Optional: beginner-friendly explanations

function App() {
  const [stock, setStock] = useState(null);

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ fontSize: 28, fontWeight: "bold", marginBottom: 20 }}>
        Agentic Stock AI
      </h1>

      {/* ---------------- Search Box ---------------- */}
      <SearchBox onSelectStock={setStock} />

      {/* ---------------- Display Dashboards ---------------- */}
      {stock && (
        <>
          <h2 style={{ marginTop: 20, marginBottom: 10 }}>{stock}</h2>

          {/* Historical Price Chart */}
          <CandlestickChart symbol={stock} />

          {/* Technical Indicators: RSI, MACD, MAs, Bollinger Bands, Volume */}
          <TechnicalDashboard symbol={stock} />

          {/* Fundamental Metrics: PE, EPS, ROE, Debt */}
          <FundamentalsDashboard symbol={stock} />

          {/* Forecasting: XGB, LSTM, Ensemble */}
          <ForecastDashboard symbol={stock} />

          {/* ---------------- Decision Agent ---------------- */}
          <DecisionPanel symbol={stock} />

          {/* ---------------- Optional Explanation Panel ---------------- */}
          {/* <ExplanationPanel symbol={stock} /> */}
          {/* 🧠 Explanation Agent */}
          <ExplanationPanel symbol={stock} />

        </>
      )}
    </div>
  );
}

export default App;
