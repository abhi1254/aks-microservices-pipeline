import React, { useState, useEffect } from "react";

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetch("http://backend-service:8000/users/")
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error(err));
  }, []);

  const addUser = () => {
    fetch("http://backend-service:8000/users/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({name, email})
    })
      .then(res => res.json())
      .then(data => setUsers([...users, data]))
      .catch(err => console.error(err));
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>User Management</h1>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <button onClick={addUser}>Add User</button>
      <ul>
        {users.map((user, index) => (
          <li key={index}>{user.name} - {user.email}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
