// components/Users/UserDetail/UserDetail.js
import React from 'react';

const UserDetail = ({ user }) => {
  if (!user) return <p>Seleccione un usuario para ver detalles</p>;

  return (
    <div>
      <h3>Detalles del Usuario</h3>
      <p>Nombre: {user.name}</p>
      <p>Email: {user.email}</p>
      {/* Otros detalles aquí */}
    </div>
  );
};

export default UserDetail;
