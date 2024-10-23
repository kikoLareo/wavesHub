import React, { useState } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';  // Añade esto para generar IDs únicos

function generateTransactionId() {
    return uuidv4();
}


function CalculateFeeForm() {
    const transaction_id = generateTransactionId();
    console.info(`[${transaction_id}] - Inicializando componente CalculateFeeForm`);

    const [formData, setFormData] = useState({
        judge_id: 1,
        championship_id: 1,
        position: '',  // Mantener este valor vacío al inicio
        hours: 0,
        travel_distance_km: 0,
        full_meal_days: 0,
        half_meal_days: 0,
        lodging_days: 0,
        refresh_days: 0,
        operator_days: 0,
    });

    const [result, setResult] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        console.info(`[${transaction_id}] - Campo actualizado: ${e.target.name} = ${e.target.value}`);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.info(`[${transaction_id}] - Enviando datos al backend:`, formData);
        try {
            const response = await axios.post('http://localhost:8000/api/calculate', formData);
            console.info(`[${transaction_id}] - Respuesta recibida:`, response.data);
            setResult(response.data);
        } catch (error) {
            console.error(`[${transaction_id}] - Error al calcular la tarifa:`, error);
        }
    };

    return (
        <div>
            <h2>Calcular Cobros</h2>
            <form onSubmit={handleSubmit}>
                <select name="position" onChange={handleChange}>
                    <option value="">Seleccione una posición</option>
                    <option value="director_competicion">Director de Competición</option>
                    <option value="delegado">Delegado</option>
                    <option value="juez">Juez</option>
                    <option value="tabulator">Tabulator</option>
                </select>
                <input type="number" name="hours" placeholder="Horas" onChange={handleChange} />
                <input type="number" name="travel_distance_km" placeholder="Distancia de Viaje (km)" onChange={handleChange} />
                <button type="submit">Calcular</button>
            </form>
            {result && (
                <div>
                    <h3>Resultado:</h3>
                    <p>Total Fee: {result.total_amount} €</p>
                </div>
            )}
        </div>
    );
}


export default CalculateFeeForm;