import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const ForecastDashboard = ({ symbol }) => {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    setLoading(true);
    setError(null);

    const fetchForecast = async () => {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/forecast/12months/${symbol}`
        );

        const cleaned = res.data.forecast.map((row) => ({
          Month: row.Month,
          XGB: Number(row.XGB),
          LSTM: Number(row.LSTM),
          Ensemble: Number(row.Ensemble),
        }));

        setForecast(cleaned);
      } catch (err) {
        console.error("Forecast fetch error:", err);
        setError("Forecast not available for this stock");
        setForecast([]);
      } finally {
        setLoading(false);
      }
    };

    fetchForecast();
  }, [symbol]);

  if (loading) return <p>Loading 12-month forecast...</p>;
  if (error) return <p>{error}</p>;
  if (forecast.length === 0) return <p>No forecast available.</p>;

  return (
    <div style={{ marginTop: 30 }}>
      <h2>12-Month Forecast ({symbol})</h2>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={forecast}>
          <XAxis dataKey="Month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="XGB" />
          <Line type="monotone" dataKey="LSTM" />
          <Line
            type="monotone"
            dataKey="Ensemble"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Table */}
      <table
        style={{
          marginTop: 20,
          width: "100%",
          borderCollapse: "collapse",
          textAlign: "center",
        }}
      >
        <thead>
          <tr style={{ background: "#f0f0f0" }}>
            <th>Month</th>
            <th>XGB</th>
            <th>LSTM</th>
            <th>Ensemble</th>
          </tr>
        </thead>
        <tbody>
          {forecast.map((row, i) => (
            <tr key={i}>
              <td>{row.Month}</td>
              <td>{row.XGB.toFixed(2)}</td>
              <td>{row.LSTM.toFixed(2)}</td>
              <td>{row.Ensemble.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ForecastDashboard;
