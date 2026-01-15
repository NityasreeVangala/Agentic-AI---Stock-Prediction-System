import React, { useState, useEffect } from "react";
import axios from "axios";

// Debounce helper function
function debounce(func, delay) {
  let timeout;
  return function (...args) {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

const SearchBox = ({ onSelectStock }) => {
  const [query, setQuery] = useState("");          // what user types
  const [results, setResults] = useState([]);      // API results
  const [loading, setLoading] = useState(false);   // loading state

  // Function to call backend API
  const fetchResults = async (q) => {
    if (!q) {
      setResults([]);
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(`http://127.0.0.1:8000/search?q=${q}`);
      setResults(res.data.results);  // array of stocks
    } catch (err) {
      console.error("API error:", err);
    }
    setLoading(false);
  };

  // Debounced version of fetchResults (300ms delay)
  const debouncedFetch = debounce(fetchResults, 300);

  // Call debounced function whenever query changes
  useEffect(() => {
    debouncedFetch(query);
  }, [query]);

  return (
    <div className="relative w-80">
      <input
        type="text"
        className="w-full border p-2 rounded"
        placeholder="Search stock..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {loading && <div className="absolute right-2 top-2 text-gray-500">Loading...</div>}

      {results.length > 0 && (
        <ul className="absolute w-full border mt-1 bg-white shadow rounded z-10 max-h-40 overflow-y-auto">
          {results.map((stock) => (
            <li
              key={stock}
              className="p-2 hover:bg-gray-200 cursor-pointer"
              onClick={() => {
                onSelectStock(stock); // notify parent component
                setQuery(stock);       // fill input with selected stock
                setResults([]);        // hide dropdown
              }}
            >
              {stock}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBox;
