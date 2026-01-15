import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  ResponsiveContainer,
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
  Line,
} from "recharts";

const CandlestickChart = ({ symbol }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (!symbol) return;

    const fetchHistory = async () => {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/history/${symbol}?limit=120`
        );

        const formatted = res.data.history.map((d) => ({
          date: d.Date,
          open: d.Open,
          close: d.Close,
          high: d.High,
          low: d.Low,
          body: Math.abs(d.Close - d.Open),
          direction: d.Close >= d.Open ? 1 : -1,
        }));

        setData(formatted);
      } catch (err) {
        console.error("Chart error:", err);
      }
    };

    fetchHistory();
  }, [symbol]);

  if (!data.length) return <p>Loading chart...</p>;

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data}>
        <XAxis dataKey="date" hide />
        <YAxis domain={["dataMin", "dataMax"]} />
        <Tooltip />

        {/* Candle body */}
        <Bar
          dataKey="body"
          barSize={4}
          fill="#8884d8"
          isAnimationActive={false}
        />

        {/* High-Low wick */}
        <Line
          type="monotone"
          dataKey="high"
          stroke="#000"
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="low"
          stroke="#000"
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default CandlestickChart;
