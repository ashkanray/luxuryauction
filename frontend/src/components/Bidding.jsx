import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../styles/Bidding.css";

// TODO: Bid Amount Increment review
// TODO: Starting price float
// TODO: CSS update - wrap text / limit width
// TODO: Auction timer
// TODO: Condition dropdown


function Bidding() {
  const [item, setItem] = useState({});
  const { item_id } = useParams();
  const [bidAmount, setBidAmount] = useState(0);
  const [bidIncrement, setBidIncrement] = useState(50);
  const [highBid, setHighBid] = useState(0);
  const [highBidUser, setHighBidUser] = useState("");
  const [highBidUsername, setHighBidUsername] = useState("");

  const user = sessionStorage.getItem('userId');
  const username = sessionStorage.getItem('username');
  const user_email = sessionStorage.getItem('email');

  //Gets the highest bidder and amount for the item
  useEffect(function fetchItemDetails() {
    fetch(`http://localhost:3500/api/bidding/highestbid/${item_id}`)
      .then((response) => response.json())
      .then((data) => {
        setHighBid(data.bid_amount);
        setHighBidUser(data.user_id);
        setHighBidUsername(data.username);
      })
      .catch((error) => console.error("Error fetching item details:", error));


    // Fetch item details
    fetch(`http://localhost:3500/api/item/get_item?id=${item_id}`)
      .then((response) => response.json())
      .then((data) => {
        setItem(data);
        setBidIncrement(item.bid_amount);
        console.log(data)
      })
      .catch((error) => console.error("Error fetching item details:", error));
  }, []);


  function handleBid() {
    //const minBidIncrement = 10; // Set minimum bid increment

    const bidAmountNumber = parseFloat(bidAmount); // Convert bid amount to a number

    // Check if highBid is a number
    const currentHighBid = parseFloat(highBid);

    // Will return False if its a string and True if its a number
    const isHighBidNumber = !isNaN(currentHighBid);

    // Check if bid is greater than current high bid or starting price if there are no bids
    
    if (!isHighBidNumber && bidAmountNumber < item.starting_price) {
        alert(`Your bid must be at least the starting price of \$${item.starting_price}.`);
        return;
    }

    // Check if bid is at least $10 higher than current high bid
    if (isHighBidNumber && bidAmountNumber <= currentHighBid) {
        alert(`Your bid must be at least \$${bidIncrement} higher than the current bid.`);
        return;
    } else if (isHighBidNumber && bidAmountNumber - currentHighBid < bidIncrement) {
        alert(`Your bid must be at least \$${bidIncrement} higher than the current bid.`);
        return;
    }

    fetch("http://localhost:3500/api/bidding/bid", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user, 
        username: username,
        amount: bidAmount,
        item_id: item_id,
        user_email: user_email }),
    })
      .then((response) => response.json())
      .then((data) => {
        setHighBid(bidAmount);
        setHighBidUser(user);
        setHighBidUsername(username);
        
      })
      .catch((error) => console.error("Error submitting bid:", error));
  }

  return (
    <div>
        <div className="watch-details">
        <img src="https://monicajewelers.com/cdn/shop/products/image_e429d3ba-6b7c-4f12-827b-e4c99b5fbfad.jpg?v=1604722425&width=1946" alt={item.name} className="watch-image"/>
            <div class="watch-info">
                <h2>{item.item_name}</h2>
                <div className="info-row"><span>Brand:</span> {item.brand}</div>
                <div className="info-row"><span>Model:</span> {item.watch_model}</div>
                <div className="info-row"><span>Year:</span> {item.watch_year}</div>
                <div className="info-row"><span>Description:</span> {item.description}</div>
                <div className="info-row"><span>Reference Number:</span> {item.watch_reference_number}</div>
                <div className="info-row"><span>Condition:</span> {item.item_condition}</div>
                <div className="info-row"><span>Starting Price:</span> ${item.starting_price}</div>
                <div className="info-row"><span>Seller:</span> {item.user_id}</div>
                <div className="info-row"></div>
                <div className="auction-details">
                    <div className="info-row"><span>Auction Start:</span> TBD</div>
                    <div className="info-row"><span>Time Left:</span> 10 Days</div>
                </div>
            </div>
        </div>

        <div className="bidding-section">
            <h3>Bidding Details</h3>
            <p><strong>Current bid: </strong>{highBid}</p>
            <p><i>Any bids made to this item must be at least {bidIncrement}$ over the current bid</i></p>
            <p><strong>Bidder Name: </strong>{highBidUsername}</p>
            <input type="number" value={bidAmount} onChange={e => setBidAmount(e.target.value)} className="bid-input"/>
            <button onClick={handleBid} className="bid-button">Place bid</button>
        </div>
    </div>
  );
}

export default Bidding;

//<img src={item_image} alt={item.name} class="watch-image"/>
