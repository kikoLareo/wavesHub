
// src/App.js
import React from 'react';

// Importa el formulario de cálculo de cobros
import CalculateFeeForm from './components/Calculate/CalculateFeeForm';

// Importa Providers y Componentes de Users, Roles y Permissions
import { UserProvider } from './components/Users/UserContext';
import UserList from './components/Users/UserList';
import UserForm from './components/Users/UserForm';

// import { RoleProvider } from './components/Roles/RoleContext';
// import RoleList from './components/Roles/RoleList';
// import RoleForm from './components/Roles/RoleForm';

// import { PermissionProvider } from './components/Permissions/PermissionContext';
// import PermissionList from './components/Permissions/PermissionList';
// import PermissionForm from './components/Permissions/PermissionForm';

function App() {
    return (
        <div className="App">
            <h1>WavesHub - Cálculo de Cobros y Gestión de Usuarios, Roles, Permisos</h1>

            {/* Componente de cálculo de cobros */}
            <CalculateFeeForm />

            {/* Gestión de Usuarios */}
            <UserProvider>
                <section>
                    <h2>Gestión de Usuarios</h2>
                    <UserForm />      {/* Formulario para crear/editar usuarios */}
                    <UserList />      {/* Lista de usuarios */}
                </section>
            </UserProvider>

        </div>
    );
}

export default App;
