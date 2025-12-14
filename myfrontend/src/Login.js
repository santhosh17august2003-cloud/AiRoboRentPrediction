import "./App.css";
import {Link} from "react-router-dom"
import { useState } from "react";
import { useNavigate } from "react-router-dom";
function Login(){
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handlelogin = async (e) => {
        e.preventDefault();

        try{
            const response = await fetch("http://127.0.0.1:5000/login",{
                method: "POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    username,
                    password,

                }),
            });

            const data = await response.json();

            if(response.ok){
                navigate("/home");
            }else{
                setError(data.message);
            }
        }catch (err){
            setError("Server error");
        }
    }

    return(
        <>
            <div>
                <img src="img1.png.png" alt="Register" className="register-image" id="robo1" />
            </div>
            <div>
                <img src = "img2.png.png" alt="img2" className="register-image2" id="robo2"/>
            </div>
            <div>
                <Link to="/register" className="register-link" id="registerbutton">Register</Link>
            </div>

            <div id="container1">
                <h2 id="login">Login</h2>
                <form onSubmit={handlelogin} id="logform">
                    <label id="logusername">Username:</label><br />
                    <input type="text" name="username" id="inputusername" onChange={(e) => setUsername(e.target.value)} /><br />
                    <label id="logpassword">Password:</label><br />
                    <input type="password" name="password" id="inputpassword"  onChange={(e) => setPassword(e.target.value)} /><br />
                    <input type="submit" value="Login" id="logsubmit"/>
                </form>
                 {error && <p style={{ color: "red" }}>{error}</p>}
            </div>
        </>
    );
}
export default Login;