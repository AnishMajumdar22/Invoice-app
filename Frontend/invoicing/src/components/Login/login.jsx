import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from '../NavBar/Navbar'


const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: username, password: password }),
      });
      const data = await response.json();
      if (!data.token) {
        alert("Login Failed");
      } else {
        localStorage.setItem("token", data.token);
        navigate("/");
      }
    } catch (error) {
      console.error("Error logging in:", error);
    }
  };

  return (
    <>
    <Navbar />
    <div
      className="container d-flex justify-content-center align-items-center vh-100"
      style={{ maxWidth: "700px" }}>
      <form className="p-4 border shadow w-100" onSubmit={handleLogin}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">
            Username:
          </label>
          <input
            type="text"
            id="username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password:
          </label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
    </div>
    </>
  );
};

export default Login;
