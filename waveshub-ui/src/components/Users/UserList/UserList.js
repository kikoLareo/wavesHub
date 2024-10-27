// components/Users/UserList/UserList.js
import React, { useContext } from 'react';
import { UserContext } from '../UserContext';

const UserList = () => {
  const { users, setUsers } = useContext(UserContext);

  const handleDelete = (userId) => {
    // Lógica para eliminar usuario (ejemplo)
    setUsers(users.filter(user => user.id !== userId));
  };

  return (
    <div>
      <h2>Lista de Usuarios</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.name} - {user.email}
            <button onClick={() => handleDelete(user.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
