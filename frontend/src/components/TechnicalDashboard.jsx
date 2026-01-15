import { useEffect, useState } from "react";
import axios from "axios";

const TechnicalDashboard = ({ symbol }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/technical/${symbol}`)
      .then(res => setData(res.data));
  }, [symbol]);

  if (!data) return <p>Loading technicals...</p>;

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Technical Analysis</h3>
      <p><strong>Score:</strong> {data.score}/100</p>
      <p><strong>Decision:</strong> {data.decision}</p>

      <ul>
        {data.insights.map((i, idx) => (
          <li key={idx}>{i}</li>
        ))}
      </ul>
    </div>
  );
};

export default TechnicalDashboard;
