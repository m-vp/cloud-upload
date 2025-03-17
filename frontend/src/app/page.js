import { useState } from "react";
import axios from "axios";

const API_URL = "http://your-ec2-public-ip:5000"; // Update with EC2 IP

export default function Home() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    await axios.post(`${API_URL}/register`, { username, password });
    alert("User Registered");
  };

  const handleLogin = async () => {
    const response = await axios.post(`${API_URL}/login`, { username, password });
    alert(`Token: ${response.data.access_token}`);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Login / Register</h2>
      <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
