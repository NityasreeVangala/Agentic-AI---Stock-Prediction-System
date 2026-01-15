import React, { useEffect, useState } from "react";
import axios from "axios";

const FundamentalsDashboard = ({ symbol }) => {
  const [insight, setInsight] = useState({});
  const [top5, setTop5] = useState({ positives: [], risks: [] });

  useEffect(() => {
    if (!symbol) return;

    axios.get(`http://127.0.0.1:8000/fundamentals/insight/${symbol}`)
      .then(res => setInsight(res.data));

    axios.get(`http://127.0.0.1:8000/fundamentals/top5/${symbol}`)
      .then(res => setTop5(res.data));

  }, [symbol]);

  return (
    <div>
      <h3>Insights</h3>
      <ul>
        {Object.entries(insight).map(([k, v]) => (
          <li key={k}>{k}: {v}</li>
        ))}
      </ul>

      <h3>Positives</h3>
      <ul>{top5.positives.map((p,i)=> <li key={i}>{p}</li>)}</ul>

      <h3>Risks</h3>
      <ul>{top5.risks.map((r,i)=> <li key={i}>{r}</li>)}</ul>
    </div>
  );
};

export default FundamentalsDashboard;
