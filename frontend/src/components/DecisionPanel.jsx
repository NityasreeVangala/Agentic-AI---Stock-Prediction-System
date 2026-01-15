import React, { useEffect, useState } from "react";
import axios from "axios";

const DecisionPanel = ({ symbol }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    axios
      .get(`http://127.0.0.1:8000/decision/${symbol}`)
      .then((res) => setData(res.data))
      .catch((err) => console.error("Decision error:", err));
  }, [symbol]);

  if (!data) return <p>Loading decision...</p>;

  // ---------------- Safely extract arrays ----------------
  const insights = data.technical_insights || [];
  const fundamentalPositives =
    data.fundamental_top5?.positives || [];
  const fundamentalRisks =
    data.fundamental_top5?.risks || [];

  return (
    <div style={{ padding: 16, border: "1px solid #ddd", marginTop: 20 }}>
      <h2>
        Technical Decision:
        <span
          style={{
            marginLeft: 10,
            color:
              data.technical_decision === "BUY"
                ? "green"
                : data.technical_decision === "SELL"
                ? "red"
                : "orange",
          }}
        >
          {data.technical_decision}
        </span>
      </h2>

      <p>
        <strong>Technical Score:</strong> {data.technical_score}
      </p>

      <p>
        <strong>Technical Confidence:</strong>{" "}
        {data.technical_score}%
      </p>

      <h3>Technical Insights:</h3>
      <ul>
        {insights.map((insight, i) => (
          <li key={i}>{insight}</li>
        ))}
      </ul>

      <h3>Fundamental Positives:</h3>
      <ul>
        {fundamentalPositives.map((p, i) => (
          <li key={i}>{p}</li>
        ))}
      </ul>

      <h3>Fundamental Risks:</h3>
      <ul>
        {fundamentalRisks.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  );
};

export default DecisionPanel;
