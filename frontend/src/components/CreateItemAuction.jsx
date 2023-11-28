import React, { useState, useEffect } from "react";
import "../styles/createItemAuction.css";
import { useNavigate } from "react-router-dom";

function CreateItemAuction() {
  // navigator to update page state and trigger router
  const navigate = useNavigate();

  const [data, setData] = useState({
    user_id: sessionStorage.getItem("userId"),
    id: "",
    item_name: "",
    bid_amount: "",
    starting_price: "",
    description: "",
    brand: "",
    watch_year: "",
    watch_model: "",
    watch_reference_number: "",
    item_condition: "",
    auction_won: 0,
    item_image: "",
    auction_start: "",
    auction_deadline: "",
  });

  useEffect(async () => {
    if (data.id) {
      console.log(data);
      auctionResponse();
    }
  }, [data.id]);
  // const handleChange = (e) => {
  //     setData({
  //         ...data,
  //         [e.target.name]: e.target.value
  //     });
  // };

  const handleChange = (e) => {
    let value = e.target.value;

    // parseInt for integer values
    if (
      e.target.name === "bid_amount" ||
      e.target.name === "starting_price" ||
      e.target.name === "watch_year"
    ) {
      value = parseInt(value, 10);
    }

    // Date for datetime values
    if (
      e.target.name === "auction_start" ||
      e.target.name === "auction_deadline"
    ) {
      value = new Date(value).toISOString().substring(0, 19);
      console.log("value: ", value);
    }

    setData({
      ...data,
      [e.target.name]: value,
    });
  };

  const auctionResponse = async () => {
    try {
      const response = await fetch("http://localhost:3500/api/auction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const auctionData = await response.json();
      console.log("Success:", auctionData);

      // Assuming `navigate` is defined and imported from a routing library (e.g., react-router-dom)
      navigate("/user/home");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(data);
    try {
      // send data to item microservice
      const itemResponse = await fetch(
        "http://localhost:3500/api/item/add_item",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );
      console.log("itemResponse:", itemResponse);
      const itemData = await itemResponse.json();
      console.log("Success:", itemData);

      // update data with the returned item data
      setData((prevData) => ({
        ...prevData,
        id: itemData.item_id,
      }));

      console.log("data:", data);

      // send updated data to auction microservice
      //   const auctionResponse = await fetch("http://localhost:3500/api/auction", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({
      //       ...data,
      //       id: itemData.item_id,
      //     }),
      //   });
      //   const auctionData = await auctionResponse.json();
      //   console.log("Success:", auctionData);

      // navigate to homepage after successful creation
      //   navigate("/user/home");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <h1>Create Item</h1>
      <label className="label">
        Item Name
        <input
          className="input"
          name="item_name"
          value={data.item_name}
          onChange={handleChange}
          placeholder="Vintage Watch"
        />
      </label>
      <label className="label">
        Bid Amount
        <input
          className="input"
          name="bid_amount"
          value={data.bid_amount}
          onChange={handleChange}
          placeholder="200"
        />
      </label>
      <label className="label">
        Starting Price
        <input
          className="input"
          name="starting_price"
          value={data.starting_price}
          onChange={handleChange}
          placeholder="5000"
        />
      </label>
      <label className="label">
        Description
        <input
          className="input"
          name="description"
          value={data.description}
          onChange={handleChange}
          placeholder="A rare vintage watch from 1950"
        />
      </label>
      <label className="label">
        Brand
        {data.brand !== "other" ? (
          <select
            className="input"
            name="brand"
            value={data.brand}
            onChange={handleChange}
          >
            {[
              "Rolex",
              "Patek Philippe",
              "Audemars Piguet",
              "Omega",
              "Cartier",
              "TAG Heuer",
              "Breitling",
              "Hublot",
              "IWC Schaffhausen",
              "Jaeger-LeCoultre",
              "Panerai",
              "Vacheron Constantin",
              "other",
            ].map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        ) : (
          <input
            className="input"
            name="brand"
            value={data.brand}
            onChange={handleChange}
            placeholder="Rolex"
          />
        )}
      </label>
      <label className="label">
        Watch Year
        <input
          className="input"
          name="watch_year"
          value={data.watch_year}
          onChange={handleChange}
          placeholder="1950"
        />
      </label>
      <label className="label">
        Watch Model
        <input
          className="input"
          name="watch_model"
          value={data.watch_model}
          onChange={handleChange}
          placeholder="Vintage Classic"
        />
      </label>
      <label className="label">
        Reference Number
        <input
          className="input"
          name="watch_reference_number"
          value={data.watch_reference_number}
          onChange={handleChange}
          placeholder="VN1950"
        />
      </label>
      <label className="label">
        Condition
        <input
          className="input"
          name="item_condition"
          value={data.item_condition}
          onChange={handleChange}
          placeholder="Good"
        />
      </label>
      <label className="label">
        Item Image
        <input
          className="input"
          name="item_image"
          value={data.item_image}
          onChange={handleChange}
          placeholder="Enter image URL"
        />
      </label>
      <h1>Create Auction</h1>
      <label className="label">
        Start Time
        <input
          className="input"
          name="auction_start"
          value={data.auction_start}
          onChange={handleChange}
          placeholder="2023-11-20 08:00:00"
        />
      </label>
      <label className="label">
        End Time
        <input
          className="input"
          name="auction_deadline"
          value={data.auction_deadline}
          onChange={handleChange}
          placeholder="2023-11-21 08:00:00"
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default CreateItemAuction;
