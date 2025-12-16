import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Register() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


  const handleLogout = () => {
    localStorage.clear();   
    navigate("/");
  };

  const handleregister = async (e) => {
    e.preventDefault();
    const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;
    if (!specialCharRegex.test(password)) {
      alert("Password must contain at least one special character!");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name,
          email,
          username,
          password
        })
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message || "Register successful");
        navigate("/");
      } else {
        alert(data.message || "Email already registered");
      }

    } catch (error) {
      alert("Server error. Try again later.");
    }
  };

  return (
    <>
      <div id="bgcolor">
        <button
          onClick={handleLogout}
          style={{
            position: "absolute",
            top: "20px",
            right: "20px",
            padding: "8px 14px",
            borderRadius: "10px",
            border: "none",
            backgroundColor: "#ff4d4d",
            color: "white",
            cursor: "pointer"
          }}
        >
          Logout
        </button>

        <div>
          <img src="img1.png.png" alt="Register" className="register-image" id="robo1" />
        </div>

        <div>
          <img src="img2.png.png" alt="img2" className="register-image2" id="robo2" />
        </div>

        <div>
          <Link to="/" className="login-link" id="loginbutton">Login</Link>
        </div>

        <div className="register-wrapper">
          <div className="register-container">
            <h2 className="register-title">Register</h2>

            <form className="register-form" onSubmit={handleregister}>

              <label className="register-label">Name</label>
              <input
                className="register-input"
                type="text"
                onChange={(e) => setName(e.target.value)}
                required
              />

              <label className="register-label">Email</label>
              <input
                className="register-input"
                type="email"
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <label className="register-label">Username</label>
              <input
                className="register-input"
                type="text"
                onChange={(e) => setUsername(e.target.value)}
                required
              />

              <label className="register-label">Password</label>
              <input
                className="register-input"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              <button className="register-btn" type="submit">
                Register
              </button>

            </form>
          </div>
        </div>

        <p id="moral1">
          Join the cutting-edge robotics prediction platform!
        </p>

      </div>
    </>
  );
}

export default Register;
