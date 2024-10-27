// components/Users/UserForm/UserForm.js
import React, { useState, useContext } from 'react';
import { UserContext } from '../UserContext';
import { createUser } from '../../../services/userService';

const UserForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const { setUsers } = useContext(UserContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newUser = await createUser({ name, email });
    setUsers(prevUsers => [...prevUsers, newUser]);
    setName('');
    setEmail('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Nombre" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button type="submit">Crear Usuario</button>
    </form>
  );
};

export default UserForm;
