import './App.css';
import Register from './Register';
import Login from './Login';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from "react-router-dom";
import { useState } from 'react';
import { apiUrl } from './api';

function HomePage() {
  const navigate = useNavigate();
  const [numRobots, setNumRobots] = useState("");
  const [hour, setHour] = useState("");
  const [numDays, setNumDays] = useState("");
  const [result, setResult] = useState("");

  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const handlepredict = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(apiUrl("/predict"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          num_robots: numRobots,
          hour: hour,
          num_days: numDays,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data.prediction);
      } else {
        alert(data.message || "Session expired. Please login again.");
        if (response.status === 401) {
          localStorage.removeItem("token");
          navigate("/");
        }
      }
    } catch (err) {
      alert("Server error during prediction");
    }
  };

  return (
    <div>
      <div>
        <h1 id="header">Robot Prediction</h1>
        <button onClick={handleLogout} id="loginbutton" style={{ border: "none", cursor: "pointer", backgroundColor: "#ff4d4d" }}>
          Logout
        </button>
      </div>
      <div>
        <img src="img1.png.png" alt="Register" className="register-image" id="robo1" />
      </div>
      <div>
        <img src="img2.png.png" alt="img2" className="register-image2" id="robo2" />
      </div>
      <div id="container1">
        <form id="form" onSubmit={handlepredict}>
          <label>Number of Robots:</label><br />
          <input type="text" name="num_robots" onChange={(e) => setNumRobots(e.target.value)} required /><br />

          <label>Day per hour:</label><br />
          <input type="text" name="hour" onChange={(e) => setHour(e.target.value)} required /><br />

          <label>Number of Days:</label><br />
          <input type="text" name="num_days" onChange={(e) => setNumDays(e.target.value)} required /><br />

          <input type="submit" value="Predict" id="submit" />
        </form>
      </div>
      <h3 id="prediction">{result ? `Robot Rent is: ${result}` : ""}</h3>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
