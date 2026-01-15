const IndicatorCard = ({ title, value }) => (
  <div className="bg-white shadow rounded p-4 w-40 text-center">
    <h4 className="text-gray-500">{title}</h4>
    <p className="text-xl font-bold">{value}</p>
  </div>
);

export default IndicatorCard;
