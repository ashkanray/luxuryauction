import "../styles/Items.css";
import { useNavigate } from "react-router-dom";
function Items({ items, error }) {
  const navigate = useNavigate();
  const handleSearchSubmit = async () => {
    try {
      const endpoint = `http://localhost:3500/api/item/search?query=${searchQuery}`;
      const response = await makeApiRequest("GET", endpoint);

      if (response.success) {
        setItems(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    }
  };
  return (
    <div className="items-container">
      {error && <p>Error: {error}</p>}
      {items.map((item, index) => (
        <div
          key={index}
          className="item"
          onClick={() => {
            navigate(`/user/bid/${item.id}`);
          }}
        >
          <p>Name: {item.item_name}</p>
          <p>Watch Model: {item.watch_model}</p>
        </div>
      ))}
    </div>
  );
}

export default Items;
