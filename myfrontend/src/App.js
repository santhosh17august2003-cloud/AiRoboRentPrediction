import './App.css';
import Register from './Register';
import Login from './Login'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from 'react';

function App() {
  const [numRobots, setNumRobots] = useState("");
  const [hour, setHour] = useState("");
  const [numDays, setNumDays] = useState("");
  const [result, setResult] = useState("");

  const handlepredict  = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/predict",{
      method: "POST",
      headers:{
        "Content-Type": "application/json",
      },
      body : JSON.stringify({
        num_robots: numRobots,
        hour: hour,
        num_days: numDays,
      }),
    });
     const data = await response.json();
    setResult(data.prediction);
  }  
  return (
    <Router>
      <Routes>

        {/* Home Page */}
        <Route
          path="/home"
          element={
            <div>
              <div>
                <h1 id="header">Robot Prediction</h1>
              </div>
              <div>
                <img src="img1.png.png" alt="Register" className="register-image" id="robo1" />
            </div>
            <div>
                <img src = "img2.png.png" alt="img2" className="register-image2" id="robo2"/>
            </div>
              <div id="container1">

                <form method="POST" id="form" onSubmit={handlepredict}>
                  <label>Number of Robots:</label><br />
                  <input type="text" name="num_robots" onChange={(e) => setNumRobots(e.target.value)} /><br />

                  <label>Day per hour:</label><br />
                  <input type="text" name="hour" onChange={(e) => setHour(e.target.value)} /><br />

                  <label>Number of Days:</label><br />  
                  <input type="text" name="num_days" onChange={(e) => setNumDays(e.target.value)} /><br />

                  <input type="submit" value="Predict" id="submit" />
                </form>
                 
              </div>
               <h3 id="prediction">Robot Rent is: {result}</h3>
            </div>
          }
        />

        {/* Register Page */}
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
