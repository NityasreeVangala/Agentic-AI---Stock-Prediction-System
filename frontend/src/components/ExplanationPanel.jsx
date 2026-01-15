import React, { useEffect, useState } from "react";
import axios from "axios";

const ExplanationPanel = ({ symbol }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!symbol) return;

    setLoading(true);

    axios
      .get(`http://127.0.0.1:8000/explain/${symbol}`)
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Explanation error:", err);
        setLoading(false);
      });
  }, [symbol]);

  if (loading) return <p>Loading explanation...</p>;
  if (!data) return <p>No explanation data available</p>;

  const { technical, fundamental, explanation } = data;

  return (
    <div style={{ padding: 16, border: "1px solid #ddd", marginTop: 20 }}>
      <h2>Stock Explanation</h2>

      {/* ================= TECHNICAL ================= */}
      <h3>📈 Technical Indicators</h3>
      {technical ? (
        <table border="1" cellPadding="6" style={{ borderCollapse: "collapse" }}>
          <tbody>
            {Object.entries(technical).map(([key, value]) => (
              <tr key={key}>
                <td><strong>{key}</strong></td>
                <td>{value !== null ? value : "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No technical data</p>
      )}

      {/* ================= FUNDAMENTAL ================= */}
      <h3 style={{ marginTop: 20 }}>📊 Fundamental Metrics</h3>
      {fundamental ? (
        <table border="1" cellPadding="6" style={{ borderCollapse: "collapse" }}>
          <tbody>
            {Object.entries(fundamental).map(([key, value]) => (
              <tr key={key}>
                <td><strong>{key}</strong></td>
                <td>{value !== null ? value : "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No fundamental data</p>
      )}

      {/* ================= EXPLANATION ================= */}
      <h3 style={{ marginTop: 20 }}>🧠 Explanation (Scratch LLM)</h3>
      {Array.isArray(explanation) && explanation.length > 0 ? (
        <ul>
          {explanation.map((line, index) => (
            <li key={index}>{line}</li>
          ))}
        </ul>
      ) : (
        <p>No explanation available</p>
      )}
    </div>
  );
};

export default ExplanationPanel;
